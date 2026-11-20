# METROV Store catalogue

METROV's Store app reads `catalog.json` from this folder at
`https://raw.githubusercontent.com/metrov-wp-launcher/metrov-app/main/store/` and caches it on the
phone. Push a change here and phones pick it up within 12 hours, or at once with refresh. No METROV
release is needed.

## catalog.json

```json
{
  "version": 1,
  "featured": "app:messages",
  "apps": [...],
  "themes": [...],
  "wallpapers": [...]
}
```

- `version`: the format version. Keep it at 1; METROV ignores a catalogue with a higher one.
- `featured`: the item on the Store's first pane, as `app:<id>`, `theme:<id>` or `wallpaper:<id>`.
- Every name and text is a map of locale to text (`{"en": "...", "vi": "..."}`). `en` is required
  and is used when the phone's language is missing.
- `added` (`YYYY-MM-DD`) is optional. An item a user has not seen yet counts towards the number
  on the Store tile.
- Fields METROV does not know are ignored, so the format can grow.

### apps

| field | |
| --- | --- |
| `id` | short unique id |
| `package` | the Android package name, used to see whether it is installed and to open Play |
| `name`, `tagline`, `description` | text maps |
| `icon` | path of a square PNG in this folder, 192 px |
| `screenshots` | optional list of screenshot paths (PNG, JPG or WebP, phone-shaped, about 720 x 1600), shown in order on the app's page |
| `status` | `live` (on Play: get opens the Play listing), `apk` (not on Play: download opens `url` in the browser) or `soon` (coming soon) |
| `url` | for `apk`: where the APK is downloaded from. While it is empty the app shows as coming soon |
| `versionCode` | optional: the version on Play. When the installed one is lower, the Store shows update |

The Store never downloads or installs an APK itself (Play policy forbids it in a Play app): get opens
the Play listing, and download hands `url` to the browser, which downloads it and lets Android ask
the user to install it.

### themes

| field | |
| --- | --- |
| `id` | must match the `id` inside the theme file, and must not be a built-in theme's id |
| `name` | text map |
| `file` | path of the theme JSON, the same format as a theme exported from METROV |
| `colors` | four `#AARRGGBB` colours for the Store card: background, surface, text, accent |

Applying a Store theme needs METROV premium.

### wallpapers

| field | |
| --- | --- |
| `id`, `name` | as above |
| `file` | full image, JPG, about 1440 x 3120 |
| `thumb` | small JPG for the grid, about 360 x 780 |

Only add images you made or may share. The starter set here was generated for METROV.
