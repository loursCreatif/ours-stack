# Screening funnel — classic deep research

Real literature reviews **search wide, screen hard, read deep**. The agent cannot open 200 full PDFs in one session — but it **must** surface 150–250+ candidates, screen them, and document exclusions (PRISMA-style).

## Funnel (target numbers by mode)

| Stage | `quick` | `standard` | `literature-review` | `extreme` |
|-------|---------|------------|---------------------|-----------|
| **1. Discover** (search hits logged) | 30–50 | 80–120 | **150–250+** | **~2 000** (20 sub-agents) |
| **2. Screen** (title + abstract relevance) | 8–12 | 25–40 | **50–80** | **300–500** |
| **3. Eligible** (on-topic, accessible, tier OK) | 5–8 | 15–25 | **25–40** | **60–100** |
| **4. Read in depth** | 2–3 | 8–12 | **15–25** | **40–60** |
| **5. Cited in synthesis** | 3–5 | 10–15 | **20–35** | **50–80** |

**Depth gate:** agent asks via `AskUserQuestion` before discovery (see SKILL.md Step 0b). Smart-skip only when the user already named a mode. Recommended default in the picker: `literature-review` (150–250+ discovered).

## Stage 1 — Discover (cast a wide net)

**Goal:** log **every distinct candidate** — not just the best 10.

| Mode | `WebSearch` rounds | Queries per round | Target unique candidates |
|------|-------------------|-------------------|--------------------------|
| `quick` | 2–3 | 5–8 | 30–50 |
| `standard` | 4–6 | 8–12 | 80–120 |
| `literature-review` | **8–15** | **10–15** | **150–250+** |
| `extreme` | **20 agents × 8–12** | **4–6 per agent per round** | **~2 000** (see `extreme-orchestration.md`) |

**Query diversification** — each round must use *different angles*, not pagination of the same query:

- Synonyms and adjacent terms
- Author names found in round 1
- `site:arxiv.org`, `site:scholar.google.com`, `site:doi.org`
- Review/survey/meta-analysis
- Conference proceedings (ICRA, NeurIPS, etc. when relevant)
- Industry reports, standards bodies
- Opposing view / limitations / failure cases
- Historical seminal work + recent 2–3 years
- French/local corpus if wedge requires it

**Dedup rule:** same URL or same paper (DOI/arXiv ID) = one entry.

**Log every candidate** to `sources-index.md` immediately — one line each:

```markdown
| # | Title | URL | Found via | Screen |
```

`Screen` values: `pending` → `include` | `exclude` | `eligible` | `read`

## Stage 2 — Screen (title + abstract)

For each candidate (batch by 20–30):

1. Read search snippet; `WebFetch` abstract only if ambiguous
2. Mark `include` if plausibly answers the research question
3. Mark `exclude` with **reason code**:

| Code | Meaning |
|------|---------|
| `OFF_TOPIC` | Adjacent but not on question |
| `LOW_TIER` | Listicle, SEO, no traceability |
| `DUPLICATE` | Same paper as higher-ranked entry |
| `PAYWALL_NO_ALT` | Gated, no preprint found |
| `LANGUAGE` | Wrong language corpus |
| `OUT_OF_DATE` | Superseded by included review |

**Target:** exclude 60–80% — screening is the work.

## Stage 3 — Eligible (quality gate)

From `include`, promote to `eligible` only if:

- Tier 1–3 (see `source-tiers.md`)
- Adds non-redundant evidence or perspective
- Accessible for at least abstract-level verification

Cap eligible pool per mode (table above). Rank eligible; top N become `read`.

## Stage 4 — Read in depth

Full `WebFetch` (or PDF mirror) for every `read` source. Extract structured notes internally before synthesis.

## Stage 5 — Report

- **Synthesis** draws from `read` sources only
- **`sources-index.md`** is the audit trail (all 150–250+ discovered)
- **Report** includes funnel counts + link to full index

## Honesty when tools cap discovery

If after max search rounds the index has **<150 entries** in `literature-review` mode:

1. State the shortfall in the report (`## Search coverage`)
2. List query angles not yet tried
3. Offer continuation: "Run `/deep-research` again with `extend` to add another 100 candidates"

Never pretend 200 sources were screened if the index has 40.

## Extreme mode honesty

`extreme` targets ~2 000 discovered via 20 parallel sub-agents (~100 each). Real counts depend on search API limits.

| Merged unique | Action |
|---------------|--------|
| ≥ 1 500 | Proceed; note any shard failures |
| 1 000–1 499 | Proceed; `## Search coverage` documents shortfall |
| < 1 000 | Tell user extreme target missed; offer `extend` or downgrade to `literature-review` |

Never inflate: raw pre-dedup rows ≠ unique discovered. Report both in `merge-log.md`.