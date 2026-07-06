# visual-proof.spec.md — schema

Every `/infographic` run writes this file. It is the audit trail and prompt source.

```markdown
---
slug: {{SLUG}}
source: {{SOURCE_PATH}}
preset: {{PRESET_ID}}
visual_type: schema | timeline | comparison | flow | card
aspect_ratio: "16:9" | "1:1" | "9:16"
lang: fr | en | …
mode: IMAGE | PROMPT
generated: {{ISO_DATE}}
type_rationale: one line — why this type was chosen
---

# {{TITLE}}

## Thesis

{{ONE_SENTENCE_SO_WHAT}}

## Visual metaphor

**Scene:** {{ONE_CONCRETE_DRAWABLE_SCENE}}

One physical scene tied to the source's domain — something an illustrator could draw from this sentence alone. Never "boxes", "diagram", "chart", "sections".

**Hero element:** {{THESIS_PHRASE_OR_KILLER_NUMBER}} — the single element rendered huge (~1/3 of canvas). Everything else supports it, smaller.

## Nodes (on-image labels, max 7, 1–2 words each)

1. {{NODE_1}}
2. {{NODE_2}}
…

## Relations (optional)

- {{A}} → {{B}}
- {{A}} vs {{B}}

## Numbers (verbatim from source only)

| Label | Value | Source line/section |
|-------|-------|---------------------|
| … | … | … |

Omit this section if no numbers in source.

## Legend (2–5 entries)

- {{LEGEND_1}} — {{MEANING}}
- …

## Palette (from preset)

| Role | Hex | Use |
|------|-----|-----|
| primary | {{HEX}} | headers, main shapes |
| secondary | {{HEX}} | secondary boxes |
| accent | {{HEX}} | highlights, arrows |
| surface | {{HEX}} | backgrounds |
| muted | {{HEX}} | captions, grid |

## Layout instruction

{{TYPE_LAYOUT_ONE_LINER}}

## Forbidden on canvas

- Long copyrighted quotes
- Trademark logos
- Exact reproduction of published figures
- Personal data (emails, addresses)
- Invented numbers or claims

## Wedge lock (if brief.md exists)

**Narrow wedge:** {{WEDGE_TEXT}}

Elements outside wedge: {{LIST_OR_NONE}}

## Source trace

| Field | Value |
|-------|-------|
| Source file | {{PATH}} |
| Sections used | {{HEADINGS}} |
| Words in source | ~{{COUNT}} |
```

**Rules when filling:**

- `title` ≤ 8 words
- `metaphor` = one drawable scene; if the sentence contains "box", "diagram", "chart" or "section", rewrite it. Pull imagery from the source's own domain (construction → chantier, robots → machines, biology → animals)
- `hero` = exactly one element (a number beats a phrase when both exist); never two heroes
- `nodes` = nouns, 1–2 words; FR: prefer accent-free synonyms when a natural one exists (image models garble é/è/ç)
- `numbers` only if verbatim in source — else omit
- `type_rationale` must cite a source signal ("chosen: comparison — source contrasts legs vs wheels")