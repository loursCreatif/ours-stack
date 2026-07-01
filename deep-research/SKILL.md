---
name: deep-research
description: |
  Standalone deep research — parallel source discovery, ranked selection, in-depth
  reading, and a structured synthesis report. Works on any topic or question without
  requiring /bear-hours or a study brief. Use when the user wants deep research,
  "recherche approfondie", "research this topic", "find the best sources and summarize",
  "literature review", "what does the evidence say", or runs /deep-research.
  Optional link to studies/<slug>/brief.md for wedge context. Outputs research/<slug>/report.md
  or studies/<slug>/research.md.
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

Classic deep research: **find the best sources, read them, synthesize.** Standalone — no pipeline prerequisite.

**Time budget:** ~10–20 minutes agent work. **Read budget:** 3–5 primary sources in depth + 2–4 supporting skims.

## When to use (vs other skills)

| Skill | Role |
|-------|------|
| `/deep-research` | **This skill** — full question → sources → read → summary report |
| `/bear-hours` | Frame a learning wedge + proof plan (no reading) |
| `/source-scout` | Curate a short reading list inside an existing `brief.md` (no reading) |

Do **not** auto-route here from `/bear-hours`. User invokes `/deep-research` when they want depth now.

## Hard rules

- **Evidence over vibes** — every major claim cites a source (author/year or org + URL).
- **Read before summarizing** — fetch abstracts, key sections, or full pages; do not invent paper content.
- **Rank, then read** — discover broadly, select 3–5 primaries, then go deep on those only.
- **Honest uncertainty** — flag contradictions, weak evidence, paywalls you could not read.
- **Own words** — synthesize; no long copyrighted quotes (see AGENTS.md privacy).
- **Standalone default** — works with a plain research question; brief is optional context, not required.

## Step 0: Intake

Extract from the user's message:

| Input | Required? |
|-------|-------------|
| Research question or topic | **Yes** — if missing, one `AskUserQuestion` |
| Depth | Optional — default `standard` |
| Output location | Optional — default `research/<slug>/` |
| Link to study | Optional — path or slug to `studies/<slug>/brief.md` |

**If the question is vague**, one `AskUserQuestion`:

**Title:** `Deep Research — Sharpen question`

**Ask:** "What exact question should this research answer? One decision, comparison, or mechanism — not a whole field."

**Options:** Infer 2–3 sharpened questions from context + `other`.

**Depth** (infer from message or ask once):

| Mode | Sources read | Report length |
|------|--------------|---------------|
| `quick` | 2 primaries + 1 skim | Executive summary + 3 findings |
| `standard` *(default)* | 3–5 primaries + 2–4 skims | Full report template |
| `exhaustive` | 5–7 primaries + surveys | Full report + theme matrix |

**Escape hatch:** "vas-y" / "just research it" → `standard` depth, no further questions.

### Optional study link

If user names `studies/<slug>/` or a slug exists in context:

1. `Read` `studies/<slug>/brief.md` if present
2. Use `## Narrow wedge` to **focus** search and synthesis (not to refuse broad questions)
3. Save output to `studies/<slug>/research.md` instead of `research/<slug>/report.md`

If no brief → derive `slug` from topic (lowercase, hyphens) and use `research/<slug>/report.md`.

## Step 1: Research plan

Before searching, write internally:

```
QUESTION: <one sentence>
SUB_QUESTIONS: <3–5 bullets>
SUCCESS: <what a good answer enables the user to do>
OUT_OF_SCOPE: <what to exclude>
QUERIES: <6–10 targeted strings>
```

### Query craft

Broader than `/source-scout` — cover definitions, mechanisms, reviews, applications, and debates.

| Query type | Template |
|------------|----------|
| Survey | `"<topic>" review OR survey OR state of the art` |
| Mechanism | `"<mechanism>" how OR principle` |
| Comparison | `"<A>" vs "<B>" <domain>` |
| Primary | `site:arxiv.org OR site:doi.org "<topic>"` |
| Applied | `"<topic>" case study OR deployment` |
| Critique | `"<topic>" limitations OR criticism` |

