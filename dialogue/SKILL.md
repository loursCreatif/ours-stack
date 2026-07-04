---
name: dialogue
description: |
  One-on-one Socratic dialogue with a historical or contemporary public figure.
  Character speaks in voice, challenges user beliefs, ties every turn to the wedge,
  respects epistemic limits (informed mode default). Outputs persona card + dialogue
  transcript. Use when the user wants to talk with Darwin, Tesla, Einstein, etc.,
  "dialogue historique", "dialogue-historique", "discuter avec", "parler à",
  challenge beliefs in character, or runs /dialogue (alias /dialogue-historique).
  Not for multi-agent panels (/council) or research.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
---

# Dialogue historique

Immersive **1-on-1** conversation with a figure who questions your ideas — not a panel, not research, not framing from scratch.

**Output:** `persona.md` + `dialogue.md` under `studies/<slug>/dialogue/<persona-slug>/` or `output/dialogue/<slug>/` (standalone).

## When to use (vs other skills)

| Skill | Role |
|-------|------|
| `/dialogue` | **This skill** — single character, Socratic back-and-forth, belief testing, transcript |
| `/council` | Live round table — several figures debate, user participates (`council.md`) |
| `/bear-hours` | Frame wedge + brief when nothing exists yet |
| `/deep-research` | Factual wide search + synthesis — not roleplay |

| User intent | Route |
|-------------|-------|
| "Talk **with** Darwin / Tesla / …" | `/dialogue` |
| "Fais discuter X, Y et Z" / round table, several figures | `/council` |
| "Did they really say that?" (facts) | `/deep-research` after out-of-character handoff |

Do **not** auto-chain from other skills.

## Hard rules

- **In character** — voice, references, era limits; never generic assistant tone in character turns.
- **Advisory fiction** — artifact header states: *dialogue pédagogique fictif — lentille interprétative, pas source primaire*.
- **No fake quotes** — no quotation marks for invented speech; paraphrase in own words.
- **Socratic** — every character turn ends with **≥1 question** challenging the user.
- **Wedge tie-in** — every character turn includes a one-sentence link to the wedge (from `brief.md` or user-stated unit).
- **Informed default** — modern topics allowed through era's concepts; tag `[extrapolation — informed]` inline. See `references/epistemic-modes.md`.
- **Wedge lock** — refuse polite scope creep beyond `## Narrow wedge` when brief exists.
- **No research mid-dialogue** — no `WebSearch` / `WebFetch` during Steps 5–6. Fact-check → out-of-character handoff to `/deep-research`.
- **Living figures** — only **public** contemporary figures (published work, public statements). Refuse private individuals, gossip, or defamation. One disclaimer in `persona.md`.
- **Persona drift control** — re-read `persona.md` before turns 1, 5, 10, 15, …
- **AskUserQuestion** — one question per call; title `Dialogue historique — {label}`.

## Interactive questions

Use **`AskUserQuestion`**. One call at a time; **STOP** after each.

**Smart-skip:** user already named figure + topic → skip Step 1. User gave study slug → skip Step 0 picker. User accepts informed mode → skip Step 3.

## Step 0: Resolve context

**If user names a study slug** → `Read` `studies/<slug>/brief.md`.

**If user names topic only** → `Glob` `studies/*/brief.md`. If matches, `AskUserQuestion`:

**Title:** `Dialogue historique — Contexte`

**Ask:** "Lier ce dialogue à une étude existante ou session ad-hoc ?"

**Options:**
- <slug A> — <wedge one-liner>
- <slug B> — <wedge one-liner>
- Ad-hoc — pas de brief (`output/dialogue/<slug>/`)
- `other`

**If no brief and ad-hoc** → derive `slug` from topic + persona (e.g. `evolution-darwin`). Create `output/dialogue/<slug>/`.

Extract from brief when present:

| Field | Use |
|-------|-----|
| `## Narrow wedge` | Wedge lock — quote in artifact |
| `## Current beliefs` | Socratic fuel — pick one to challenge first |
| `## Open questions` | Question targets |
**Resume:** if `dialogue.md` exists with `## Session` markers → `AskUserQuestion`:

**Title:** `Dialogue historique — Reprise`

**Ask:** "Une session existe déjà. Continuer ou recommencer ?"

**Options:**
- Continue — append new `## Session <date>` section
- Restart — archive by renaming to `dialogue-<date>-archived.md`, fresh file
- Cancel

On continue: re-read `persona.md` + last session's last 3 turns before replying.

## Step 1: Choose figure

**Title:** `Dialogue historique — Personnage`

**Ask:** "Avec qui veux-tu dialoguer ?"

**Options:** Infer 2–3 figures from wedge/topic + `other` (name in chat) + `Surprise me — pick the best fit`.

Examples:

