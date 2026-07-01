---
name: bear-hours
description: |
  School of the Bear topic framing — seven forcing questions before deep learning.
  Defines scope, wedge, success criteria, source material, and public proof commitment.
  Asks consent before optional local scan; never reads source material during framing.
  Use when the user starts a new study, asks what to learn, wants to frame a topic,
  or says "bear hours", "cadrer mon apprentissage", "what should I study".
  Outputs studies/<slug>/brief.md.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
---

# Bear Hours

Frame *what* to learn and *why* before reading anything. Like YC office hours, but for autodidacts.

## Interactive questions

Use the **`AskUserQuestion`** tool for every framing question (Claude Code native; Grok Build maps it to the same CLI widget as plan mode).

**Hard rules:**
- **Never** list numbered questions in chat — always call `AskUserQuestion`
- **One question per call** — a single entry in `questions[]`, never batch Q1+Q2
- **STOP** after each call; wait for the answer before the next question
- **Smart-skip** — if the user's initial message already answers a question, skip it
- **Title format:** `Bear Hours — Q{n}/7 : {label}`

**Open vs fixed questions:**
- **Open** (Q1–Q4): infer 2–3 contextual options from what the user said, plus a final option `other` — "Other — I'll clarify in my next message". If they pick `other`, accept a short free-text reply in chat, then continue with the next `AskUserQuestion`.
- **Fixed** (Q5–Q6): use the explicit options listed below.

**Escape hatch:** If the user says "skip", "just do it", or "vas-y" — ask at most 2 remaining questions via `AskUserQuestion`, then write the brief and list gaps under `Open questions`.

## Step 0: Local context scan

Before Q1, ask permission to search the user's machine for prior learning context (inspired by gstack `/office-hours`). Keep the ask simple — no mention of data, APIs, or providers.

**Title:** `Bear Hours — Local scan`

**Ask:** "Je peux chercher dans tes anciennes études enregistrées liées à ce sujet. OK ?"

**Options:**
- Yes — search registered studies
- No — start fresh

If **No** → skip to Step 1.

If **Yes** → one more `AskUserQuestion`:

**Title:** `Bear Hours — Scan scope`

**Ask:** "How wide should I search?"

**Options:**
- **A)** This repo only — `studies/` in the current project
- **B)** Repo + global index — `studies/` + `~/.ours-stack/studies-index.jsonl` + `~/.ours-stack/learnings.jsonl` *(recommended)*

### Run the scan

Extract 2–4 keywords from the user's topic. Then:

| Scope | Actions |
|-------|---------|
| **A** | `Glob` `studies/*/brief.md` · `Grep` keywords in `studies/` · read matching `brief.md` / `notes.md` if relevant |
| **B** | Everything in **A** · `Read` `~/.ours-stack/studies-index.jsonl` · keep entries matching slug or keywords (title, wedge, repo_name) · skip entries whose `study_path` is already covered by scope A · read top 2–3 external `brief_path` matches only · `Read` or `tail` `~/.ours-stack/learnings.jsonl` (last 30 lines) · keep entries matching keywords |

**Index-only rule:** cross-project discovery reads **only** `~/.ours-stack/` — never run `find` on `$HOME` at runtime. Studies from other repos appear only if registered in the index (via `./setup` backfill or `bin/ours-stack-register-study` after each brief).

**Limits:** max 3 study folders opened · max 5 index/learnings entries surfaced · framing scan only — do not summarize source material.

### Report findings

If anything relevant, show 2–4 bullets in chat. When a past learning applies:

> **Prior learning applied:** [insight] (confidence: high|medium|low, [date])

**Use findings to:**
- **Suggest** resuming an existing slug in Step 2 — never auto-resume without user confirmation
- Pre-fill or smart-skip **Q3** (current beliefs) when prior briefs already state them
- Smart-skip **Q7** (source material) when the user already shared a URL, paper, chapter, or file path
- Add `## Prior progress` in the brief (Step 3) when scan found context

If nothing found: one line — "No prior local context — starting fresh."

## Step 1: Gather context

Ask via `AskUserQuestion` until all seven are answered (or smart-skipped).

### Q1 — Topic

**Ask:** "What exactly do you want to learn? One paper, one chapter, one system, or one concept — not a whole field."

**Options:** Infer 2–3 concrete topics from the user's message + `other`.

### Q2 — Why now

**Ask:** "Why now? What decision, project, or deadline depends on understanding this?"

**Options:** Infer plausible motivations from context + `other`.

