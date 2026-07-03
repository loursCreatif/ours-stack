---
name: source-scout
description: |
  Curated source discovery for ours-stack studies — wedge-locked, ranked, time-boxed.
  Reads studies/<slug>/brief.md, searches in parallel (papers, docs, repos, demos),
  dedupes prior studies, and writes a short actionable list into ## Source material.
  Use when source material is TBD, the user asks for papers/sources/references,
  "trouve des sources", "recherche de sources", "quelle source lire", or runs /source-scout.
  Run after /bear-hours; before dense reading. Screens candidate pools (~10 per slot, on-wedge
  only) before ranking exactly 3 sources (article + YouTube or fallback + joker); opens URLs in browser.
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

# Source Scout

Find the **smallest set of sources** that unlock the wedge in `brief.md` — not a bibliography, not a literature review.

**Time budget:** ~3–5 minutes of search. **Output:** exactly **3 sources** — one written article, one YouTube video (or honest fallback), one joker (site, second video, or second article).

## Hard rules

- **Wedge lock** — every source must help explain the `## Narrow wedge` unit. Reject everything else, even if interesting.
- **Fetch before you pick** — `WebFetch` **every finalist** before it enters the final 3. A snippet or a promising title is never enough: you must have seen the actual content and judged its density. No exceptions, including the joker.
- **Evidence in every Why** — each source's `Why:` or score justification must name **one concrete element you saw in the fetched page** (a section, figure, dataset, measured result, argument). If you can't name one, you haven't screened it — fetch again or drop it.
- **No reading** — scout landing pages, abstracts, tables of contents. Do not summarize content; do not write `notes.md`.
- **Density over breadth** — prefer one review paper over five blog posts. See `references/source-tiers.md`.
- **Candidate pools first** — screen ~10 on-wedge candidates per slot before picking the final 3; never pad pools with off-wedge hits.
- **Show rejections** — list 1–3 sources you considered and skipped (teaches the wedge boundary); include a rejected YouTube when the video slot was weak or fallback-replaced.
- **Respect prior work** — never re-recommend sources already marked `[x]` in this or related studies.
- **Open access first** — flag paywalls upfront; always offer a free alternative when one exists.

## Step 0: Resolve study

**If the user names a slug or path** → use it.

**Else** → `Glob` `studies/*/brief.md`. Then `AskUserQuestion`:

**Title:** `Source Scout — Which study?`

**Ask:** "Which study should I scout sources for?"

**Options:** Up to 3 slugs with one-line wedge summaries + `other`.

**If `other`** → accept slug or topic in chat, then locate or create via `/bear-hours` if no brief exists.

**If no brief** → stop: "Run `/bear-hours` first — I need a wedge before I can scout."

## Step 1: Load context

Read `studies/<slug>/brief.md`. Extract:

| Field | Use for |
|-------|---------|
| `## Narrow wedge` | Primary filter — quote the one-line unit in every relevance check |
| `## Current beliefs` | Prioritize sources that **test** beliefs marked "à tester" |
| `## Open questions` | Map each core source to ≥1 question it **targets** (not resolves) |
| `## Prior progress` | Related slugs → read their `brief.md` `## Source material` for dedup |
| `## Source material` | Skip if already curated (not `TBD`) — see smart-skip below |

**Smart-skip:** If `## Source material` already has ≥3 unchecked `[ ]` items scoped to the wedge, call `AskUserQuestion`:

**Title:** `Source Scout — Sources exist`

**Ask:** "This brief already has sources. What do you want?"

**Options:**
- Refresh — re-scout from scratch (replace list)
- Extend — re-scout with a named gap; still outputs exactly 3 sources (may swap one slot)
- Keep — cancel scout

### Cross-study dedup (optional, with consent)

**Always dedupe** against the current `brief.md` (`[x]` consumed sources).

**Before reading `~/.ours-stack/studies-index.jsonl`**, call `AskUserQuestion`:

**Title:** `Source Scout — Prior studies`

**Ask:** "Search registered prior studies for already-read sources?"

**Options:**
- Yes — check prior studies *(recommended if `## Prior progress` mentions related slugs)*
- No — scout this brief only

