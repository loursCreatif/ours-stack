# Node schema — mind-map.json

## Top-level shape

```json
{
  "meta": {
    "title": "string — display title",
    "slug": "string — lowercase-hyphen",
    "source": "string — path to origin .md",
    "preset": "editorial | minimal | warm | creative | custom",
    "customTokens": { "accent": "#8b2942", "bg": "#faf8f5" },
    "lang": "fr | en",
    "generated": "YYYY-MM-DD",
    "nodeCount": 0
  },
  "layout": "auto | tree | centered — optional, defaults to auto",
  "root": { /* Node */ }
}
```

## Custom preset (`meta.customTokens`)

Required when `preset: "custom"`, ignored otherwise. Keys limited to: `bg`, `surface`, `text`, `muted`, `border`, `accent`, `accent-light`, `secondary`, `success`, `warning`, `radius`. Values are plain CSS values (`#hex`, `rgb(…)`, `10px`) — characters outside `#a-zA-Z0-9 .,%()-` are rejected (no `;`, `}`, quotes). Missing tokens fall back to `warm`.

## Layout mode

| Value | Meaning |
|-------|---------|
| `auto` or omitted | Use `centered` when root has at least 4 direct children and max depth is ≤ 3; otherwise use `tree` |
| `tree` | Force the horizontal hierarchy layout |
| `centered` | Force the centered bilateral mind-map layout |

## Node object

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `id` | yes | string | Unique within file; lowercase-hyphen |
| `label` | yes | string | Short display text (≤ 80 chars) |
| `type` | yes | enum | `concept` \| `detail` \| `example` \| `source` |
| `summary` | no | string | One clear sentence for hover tooltip (≤ 200 chars) |
| `note` | no | string | Expanded detail for side panel on click — 2–4 sentences (≤ 600 chars) |
| `importance` | no | integer | Visual weight from 1 to 5; omitted nodes are auto-sized |
| `href` | no | string | URL — required for `type: source` when URL exists |
| `collapsed` | no | boolean | Default `false` for depth ≤ 2, `true` for depth ≥ 3 |
| `children` | no | Node[] | Omit or `[]` for leaves |

## Type semantics

| Type | Role | Visual |
|------|------|--------|
| `concept` | Main branches (wedge, beliefs, findings, synthesis sections) | Filled rect, `var(--accent)` |
| `detail` | Sub-points, criteria, mechanisms, funnel counts | Lighter fill, `var(--surface)` border |
| `example` | Concrete cases, robots, demos | `var(--success)` accent border |
| `source` | Bibliography leaves | `var(--secondary)` + link icon; click opens `href` |

## Importance

| Value | Use |
|-------|-----|
| `5` | Root, central thesis, one-map anchor |
| `4` | Major branches a reader should retain |
| `3` | Supporting concepts or dense grouped details |
| `2` | Ordinary detail or example |
| `1` | Source, citation, minor leaf |

If absent, the HTML renderer infers importance from depth, type, and visible children. Importance changes bubble size, font size, and stroke weight; it must not change the meaning or order of nodes.

## Limits (enforced at extraction)

- **80 nodes** total (including root)
- **Depth 5** max
- If over limit: merge siblings into one `detail` node with bullet `note`

## ID conventions

```
root
wedge
beliefs
belief-copy-nature
success-criteria
open-questions
sources
src-tripod-gait
finding-1
synthesis-taxonomy
```

## Validation rules

1. Every `id` unique
2. `source` nodes with `href` must have `http` URL
3. `root.type` always `concept`
4. No empty `label`; `label` ≤ 80 chars, `summary` ≤ 200, `note` ≤ 600 (enforced by `validate-map.py`)
5. `importance`, when present, is an integer from 1 to 5
6. `meta.nodeCount` mismatch → validator warning only; the HTML always displays the actual count
7. `preset: "custom"` requires valid `meta.customTokens` (see § Custom preset)

Legacy note: old JSON files with `meta.preset: "academic"` still render, but new maps should not propose it as a style choice.
