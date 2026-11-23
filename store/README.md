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