If **Yes**: read the index, find entries with overlapping keywords in `wedge` or `title`, read their `## Source material` only, note consumed `[x]` and pending `[ ]` sources. **Limit:** max 2 related briefs opened.

## Step 2: Derive search plan

Before any search, write internally (do not show the user yet):

```
WEDGE_UNIT: <one sentence from brief>
BELIEFS_TO_TEST: <bullets>
OPEN_QUESTIONS: <bullets>
OUT_OF_SCOPE: <from "Hors scope" lines in wedge section>
QUERIES: <3–6 targeted strings>
```

### Query craft (this is where time is won or lost)

Derive **3–6 queries** from the wedge — not from the study title.

| Query type | Template | Example |
|------------|----------|---------|
| **Anchor** | `"<wedge concept>" review OR survey` | `legged locomotion irregular terrain review` |
| **Primary** | `"<specific mechanism>" <domain> paper` | `tripod gait hexapod stability` |
| **Applied** | `"<real system>" <constraint from wedge>` | `construction robot brick laying site` |
| **Maker** | `"<topic>" open source OR github` | `hexapod robot open source arduino` |
| **Belief test** | `"<belief keyword>" vs OR comparison` | `wheels vs legs rough terrain robot` |
| **Video** *(mandatory, timeboxed)* | `"<wedge concept>" lecture OR conference OR demo` | `legged locomotion conference talk` |
| **Measured** *(hardware/energy wedges)* | `"<device>" <metric> measured review` | `RTX 4090 power consumption measured review` |

Use only types that fit the wedge. Do not force Maker or Belief test if the wedge is purely theoretical.

**Language:** search in English for STEM; add French queries only for réglementation, marché local, or francophone-only corpora.

**Anti-queries** — do NOT search: the broad field name alone, "introduction to X", "top 10", "best resources", the study title verbatim.

Load `references/source-tiers.md` for tier definitions and rejection patterns.

## Step 3: Search and screen pools

Run **3–6 `WebSearch` calls in parallel** (one per query, including the mandatory **Video** query). Then screen hits into three pools:

| Pool | Slot | Target size | Acceptable formats |
|------|------|-------------|-------------------|
| **A** | article | **10** candidates screened | paper, reference doc, dense post (Tier 1–2) |
| **V** | video | **10** candidates screened | YouTube only |
| **J** | joker | **10** candidates screened | site, second video, or second article |

**Target 10** = candidates **examined** (snippet + selective `WebFetch`), not final sources.

**On-wedge rule:** add a candidate only if it helps explain `WEDGE_UNIT`. **Never** pad a pool with adjacent-topic, primer, or listicle hits just to reach 10. If only 4 good article candidates exist, pool A size = 4 — note internally `pool < target`.

**Per candidate (quick screen):** page real (not 404) · matches wedge (not adjacent) · tier acceptable (`references/source-tiers.md`) · not duplicate of another pool entry or prior `[x]` source.

**Search breadth:** for each pool, paginate or vary queries until ~10 screened **or** diminishing returns (2 consecutive pages with zero on-wedge adds). Use source-type shortcuts: arXiv/DOI (papers), `site:youtube.com` (video), company docs/GitHub (joker site/repo).

### YouTube pool — strict quality bar + timebox (Pool V)

**Timebox:** max **2 minutes** on Pool V total · max **3** `WebFetch` on YouTube URLs · if zero strong survivors → **immediate fallback** (do not retry `site:youtube.com`). Prefer broad queries over operator lock.

`WebFetch` every YouTube survivor — snippet alone is not enough (title, channel, duration, description).

**Verify WHO speaks:** before keeping a Pool V candidate, identify the **channel or speaker**. If unknown after `WebFetch`, run **one timeboxed `WebSearch`** on the channel name (≤30 s). Anonymous or unverifiable channels fail the authority bar (cap ≤6/10 → article fallback).

| Accept | Reject |
|--------|--------|
| Course lecture, conference talk (ICRA, etc.), expert talk, technical demo, full recording with real wedge content | Teaser, trailer, hype clip, generalist « introduction to », SEO tutorial, superficial recap, news without mechanism, off-wedge tangent |
| Named speaker or institution-backed channel; corpus specialized in the wedge domain | Anonymous channel, marketing-only channel, corpus mainly off-wedge |

