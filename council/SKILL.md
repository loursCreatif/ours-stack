---
name: council
description: |
  Table ronde vivante — a live round-table meeting between 3–5 historical or
  relevant figures on any topic, with the user seated at the table.
  Figures speak in voice, disagree with each other, and challenge the user;
  the meeting unfolds turn by turn in chat and the user can intervene at any
  moment. Outputs meeting minutes (council.md).
  Use when the user asks for council, panel, round table, "table ronde",
  "réunion", "débat entre X et Y", "fais discuter X, Y et Z", or runs /council.
  Not for 1-on-1 conversation (/dialogue) or research (/deep-research).
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
---

# Council — Table ronde

A **live meeting** between named figures (historical or contemporary) around one topic — and the user is a **participant at the table**, not a reader of minutes.

**Output:** `studies/<slug>/council.md` (study-linked) or `output/council/<slug>/council.md` (standalone).

## When to use (vs other skills)

| Skill | Role |
|-------|------|
| `/council` | **This skill** — multi-figure live debate, user participates, meeting minutes |
| `/dialogue` | 1-on-1 Socratic conversation with a single figure |
| `/deep-research` | Facts and sources — not roleplay |
| `/bear-hours` | Frame a study wedge — not a meeting |

Do **not** auto-chain from other skills.

## Hard rules

1. **Live, never simulated** — the meeting happens turn by turn **in chat**. Never generate the whole meeting in one message. After the opening round, **STOP and wait for the user** — then never more than **3 figure turns** before the floor returns to the user.
2. **Real people only** — every seat at the table is a real historical or public contemporary figure speaking in their own voice, references, and era. **No invented personas, no generic roles** (no « Modérateur », no « une ingénieure robotique »). If an angle has no obvious figure, pick the closest real one. The host is a real figure too (rule 11).
3. **Built-in conflict** — compose the panel around at least one real axis of disagreement (Edison vs Tesla, Bohr vs Einstein, Keynes vs Hayek…). A panel that agrees is a failed panel.
4. **Short turns** — each figure speaks in **≤4 sentences**. No monologues, no transcript blobs.
5. **The user matters** — figures react to what the user actually said, may challenge it, and may address the user directly by question. The host regularly hands the floor back: « Et vous, qu'en dites-vous ? »
6. **Honest fiction** — artifact header states: *réunion pédagogique fictive — lentilles interprétatives, pas sources primaires*. No quotation marks on invented speech; paraphrase only.
7. **Era limits** — informed mode by default: modern topics through each figure's own concepts, tagged `[extrapolation]` inline. Modes and turn discipline: see `dialogue/references/epistemic-modes.md` (shared with /dialogue).
8. **No research** — never `WebSearch` / `WebFetch` during the meeting. Fact-check request → break character once, offer `/deep-research`.
9. **Living figures** — only public contemporary figures (published work, public positions). Refuse private individuals or defamation.
10. **French by default** — host and figures speak the user's language.
11. **Real host** — the meeting is animated by a real figure known for hosting or questioning (défaut français : Bernard Pivot ; alternatives selon sujet : Socrate, Jacques Chancel, Oprah Winfrey, David Attenborough…). The host frames, distributes the floor, and needles — in their own style. The user can swap the host or run « sans hôte » (figures self-manage, address the user directly).

## Step 0: Topic

- **User gave a topic or question** → use it directly. No framing gate: a raw topic is enough for a meeting.
- **User named a study slug** → `Read` `studies/<slug>/brief.md`; topic = `## Narrow wedge`, and `## Current beliefs` become debate fuel (figures may attack them).
- **Nothing clear** → one `AskUserQuestion` (title `Table ronde — Sujet`): "Sur quel sujet ou quelle question réunir la table ?" with 2–3 options inferred from `studies/*/brief.md` if any + `other`.

Sharpen loose topics into a **debatable question** (« l'IA » → « Faut-il craindre que l'IA centralise le pouvoir ? »). State the reframing in one line; adjust if the user objects.

## Step 1: Compose the panel

**Size:** 3–5 figures (hard cap 6, including mid-meeting invitations).

**Selection priorities, in order:**
1. Figures with a **real historical stake** in the question
2. At least two who **genuinely disagree** (historically or by doctrine)
3. One **unexpected but relevant** voice (different era or field) — optional, often the best turn generator
4. A **real host** fitting topic and language (rule 11) — announced with the panel

**If the user already named figures** → take them, suggest at most one addition if an obvious tension axis is missing, and go.

**Else** one `AskUserQuestion` (title `Table ronde — Panel`):

**Ask:** "Voici la table que je propose. On garde ?"

**Options:**
- **Ce panel (Recommended)** — list the 3–5 names, one line each: figure + why + against whom
- **Variante** — a second panel with a different angle
- **Je choisis moi-même** — user names figures in chat

**Persona line schema** (goes into the artifact, one card per figure):

```markdown
### <Nom> (<dates>, <domaine>)
- **Position de départ :** one sentence on the topic
- **Conteste :** what they push back on
- **Tension avec :** <autre membre> — sur quoi
```

The host gets a one-line card too (name, era, hosting style).

## Step 2: Open the meeting

In chat:

