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

**Time budget for the agent:** ~3–5 minutes of search. **Output budget for the user:** exactly **3 sources** — one written article, one YouTube video, one joker (site, second video, or second article).

## Hard rules

- **Wedge lock** — every source must help explain the `## Narrow wedge` unit. Reject everything else, even if interesting.
- **No reading** — scout landing pages and abstracts only. Do not summarize content; do not write `notes.md`.
- **Density over breadth** — prefer one review paper over five blog posts. See `references/source-tiers.md`.
- **Candidate pools first** — screen ~10 on-wedge candidates per slot (article, YouTube, joker) before picking the final 3; never pad pools with off-wedge hits.
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
| **Video** *(try, timeboxed)* | `"<wedge concept>" lecture OR conference OR demo` (avoid `site:youtube.com` if flaky) | `GPU inference power consumption lecture` |
| **Storage** *(if autonomy/battery in wedge or success criteria)* | `"power capacity" kW "energy capacity" kWh storage electricity` | `EIA energy storage power capacity kWh` |
| **Measured** *(hardware/energy wedges)* | `"<device>" power consumption measured review watts` | `RTX 4090 power consumption measured review` |
| **AI workload** *(local GPU / inference wedges)* | `LLM inference energy footprint GPU measurement arXiv` | `From Prompts to Power GPU inference energy` |

Pick **3–6 queries** from the types above — use only types that fit the wedge. Do not force Maker or Belief test if the wedge is purely theoretical.

**Mandatory:** attempt **Video** pool (one query) — but **never block** on `site:youtube.com` or long YouTube pagination (see Pool V timebox).

**Language:** search in English for STEM; add French queries only for réglementation, marché local, or francophone-only corpora.

**Anti-queries** — do NOT search: the broad field name alone, "introduction to X", "top 10", "best resources", the study title verbatim.

Load `references/source-tiers.md` for tier definitions and rejection patterns.

### Scout live capture + transcript (mandatory audit trail)

**After every `WebSearch` / `WebFetch`** during Steps 2–4, log the live tool output **before** ranking picks:

```bash
_REPO="$(git rev-parse --show-toplevel)"
# WebSearch (repeat per query; --urls = comma-separated hits from provider)
"$_REPO/bin/ours-stack-source-scout-log-tool" \
  --raw "$_REPO/studies/<slug>/scout-raw.jsonl" --run 1 \
  --tool WebSearch --query "<exact query string>" \
  --urls "https://example.com/a,https://example.com/b"

# WebFetch (repeat per screened URL; --snippet-chars = len of fetched body)
# Tier 3 / Pool V: capture channel or speaker via page or YouTube oembed → --author
"$_REPO/bin/ours-stack-source-scout-log-tool" \
  --raw "$_REPO/studies/<slug>/scout-raw.jsonl" --run 1 \
  --tool WebFetch --url "https://www.youtube.com/watch?v=EXAMPLE" --status ok \
  --snippet-chars 12000 --author "Prof. Alex Rivera — MIT Energy Initiative"
```

At end of pool screening (before Step 4b scoring), **derive** transcript tool lines from raw capture only:

```bash
"$_REPO/bin/ours-stack-source-scout-sync-transcript-from-raw" \
  "$_REPO/studies/<slug>/scout-raw.jsonl" \
  "$_REPO/studies/<slug>/scout-transcript.jsonl"
```

Then append gate lines via Step 4b `finalize-transcript` (preflight + validate). **Never** hand-write transcript URLs without a matching `scout-raw.jsonl` line.

| File | Role |
|------|------|
| `scout-raw.jsonl` | Immutable live tool log (`seq`, `ts`, `query`, `hits[]`, `snippet_chars`) |
| `scout-transcript.jsonl` | Derived + gates (`raw_seq` links back to `scout-raw.jsonl`) |

| `tool` (transcript) | Required fields |
|--------|-----------------|
| `WebSearch` | `ts`, `raw_seq`, `query`, `results` (URLs from raw `hits`) |
| `WebFetch` | `ts`, `raw_seq`, `url`, `status` |
| `preflight` | `status` (`ok` \| `error`) |
| `validate` | `status` (`ok` \| `error`), `message` (validator stdout) |

**Minimum before write:** ≥3 `WebSearch` · ≥1 `WebFetch` in raw · `evidence-check` OK · every brief URL in transcript.

### Provider log recovery (batch ingest — fallback only)

**Preferred:** `log-tool` immediately after each tool call (above). **Do not** defer all logging to the end of the scout.

If provider output was captured during the session but not logged inline, batch-ingest **before** `sync-from-raw`:

```bash
_REPO="$(git rev-parse --show-toplevel)"
# provider.log — one JSON object per line from live WebSearch/WebFetch:
# WebSearch: {"tool":"WebSearch","query":"...","provider_status":"ok|error","results":["url",...]}
# WebFetch:  {"tool":"WebFetch","url":"...","status":"ok","snippet_chars":12000}

"$_REPO/bin/ours-stack-source-scout-ingest-provider-log" \
  provider.log "$_REPO/studies/<slug>/scout-raw.jsonl" <run_id>

"$_REPO/bin/ours-stack-source-scout-sync-transcript-from-raw" \
  "$_REPO/studies/<slug>/scout-raw.jsonl" \
  "$_REPO/studies/<slug>/scout-transcript.jsonl"

# Or one shot (ingest → sync → evidence → transcript-check → validate):
"$_REPO/bin/ours-stack-source-scout-complete-run" \
  provider.log \
  "$_REPO/studies/<slug>/scout-raw.jsonl" \
  "$_REPO/studies/<slug>/scout-transcript.jsonl" \
  "$_REPO/studies/<slug>/brief.md" \
  <run_id>
```

**Live refresh (production):**

```bash
_REPO="$(git rev-parse --show-toplevel)"
# Agent: WebSearch/WebFetch live → append JSON lines to provider.log
"$_REPO/bin/ours-stack-source-scout-live-harness" \
  "$_REPO/studies/<slug>/brief.md" \
  "$_REPO/studies/<slug>/provider.log"
```

**Audit:** save `provider.log` + `provider.manifest.json` (engine roles/coverage). CI uses **noisy synthetic cassettes** to exercise dynamic pool/score/pick; live proof = agent WebSearch session + `live-harness`.

## Step 3: Search (agent) — pools built by engine

Run **3–5 `WebSearch` calls in parallel** (one per query, including the mandatory **Video** query). **Log each** to `scout-raw.jsonl` via `log-tool` immediately after the provider returns. Collect hits for the engine — do not hand-pick finalists in prose.

**Pool building, /10 scoring, swap heuristics, and final 3-source pick are NOT manual** — they run in:

```bash
_REPO="$(git rev-parse --show-toplevel)"
# provider.log = one JSON line per WebSearch/WebFetch (see Provider log recovery)
"$_REPO/bin/ours-stack-source-scout-run" \
  --brief "$_REPO/studies/<slug>/brief.md" \
  --cassette "$_REPO/studies/<slug>/provider.log" \
  --run-id 1
# Writes ## Source material, scout-raw.jsonl, scout-transcript.jsonl; runs gates; exits non-zero if set <9/10
```

Save live captures to `studies/<slug>/provider.log` before calling `source-scout-run`. The agent's job in Step 3 is **search + log**; the engine's job is **pool → score → pick → write**.

### Three pools (internal — not written to brief)

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

**Timebox:** max **2 minutes** on Pool V total · max **3** `WebFetch` on YouTube URLs · if zero strong survivors → **immediate fallback** (do not retry `site:youtube.com`). Prefer broad queries (`homelab GPU power kWh`) over operator lock.

`WebFetch` every YouTube survivor — snippet alone is not enough (title, channel, duration, description).

**Verify WHO speaks:** before keeping a Pool V candidate, identify the **channel or speaker**. If unknown after `WebFetch`, run **one timeboxed `WebSearch`** on the channel name (≤30 s) — log the identity with `--author` on the `WebFetch` line in `scout-raw.jsonl`. Anonymous or unverifiable channels fail the authority bar (engine cap ≤6/10 → article fallback).

| Accept | Reject |
|--------|--------|
| Course lecture, conference talk (ICRA, etc.), expert talk, technical demo, full recording with real wedge content | Teaser, trailer, hype clip, generalist « introduction to », SEO tutorial, superficial recap, news without mechanism, off-wedge tangent |
| Named speaker or institution-backed channel; corpus specialized in the wedge domain | Anonymous channel, marketing-only channel, corpus mainly off-wedge |

**Minimum to stay in Pool V:** **strong** wedge alignment (core topic, not a passing mention) **and** density (mechanism, argument, or demo — not vocabulary-only) **and** identifiable authority. Weak videos stay out of the pool; log rejection reason for `### Skipped`.

**Video fallback:** if **no** Pool V candidate passes the bar, replace slot 2 with the best **article or site Tier 1–3** from Pool A or J (not a bad video). Tell the user: *« Aucune vidéo YouTube assez forte sur le wedge — slot vidéo remplacé par [format]. »* Joker may beat a marginal second video if an article/site is objectively stronger.

**Stop when:** all three pools are built (up to target size or honestly exhausted) — **not** when 3 finalists are found. Final pick happens in Step 4.

## Step 4: Rank and package (engine — `source-scout-run`)

**Do not rank or write sources by hand.** `source-scout/scripts/scout-engine.py` (invoked by `ours-stack-source-scout-run`) scores pool survivors, applies swap heuristics, and picks exactly 3 sources. Reference logic for humans:

