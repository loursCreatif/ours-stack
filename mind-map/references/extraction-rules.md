# Extraction rules — markdown → mind-map.json

Work only from provided text. No WebSearch. Never invent URLs or claims.

## From `brief.md` (study mode)

**Root:** first H1 title → `type: concept`

**Branches** (H2 sections → `concept` children of root):

| Section | Children |
|---------|----------|
| `## Narrow wedge` | First bold line → `concept` "Wedge"; bullet "Dans le scope" → `detail` each; "Hors scope" → `detail` grouped in one node |
| `## Current beliefs` | Each bullet → `detail`; "À tester" line → `detail` with `note` |
| `## Success criteria` | Each `- [ ]` → `detail` |
| `## Open questions` | Each bullet → `detail` |
| `## Source material` | Section → `concept` "Sources"; each source line → `source` with `href` if URL present |

**Skip:** `## Why now` (fold into root `note` if ≤ 200 chars)

**Sources parsing:** lines like `- [x] Label — https://…` → `{ type: "source", label: "Label", href: "…" }`

## From `report.md` (research mode)

**Root:** H1 or `**Question:**` → `concept` with question as `label`

**Branches:**

| Section | Mapping |
|---------|---------|
| Screening funnel | Optional `detail` under root: "179 discovered · 20 read" (only if table present) |
| `## Key findings` | `concept` "Key findings" → each numbered finding → `detail` (truncate label to 80 chars) |
| `## Synthesis` | Each H3 → `concept`; paragraphs → `detail` children (max 3 per H3) |
| `## Contradictions` | `concept` → each item `detail` |
| `## Open questions` | Each → `detail` |
| `## Recommended reading` | `source` nodes with `href` |

**sources-index.md:** attach top 10 `read`/`eligible` URLs as `source` leaves under relevant finding (best-effort title match); unmatched → under `concept` "Sources"

## From generic `.md` (file / pasted mode)

- H1 → root
- H2 → `concept` branches
- H3 → `concept` or `detail` depending on depth
- List items → `detail`
- Bare URLs → `source`

## Collapse defaults

| Depth | `collapsed` |
|-------|-------------|
| 0–1 | `false` |
| 2 | `false` |
| ≥ 3 | `true` |

## Summary & note

For every `concept` and `detail` node:

- **`summary`** — one sentence faithfully reformulating the source content (never invented). Shown as hover tooltip.
- **`note`** — expanded detail (2–4 sentences) when the source text allows it; omit if insufficient material.

For `source` nodes: set `summary` to what the source contributes, when deducible from the text.

## Importance

Assign `importance` only when the source structure makes hierarchy clear:

- `5` for the root / central thesis
- `4` for major H2 branches or decisive findings
- `3` for supporting concepts, dense grouped details, or high-value open questions
- `2` for ordinary details and examples
- `1` for source leaves and minor citations

When unsure, omit `importance`; the renderer auto-sizes nodes from type, depth, and visible children.

## Language

Set `meta.lang` from source (`fr` if accents/French headings dominate, else `en`).

## Regenerate mode (E)

Read existing `mind-map.json` only. Do not re-parse markdown. Update `meta.generated` and recompose HTML.
