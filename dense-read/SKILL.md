---
name: dense-read
description: |
  Deep structured reading of dense material — papers, chapters, docs, repos.
  Accepts URL, PDF path, local file, or pasted text. Produces notes.md and proof.md.
  Use when the user shares a paper, article, chapter, arXiv link, dense doc,
  or says "dense read", "read this deeply", "study this paper", "lecture dense".
  Requires studies/<slug>/brief.md or creates a minimal brief first.
---

# Dense Read

Read one dense source deeply. No shallow summary. Extract, question, prove.

## Step 1: Resolve study context

1. Find or confirm `studies/<slug>/`
2. If no `brief.md` exists, ask the user for topic + wedge OR run a 2-minute mini-brief inline, then write `brief.md`
3. Read `brief.md` — stay inside the declared wedge

## Step 2: Ingest source material

Accept any of:

| Input | Action |
|-------|--------|
| URL | Fetch and read (web fetch or browser) |
| Local PDF/file path | Read file |
| Pasted text | Use directly |
| GitHub repo | Read README, AGENTS.md, key dirs named in brief |

If source is inaccessible, tell the user what's missing and ask for paste or file.

Record the source in `brief.md` under **Source material** if not already there.

## Step 3: Write notes.md

Create or update `studies/<slug>/notes.md`:

```markdown
# Notes: <title>

**Source:** <citation or link>
**Read date:** <YYYY-MM-DD>

## One-sentence thesis
<what the source claims, in plain language>

## Problem & context
<why this exists>

## Core mechanisms
<numbered list — how it works, not buzzwords>

## Key insights
1. ...
2. ...

## Feynman check
<explain the wedge topic as if to a smart friend — no jargon allowed>

## Connections
<links to prior studies, other papers, your projects>

## Open questions
- things you still don't understand
- claims you can't verify yet

## Quotable (paraphrase only)
<short paraphrased lines worth remembering — no long copyright quotes>
```

### Reading rules

- **Dense over shallow** — if a paragraph is unclear, say what's unclear
- **No fake mastery** — mark `[?]` next to anything you're uncertain about
- Stop at wedge boundary — don't expand scope without user approval

## Step 4: Write proof.md

Create or update `studies/<slug>/proof.md`:

```markdown
# Public proof draft: <title>

**Format:** <thread | gist | blog | video script | repo note>
**Audience:** <who benefits>
**Status:** draft

## Hook
<one line that makes someone care>

## Core claim
<what you now believe that you didn't before>

## Evidence
<3 bullets — mechanisms, examples, or results from notes>

## Takeaway
<what the reader should do or think differently>

## Redaction check
- [ ] No long copyrighted quotes
- [ ] No personal or unreleased data
- [ ] Written in my own words
```

Proof is a **draft**. User publishes manually.

## Step 5: Handoff

Tell the user:
- Paths to `notes.md` and `proof.md`
- One honest gap from **Open questions**
- Suggest `/checkpoint-learnings` when done for this session