### Q3 — Current beliefs

**Ask:** "What do you already believe about this? What would genuinely surprise you?"

**Options:** Infer 2–3 beliefs they might hold + `other`.

### Q4 — Narrow wedge

**Ask:** "What's the smallest slice that counts as 'learned'? Not the whole topic — one explainable unit."

**Options:** Propose 2–3 plausible wedges derived from Q1 + `other`. Push back if the wedge is too wide.

### Q5 — Proof commitment

**Ask:** "What public artifact will prove you understood? Even small counts."

**Options:**
- Thread X (3–5 posts)
- GitHub gist or short write-up
- LinkedIn / blog post
- Small demo or screen recording
- `other`

### Q6 — Time box

**Ask:** "How long are you giving yourself?"

**Options:**
- One session (today)
- One week
- Ongoing (no hard deadline)
- `other`

### Q7 — Source material

**Ask:** "Do you already have source material? A URL, paper, chapter, repo, or file path."

**Options:**
- Yes — I have a specific source
- Not yet — I'll find it later
- `other`

If **Yes** or `other` with a source → accept URL/title/path in chat (one short reply), record verbatim in `## Source material`. If **Not yet** → write `TBD` in the brief and add a line under `## Open questions`.

**Smart-skip:** if the user's opening message already includes a URL, arXiv link, paper title, chapter, repo, or file path, skip Q7 and use that source directly.

### Confirm before writing

After Q7 (or Q6 if Q7 smart-skipped), call `AskUserQuestion` once more:

**Title:** `Bear Hours — Confirm brief`

**Ask:** Summarize topic, wedge, proof plan, time box, and source material (or "TBD") in 3–5 bullets. "Ready to write `studies/<slug>/brief.md`?"

**Options:**
- Yes — write the brief
- Adjust the wedge
- Adjust the public proof plan
- Adjust source material

If they pick an adjustment option, ask one targeted `AskUserQuestion`, then confirm again.

## Step 2: Choose slug

Derive `slug` from the topic: lowercase, hyphens, no spaces (per AGENTS.md).

1. `Glob` `studies/<slug>/brief.md` (or list `studies/` and match).
2. **If slug does not exist** → use it.
3. **If slug exists** → read existing `brief.md` (`#` title, `## Narrow wedge`, `Created`). Call `AskUserQuestion`:

**Title:** `Bear Hours — Existing study`

**Ask:** "A study `studies/<slug>/` already exists: **[title]** — wedge: *[one-liner]*. What do you want to do?"

**Options:**
- Resume this study — update brief in place
- Same topic, new scope — fork as `<slug>-v2`
- Different topic — use a new slug (agent proposes 2 alternatives in chat)

4. **Never** overwrite or resume without explicit user choice (AGENTS.md: ask before reusing an existing slug).
5. **Suffix chain:** if `<slug>-v2` exists, try `-v3`, then `-v4`, until a free slug is found.

## Step 3: Write brief.md

Create `studies/<slug>/brief.md` with this structure:

```markdown
# <Title>

**Slug:** <slug>
**Created:** <YYYY-MM-DD>
**Time box:** <duration>

## Why now
<desperate specificity>

## Current beliefs
<status quo>

## Prior progress
<only if Step 0 found context — related slug, brief one-liner, open questions from notes; omit section if none>

## Narrow wedge
<smallest learnable unit — be concrete>

## Success criteria
- [ ] I can explain <X> without jargon
- [ ] I can answer <Y> from memory
- [ ] I produced <proof artifact>

## Public proof plan
<format + audience + draft hook>

## Source material
<URLs, papers, chapters, repos — to read against the wedge>

## Open questions
- ...
```

After writing `brief.md`, register the study in the global index:

```bash
~/.claude/skills/ours-stack/bin/ours-stack-register-study studies/<slug>/brief.md
```

(Use the repo-local path if developing outside the symlink.)

## Step 4: Confirm and route

Tell the user:
- Slug and path to `brief.md`
- Next step: read a source from `## Source material` in chat (paste URL + wedge), or draft public proof (future `/proof-draft`)
- Remind: deep over wide — resist scope creep beyond the wedge

## Rules

- Do not start reading or summarizing source material here — framing only
- Do not open or inspect source documents even if the user supplies URLs or file paths — record them in the brief only
- Push back on "learn everything about X" — force a wedge
- Every study must have a public proof plan, even if small (one tweet thread counts)
- Cross-project scan: `~/.ours-stack/studies-index.jsonl` only — never `find $HOME` at runtime