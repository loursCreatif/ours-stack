---
name: source-scout
description: |
  Curated source discovery for ours-stack studies — wedge-locked, ranked, time-boxed.
  Reads studies/<slug>/brief.md, searches in parallel (papers, docs, repos, demos),
  dedupes prior studies, and writes a short actionable list into ## Source material.
  Use when source material is TBD, the user asks for papers/sources/references,
  "trouve des sources", "recherche de sources", "quelle source lire", or runs /source-scout.
  Run after /bear-hours; before dense reading. Outputs exactly 3 wedge-locked sources
  (article + YouTube video + joker) with anchor designation; opens URLs in browser.
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

**Time budget for the agent:** ~3–5 minutes of search. **Output budget for the user:** exactly **3 sources** — one written article, one YouTube video, one joker (site, second video, or second article).

## Hard rules

- **Wedge lock** — every source must help explain the `## Narrow wedge` unit. Reject everything else, even if interesting.
- **No reading** — scout landing pages and abstracts only. Do not summarize content; do not write `notes.md`.
- **Density over breadth** — prefer one review paper over five blog posts. See `references/source-tiers.md`.
- **Show rejections** — list 1–3 sources you considered and skipped (teaches the wedge boundary).
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

If **No** → skip index; only dedupe within current brief.

If **Yes**:

1. `Read` index · find entries with overlapping keywords in `wedge` or `title`
2. Read their `brief.md` `## Source material` only
3. Note consumed `[x]` and pending `[ ]` sources — do not duplicate

**Limit:** max 2 related briefs opened.

## Step 2: Derive search plan

Before any search, write internally (do not show the user yet):

```
WEDGE_UNIT: <one sentence from brief>
BELIEFS_TO_TEST: <bullets>
OPEN_QUESTIONS: <bullets>
OUT_OF_SCOPE: <from "Hors scope" lines in wedge section>
QUERIES: <3–5 targeted strings>
```

### Query craft (this is where time is won or lost)

Derive **3–5 queries** from the wedge — not from the study title.

| Query type | Template | Example |
|------------|----------|---------|
| **Anchor** | `"<wedge concept>" review OR survey` | `legged locomotion irregular terrain review` |
| **Primary** | `"<specific mechanism>" <domain> paper` | `tripod gait hexapod stability` |
| **Applied** | `"<real system>" <constraint from wedge>` | `construction robot brick laying site` |
| **Maker** | `"<topic>" open source OR github` | `hexapod robot open source arduino` |
| **Belief test** | `"<belief keyword>" vs OR comparison` | `wheels vs legs rough terrain robot` |
| **Video** *(required)* | `site:youtube.com "<wedge concept>" lecture OR conference OR talk` | `site:youtube.com hexapod locomotion ICRA talk` |

Pick **3–5 queries** from the types above — use only types that fit the wedge. Do not force Maker or Belief test if the wedge is purely theoretical.

**Mandatory:** at least one query must be type **Video** (`site:youtube.com` + wedge concept + lecture/conference/talk/demo). Without it, the scout contract is incomplete.

**Language:** search in English for STEM; add French queries only for réglementation, marché local, or francophone-only corpora.

**Anti-queries** — do NOT search: the broad field name alone, "introduction to X", "top 10", "best resources", the study title verbatim.

Load `references/source-tiers.md` for tier definitions and rejection patterns.

## Step 3: Search in parallel

Run **3–5 `WebSearch` calls in parallel** (one per query, including the mandatory **Video** query). Then selectively `WebFetch` top hits to verify:

- Page is real (not 404 / paywall trap)
- Content matches wedge (not adjacent topic)
- Tier is acceptable (see references)

**YouTube slot (required):** `WebFetch` the chosen YouTube URL — confirm the video exists and matches the wedge (title, channel, duration from page/snippet). Snippet alone is not enough. Reject teasers, trailers, and off-wedge tangents.

**Video fallback:** if no relevant YouTube video exists on the wedge, replace slot 2 with a second article or site (Tier 1–3). Tell the user explicitly in delivery: *« Aucune vidéo YouTube pertinente sur le wedge — slot vidéo remplacé par [format]. »* Never pad with an off-wedge video.

**Source-type shortcuts** (use when wedge fits):

| Need | Where to search |
|------|-----------------|
| Seminal paper | `site:arxiv.org`, `site:doi.org`, author name + year from search snippets |
| Industrial system | Company docs, `site:youtube.com` demo, `site:github.com` |
| Textbook chapter | Google Books snippet + library link; cite chapter, not whole book |
| Standards / regs | Official body site (`.gouv.fr`, ISO, IEEE Xplore abstract) |

**Stop when:** you have exactly 3 candidates filling the format slots (article · video · joker) with one designated anchor. Do not add a 4th source.

## Step 4: Rank and package

Score each candidate (internal, not shown):

| Criterion | Weight |
|-----------|--------|
| Wedge alignment | 40% |
| Density (primary > secondary > demo > primer) | 25% |
| Answers an open question or tests a belief | 20% |
| Accessible (open PDF, working link) | 10% |
| Not redundant with another pick | 5% |

### Output structure (for brief.md)

Exactly **3 sources**, formats imposed:

| Slot | Format | Role |
|------|--------|------|
| 1 | `article` | Written piece — paper, reference doc, dense post (Tier 1–2 preferred) |
| 2 | `video` | YouTube — course, conference, demo on the wedge (not a teaser) |
| 3 | `joker` | Best wedge fit — `site`, second `video`, or second `article` |

One of the 3 is the **anchor** (start here) → listed under `### Read first (anchor)`. The other two → `### Core` (exactly 2 items). If the video slot was fallback-replaced, note it on that source's `Why:` line.

```markdown
## Source material

Scouted <YYYY-MM-DD> via `/source-scout` :

### Read first (anchor)
- [ ] **Author (year)** — *Title* — <URL>
  - Format: article | video | site
  - Tier: 1|2|3 · ~<15|45|90> min · <open access|paywall>
  - Why: <one line — what wedge unit this unlocks>
  - Targets: <open question or belief this source is likely useful for>

### Core
- [ ] **…** — *Title* — <URL>
  - Format: article | video | site
  - Tier: … · ~… min · …
  - Why: …
  - Targets: …
- [ ] **…** — *Title* — <URL>
  - Format: article | video | site
  - Tier: … · ~… min · …
  - Why: …
  - Targets: …

### Skipped (wedge boundary)
- *Title* — <why out of scope or redundant>
```

**Checkbox convention:** `[ ]` = not read · `[x]` = consumed (set by future read skills, not here).

**Anchor rule:** exactly one of the 3 sources is anchor. The user should start there without deciding.

**Count rule:** exactly 3 sources total (1 anchor + 2 core). No `### Optional` section.

**Honesty rule:** Do not claim a source *answers* a question during scouting. Say it **targets**, **tests**, or is **likely relevant to** the question. Resolution happens in `/dense-read`.

## Step 5: Confirm before write

**Default:** if the user invoked `/source-scout` and the brief has `TBD` or thin sources, **skip confirmation** and write directly (escape hatch default). Confirm only when replacing an existing curated list (≥3 `[ ]` items) or when the user did not explicitly invoke the skill.

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

1. Replace or merge `## Source material` in `brief.md`:
   - **Refresh** → replace section entirely
   - **Extend** → replace section with a new set of exactly 3 sources (gap-focused)
2. **Do not remove** items from `## Open questions`. Reference targeted questions under each source via `Targets:`. Only `/dense-read` may mark questions resolved after extraction.
3. Re-register study:

```bash
~/.claude/skills/ours-stack/bin/ours-stack-register-study studies/<slug>/brief.md
```

4. **Open sources in browser** (only if Step 5 was not cancelled):

```bash
# macOS (default)
open "<url1>"
open "<url2>"
open "<url3>"
# Linux fallback if open unavailable
xdg-open "<url1>"
```

One command per URL. Extract URLs from the 3 written sources (anchor + 2 core).

5. **Handoff — passation et enchaînement** (skip if Step 5 cancelled). Three beats — tone like `bear-hours` Step 4; personalized, direct, no ceremony.

**Anti-slop:** quote the `## Narrow wedge` unit; no « Félicitations ! », no filler. GOOD: « Sur [wedge], 3 sources sont dans le brief — commence par [anchor]. » BAD: template sentence alone. One line: scout found sources; it did not read them.

**Beat 1 — Ce qui vient d'être fait:** One short paragraph — 3 sources for **« <wedge unit> »** in `studies/<slug>/brief.md`; if browser opened → **les 3 sources sont ouvertes dans ton navigateur**; name the anchor (read first); video fallback line if slot 2 is not YouTube.

**Beat 2 — Carte du parcours:**

```
✅ /bear-hours — cadrage (fait)
✅ /source-scout — 3 sources trouvées (fait)
→ /dense-read — lecture guidée de l'anchor, tranche par tranche
  /study-status — à tout moment, pour voir où tu en es
```

**Beat 3 — Enchaînement:** `AskUserQuestion` — title `Source Scout — On enchaîne ?`, ask « On enchaîne sur /dense-read pour l'anchor de <slug> ? » Options: **Oui — lance /dense-read sur l'anchor maintenant** | **Plus tard — je m'arrête ici**. If Oui → **Read** and follow `dense-read/SKILL.md` for this `<slug>` and anchor in the **same session**; do not stop after handoff. If Plus tard → one line: `Quand tu veux : /dense-read <slug>`.

## Escape hatches

| User says | Action |
|-----------|--------|
| "just find something" / "vas-y" | Skip Step 5, write exactly 3 picks (article + video + joker) |
| "no video" / "skip youtube" | Replace video slot with article or site; say so explicitly |
| "French only" | Restrict to FR sources; note gap if wedge needs English primaries |
| "free only" | Drop paywalled; note what was skipped |

## Quality bar (self-check before write)

- [ ] Exactly 3 sources: article + video (or honest fallback) + joker
- [ ] Each source has `Format: article | video | site`
- [ ] Anchor is Tier 1 or 2 when possible and directly on the wedge unit
- [ ] YouTube pick verified via WebFetch (or fallback stated)
- [ ] Every source targets an open question or belief test (no false "answered" claims)
- [ ] ≥1 skipped source documented (proves wedge discipline)
- [ ] No source already `[x]` in this or related studies
- [ ] User knows which single source to open first
- [ ] Handoff delivered (3 beats + enchaînement) unless Step 5 cancelled