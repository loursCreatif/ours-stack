---
name: bear-hours
description: |
  School of the Bear topic framing — five forcing questions before deep learning.
  Defines scope, wedge (via entry angle), and success criteria; source material defaults
  to TBD (or inserted from the opening message). Asks consent before optional local scan;
  never reads source material during framing.
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
  - WebSearch
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
- **Title format:** `Bear Hours — Q{n}/5 : {label}`

**Open vs fixed questions:**
- **Open** (Q1–Q4): infer 2–3 contextual options from what the user said, plus a final option `other` — "Other — I'll clarify in my next message". If they pick `other`, accept a short free-text reply in chat, then continue with the next `AskUserQuestion`.
- **Fixed** (Q5): use the explicit options listed below (time box).

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
- **Opening-message source:** if the user already shared a URL, arXiv link, paper title, chapter, repo, or file path in their opening message, record it for direct insertion into `## Source material` in Step 3 (no question asked)
- Add `## Prior progress` in the brief (Step 3) when scan found context

If nothing found: one line — "No prior local context — starting fresh."

## Step 1: Gather context

Ask via `AskUserQuestion` until all five are answered (or smart-skipped).

### Q1 — Topic

**Ask:** "What exactly do you want to learn? One paper, one chapter, one system, or one concept — not a whole field."

**Options:** Infer 2–3 concrete topics from the user's message + `other`.

### Q2 — Why now

**Ask:** "Why now? What decision, project, or deadline depends on understanding this?"

**Options:** Infer plausible motivations from context + `other`.

### Q3 — Current beliefs

**Ask:** "What do you already believe about this? What would genuinely surprise you?"

**Options:** Infer 2–3 beliefs they might hold + `other`.

### Q4 — Entry angle (derives the wedge)

**Ask:** "Par où tu veux commencer ?"

**Options:** Three angles **instanciés sur le sujet de Q1** (une ligne concrète chacun) + `other` — "Other — I'll clarify in my next message".

**Avant d'afficher les options :** si tu n'es pas sûr de nommer une entrée narrative réelle pour l'angle « histoire », fais une **WebSearch rapide** (1–2 requêtes ciblées sur le sujet de Q1) pour identifier personnage, événement ou anecdote documentée — puis instancie les trois libellés.

**Règle « Par une histoire » :** jamais de libellé générique (`Par une histoire`, `une anecdote qui incarne le sujet`, etc.). L'option doit **nommer** une entrée narrative réelle et précise liée au sujet — personnage historique, événement, anecdote documentée — dans le libellé même : `Par une histoire — <nom précis>`.

Modèle (niveau de précision attendu) — sujet **« Bitcoin »** :

- **Les bases fondamentales** — comprendre la blockchain, les clés et le minage, brique par brique
- **Par une histoire — Satoshi Nakamoto et le bloc genesis** *(jamais « Par une histoire » seul ni « une anecdote qui incarne le sujet »)*
- **Vision d'ensemble d'abord** — la carte globale du protocole, une verticale à creuser viendra plus tard

Modèle — sujet **« électricité »** :

- **Les bases fondamentales** — tension, courant et résistance, loi d'Ohm en premier
- **Par une histoire — la guerre des courants, Edison vs Tesla**
- **Vision d'ensemble d'abord** — du générateur au réseau, une verticale viendra plus tard

