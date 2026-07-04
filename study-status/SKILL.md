---
name: study-status
description: |
  Read-only study dashboard — where each study stands (criteria checked, artifacts produced,
  suggested next step). Scans studies/*/brief.md in the current repo; optionally includes
  ~/.ours-stack/studies-index.jsonl for cross-repo studies.
  Use when the user asks "study status", "où j'en suis", "statut de mes études",
  "tableau de bord", "what's next", "what should I do next" (status view, not strategy debate),
  or runs /study-status. Never creates or modifies files.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Study Status

**Read-only dashboard** — one glance at every local study: wedge, success criteria progress, artifacts on disk, and the next skill the routing table suggests. No file writes, no research, no summary theater.

**Time budget:** ~1–2 minutes. Scan briefs + artifact presence only — do not read `notes.md` or anchor sources in depth.

## Hard rules

- **Read-only** — never `Write`, `Edit`, or create files. Output lives in chat only.
- **No summary theater** — table + 2–3 bullets. No essay, no "great progress!" filler.
- **Routing fidelity** — next-step suggestions must follow `AGENTS.md` routing (see below). Do not auto-chain skills.
- **Wedge in one line** — truncate `## Narrow wedge` to ≤80 chars for the table; full wedge only if user asks.
- **AskUserQuestion** — one question per call; title `Study Status — {label}`.

## When to use (vs other skills)

| Skill | Role |
|-------|------|
| `/study-status` | **This skill** — status table + next step per study |
| `/council` | Live round table — debate the topic with a multi-figure panel |
| `/source-scout` | Find sources — does not report status |
| `/bear-hours` | Frame a new study — not a dashboard |

**Not auto-chained** from any other skill.

## Step 0: Scope

**Default:** current workspace — `Glob` `studies/*/brief.md`.

**If no briefs found** → say so; suggest `/bear-hours` for a new topic. Stop unless user names another repo path.

**Optional global index** — after listing local studies, `AskUserQuestion`:

**Title:** `Study Status — Cross-repo?`

**Ask:** "Inclure les études d'autres repos via ~/.ours-stack/studies-index.jsonl ?"

**Options:**
- Oui — afficher slug, titre, repo, chemin (sans ouvrir les briefs externes)
- Non — repo courant seulement
- `other`

**If yes** → `Read` `~/.ours-stack/studies-index.jsonl` (or `$OURS_STACK_HOME/studies-index.jsonl` if set). For each line, parse JSON fields: `slug`, `title`, `wedge`, `repo`, `path`. Skip entries whose `path` is already in the local scan. **Do not** open external briefs except top 2–3 most relevant (same wedge keyword overlap or user-named slug).

**If user names one slug** → scan only `studies/<slug>/brief.md` (still list others only if they ask "all studies").

## Step 1: Discover studies

```bash
# List local study folders with briefs
Glob studies/*/brief.md
```

For each match, record `slug` from the path (`studies/<slug>/brief.md`).

## Step 2: Extract brief fields

`Read` each `studies/<slug>/brief.md`. Extract:

| Field | How |
|-------|-----|
| **Title** | First `#` heading line |
| **Slug** | `**Slug:**` line, or dirname |
| **Created** | `**Created:**` line (ISO date) |
| **Time box** | `**Time box:**` line (free text) |
| **Wedge** | First substantive line under `## Narrow wedge` (bold unit line preferred) |
| **Criteria** | All `- [ ]` and `- [x]` under `## Success criteria` — count `checked/total` |
| **Sources** | `## Source material` — **TBD** if section missing, empty, or contains only "TBD" / "à scout" / placeholder; **OK** if anchor + core list present |

**Criteria parsing:** only lines matching `^- \[[ x]\]` inside `## Success criteria` until the next `##` heading.

**Source material heuristic:**

| State | Condition |
|-------|-----------|
| **TBD** | Section absent, or only placeholders ("TBD", "à définir", "run /source-scout") |
| **OK** | Has `### Read first` or `### Core` or `### Anchor` with at least one linked source |
| **Partial** | Some sources listed but no clear anchor — note in table, suggest `/source-scout` refresh |

## Step 3: Detect artifacts

For each `studies/<slug>/`, `Glob` or `Bash` `test -f` / `test -d` against the AGENTS.md contract:

| Artifact | Path | Label |
|----------|------|-------|
| Notes | `notes.md` | notes |
| Council | `council.md` | council |
| Dialogue | `dialogue/*/` (any subfolder with `dialogue.md`) | dialogue |
| Layout | `report.html` | html |
| Mind map | `mind-map.json` or `mind-map.html` | mind-map |
| Infographic | `visual-proof.png`, `visual-proof.spec.md`, or `infographic-prompt.md` | visual |
| Memory palace | `memory-palace.json` or `memory-palace.html` | palace |
| Deep research link | `research.md` or `sources-index.md` | research |

**Display:** compact comma-separated labels in the Artefacts column (e.g. `notes, council, mind-map`). Use `—` if none beyond `brief.md`.

Do not count `brief.md` as an artifact.

## Step 4: Time box signal

Parse **Created** as `YYYY-MM-DD`. Interpret **Time box** heuristically:

| Time box text | Deadline estimate |
|---------------|-------------------|
| "aujourd'hui", "one session", "today" | Created + 0 days |
| "une semaine", "1 week" | Created + 7 days |
| "deux semaines", "2 weeks" | Created + 14 days |
| explicit date in text | use that date |
| unclear | skip overdue check |

If estimated deadline **< today** (from user_info `Today's date`) → append `⏰` to the study row in Prochaine étape and mention in bullets ("time box dépassée").

