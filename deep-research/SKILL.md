---
name: deep-research
description: |
  Standalone classic deep research — wide discovery (150–250+ sources screened in
  literature-review mode), PRISMA-style funnel, ranked selection, in-depth reading
  on the top 15–25, structured synthesis report. Works on any topic without
  requiring /bear-hours. Use when the user wants deep research, "recherche approfondie",
  "literature review", "research this topic", "find the best sources and summarize",
  or runs /deep-research. Modes: quick (30–50), standard (80–120), literature-review
  (150–250+ discovered). Outputs research/<slug>/report.md + sources-index.md.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - AskUserQuestion
  - Bash
---

# Deep Research

Classic deep research = **search wide (100s) → screen → read deep (10s–20s) → synthesize.**

Standalone — no pipeline prerequisite. Follow `references/screening-funnel.md` for target numbers.

## When to use (vs other skills)

| Skill | Role |
|-------|------|
| `/deep-research` | **This skill** — 150–250+ candidates screened, top sources read, full report |
| `/bear-hours` | Frame a learning wedge (no reading) |
| `/source-scout` | 5–7 reading picks in `brief.md` (no reading) |

Do **not** auto-route here from other skills.

## Hard rules

- **Search wide before reading** — log every candidate; never jump to 5 sources and call it done.
- **Screening is mandatory** — document exclusions with reason codes (see funnel reference).
- **Read before summarizing** — deep-read only `eligible` top picks; do not invent paper content.
- **Two artifacts** — `sources-index.md` (full audit trail) + `report.md` (synthesis).
- **Honest counts** — if discovery < target for the mode, say so; never fake 200 screened.
- **Own words** — synthesize; no long copyrighted quotes (AGENTS.md).

## Step 0: Intake

| Input | Required? |
|-------|-------------|
| Research question | **Yes** |
| Depth mode | Optional — default `literature-review` |
| Study link | Optional — `studies/<slug>/brief.md` |

**Depth modes:**

| Mode | Discovered | Screened in | Read in depth | Time hint |
|------|------------|-------------|---------------|-----------|
| `quick` | 30–50 | 8–12 | 2–3 | ~10 min |
| `standard` | 80–120 | 25–40 | 8–12 | ~20 min |
| `literature-review` *(default)* | **150–250+** | **50–80** | **15–25** | ~40–60 min |

**Default:** `literature-review` — user invoked `/deep-research` or said "recherche approfondie".

**Escape hatch:** "quick" / "5 min" → `quick`. "vas-y" without time hint → `literature-review`.

If question vague → one `AskUserQuestion` (sharpen question). See prior version for wording.

### Optional study link

If `studies/<slug>/brief.md` exists → use wedge to focus screening; save to `studies/<slug>/research.md` + `studies/<slug>/sources-index.md`.

Else → `research/<slug>/report.md` + `research/<slug>/sources-index.md`.

## Step 1: Research plan

```
QUESTION: <one sentence>
SUB_QUESTIONS: <5–8 bullets>
INCLUSION: <what counts as on-topic>
EXCLUSION: <what to reject>
QUERY_ANGLES: <12–20 distinct angles for literature-review>
```

Load `references/screening-funnel.md`, `references/source-tiers.md`, `references/report-template.md`.

## Step 2: Discover — cast the wide net

**This step dominates.** Do not proceed to deep reading until the discovery target is met or max rounds exhausted.

### Search rounds (literature-review)

Run **8–15 rounds** of parallel `WebSearch` (4–5 queries per round). Each round uses **new query angles** from the plan — not repeats.

Rotate across:

| Angle | Example |
|-------|---------|
| Survey / SOTA | `"<topic>" systematic review` |
| Mechanism | `"<mechanism>" principle` |
| Seminal | `<founding author> <year>` |
| Recent | `<topic> 2024..2026` |
| Venue | `site:arxiv.org`, `site:ieee.org`, conference name |
| Applied | `case study deployment` |
| Critique | `limitations challenges` |
| Adjacent | synonym terms, related subfields |
| Grey lit | technical reports, theses, industry whitepapers |
| FR/local | if question needs it |

**After each round:** append new unique candidates to `sources-index.md`:

```markdown
# Sources index — <slug>

**Question:** ...
**Mode:** literature-review
**Last updated:** <YYYY-MM-DD>

| # | Title | URL | Found via | Tier est. | Screen | Exclude reason |
|---|-------|-----|-----------|-----------|--------|----------------|
| 1 | ... | ... | survey query | 2 | pending | |
```

Dedup by URL / DOI / arXiv ID. **Target: 150–250+ rows** before screening.

`quick` / `standard`: fewer rounds per funnel table — same logging discipline.

## Step 3: Screen — title + abstract

Process **every** `pending` row in batches of 25–40.

1. Use snippet; `WebFetch` abstract only when title/snippet ambiguous
2. Set `Screen`: `include` or `exclude` + reason code (`OFF_TOPIC`, `DUPLICATE`, `LOW_TIER`, `PAYWALL_NO_ALT`, `LANGUAGE`, `OUT_OF_DATE`)
3. For `include` → assign tier estimate; promote best to `eligible`

**Screen 60–80% out.** Typical literature-review outcome: ~50–80 `include` from 200 discovered.

Update `sources-index.md` in place as you go.

## Step 4: Rank eligible → select for deep read

Rank `eligible` sources (weights: answers question 35%, tier 25%, recency 15%, access 15%, non-redundancy 10%).

Promote top N to `read` per mode (15–25 for literature-review). Mark others `eligible — not deep-read` with one-line why.

## Step 5: Read in depth

`WebFetch` each `read` source. Extract: thesis, methods, results, limitations.

Prefer arXiv / author PDF when paywalled. Skim abstracts only for `eligible` not promoted if they inform the funnel counts.

## Step 6: Synthesize

Write `report.md` per `references/report-template.md`:

- **Screening funnel table** with real counts from `sources-index.md`
- **Executive summary** — answer first
- **Synthesis by theme** — from `read` sources only
- **Exclusion summary** — aggregate reason codes
- Pointer to full `sources-index.md`

If discovered < 150 in literature-review mode → `## Search coverage` section: shortfall, untried angles, offer `extend` pass.

## Step 7: Confirm overwrite (smart-skip)

Skip confirmation on fresh slug. Ask only when overwriting recent `report.md` / `sources-index.md`.

## Step 8: Deliver

Tell the user:

1. Paths: `report.md` + `sources-index.md`
2. **Funnel counts** — discovered / screened / read
3. **Direct answer** — 2–3 sentences
4. **Best source to read first**
5. **Confidence** — high | medium | low

If discovered < target: say how many more rounds would close the gap.

## Escape hatches

| User says | Action |
|-----------|--------|
| `quick` / `5 min` | 30–50 discovered, 2–3 read |
| `standard` | 80–120 discovered, 8–12 read |
| `literature-review` / default | 150–250+ discovered, 15–25 read |
| `extend` | Append new discovery round to existing `sources-index.md`, re-screen, update report |
| `free only` | Exclude paywalled without preprint |
| `no file` | Chat summary + funnel counts only |

## Self-check

- [ ] `sources-index.md` exists with **actual** discovered count
- [ ] Literature-review: ≥150 discovered OR shortfall documented
- [ ] Every exclude has a reason code
- [ ] 15–25 deep-reads (literature-review) or mode-appropriate count
- [ ] Funnel table in report matches index counts
- [ ] Synthesis cites only deep-read sources