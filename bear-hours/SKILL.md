---
name: bear-hours
description: |
  School of the Bear topic framing — six forcing questions before deep learning.
  Defines scope, wedge, success criteria, and public proof commitment.
  Use when the user starts a new study, asks what to learn, wants to frame a topic,
  or says "bear hours", "cadrer mon apprentissage", "what should I study".
  Outputs studies/<slug>/brief.md. Run before /dense-read on new topics.
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
- **Title format:** `Bear Hours — Q{n}/6 : {label}`

**Open vs fixed questions:**
- **Open** (Q1–Q4): infer 2–3 contextual options from what the user said, plus a final option `other` — "Other — I'll clarify in my next message". If they pick `other`, accept a short free-text reply in chat, then continue with the next `AskUserQuestion`.
- **Fixed** (Q5–Q6): use the explicit options listed below.

**Escape hatch:** If the user says "skip", "just do it", or "vas-y" — ask at most 2 remaining questions via `AskUserQuestion`, then write the brief and list gaps under `Open questions`.

## Step 0: Local context scan

Before Q1, ask permission to search the user's machine for prior learning context (inspired by gstack `/office-hours`). Keep the ask simple — no mention of data, APIs, or providers.

**Title:** `Bear Hours — Local scan`

**Ask:** "Je peux fouiller sur ta machine pour voir où tu en es sur ce sujet (études passées, checkpoints, learnings). OK ?"

**Options:**
- Yes — search locally
- No — start fresh

If **No** → skip to Step 1.

If **Yes** → one more `AskUserQuestion`:

**Title:** `Bear Hours — Scan scope`

**Ask:** "How wide should I search?"

**Options:**
- **A)** This repo only — `studies/` in the current project
- **B)** Repo + global learnings — `studies/` + `~/.ours-stack/learnings.jsonl` *(recommended)*
- **C)** Everywhere on this machine — other `studies/` folders too (slower, cross-project)

### Run the scan

Extract 2–4 keywords from the user's topic. Then:

| Scope | Actions |
|-------|---------|
| **A** | `Glob` `studies/*/brief.md` · `Grep` keywords in `studies/` · read matching `checkpoint.md` if any |
| **B** | Everything in **A** · `Read` `~/.ours-stack/learnings.jsonl` (or `tail` last 30 lines) · keep entries matching slug or keywords |
| **C** | Everything in **B** · bounded find for other study trees: `find "$HOME" -maxdepth 8 -path "*/studies/*/brief.md" ! -path "*/node_modules/*" ! -path "*/.git/*" 2>/dev/null \| head -25` · `Grep` keywords in hits · read top 2–3 matches only |

**Limits:** max 3 study folders opened · max 5 learnings surfaced · framing scan only — do not summarize source material.

### Report findings

If anything relevant, show 2–4 bullets in chat. When a past learning applies:

> **Prior learning applied:** [insight] (confidence: high|medium|low, [date])

**Use findings to:**
- Propose **resuming** an existing slug (same scope) instead of creating a duplicate
- Pre-fill or smart-skip **Q3** (current beliefs) when checkpoints already state them
- Add `## Prior progress` in the brief (Step 3) when scan found context

If nothing found: one line — "No prior local context — starting fresh."

## Step 1: Gather context

Ask via `AskUserQuestion` until all six are answered (or smart-skipped).

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

### Confirm before writing

After Q6, call `AskUserQuestion` once more:

**Title:** `Bear Hours — Confirm brief`

**Ask:** Summarize topic, wedge, proof plan, and time box in 3–4 bullets. "Ready to write `studies/<slug>/brief.md`?"

**Options:**
- Yes — write the brief
- Adjust the wedge
- Adjust the public proof plan

If they pick an adjustment option, ask one targeted `AskUserQuestion`, then confirm again.

## Step 2: Choose slug

Derive `slug` from the topic: lowercase, hyphens, no spaces.

- Check `studies/` for collisions
- If slug exists with same scope → resume that study
- If scope diverged → new slug with suffix (`topic-v2`)

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
<only if Step 0 found context — related slug, checkpoint one-liner, 1–3 learnings; omit section if none>

## Narrow wedge
<smallest learnable unit — be concrete>

## Success criteria
- [ ] I can explain <X> without jargon
- [ ] I can answer <Y> from memory
- [ ] I produced <proof artifact>

## Public proof plan
<format + audience + draft hook>

## Source material
<URLs, papers, chapters, repos — to be consumed in /dense-read>

## Open questions
- ...
```

## Step 4: Confirm and route

Tell the user:
- Slug and path to `brief.md`
- Recommended next step: `/dense-read` with the source material
- Remind: deep over wide — resist scope creep beyond the wedge

## Rules

- Do not start reading or summarizing source material here — framing only
- Push back on "learn everything about X" — force a wedge
- Every study must have a public proof plan, even if small (one tweet thread counts)