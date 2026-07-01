---
name: deep-research
description: |
  Standalone classic deep research — wide discovery (150–250+ sources screened in
  literature-review mode), PRISMA-style funnel, ranked selection, in-depth reading
  on the top 15–25, structured synthesis report. Works on any topic without
  requiring /bear-hours. Use when the user wants deep research, "recherche approfondie",
  "literature review", "research this topic", "find the best sources and summarize",
  or runs /deep-research. Asks depth level up front (source counts per mode). Modes:
  quick (30–50), standard (80–120), literature-review (150–250+), extreme (~2 000
  via 20 sub-agents — double confirmation + token/time warning). Outputs
  research/<slug>/report.md + sources-index.md.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - AskUserQuestion
  - Task
  - Bash
---

# Deep Research

Classic deep research = **search wide (100s) → screen → read deep (10s–20s) → synthesize.**

Standalone — no pipeline prerequisite. Follow `references/screening-funnel.md` for target numbers.

## When to use (vs other skills)

| Skill | Role |
|-------|------|
| `/deep-research` | **This skill** — 30–2 000 candidates (mode-dependent), top sources read, full report |
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

## Interactive questions

Use **`AskUserQuestion`** for intake gates (Grok Build maps it to the plan-mode widget).

**Hard rules:**
- **Never** list depth options as plain chat bullets — always call `AskUserQuestion`
- **One question per call** — sharpen question and depth are separate calls
- **STOP** after each call; wait for the answer before continuing
- **Do not start discovery** (Step 2) until depth is confirmed
- **`extreme` requires two confirmations** — picker + dedicated cost gate (Step 0c)

**Title format:** `Deep Research — {label}`

## Step 0: Intake

| Input | Required? |
|-------|-------------|
| Research question | **Yes** |
| Depth mode | **Yes** — via `AskUserQuestion` (unless smart-skipped) |
| Study link | Optional — `studies/<slug>/brief.md` |

### 0a — Research question

Take the question from the user's message. If missing or too broad for one sentence → `AskUserQuestion`:

**Title:** `Deep Research — Question`

**Ask:** "Quelle question précise veux-tu que je réponde ? (une phrase, cadrée)"

**Options:** infer 2–3 sharpened variants from context, plus `other` — "Autre — je précise dans mon prochain message".

### 0b — Depth level (mandatory gate)

**Always** call `AskUserQuestion` before Step 1 — unless smart-skipped (below).

**Title:** `Deep Research — Profondeur`

**Ask:** "Quel niveau de profondeur ? Ça fixe combien de sources je **cherche**, **filtre** et **lis** en profondeur."

**Options** (fixed — show all four with counts):

| Option label | Mode ID |
|--------------|---------|
| **Quick** — ~30–50 sources cherchées · 8–12 retenues au filtre · 2–3 lues · ~10 min | `quick` |
| **Standard** — ~80–120 cherchées · 25–40 retenues · 8–12 lues · ~20 min | `standard` |
| **Literature review** *(recommandé)* — **150–250+** cherchées · 50–80 retenues · **15–25** lues · ~40–60 min | `literature-review` |
| **Extrême** ⚠️ — **~2 000** cherchées · **20 sous-agents** · 40–60 lues · **coût tokens & temps élevés** (~1–3 h) | `extreme` |

If user picks **`extreme`** → **STOP** — go to Step 0c (do not confirm or start yet).

For `quick` / `standard` / `literature-review`, **confirm in one line** before Step 1, e.g.:
`Mode literature-review — je vise 150–250+ sources découvertes, 15–25 lectures en profondeur.`

### 0c — Extreme confirmation (mandatory for `extreme` only)

Second gate — never skip. Call `AskUserQuestion`:

**Title:** `Deep Research — Extrême ⚠️`

**Ask:** "Mode extrême : **~2 000 sources** via **20 sous-agents** en parallèle (WebSearch massif). **Coût estimé : 500k–2M+ tokens** et **1–3 heures**. Les APIs peuvent plafonner avant 2k — je rapporterai le compte réel. Tu confirmes ?"

