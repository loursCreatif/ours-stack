---
name: study-session
description: |
  School of the Bear deep reading — turn one source into dense notes against an existing brief wedge.
  Requires studies/<slug>/brief.md from /bear-hours. Reads URL, paper, chapter, or file;
  extracts mechanisms, insights, Feynman check, and open questions; writes studies/<slug>/notes.md.
  Use when the user wants to read a source, take study notes, dense-read a paper,
  or says "study session", "lis cette source", "notes sur ce paper".
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
  - WebFetch
---

# Study Session

Turn **one source** into **dense notes** locked to the wedge in `brief.md`. Framing happened in `/bear-hours` — this skill only reads and extracts.

## Hard rules

- **Wedge is law** — read `## Narrow wedge` in `brief.md` before every extraction. Drop anything out of scope; note dropped topics under `## Connections` as "hors wedge".
- **No summary theater** — mechanisms and insights, not a generic recap. If you cannot explain a mechanism, mark `[?]`.
- **Paraphrase only** — no long quotes. `## Quotable` = short paraphrases in your own words (see Privacy in AGENTS.md).
- **Feynman check required** — plain-language explanation as if teaching a smart non-expert.
- **One session = one primary source** — additional sources get their own `/study-session` run (append mode).
- **Never** start without a `brief.md`. Route to `/bear-hours` first.

## Step 0: Resolve study

Find the active study slug.

**Hard rule — never hang on Glob:** Do **not** `Glob` from workspace root `/` or `$HOME`. That scans the whole disk and can run for minutes. Repo-local `Glob` is allowed only when cwd is a real project directory (not `/`).

Resolution order:

1. **User names a slug or path** → use it (`studies/<slug>/brief.md` or absolute `brief_path`).
2. **Repo-local** (only if cwd ≠ `/` and `studies/` exists or is plausible):
   - `Glob` `studies/*/brief.md` relative to cwd
   - Exactly one match → use it
   - Multiple matches → `AskUserQuestion` (slug + `#` title from each `brief.md`, max 4 + `other`)
3. **Global index** (always safe; preferred when cwd is `/` or no local `studies/`):
   - `Read` `~/.ours-stack/studies-index.jsonl`
   - Parse JSONL; use `brief_path` / `study_path` / `slug` / `title`
   - Exactly one entry → use it
   - Multiple entries → `AskUserQuestion`:

**Title:** `Study Session — Which study?`

**Ask:** "Which study should I read against?"

**Options:** List each slug + `title` from the index (max 4) + `other`.

4. **If none** → stop. Tell the user: run `/bear-hours` first, or open the repo that owns the study (e.g. `ours-stack`) and retry.

**Index-only rule:** cross-project discovery uses **only** `~/.ours-stack/studies-index.jsonl` — never `find $HOME` at runtime (same as `/bear-hours`).

Read `studies/<slug>/brief.md`. Extract and keep in mind:
- `## Narrow wedge` (filter)
- `## Current beliefs` (test against source)
- `## Success criteria` (inform Feynman check)
- `## Source material` (candidate sources)
- `## Open questions` (update at end)

## Step 1: Pick source

**Smart-skip:** if the user's message includes a URL, arXiv link, file path, or paper title → use it directly.

Else if `brief.md` lists exactly one unread source → use it.

Else `AskUserQuestion`:

**Title:** `Study Session — Source`

**Ask:** "Which source for this session? (one primary source)"

**Options:**
- Infer 2–3 from `## Source material` (mark unread `- [ ]` first) + paste URL in chat (`other`)
- If all sources are `TBD` → options: "Paste a URL now" (`other`) · "Stop — find sources first"

If source is `TBD` and user has nothing → stop. Suggest finding sources (future `/source-hunt` or manual) before reading.

## Step 2: Existing notes?

If `studies/<slug>/notes.md` exists → `AskUserQuestion`:

**Title:** `Study Session — Notes mode`

**Ask:** "`notes.md` already exists for this study. What do you want?"

**Options:**
- Append — add this source's extraction to existing notes
- Replace — rewrite notes from scratch (this source + prior context)
- Cancel

**Append behavior:** add source to `**Source :**` list · add dated `### Session <YYYY-MM-DD>` under relevant sections or new bullets · do not duplicate identical insights.

## Step 3: Read the source

Read the primary source fully (or the relevant section if the user scoped a chapter):

| Type | How |
|------|-----|
| URL / arXiv | `WebFetch` or `curl -sL` via `Bash` |
| Local file | `Read` |
| Repo | `Read` key files only — stay inside wedge |

**Limits:** one primary source per session. If the source is huge (book), ask via `AskUserQuestion` which chapter/section — default to the smallest slice that serves the wedge.

While reading, actively test `## Current beliefs` from the brief — confirm, nuance, or refute in `## Key insights`.

## Step 4: Write notes.md

Create or update `studies/<slug>/notes.md` with this structure:

```markdown
# Notes : <short title aligned with wedge>

**Source :**
- <label> — <URL or path>

**Read date :** <YYYY-MM-DD>

## One-sentence thesis

<One line — the main claim relative to the wedge>

## Problem & context

<Why this matters for the wedge — not the whole field>

## Core mechanisms

1. **<Name>** — <how it works, plain language>
2. ...

## Key insights

1. **<Insight>** — <so what for the wedge / user's project>
2. ...

## Feynman check

<Explain the core idea in simple language, no jargon — 1 short paragraph or analogy>

## Connections

- **<Link to user project / prior studies / alternatives>**
- **Hors wedge :** <topics deliberately skipped>

## Open questions

- [?] <genuine confusion or untested claim>
- ...

## Quotable (paraphrase only)

- « <short paraphrase in your own words> »
```

**Quality bar:**
- Every `## Core mechanisms` item must be a *how*, not a label
- At least 3 `## Key insights`, at least 1 must address a `## Current beliefs` item from the brief
- At least 2 `[?]` or concrete open questions — if none, you read too shallow
- `## Feynman check` must pass the "no jargon" test from `## Success criteria` in the brief

## Step 5: Update brief (light touch)

In `studies/<slug>/brief.md`, under `## Source material`, mark the consumed source:

```markdown
- [x] <label> — <URL>  <!-- read YYYY-MM-DD via /study-session -->
```

Do not rewrite the rest of the brief.

## Step 6: Confirm and route

Tell the user (concisely):
- Path to `notes.md`
- One-sentence thesis
- Top 2 insights
- Biggest open question remaining
- Next step: another source (`/study-session`), or draft public proof (future `/proof-draft`)

## Rules

- Never `Glob` from `/` or `$HOME` — use `~/.ours-stack/studies-index.jsonl` instead
- Wedge from `brief.md` overrides user curiosity mid-session — park tangents in `## Connections`
- Do not produce `proof.md` here — notes only
- Do not write to `~/.ours-stack/learnings.jsonl` here — that's a future checkpoint skill
- If the source contradicts the wedge, say so and suggest `/bear-hours` to fork scope