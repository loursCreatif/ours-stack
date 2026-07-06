# Design decisions — implementation fusion (2026-07-01)

Merged plan + independent implementation consult. Kept ours-stack conventions; adopted the hardening recommendations that matched this repo.

## Adopted from consult

| Finding | Resolution |
|---------|------------|
| Zero CDN underspecified | Hard rule: no external fonts, scripts, images, stylesheets, or `fetch()` |
| Preset coupling risk | Duplicate stable `:root` token blocks in `compose-html.py` (names aligned with layout-html) |
| No failure model | SKILL.md § Errors: invalid JSON, empty input, node overflow → merge siblings |
| 80-node limit arbitrary | Deterministic: group overflow into single `detail` node with bullet `note` |
| No schema contract | `node-schema.md` + `validate-map.py` |
| Security | JSON embedded via `json.dumps`; no user HTML in labels |
| Testing gap | `validate-map.py` + `compose-html.py` + fixture in `studies/biomimetisme-…` |
| Accessibility v1 | `tabindex`, `aria-label`, keyboard Enter/Space on nodes |

## Rejected / deferred

| Finding | Decision |
|---------|----------|
| Defer all presets to v2 | Kept 5 presets — tokens already duplicated, low cost |
| Single neutral preset only | User chose reuse layout-html presets |
| Copy svg-graph code | Inspiration only; tree layout is original vanilla JS |
| Full keyboard tree nav | v2 — v1 has search + focusable nodes |

## Output paths (canonical)

- `studies/<slug>/mind-map.json` + `mind-map.html`
- `research/<slug>/mind-map.json` + `mind-map.html`
- `output/mind-map/<slug>/map.json` + `map.html` (pasted / ad-hoc)