**Options:**
- **Oui** — lancer le mode extrême (j'accepte tokens + temps)
- **Non** — revenir au choix de profondeur (Step 0b)

If **Non** → re-run Step 0b.

If **Oui** → confirm in one line, e.g.:
`Mode extreme confirmé — 20 sous-agents, cible ~2 000 sources découvertes, 40–60 lectures en profondeur.`

**Smart-skip** (no depth question) only when the user **already named** a mode or time budget:

| User said | Mode |
|-----------|------|
| `quick`, "rapide", "5 min", "10 min" | `quick` |
| `standard`, "moyen", "~20 min" | `standard` |
| `literature-review`, "recherche approfondie", "literature review", "complet", "full" | `literature-review` |
| `extreme`, "extrême", "2000", "2 000", "max depth" | `extreme` — **still run Step 0c** |
| `/deep-research quick` (mode in slash args) | matching mode |

**Not smart-skip:** bare `/deep-research`, "vas-y", "go", "lance" without a mode → **ask**.

**Extreme never smart-skips Step 0c** — even if user said "extreme" upfront, always show the cost gate.

**Depth modes reference:**

| Mode | Discovered | Screened in | Read in depth | Time hint |
|------|------------|-------------|---------------|-----------|
| `quick` | 30–50 | 8–12 | 2–3 | ~10 min |
| `standard` | 80–120 | 25–40 | 8–12 | ~20 min |
| `literature-review` | **150–250+** | **50–80** | **15–25** | ~40–60 min |
| `extreme` | **~2 000** | **300–500** | **40–60** | **~1–3 h** ⚠️ |

### Optional study link

If `studies/<slug>/brief.md` exists → use wedge to focus screening; save to `studies/<slug>/research.md` + `studies/<slug>/sources-index.md`.

Else → `research/<slug>/report.md` + `research/<slug>/sources-index.md`.

## Step 1: Research plan

```
QUESTION: <one sentence>
SUB_QUESTIONS: <5–8 bullets>
INCLUSION: <what counts as on-topic>
EXCLUSION: <what to reject>
QUERY_ANGLES: <12–20 distinct angles for literature-review; 20 non-overlapping clusters for extreme>
```

Load `references/screening-funnel.md`, `references/source-tiers.md`, `references/report-template.md`.

For **`extreme`** also load `references/extreme-orchestration.md` and write `research/<slug>/discovery/plan.md` (20 agent clusters).

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

### Extreme — parallel sub-agent discovery

**Only after Step 0c confirmed.** Follow `references/extreme-orchestration.md`.

1. Create `research/<slug>/discovery/` and `discovery/plan.md` (20 angle clusters)
2. Launch **20 `Task` sub-agents in one parallel message** (`subagent_type: generalPurpose`, `model: composer-2.5-fast`)
3. Each agent targets **~100** candidates → `discovery/shard-NN.md` (WebSearch only, no WebFetch)
4. Merge all shards → `sources-index.md` + `discovery/merge-log.md` (global dedup, honest count)
5. If merged unique **< 1 000** → tell user extreme target missed; offer `extend` or downgrade

Do **not** run extreme discovery single-threaded — the 20-agent fan-out is the point.

## Step 3: Screen — title + abstract

Process **every** `pending` row in batches of 25–40.

1. Use snippet; `WebFetch` abstract only when title/snippet ambiguous
2. Set `Screen`: `include` or `exclude` + reason code (`OFF_TOPIC`, `DUPLICATE`, `LOW_TIER`, `PAYWALL_NO_ALT`, `LANGUAGE`, `OUT_OF_DATE`)
3. For `include` → assign tier estimate; promote best to `eligible`

**Screen 60–80% out.** Typical literature-review outcome: ~50–80 `include` from 200 discovered.

**Extreme:** always launch up to **10 screening sub-agents** in parallel (see `extreme-orchestration.md`); merge into `sources-index.md`. Target **300–500** `include` from ~2 000.

Update `sources-index.md` in place as you go.

## Step 4: Rank eligible → select for deep read

Rank `eligible` sources (weights: answers question 35%, tier 25%, recency 15%, access 15%, non-redundancy 10%).

Promote top N to `read` per mode (15–25 for literature-review; **40–60 for extreme**). Mark others `eligible — not deep-read` with one-line why.

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

If **`extreme`** and discovered < 1 500 → `## Search coverage` + `## Extreme run metadata` per `extreme-orchestration.md`.

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

Suggest (do not auto-route): `/layout-html` for mise en page HTML — works on this report or any other text.

## Escape hatches

| User says | Action |
|-----------|--------|
| `quick` / `5 min` | Smart-skip depth ask → 30–50 discovered, 2–3 read |
| `standard` | Smart-skip depth ask → 80–120 discovered, 8–12 read |
| `literature-review` / "recherche approfondie" | Smart-skip depth ask → 150–250+ discovered, 15–25 read |
| `extreme` / "extrême" | Smart-skip depth ask → **still require Step 0c** → 20 agents, ~2k target |
| `vas-y` / `go` without mode | **Ask** depth via `AskUserQuestion` — do not default silently |
| `stop` / `arrête` (extreme) | Halt sub-agents; merge partial index; report funnel so far |
| `extend` | Append new discovery round to existing `sources-index.md`, re-screen, update report |
| `free only` | Exclude paywalled without preprint |
| `no file` | Chat summary + funnel counts only |

## Self-check

- [ ] `sources-index.md` exists with **actual** discovered count
- [ ] Literature-review: ≥150 discovered OR shortfall documented
- [ ] Every exclude has a reason code
- [ ] 15–25 deep-reads (literature-review) or mode-appropriate count (40–60 for extreme)
- [ ] Extreme: Step 0c confirmed; 20 shard files attempted; `merge-log.md` exists
- [ ] Extreme: never claim 2k discovered if merge count is lower
- [ ] Funnel table in report matches index counts
- [ ] Synthesis cites only deep-read sources