| Criterion | Weight |
|-----------|--------|
| Wedge alignment | 35% |
| Density (primary > secondary > demo > primer) | 25% |
| Authority / traceability | 15% |
| Answers an open question or tests a belief | 15% |
| Accessible (open PDF, working link) | 5% |
| Not redundant with another pick | 5% |

**Final pick:** exactly **1 article** (Pool A) + **1 video or fallback** (Pool V winner, else best article/site) + **1 joker** (Pool J) → designate **anchor** (best wedge unlock). Do not add a 4th source.

### Swap heuristics (apply before final pick)

| If pool has… | Prefer instead… |
|--------------|-----------------|
| Vendor GPU spec sheet only | Third-party **measured** power review (Tom's Hardware, AnandTech, etc.) |
| Homelab blog / listicle for cost | Tier 1–2 **measurement paper** or official doc when wedge is AI/GPU energy |
| Wedge mentions autonomie / batteries / stockage | Add **Storage** query → official source on **power capacity (kW)** vs **energy capacity (kWh)** |
| Cloud/API-only energy paper | Local GPU + vLLM measurement paper when wedge is *home lab* |

*(Domain examples — the engine is domain-agnostic: it derives wedge alignment from brief-token overlap, so these preferences emerge from generic scoring — fetched > unfetched, measured/dense > vendor/listicle — not from per-topic rules.)*

### Quality gate — score /10 before write (Step 4b)

Score **each finalist** on a **0–10** scale (same weights as ranking). Record internally:

| Criterion | Weight | 9/10 requires… |
|-----------|--------|----------------|
| Wedge alignment | 35% | Core mechanism of `WEDGE_UNIT`, not adjacent topic |
| Density | 25% | Mechanism, data, or measurement — not vocabulary-only |
| Authority / traceability | 15% | Named verifiable author, institution, established technical media, or on-wedge specialized corpus |
| Open question / belief | 15% | Maps to ≥1 `## Open questions` or `## Success criteria` |
| Accessible | 5% | Working link, open or honest paywall note |
| Non-redundant | 5% | No overlap with other 2 picks |

**Authority hard cap:** source without identifiable author/channel **≤6/10** — slot 2 falls back to best article/site (never a weak anonymous video).

**Write rule:** `source-scout-run` exits non-zero if **any source <9/10** or **set global <9/10**. If pools honestly exhausted and best set <9 → document in `.context/` (goal loop); do not bypass the engine.

**Enforcement (mandatory):** `source-scout-run` already runs `ours-stack-source-scout-preflight` → `ingest` → `sync` → `ours-stack-source-scout-evidence-check` → `ours-stack-source-scout-transcript-check` → `ours-stack-source-scout-finalize-transcript` → `ours-stack-source-scout-validate`. Any **non-zero** exit blocks handoff. **Always** use `git rev-parse --show-toplevel` paths.

**Journal:** on improvement-loop runs, append scores + 1-line justification per source to `.context/source-scout-loop.md`.

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

1. **Write via engine:** `source-scout-run` replaces `## Source material` in `brief.md` (refresh or extend — same command, new `provider.log`).
2. **Quality gate (blocks on failure):** already inside `source-scout-run` — if non-zero, add queries to `provider.log` and re-run; **do not** open browser or hand off until exit 0.
3. **Do not remove** items from `## Open questions`. Reference targeted questions under each source via `Targets:`. Do not mark questions resolved here — that happens after reading the anchor.
4. Re-register study:

```bash
bin/ours-stack-register-study studies/<slug>/brief.md
```

5. **Open sources in browser** (only if Step 5 was not cancelled and validate passed):

```bash
# macOS (default)
open "<url1>"
open "<url2>"
open "<url3>"
# Linux fallback if open unavailable
xdg-open "<url1>"
```

One command per URL. Extract URLs from the 3 written sources (anchor + 2 core).

6. **Handoff — passation** (skip if Step 5 cancelled or validate failed). Two beats — tone like `bear-hours` Step 4; personalized, direct, no ceremony.

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
- [ ] **Each source ≥9/10** and **set global ≥9/10** (Step 4b) — or exhaustion documented
- [ ] Swap heuristics applied (measured GPU > vendor spec; storage source if autonomie in criteria)
- [ ] YouTube timebox respected (≤2 min, ≤3 WebFetch) — fallback stated on `Why:` if used
- [ ] Each source has `Format: article | video | site`
- [ ] Anchor is Tier 1 or 2 when possible and directly on the wedge unit
- [ ] Every source targets an open question or success criterion (no false "answered" claims)
- [ ] ≥1 skipped documented; rejected YouTube noted when video slot weak or replaced
- [ ] No source already `[x]` in this or related studies
- [ ] User knows which single source to open first
- [ ] Handoff delivered (2 beats) unless Step 5 cancelled