Adapter chaque libellé au sujet exact de Q1 — pas de formulation générique. Les deux autres angles (bases, vision d'ensemble) restent instanciés comme ci-dessus ; seul l'angle histoire exige le nom nominatif dans le libellé.

**After the choice:** dériver le **wedge concret** (sujet + angle) et le confirmer en **une phrase** dans le chat (ou une micro `AskUserQuestion` si le wedge reste trop large). Repousser si le wedge couvre tout le champ de Q1. L'angle choisi sera noté dans `## Narrow wedge` du brief.

### Q5 — Time box

**Ask:** "How long are you giving yourself?"

**Options:**
- One session (today)
- One week
- Ongoing (no hard deadline)
- `other`

### Confirm before writing

After Q5, call `AskUserQuestion` once more:

**Title:** `Bear Hours — Confirm brief`

**Ask:** Summarize topic, wedge (sujet + angle d'entrée), time box, and source material status (verbatim source if captured from the opening message, else `TBD — /source-scout`) in 3–5 bullets. Include: **« Tu as déjà un lien ? Colle-le maintenant, sinon /source-scout s'en chargera. »** Then: "Ready to write `studies/<slug>/brief.md`?"

**Options:**
- Yes — write the brief
- Adjust the wedge
- Adjust source material

If they pick **Adjust source material** or paste a URL/title/path in chat at this step, accept it verbatim for `## Source material`, then confirm again. If they pick another adjustment option, ask one targeted `AskUserQuestion`, then confirm again.

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

**`## Source material` rules:**
- **Default:** `TBD — run /source-scout`
- **Opening-message source:** if the user's initial message included a URL, arXiv link, paper title, chapter, repo, or file path → write it verbatim instead of TBD
- **Confirm-step paste:** if the user pasted a link during the confirm recap → write it verbatim instead of TBD

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
**Entry angle:** <bases fondamentales | par une histoire | vision d'ensemble — one line how this angle applies>

## Success criteria
- [ ] I can explain <X> without jargon
- [ ] I can answer <Y> from memory

## Source material
TBD — run /source-scout

## Open questions
- ...
```

*(Default `## Source material` to `TBD — run /source-scout`; replace with the verbatim source when captured from the opening message or confirm step.)*

After writing `brief.md`, register the study in the global index:

```bash
~/.claude/skills/ours-stack/bin/ours-stack-register-study studies/<slug>/brief.md
```

(Use the repo-local path if developing outside the symlink.)

## Step 4: Handoff — passation et enchaînement

After `brief.md` is written and registered, deliver the closing in **three beats**. Tone inspired by office-hours Phase 6 Handoff — personalized, direct, no ceremony.

**Anti-slop (mandatory):**
- Quote the user's **actual words** for why now (Q2) and entry angle (Q4) — not paraphrased generics
- **No** « Félicitations ! », no praise paragraphs, no filler
- GOOD: « Tu veux comprendre ça parce que [their why now]. Tu commences par [their angle choice]. »
- BAD: « Votre parcours d'apprentissage est maintenant bien structuré. »

**Interdits inchangés :** ne pas lire ni résumer de source ici ; ne pas créer `proof.md` ; rappeler deep over wide seulement si le wedge sonne trop large (une ligne max).

### Beat 1 — Ce qui vient d'être créé

One short paragraph in plain language:

> Ton étude **« <titre> »** est lancée. Ta feuille de route est dans `studies/<slug>/brief.md` : ton sujet, ton angle d'entrée, tes critères de réussite. C'est le document que tous les autres skills liront.

Personalize with the user's exact phrases — their why now and their chosen angle. Never ship the template sentence alone.

### Beat 2 — Carte du parcours

Show where they are and what follows (short block, no essay):

```
✅ /bear-hours — cadrage (fait)
→ /source-scout — trouve 3 sources adaptées à ton angle
  /dense-read — lecture guidée de la source, tranche par tranche
  /study-status — à tout moment, pour voir où tu en es
```

### Beat 3 — Enchaînement direct

**Next skill:** if `## Source material` is still `TBD — run /source-scout` → `/source-scout` ; otherwise → `/dense-read` (source already in the brief).

Call `AskUserQuestion` once:

**Title:** `Bear Hours — On enchaîne ?`

**Ask:** One line — e.g. « On enchaîne sur <slug> ? »

**Options:**
- **Oui — lance /source-scout maintenant** *(or **Oui — lance /dense-read maintenant** when a source is already listed)*
- **Plus tard — je m'arrête ici**

**If Oui:** immediately **Read** and follow `source-scout/SKILL.md` or `dense-read/SKILL.md` for this `<slug>` in the **same session** (equivalent to invoking via the Skill tool). Do not stop after the handoff.

**If Plus tard:** one line only — e.g. `Quand tu veux : /source-scout <slug>` or `/dense-read <slug>`.

## Rules

- Do not start reading or summarizing source material here — framing only
- Do not open or inspect source documents even if the user supplies URLs or file paths — record them in the brief only
- Push back on "learn everything about X" — force a wedge via Q4 entry angle
- **Never create `proof.md`** (or any standalone proof draft) unless the user explicitly runs `/proof-draft` or asks to draft public proof
- Cross-project scan: `~/.ours-stack/studies-index.jsonl` only — never `find $HOME` at runtime