**Minimum to stay in Pool V:** **strong** wedge alignment (core topic, not a passing mention) **and** density (mechanism, argument, or demo — not vocabulary-only) **and** identifiable authority.

**Video fallback:** if **no** Pool V candidate passes the bar, replace slot 2 with the best **article or site Tier 1–3** from Pool A or J (not a bad video). Tell the user: *« Aucune vidéo YouTube assez forte sur le wedge — slot vidéo remplacé par [format]. »*

**Stop when:** all three pools are built (up to target size or honestly exhausted) — **not** when 3 finalists are found.

## Step 4: Rank and score (your judgment, on fetched content)

You rank — based on what you actually saw in the fetched pages, not on titles or URLs. Score each candidate:

| Criterion | Weight | 9/10 requires… |
|-----------|--------|----------------|
| Wedge alignment | 35% | Core mechanism of `WEDGE_UNIT`, not adjacent topic |
| Density | 25% | Mechanism, data, or measurement seen in the fetched page — not vocabulary-only |
| Authority / traceability | 15% | Named verifiable author, institution, established technical media, or on-wedge specialized corpus |
| Open question / belief | 15% | Maps to ≥1 `## Open questions` or `## Success criteria` |
| Accessible | 5% | Working link, open or honest paywall note |
| Non-redundant | 5% | No overlap with other 2 picks |

**Authority hard cap:** source without identifiable author/channel **≤6/10** — slot 2 falls back to best article/site (never a weak anonymous video).

**Swap heuristics:** prefer third-party **measured** data over vendor spec sheets; prefer a Tier 1–2 measurement paper or official doc over a homelab blog/listicle; when the wedge mentions a quantitative constraint (autonomie, coût, capacité…), include one source with real numbers on it.

**Final pick:** exactly **1 article** (Pool A) + **1 video or fallback** (Pool V winner, else best article/site) + **1 joker** (Pool J) → designate **anchor** (best wedge unlock). Do not add a 4th source.

**Fetch check (mandatory):** before writing, confirm all 3 finalists were `WebFetch`ed during screening. If one wasn't, fetch it now — and re-score it on what you see.

**Floor:** every source **≥9/10** and set global **≥9/10**. If pools are honestly exhausted and the best set is <9 → widen or vary queries once; if still <9, say so to the user and document the gap in `.context/` — do not inflate scores to pass the gate.

## Step 5: Confirm before write

**Default:** if the user invoked `/source-scout` and the brief has `TBD` or thin sources, **skip confirmation** and write directly. Confirm only when replacing an existing curated list (≥3 `[ ]` items) or when the user did not explicitly invoke the skill.

Otherwise, call `AskUserQuestion`:

**Title:** `Source Scout — Confirm`

**Ask:** Show anchor title + 3-line wedge + the 3 sources with formats (article / video / joker). "Write this to `studies/<slug>/brief.md`?"

**Options:**
- Yes — write sources
- Swap anchor — user names which of the 3 should be anchor
- Swap slot — user names which source to replace (re-scout that slot only)
- Add constraint — user adds access/language/format requirement (one chat reply, then re-confirm)

If the user cancels or chooses **Keep** at Step 1 smart-skip → do not write; do not open browser tabs.

## Step 6: Write and route

Replace (or create) `## Source material` in `brief.md` with exactly this structure:

```markdown
## Source material

Scouted <YYYY-MM-DD> via `/source-scout` :

### Read first (anchor)
- [ ] **Author (year)** — *Title* — <URL>
  - Format: article | video | site
  - Tier: 1|2|3 · ~<15|45|90> min · <open access|paywall>
  - Why: <one line — what wedge unit this unlocks + one concrete element seen in the fetched page>
  - Targets: <open question or belief this source is likely useful for>
  - Score: <N>/10 — <one line justification>

### Core
- [ ] **…** — *Title* — <URL>
  - Format: article | video | site
  - Tier: … · ~… min · …
  - Why: …
  - Targets: …
  - Score: <N>/10 — <one line justification>
- [ ] **…** — *Title* — <URL>
  - Format: article | video | site
  - Tier: … · ~… min · …
  - Why: …
  - Targets: …
  - Score: <N>/10 — <one line justification>

### Skipped (wedge boundary)
- *Title* — <why out of scope, redundant, or weak video rejected>

### Scout scores
- Set: <N>/10 — <one line global justification>
```