1. **The host** (2–3 sentences, in their own style): frames the question, names what is off-topic today, and announces the tour de table.
2. **Tour de présentations** — each figure introduces **themselves** in 2–3 sentences, in voice, assuming the user does not know them: who they are (era, field), what they are known for, and why they have a stake in today's question. No opening position yet — just « qui je suis et pourquoi je suis à cette table ». The host may add one teasing line per figure (« …et il n'est pas d'accord avec Monsieur Tesla, vous verrez »).
3. **Tour de table** — each figure gives an opening position (≤4 sentences, in voice, ending on a hook: a provocation, a doubt, or a question).
4. **The host hands the floor to the user**: one direct question tied to what was just said.
5. **STOP. Wait for the user.** The meeting does not continue without them.

Steps 2 and 3 may be merged for panels of 3 (presentation + position in one turn, ≤6 sentences); keep them separate for 4+ figures so the opening stays digestible.

Write the artifact header + panel cards + opening round to `council.md` now (path per Step 4).

## Step 3: Debate loop

For each user message:

1. Pick **1–3 figures** who respond — priority to: a figure the user addressed by name, then a figure who *disagrees* with what was just said, then relevant expertise. Not everyone speaks every turn.
2. Figures may **argue with each other** for at most 2 exchanges before the host cuts in.
3. End the block with the floor open to the user — a question from a figure or a relaunch from the host.
4. Append the exchange (user turn included, as `**Toi :**`) to the current `## Session` in `council.md`.

**Table commands:**

| User says | Action |
|-----------|--------|
| Names a figure (« Darwin ? », « Tesla, ton avis ») | That figure alone answers |
| « à table » / « réagissez tous » | Every figure reacts in 1–2 sentences |
| « invite <nom> » | Add the figure (cap 6), one-line card appended to Panel; the newcomer introduces themselves (2–3 sentences, as in Step 2) before speaking on the topic |
| « sortez <nom> » | Figure leaves politely |
| « on change d'angle : … » | Host reframes, quick re-positioning round |
| « recap » / « synthèse » | Host: 3 bullets (accords, désaccords, question ouverte) — meeting continues |
| « change d'hôte : <nom> » / « sans hôte » | Swap or remove the host |
| « hors personnage » | Reply as assistant; offer resume |
| « termine » / « on conclut » | Close the meeting (Step 4) |

**Soft budget:** after ~10 user exchanges, the host offers to close — the user decides.

**Drift control:** re-read the panel cards in `council.md` every 5 exchanges; keep voices distinct (vocabulary, era, temperament).

## Step 4: Close the meeting

Trigger: « termine », « on conclut », or accepted wrap-up offer.

1. Each figure gives **one closing sentence** (their position now — moved or not).
2. Host synthesis (in their style, but honest), appended to `council.md`:

```markdown
## Synthèse — <YYYY-MM-DD>

**Accords :**
- ...

**Désaccords restés ouverts :**
- <qui vs qui — sur quoi — ce qui trancherait>

**Ce que la discussion a déplacé :**
- <idées du user renforcées / ébranlées / apparues>

**Prochain pas suggéré :** <one concrete step — optionally /dialogue avec <figure>, /source-scout, /deep-research, /layout-html sur ce fichier, ou rien>
```

3. Append one line to `~/.ours-stack/learnings.jsonl`:

```json
{"ts":"<ISO8601>","skill":"council","slug":"<slug>","panel":"<noms>","insight":"<one durable sentence>"}
```

4. In chat: path to `council.md` + the synthesis's 3 strongest bullets. Nothing more.

**Artifact template:**

```markdown
# Table ronde — <question débattue>

> Réunion pédagogique fictive — les personnages sont des lentilles interprétatives, pas des sources primaires. Aucune recherche web effectuée.

**Slug :** <slug ou standalone>
**Sujet :** <question débattue>
**Panel :** <noms>
**Mode :** informé | strict | spéculatif
**Date :** <YYYY-MM-DD>

## Panel
<persona cards>

## Session <YYYY-MM-DD>
**<Hôte> :** ...
**<Figure> :** ...
**Toi :** ...
...

## Synthèse — <YYYY-MM-DD>
...
```

**Resume:** if `council.md` already exists with a `## Session` marker, one `AskUserQuestion` (title `Table ronde — Reprise`): continue (append new `## Session <date>`, re-read panel cards + last 3 turns), restart (archive as `council-<date>-archived.md`), or cancel.

## Escape hatches

| User says | Action |
|-----------|--------|
| « vas-y » / « surprends-moi » | Skip the panel question; best panel, straight to opening |
| « débat entre X et Y sur Z » | Panel = X + Y (+ real host, or sans hôte); skip Steps 0–1 |
| « sans moi » / « laisse-les débattre » | Exception to rule 1: run 3 autonomous rounds, then synthesis — say once that live mode is richer |
| « strict » / « pas d'anachronisme » | Strict era mode for all figures |
| « stop » | Close immediately (Step 4) |

## Self-check before close

- [ ] Meeting ran live — user spoke at least once (unless « sans moi »)
- [ ] Each figure introduced themselves at the opening (who, era, why at this table) — never assume the user knows them
- [ ] Never more than 3 figure turns between user turns
- [ ] Real disagreement surfaced and named in the synthesis
- [ ] Figure turns ≤4 sentences, distinct voices, no invented quotes in quotation marks
- [ ] Fiction disclaimer in artifact header
- [ ] `council.md` contains panel cards + transcript + synthesis
- [ ] `learnings.jsonl` appended on close
- [ ] `brief.md` untouched (council is advisory)
