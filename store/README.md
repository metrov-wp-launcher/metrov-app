# METROV Store catalogue

METROV's Store app reads `catalog.json` from this folder at
`https://raw.githubusercontent.com/metrov-wp-launcher/metrov-app/main/store/` and caches it on the
phone. Push a change here and phones pick it up the next time the Store is opened, a few minutes
later at most (GitHub caches the file for about five minutes); the Store tile checks every 12 hours,
and refresh fetches at once. No METROV release is needed.

Builds after 2.10.2 also read `notices`, `front`, `panes` and the per-item fields under
[Showing, ordering and badges](#showing-ordering-and-badges). Older builds ignore them, so keep
`notice` filled in for them while they are still around.

## catalog.json

```json
{
  "version": 1,
  "featured": "app:messages",
  "apps": [...],
  "collections": [...],
  "themes": [...],
  "wallpapers": [...],
  "tiles": [...],
  "fonts": [...]
}
```

- `version`: the format version. Keep it at 1; METROV ignores a catalogue with a higher one.
- `featured`: the item on the Store's first pane (the weekly pick), as `app:<id>`, `theme:<id>`,
  `wallpaper:<id>`, `tile:<id>` or `font:<id>`. METROV builds before tiles and fonts show their
  first app when it names anything but an app.
- Every name and text is a map of locale to text (`{"en": "...", "vi": "..."}`). `en` is required
  and is used when the phone's language is missing.
- `added` (`YYYY-MM-DD`) is optional. An item a user has not seen yet counts towards the number
  on the Store tile.
- Fields METROV does not know are ignored, so the format can grow.

### notice

Optional. A message at the top of the Store's front, above everything else. Leave it out (or let
`until` pass) and nothing shows. Newer builds read `notices` instead when it is there.

```json
"notice": {
  "title": { "en": "Winter themes are here" },
  "text": { "en": "Five new themes, free this week." },
  "image": "notices/winter.jpg",
  "open": "theme:winter",
  "from": "2026-12-01",
  "until": "2026-12-07"
}
```

| field | |
| --- | --- |
| `title` | text map, required |
| `text` | text map, one or two short lines |
| `image` | path in this folder, drawn 2:1 across the pane (about 1200 x 600) |
| `open` | what a tap opens: an item key (`app:dial`, `theme:x`, `tile:x`, `wallpaper:x`, `font:x`) or an `https://` link. Leave it out for nothing |
| `from`, `until` | first and last day it shows (`YYYY-MM-DD`), in the phone's own time; either may be left out |

### notices

Newer builds: a list of notices, each as `notice` above plus an `id`. A `notice` block in `front` or
a pane places one; with no `front`, all of them show at the top of the front, in order. When
`notices` is present, newer builds ignore `notice`.

```json
"notices": [
  { "id": "winter", "title": { "en": "Winter themes are here" }, "open": "theme:winter",
    "from": "2026-12-01", "until": "2026-12-07" }
]
```

### front

Newer builds: the sections of the Store's first pane, top to bottom. Leave it out for the usual
order: every notice, then featured, new, collections. The user's own news (items they sent, app
updates) always shows near the top, under any notices that open the list.

```json
"front": [
  { "type": "notice", "id": "winter" },
  { "type": "featured" },
  { "type": "new", "days": 14, "limit": 6, "title": { "en": "New this fortnight" } },
  { "type": "collection", "id": "dark", "limit": 6 },
  { "type": "collections" }
]
```

| `type` | shows |
| --- | --- |
| `notice` | the notice with this `id` |
| `featured` | the `featured` items, large |
| `new` | themes and tiles whose `added` is within `days` (default 7), newest first, at most `limit` (default 6) |
| `collection` | the collection with this `id`: its name, up to `limit` themes and tiles as pictures, and "more" to its page |
| `collections` | every collection, each a line opening its page |

Every block may have a `title` (text map) to replace its heading, and `from`, `until`, `minApp`,
`maxApp` as below. Unknown types are skipped.

### panes

Newer builds: up to two extra panes in the Store's panorama, each after a fixed one (`featured`,
`apps` or `categories`; `apps` when left out). A pane holds blocks, as `front` does. A pane whose
blocks are all outside their dates does not show.