| Topic / wedge | Suggestions |
|---------------|-------------|
| Evolution, adaptation | Darwin, Wallace, Mendel |
| Electricity, AC/DC | Tesla, Faraday, Edison |
| Structural assembly / construction | Brunelleschi, Babbage |
| User's `brief.md` beliefs | Figure who historically **disagreed** with a core belief |

**Legitimacy:** if figure has weak wedge fit, say so once and offer closer match before locking persona.

## Step 2: Dialogue goal

**Title:** `Dialogue historique — Objectif`

**Ask:** "Quel est l'objectif de ce dialogue ?"

**Options:**
- Challenger mes croyances *(default if brief has `## Current beliefs`)*
- Explorer un concept par questions
- Préparer une preuve publique (hook / thread)
- `other`

## Step 3: Epistemic mode

**Title:** `Dialogue historique — Mode`

**Ask:** "Quel niveau d'anachronisme autoriser ?"

**Options:**
- **Informé** — sujets modernes via mon cadre d'époque *(défaut)*
- **Strict** — limites d'époque, pas d'extrapolation
- **Spéculatif** — contre-factuel explicite
- `other`

Load `references/epistemic-modes.md` for turn tags.

## Step 4: Write persona.md

Create `persona.md` per `references/persona-template.md`.

**Grounding only from:** brief fields, user wedge, user-supplied bio (if any). No WebSearch.

Set `persona-slug` = lowercase hyphenated short name (`darwin`, `tesla`, `wallace`).

## Step 5: Open dialogue.md

Path:

- Study-linked: `studies/<slug>/dialogue/<persona-slug>/`
- Standalone: `output/dialogue/<slug>/`

Write `dialogue.md` header:

```markdown
# Dialogue — <Personnage> × <Sujet>

> Dialogue pédagogique fictif — lentille interprétative, pas source historique primaire.

**Study slug:** <slug or standalone>
**Persona:** <persona-slug>
**Wedge:** <one line>
**Mode:** informed | strict | speculative
**Goal:** <from Step 2>
**Started:** <YYYY-MM-DD>

---

## Session <YYYY-MM-DD>
```

First character turn — use turn schema from `references/epistemic-modes.md`. Open with welcome + wedge-sharp question targeting one belief or open question.

## Step 6: Conversation loop

For each user message:

1. Re-read `persona.md` if turn number ∈ {1, 5, 10, 15, …}
2. Reply in character — append turn to current `## Session` in `dialogue.md`
3. Enforce: wedge tie-in, ≥1 question, mode tag, confidence level
4. Optional domain analogy when natural — **not** on a fixed schedule; never forced

**Pause commands** (`pause`, `résume`, `recap`): 3 bullets in chat — beliefs touched, open questions, suggested next user move. Do not break character in recap bullets (label as moderator recap).

**Fact-check request:** break character once → offer `/deep-research`; do not search.

**Turn budget (soft):** after ~12 character turns without user saying "continue", offer to close with synthesis.

## Step 7: Close session

Trigger: user says `termine`, `insights`, `sauvegarde`, `close`, or accepts wrap-up offer.

1. Append to `dialogue.md`:

```markdown
## Session close — <YYYY-MM-DD>

**Beliefs tested:**
- <strengthened / shaken / unresolved — bullet per belief>

**Open questions remaining:**
- ...

**Suggested next step:** </source-scout | /deep-research | /proof-draft | /layout-html on this file>
```

2. Append one line to `~/.ours-stack/learnings.jsonl`:

```json
{"ts":"<ISO8601>","skill":"dialogue","slug":"<slug>","persona":"<name>","insight":"<one durable sentence>"}
```

3. Tell user in chat: path, 3-bullet summary, next skill — **no separate `insights.md`**.

## Step 8: Route

| Outcome | Suggest |
|---------|---------|
| Beliefs shaken | `/source-scout` or anchor read |
| Need facts about figure | `/deep-research` |
| Rich thread material | `/layout-html` on `dialogue.md` |
| Wedge itself wrong | `/bear-hours` to adjust |
| Wants several figures at once | `/council` (table ronde, not 1-on-1) |

## Escape hatches

| User says | Action |
|-----------|--------|
| `vas-y` / `go` | Smart-skip Steps 2–3; default informed + challenge beliefs |
| `strict only` | Force strict mode; skip Step 3 |
| `one question only` | Single character turn + offer close |
| `out of character` | Next reply as assistant; offer resume |
| `stop` | Close session (Step 7) immediately |

## Self-check before close

- [ ] `persona.md` exists with uncertainty flags on positions
- [ ] `dialogue.md` header has fiction disclaimer
- [ ] Every character turn has wedge tie-in + question + mode/confidence
- [ ] No quotation marks on invented speech
- [ ] Living figure (if any) is public + disclaimer present
- [ ] `learnings.jsonl` appended on close

## Quality references

- Persona structure: `references/persona-template.md`
- Modes + turn schema: `references/epistemic-modes.md`
- Examples + vs council: `references/example-prompts.md`