# Report template

Copy this structure into `research/<slug>/report.md` or `studies/<slug>/research.md`.

```markdown
# <Research title>

**Slug:** <slug>
**Question:** <one-sentence research question>
**Researched:** <YYYY-MM-DD>
**Depth:** quick | standard | literature-review | extreme
**Study link:** <studies/<slug>/ or none>
**Full source index:** <research/<slug>/sources-index.md>

## Screening funnel

| Stage | Count |
|-------|-------|
| Discovered (logged) | <N> |
| Screened — included | <N> |
| Screened — excluded | <N> |
| Eligible | <N> |
| Read in depth | <N> |
| Cited in synthesis | <N> |

<If literature-review and N_discovered < 150: note shortfall + missing query angles>

## Executive summary

<150–300 words. Lead with the answer. What should the user believe or do?>

## Key findings

1. **<Finding>** — <one sentence> *(Source: Author year / Org)*
2. ...

## Synthesis

### <Theme 1 — e.g. Mechanisms>

<Prose weaving multiple sources. Cite inline: (Author, year).>

### <Theme 2 — e.g. Trade-offs>

...

### <Theme 3 — optional>

...

## Contradictions and uncertainty

| Topic | Position A | Position B | Assessment |
|-------|------------|------------|------------|
| ... | ... | ... | strong / mixed / weak evidence |

## Source map

> Full audit trail (all discovered sources + exclude reasons): `sources-index.md`

### Read in depth

| Source | Tier | Access | Why selected |
|--------|------|--------|--------------|
| Author (year) — *Title* — URL | 1 | open | ... |

### Eligible — not read (capacity / redundancy)

| Source | Tier | Why not deep-read |
|--------|------|-------------------|
| ... | 2 | Covered by survey X |

### Exclusion summary (top reasons)

| Reason code | Count | Example |
|-------------|-------|---------|
| OFF_TOPIC | <N> | ... |
| DUPLICATE | <N> | ... |
| LOW_TIER | <N> | ... |

## Open questions

- <What this research did not resolve>
- ...

## Recommended next steps

- **Read first:** <anchor source + why>
- **If deciding:** <concrete decision this enables>
- **If learning deeper:** <optional: run /bear-hours on sub-topic X>

## Confidence

**Overall:** high | medium | low

**Why:** <one line — source quality, agreement, gaps>
```