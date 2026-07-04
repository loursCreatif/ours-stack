# HTML template — memory-palace (relief map)

Composed by `memory-palace/scripts/compose-html.py`. Manual edits rare.

## Structure

- `#relief-canvas` — Three.js oblique relief (primary)
- `#iso-map` — isometric SVG fallback
- `#detail-panel` — concept cards (right side)
- `#breadcrumb` + `#btn-back` — navigation
- `#overlay-first` — first-run hint (click buildings, no walking)

## Data

Embed `memory-palace.json` as `const PALACE_DATA = …` with `view_mode: "relief"`.

## Vendor

```bash
bash memory-palace/scripts/fetch-three.sh
```

Inline full `references/vendor/three.min.js` in first `<script>` block.

## UX spec

See `navigation-ux.md` — no WASD, no pointer-lock.