## Step 5: Suggest next step (routing)

Apply **in order** per study — first match wins:

| Condition | Suggested step |
|-----------|----------------|
| No `brief.md` | `/bear-hours` |
| Sources **TBD** or **Partial** | `/source-scout` |
| Sources **OK**, no `notes.md` | `/dense-read` (anchor from brief) |
| `notes.md` present, criteria not all checked | Continue `/dense-read` — or `/council` to debate the topic if stuck |
| All criteria checked | Étude terminée — archiver, ou nouveau wedge via `/bear-hours` |
| User asked "what should I do next?" on one study with real ambiguity | This skill shows facts first; suggest `/council` only if the user wants to debate the topic |

**Optional artifacts** (never auto-suggest unless user history implies it): `/mind-map`, `/layout-html`, `/infographic`, `/memory-palace`, `/dialogue` — mention in bullets only if criteria nearly done and no visual artifact yet.

## Step 6: Output format

### Main table

```markdown
| Étude | Wedge | Critères | Artefacts | Prochaine étape |
|-------|-------|----------|-----------|-----------------|
| robotique-assemblage-structurel | comment un robot pose des éléments structurels… | 0/3 | — | `/dense-read` |
| biomimetisme-locomotion-chantier | locomotion pattes sur terrain instable… | 2/3 | notes, council, mind-map, visual, palace | `/dense-read` |
```

- **Étude** column: slug (link path `studies/<slug>/brief.md` if the UI supports it, else plain slug).
- Keep wedge ≤80 chars with `…` if truncated.
- **Prochaine étape**: one skill or short phrase; add `⏰` prefix if time box overdue.

### Cross-repo appendix (if index included)

Separate small table — no wedge/criteria unless brief was opened:

```markdown
| Slug | Titre | Repo | Chemin |
|------|-------|------|--------|
```

### Synthesis bullets (2–3 only)

Pick concrete facts, e.g.:

- **Closest to done:** `<slug>` — N/M criteria, artifacts: …
- **Stalled:** `<slug>` — sources TBD since Created, or time box ⏰
- **Dormant:** studies with Created >14 days ago and no `notes.md`

No motivational language. No recommendations beyond the routing table.

## Example invocation

```
/study-status
/study-status robotique-assemblage-structurel
/où j'en suis sur mes études
```

## Failure modes

| Situation | Response |
|-----------|----------|
| No `studies/` in workspace | "Aucune étude locale. Lance `/bear-hours` pour cadrer un sujet." |
| Slug not found | List available slugs from Glob; ask once |
| `studies-index.jsonl` missing | Note file absent; local scan only |
| Malformed brief (no wedge) | Show row with wedge `—`; suggest brief cleanup via `/bear-hours` revisit |

## Privacy

Status output may echo wedge text and criteria from briefs. Do not paste long quotes from `notes.md` or copyrighted source titles beyond what the brief already lists.