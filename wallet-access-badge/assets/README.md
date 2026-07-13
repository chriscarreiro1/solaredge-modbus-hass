# Optional custom images

Drop PNG files here to override the auto-generated placeholders. Apple expects these names:

| File | Size (1x / @2x / @3x) |
|------|------------------------|
| `icon.png` | 29×29 / 58×58 / 87×87 |
| `logo.png` | 160×50 / 320×100 / 480×150 |
| `strip.png` | 375×144 / 750×288 / 1125×432 | **Pass front** — main artwork banner |
| `thumbnail.png` | 90×90 / 180×180 / 270×270 | Info (ⓘ) screen preview |

If any file is present, only those files are copied; missing sizes fall back to generation only when the entire `assets/` folder is empty.

For a Disney-style look, add your own branded `strip.png` (pass front artwork) and `thumbnail.png` here. The strip image is what users see before tapping the info button.
