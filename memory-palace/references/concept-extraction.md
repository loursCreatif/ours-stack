# Concept extraction — memory-palace

Extract only what exists in source files. Never pad, invent, or import external knowledge.

## Source priority (study mode)

1. `notes.md` — densest; primary for loci
2. `brief.md` — wedge, beliefs, questions, success criteria
3. `research.md` — if linked study research
4. `sources-index.md` — top 5–8 `read` entries (titles only, as object plaques)
5. User-pasted concept list — ordering wins; gloss from files if available

## Source priority (research mode)

1. `report.md` — key findings, synthesis themes, contradictions
2. `brief.md` — if `**Study link:**` points to study with brief
3. `sources-index.md` — top sources as plaques only

## Extraction targets by section

| Source section | Concept type | Palace role |
|----------------|--------------|-------------|
| `## Narrow wedge` | `finding` | Foyer plaque |
| `## Why now` | `finding` | Foyer context |
| `## Current beliefs` | `belief` | Alcove / paired room |
| `**À tester :**` under beliefs | `question` | Blocked door or dim alcove |
| `## Success criteria` | `finding` | End chamber |
| `## Core mechanisms` bullets | `mechanism` | Main path rooms |
| `## Key insights` bullets | `finding` | Main path rooms |
| `## Open questions` | `question` | Blocked doors |
| `## Connections` — in-wedge links | `relationship` | Portal between rooms |
| `## Connections` — "Hors wedge" | `finding` | Tag `out-of-wedge`, exclude default |
| Report `## Key findings` | `finding` | Main path |
| Report synthesis `###` themes | `finding` | Wing labels (museum) |
| Contradiction table rows | `relationship` | Branch alcove |

## Concept record shape

```json
{
  "id": "kebab-case-slug",
  "label": "Short label (≤6 words)",
  "gloss": "One sentence, source-faithful",
  "type": "mechanism|finding|belief|question|date|relationship|source",
  "importance": 1,
  "source": {
    "file": "studies/foo/notes.md",
    "section": "Core mechanisms",
    "anchor": "optional-kebab"
  },
  "relations": [{ "to": "other-id", "kind": "supports|contradicts|extends" }],
  "tags": []
}
```

## Rules

- **One substantive bullet = one concept** (skip empty or purely structural bullets).
- **Merge duplicates** — same idea in brief and notes → one concept, note both sources in `source`.
- **Importance** — 1 (highest) to 5 (lowest); mechanisms/insights from notes = 1–2; sources plaques = 4–5.
- **Gloss** — paraphrase only; no long quotes (privacy + memory aid).
- **Dates** — extract only if explicit in source (paper year, `Created:` in brief).
- **Minimum viable** — need ≥5 concepts or abort with guidance to add `notes.md`.
- **Maximum default** — 16 concepts; ask before exceeding 20.

## Wedge lock

When `brief.md` exists:

1. Read `## Narrow wedge` and `## Connections` hors-wedge markers.
2. Tag out-of-scope concepts `out-of-wedge`.
3. Exclude `out-of-wedge` from default `path[]` unless user says `include all`.

## Refuse as sole input

- `sources-index.md` alone — not enough concepts.
- Empty `brief.md` with TBD everywhere and no notes — ask for content first.

## Pasted concepts (mode D)

User list → one concept per line/item. Agent adds gloss from nearest file context if a slug/file was also given. Provenance `source.file` = `"user-paste"`.