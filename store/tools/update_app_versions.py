"""Writes each live app's version on Google Play into store/catalog.json.

For every app with "status": "live", reads the newest completed release on the
production track and sets the app's "version" (the release name's version) and
"versionCode". METROV compares them with what is installed to offer an update.

Needs PLAY_SERVICE_ACCOUNT_JSON: a service account with read access to the
apps in Play Console. Run from the repo root.
"""

import json
import os
import re
import sys
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

CATALOG = Path("store/catalog.json")
API = "https://androidpublisher.googleapis.com/androidpublisher/v3/applications"


def token() -> str:
    info = json.loads(os.environ["PLAY_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/androidpublisher"]
    )
    creds.refresh(Request())
    return creds.token


def latest_release(session: requests.Session, package: str):
    """(versionName, versionCode) of the newest completed production release."""
    edit = session.post(f"{API}/{package}/edits")
    if edit.status_code != 200:
        print(f"{package}: no access ({edit.status_code})", file=sys.stderr)
        return None
    edit_id = edit.json()["id"]
    try:
        track = session.get(f"{API}/{package}/edits/{edit_id}/tracks/production")
        if track.status_code != 200:
            return None
        best = None
        for release in track.json().get("releases", []):
            if release.get("status") != "completed":
                continue
            codes = [int(c) for c in release.get("versionCodes", [])]
            if not codes:
                continue
            code = max(codes)
            if best is None or code > best[1]:
                # Play names a release "42 (1.5.0)" unless renamed by hand.
                name = release.get("name", "")
                match = re.search(r"\(([^)]+)\)", name)
                best = ((match.group(1) if match else name).strip() or None, code)
        return best
    finally:
        session.delete(f"{API}/{package}/edits/{edit_id}")


def main() -> int:
    raw = CATALOG.read_text(encoding="utf-8")
    catalog = json.loads(raw)
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token()}"
    changed = False
    for app in catalog.get("apps", []):
        if app.get("status") != "live" or not app.get("package"):
            continue
        found = latest_release(session, app["package"])
        if found is None:
            continue
        name, code = found
        if app.get("versionCode") != code or (name and app.get("version") != name):
            print(f"{app['id']}: {app.get('version')} ({app.get('versionCode')}) -> {name} ({code})")
            app["versionCode"] = code
            if name:
                app["version"] = name
            changed = True
    if changed:
        CATALOG.write_text(
            json.dumps(catalog, indent=2, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""),
            encoding="utf-8",
        )
    else:
        print("No version changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
