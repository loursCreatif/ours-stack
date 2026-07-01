---
name: bear-hours
description: |
  School of the Bear topic framing — six forcing questions before deep learning.
  Defines scope, wedge, success criteria, and public proof commitment.
  Use when the user starts a new study, asks what to learn, wants to frame a topic,
  or says "bear hours", "cadrer mon apprentissage", "what should I study".
  Outputs studies/<slug>/brief.md. Run before /dense-read on new topics.
---

# Bear Hours

Frame *what* to learn and *why* before reading anything. Like YC office hours, but for autodidacts.

## Step 1: Gather context

Ask **one question at a time** until you have answers for all six:

1. **Topic** — What exactly? (one paper, one chapter, one system, one concept)
2. **Desperate specificity** — Why now? What decision or project depends on this?
3. **Status quo** — What do you already believe? What would surprise you?
4. **Narrow wedge** — Smallest slice that counts as "learned" (not the whole field)
5. **Proof commitment** — What public artifact will show you understood? (thread, gist, post, demo)
6. **Time box** — One session, one week, or ongoing?

If the user already answered some, skip those questions.

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