---
name: checkpoint-learnings
description: |
  Save learning session state and append durable insights to cross-session memory.
  Writes studies/<slug>/checkpoint.md and appends to ~/.ours-stack/learnings.jsonl.
  Use when the user pauses, resumes, says checkpoint, "where was I", "what did I retain",
  "save progress", or ends a study session.
---

# Checkpoint + Learnings

Persist where you are. Capture what stuck.

## Step 1: Resolve study

1. List `studies/` if slug unknown
2. Use latest modified study or ask user to pick
3. Read `brief.md`, `notes.md`, `proof.md` if they exist

## Step 2: Write checkpoint.md

Create or update `studies/<slug>/checkpoint.md`:

```markdown
# Checkpoint: <title>

**Updated:** <YYYY-MM-DD HH:MM>
**Slug:** <slug>

## Progress
- Brief: done | partial | missing
- Notes: done | partial | missing
- Proof: draft | ready | missing

## Where I stopped
<last section or concept being worked on>

## Decisions made
- ...

## Next session (first 15 minutes)
1. ...
2. ...

## Blockers
- ...
```

## Step 3: Append learnings

Append one JSON line per **durable insight** to `~/.ours-stack/learnings.jsonl`:

```json
{"ts":"<ISO8601>","slug":"<slug>","insight":"<one sentence>","source":"<paper|repo|chapter>","confidence":"high|medium|low"}
```

Rules:
- Max 5 lines per session — quality over quantity
- Only insights you'd want in 30 days, not session noise
- `confidence: low` if shaky — honest calibration

Create `~/.ours-stack/` and empty `learnings.jsonl` if missing.

## Step 4: Resume mode

If user says **resume** / **where was I**:

1. Read latest `checkpoint.md`
2. Summarize: wedge, progress, next 15 minutes
3. Suggest `/dense-read` or `/bear-hours` based on what's missing

## Step 5: Search learnings (optional)

If user asks what they retained across topics:

```bash
cat ~/.ours-stack/learnings.jsonl | tail -20
```

Or grep by slug keyword. Surface the 3 most relevant entries.

## Rules

- Checkpoint is **project-local** (`studies/<slug>/`) — travels with the repo
- Learnings are **global** (`~/.ours-stack/`) — cross-study memory
- Never delete learnings without explicit user request