```json
"panes": [
  { "id": "holiday", "name": { "en": "holiday" }, "after": "featured",
    "from": "2026-12-15", "until": "2026-12-31",
    "blocks": [ { "type": "notice", "id": "winter" }, { "type": "collection", "id": "xmas" } ] }
]
```

### Showing, ordering and badges

Newer builds read these on any app, theme, wallpaper, tile or font (and `from` to `maxApp` on
collections, notices, blocks and panes too):

| field | |
| --- | --- |
| `hidden` | `true` leaves the item out everywhere, without deleting it |
| `from`, `until` | first and last day it shows (`YYYY-MM-DD`), in the phone's own time |
| `minApp`, `maxApp` | the METROV versions it shows in (`2.11.0`). Older builds ignore these and show it anyway |
| `order` | items with a number come first in their list, lowest first; the rest keep their usual order |
| `badge` | `new`, `popular` or `updated`: a word in the accent colour by its name, translated |

### apps

| field | |
| --- | --- |
| `id` | short unique id |
| `package` | the Android package name, used to see whether it is installed and to open Play |
| `name`, `tagline`, `description` | text maps |
| `icon` | path of a square PNG in this folder, 512 px |
| `screenshots` | optional list of screenshot paths (PNG, JPG or WebP, phone-shaped, about 720 x 1600), shown in order on the app's page |
| `status` | `live` (on Play: get opens the Play listing), `web` (not on Play: learn more opens `url` in the browser) or `soon` (coming soon) |
| `url` | the app's page on the web. For `web`, learn more opens it and it offers the download; never a direct `.apk` link, and while it is empty the app shows as coming soon. For `soon`, share sends it. |
| `versionCode` | optional: the version on Play. When the installed one is lower, the Store shows update |

The Store never downloads or installs an app itself, and never links an APK directly: Play's policy
does not allow a Play app to install apps from outside Play, and reviewers have flagged apps that
steer users to APK downloads. Get opens the Play listing; learn more opens the app's own web page.

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

### collections

Hand-picked sets, listed under the featured item.

| field | |
| --- | --- |
| `id`, `name`, `description` | as above; `description` is optional |
| `items` | item keys (`theme:store-ember`, `font:inter`). Keys not in the catalogue are skipped |

### tiles

Custom tiles, as `.mvtile` files exported from METROV's tile editor (Settings > Tiles > custom
tiles > export). Adding one pins it to Start and puts it in the user's custom tiles. Needs premium.

| field | |
| --- | --- |
| `id`, `name` | as above |
| `file` | the `.mvtile` file |
| `preview` | PNG of the tile at its shape, about 200 px per small-tile unit |

### fonts

| field | |
| --- | --- |
| `id` | as above |
| `name` | the family's name, plain text (not a text map) |
| `file` | `.ttf` or `.otf` |
| `license` | shown on the font's page. Ship the licence file next to the font |

METROV holds one custom font: a Store font replaces one the user imported (it asks first). Needs
premium. Only add fonts whose licence allows redistribution, such as the SIL Open Font License.

Only add images you made or may share. The starter set here was generated for METROV.

## Community rules

Premium users can send their own tiles and themes to the Store. Everything is reviewed before it
appears, and what you send carries the name you chose.

Send only what you made yourself:

- **Your own work.** No copies of someone else's tile, theme or artwork, with or without changes.
- **Brand logos only on tiles that open that brand's app.** A tile with an app's logo that opens
  that app is fine. A logo used for anything else, or a tile that pretends to be official, is
  turned down. Brand owners can ask for any item using their logo to be taken down.
- **Nothing adult, violent, hateful or offensive**, in pictures or in names. Pictures are checked
  automatically when you send them.
- **No links, contact details or ads** in names or on tiles.

Items that break these rules are turned down or removed. A sender who keeps sending them is
blocked from the Store.

**Reports.** Anyone can report an item from its page. An item reported by three people leaves the
Store at once and comes back only if review finds nothing wrong.

**Taking something back.** You can withdraw what you sent from **my submissions** in the
Store at any time.

**Copyright or trademark complaints.** Email tuannguyenitpy@gmail.com with a link to the item, or
its name and author, and why it infringes your rights. Items are taken down within two working
days of a valid request.