**Skipped quality:** ≥1 entry always; when Pool V was thin or fallback used, include **≥1 rejected YouTube** with reason (teaser / off-wedge / low density). Keep list to 1–3 lines — not a full pool dump.

**Checkbox convention:** `[ ]` = not read · `[x]` = consumed (set by future read skills, not here).

**Anchor rule:** exactly one of the 3 sources is anchor. The user should start there without deciding.

**Count rule:** exactly 3 sources total (1 anchor + 2 core). No `### Optional` section.

**Honesty rule:** Do not claim a source *answers* a question during scouting. Say it **targets**, **tests**, or is **likely relevant to** the question. Resolution happens when the anchor is read in depth — not here.

Then:

1. **Quality gate (blocks handoff):**

```bash
"$(git rev-parse --show-toplevel)/bin/ours-stack-source-scout-validate" studies/<slug>/brief.md
```

Non-zero exit → fix the section (structure or honest re-scout) and re-run; do not open browser or hand off until exit 0.

2. **Do not remove** items from `## Open questions`. Reference targeted questions under each source via `Targets:`. Do not mark questions resolved here.

3. Re-register study:

```bash
bin/ours-stack-register-study studies/<slug>/brief.md
```

4. **Open sources in browser** (only if Step 5 was not cancelled and validate passed) — one command per URL, `open` on macOS, `xdg-open` fallback on Linux.

5. **Handoff — passation** (skip if Step 5 cancelled or validate failed). Two beats — tone like `bear-hours` Step 4; personalized, direct, no ceremony.

**Anti-slop:** quote the `## Narrow wedge` unit; no « Félicitations ! », no filler. GOOD: « Sur [wedge], 3 sources sont dans le brief — commence par [anchor]. » BAD: template sentence alone. One line: scout found sources; it did not read them.

**Beat 1 — Ce qui vient d'être fait:** One short paragraph — 3 sources for **« <wedge unit> »** in `studies/<slug>/brief.md`; if browser opened → **les 3 sources sont ouvertes dans ton navigateur**; name the anchor (read first); video fallback line if slot 2 is not YouTube. Close with one line: prochaine étape = `/dense-read` sur l'anchor (lecture guidée tranche par tranche).

**Beat 2 — Carte du parcours:**

```
✅ /bear-hours — cadrage (fait)
✅ /source-scout — 3 sources trouvées (fait)
→ /dense-read — lecture guidée de l'anchor, tranche par tranche
  /study-status — à tout moment, pour voir où tu en es
```

## Escape hatches

| User says | Action |
|-----------|--------|
| "just find something" / "vas-y" | Skip Step 5, write exactly 3 picks (article + video + joker) |
| "no video" / "skip youtube" | Replace video slot with article or site; say so explicitly |
| "French only" | Restrict to FR sources; note gap if wedge needs English primaries |
| "free only" | Drop paywalled; note what was skipped |

## Quality bar (self-check before write)

- [ ] Pools screened: ~10 on-wedge candidates per slot **if available** — never padded off-wedge
- [ ] Exactly 3 sources: article + video (or honest Tier 1–3 fallback) + joker
- [ ] **All 3 finalists `WebFetch`ed** — every `Why:` names a concrete element seen in the page
- [ ] **Each source ≥9/10** and **set global ≥9/10** — or gap stated honestly, never score inflation
- [ ] YouTube timebox respected (≤2 min, ≤3 WebFetch) — fallback stated on `Why:` if used
- [ ] Each source has `Format: article | video | site`
- [ ] Anchor is Tier 1 or 2 when possible and directly on the wedge unit
- [ ] Every source targets an open question or success criterion (no false "answered" claims)
- [ ] ≥1 skipped documented; rejected YouTube noted when video slot weak or replaced
- [ ] No source already `[x]` in this or related studies
- [ ] `ours-stack-source-scout-validate` exits 0
- [ ] User knows which single source to open first
- [ ] Handoff delivered (2 beats) unless Step 5 cancelled