**Language:** English for STEM; add French for local regulation/market if relevant.

Load `references/source-tiers.md` for ranking. Load `references/report-template.md` before writing.

## Step 2: Discover sources (parallel)

Run **6–10 `WebSearch` calls in parallel** (batch in groups of 4–5 if needed).

Then `WebFetch` candidates to verify: real page, on-topic, acceptable tier.

**Collect 12–20 candidates**, then down-select to:

| Bucket | Count |
|--------|-------|
| Primary (read in depth) | 3–5 (`quick`: 2) |
| Supporting (abstract/skim) | 2–4 |
| Skipped (document why) | 2–4 |

**Ranking weights:**

| Criterion | Weight |
|-----------|--------|
| Answers the research question | 35% |
| Source tier (1 > 2 > 3) | 25% |
| Recency / still cited | 15% |
| Accessible (open PDF/HTML) | 15% |
| Non-redundant with other picks | 10% |

**Cross-study dedup (optional):** If `studies/<slug>/brief.md` exists, skip sources already marked `[x]` in `## Source material`.

## Step 3: Read in depth

For each **primary** source:

1. `WebFetch` landing page, abstract, or PDF HTML mirror
2. Extract: thesis, methods, key results, limitations, relevance to question
3. Note access: `open access` | `paywall` | `partial`

**Stop reading** when primaries are covered — do not chase tangents.

If a paywalled paper has an arXiv preprint or author PDF, fetch that instead.

## Step 4: Synthesize

Follow `references/report-template.md`. Requirements:

- **Executive summary** — 150–300 words; answer the question upfront
- **Key findings** — 5–8 bullets, each with source attribution
- **Synthesis by theme** — group mechanisms/evidence, not one paragraph per source
- **Contradictions** — where sources disagree
- **Open questions** — what remains unresolved
- **Source map** — ranked list with tier, access, and one-line "why selected"

**Quality bar:**

- [ ] Question answered in executive summary (not buried)
- [ ] ≥3 primary sources read and cited
- [ ] ≥2 sources explicitly skipped with reason
- [ ] No claim without a traceable source
- [ ] User can act on "Recommended next steps"

## Step 5: Confirm output location (smart-skip)

**Default:** write directly when user invoked `/deep-research` or said "vas-y".

**Ask** only if overwriting an existing `research.md` / `report.md` from the last 7 days:

**Title:** `Deep Research — Overwrite?`

**Ask:** "A report exists for this slug. Replace or append?"

**Options:**
- Replace — new report
- Append — add `## Update <date>` section
- Cancel

## Step 6: Write artifact

**Standalone path:**

```
research/<slug>/report.md
```

**Study-linked path:**

```
studies/<slug>/research.md
```

Create parent directory if needed. Set `Researched: <YYYY-MM-DD>` in frontmatter block.

**Do not** auto-update `brief.md` `## Source material` — user may run `/source-scout` separately if they want a reading list in the brief.

If study-linked and brief exists, optionally append one line under `## Open questions` only when user asked to link study — never rewrite the brief silently.

## Step 7: Deliver

Tell the user:

1. Path to report
2. **Direct answer** — 2–3 sentences (repeat executive summary lead)
3. **Best source to read first** — name + URL
4. **Confidence** — high | medium | low + one-line why
5. Optional: "Run `/bear-hours` to turn this into a learning wedge" or "/source-scout to curate papers in a brief" — mention only, do not auto-route

## Escape hatches

| User says | Action |
|-----------|--------|
| "quick" / "5 min" | `quick` depth |
| "exhaustive" / "everything" | `exhaustive`, warn on time |
| "French only" / "English only" | Restrict sources; note gaps |
| "free only" | Drop paywalled; note skipped |
| "no file" | Chat-only summary, skip Write |
| "update my brief" | After report, offer to copy source list into `brief.md` via user confirmation |

## Self-check before finish

- [ ] Research question stated at top of report
- [ ] Source map lists anchor + primaries + skipped
- [ ] Synthesis is thematic, not a bibliography dump
- [ ] Paywalled gaps acknowledged
- [ ] Report path communicated to user