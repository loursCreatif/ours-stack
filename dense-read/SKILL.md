---
name: dense-read
description: |
  Guided wedge-locked reading — slice-by-slice session: explain in plain French, ONE question per
  tranche, user responds (3–6 tranches). Writes notes.md as session trace (user answers included).
  Escape hatch "lis tout seul" = solo Feynman extraction. Triggers: dense read, lire en profondeur,
  extraction Feynman, /dense-read. After /source-scout or /bear-hours; before /mind-map.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch
  - AskUserQuestion
  - Bash
---

# Dense Read

Guided reading **against the wedge** — slice by slice, plain French, your answers in `notes.md`. Not a solo summary, not a chapter recap.

**Default:** interactive session (3–6 tranches). **Stop when wedge is covered.** **Escape:** `lis tout seul` → [solo mode](#mode-solo--lis-tout-seul) (no questions).

**Pipeline:** `/bear-hours → /source-scout → /dense-read → /mind-map | /layout-html | /infographic` — do **not** auto-chain.

| Skill | Role |
|-------|------|
| `/dense-read` | **This skill** — guided tranches → `notes.md` (session trace) |
| `/source-scout` | Find sources — does not read |
| `/deep-research` | Wide funnel — not wedge extraction |
| `/bear-hours` | Frame wedge + brief |

## Hard rules

- **Wedge lock** — only sections/pages on `## Narrow wedge`; skip the rest.
- **No summary theater** — start with what the source says, not « ce papier traite de… ».
- **Plain French** — 2–4 sentences per tranche, zero jargon (define once inline if unavoidable).
- **One question per tranche** — wait for user reply before the next tranche.
- **Traceable claims** — location per tranche: section, page, paragraph, or timestamp.
- **No invented synthesis** — gaps go under « Ce que l'auteur ne dit pas » (end of session).
- **One anchor per run** unless user requests a second source.
- **AskUserQuestion** — confirmations only (anchor, existing notes, handoff); title `Dense Read — {label}`.
- **User words in notes** — `Ta réponse` = verbatim or quasi-verbatim; agent analysis lives in `Ce que dit la source` / `Explication`.

## Input modes

| Mode | Trigger | Output |
|------|---------|--------|
| **A — Study** *(default)* | slug / `studies/<slug>/` | `studies/<slug>/notes.md` |
| **B — Source direct** | URL/PDF/path, no brief | propose `/bear-hours` first |
| **C — Ad-hoc** | refuses brief | `output/dense-read/<slug>/notes.md` |

**Mode B:** no `brief.md` → `AskUserQuestion` title `Dense Read — No brief`, ask « Pas de brief trouvé. Que veux-tu faire ? », options: `/bear-hours` *(recommandé)* | Ad-hoc | `other`. Ad-hoc slug: lowercase-hyphen from title/URL; ask once if ambiguous.

## Step 0: Resolve study and source

Slug given → `Read` `studies/<slug>/brief.md`. Else → `Glob` `studies/*/brief.md`, `AskUserQuestion` title `Dense Read — Which study?`, up to 3 slugs + `other`.

From brief: `## Narrow wedge` (scope) · `## Current beliefs` (belief questions) · `## Success criteria` (check when met) · `## Source material` (first unchecked `[ ]` anchor) · `## Open questions` (track status in notes).

TBD/empty `## Source material` → stop: run `/source-scout` first. Direct URL/path → use as anchor; load brief if slug known. `lis tout seul` → solo mode after Steps 0–2.

## Step 1: Confirm anchor

`AskUserQuestion` title `Dense Read — Anchor` — anchor title + wedge one-liner: « On lit cette source tranche par tranche contre le wedge ? » Options: Oui (séance guidée) | Source différente | Wedge plus étroit | Lis tout seul. **Smart-skip:** `/dense-read <slug>` + one obvious unchecked anchor.

## Step 2: Fetch and scope

1. `WebFetch` or `Read` anchor. 2. Scan TOC/headings — **no body yet**. 3. Plan **3–6 tranches** (wedge slices only). 4. Paywall → offer paste, scout alternate, or abstract-only hatch.

Book/long paper → 3–6 slices for wedge, not whole doc. Note planned skips.

## Step 3: Séance guidée — boucle par tranche

**Default mode.** Repeat until wedge covered or 6 tranches done.

### Per tranche (in chat)

1. **Lire** une seule tranche (wedge only).
2. **Expliquer** en 2–4 phrases, français simple, zéro jargon — ce que cette partie dit *pour le wedge*.
3. **Poser UNE question** — varier le type :
   - « Redis-le dans tes mots : qu'est-ce que ça dit, pour toi ? »
   - « Ça colle avec ce que tu croyais ? » *(citer une croyance de `## Current beliefs` si dispo)*
   - « Qu'est-ce qui te surprend ici ? »
   - « Ça répond à quelle de tes questions ouvertes ? » *(si pertinent)*
4. **Attendre** la réponse dans le chat — ne pas enchaîner sans réponse. Réponse à côté → reformuler une fois, puis avancer.
5. **Noter** la tranche (Step 4 — incrementally or batch at end).

**Stop rule:** wedge covered → stop, even if tranches remain. Never read « to finish the document ».

**After last tranche:** bilan chat (1–2 lignes) — wedge oui/partiel, plus grosse surprise → Steps 4–7.

## Step 4: Write notes.md — trace de séance

Paths: `studies/<slug>/notes.md` or `output/dense-read/<slug>/notes.md`. Existing file → `AskUserQuestion` title `Dense Read — Existing notes`: Append (`## Séance <date> — <anchor>`) | Replace (archive `notes-<date>-archived.md`) | Cancel.

### File structure (mode guidé)

```markdown
# Notes — <anchor short title>

**Study:** <slug or ad-hoc>
**Source:** <citation + URL/path>
**Wedge:** <one line from brief>
**Séance:** <YYYY-MM-DD> — lecture guidée (<N> tranches)
**Sections lues:** <list> · **Ignoré:** <list + reason>

---

## Tranche 1 — <section / pages / timestamp>

**Ce que dit la source:** <claim, wedge-locked>
**Localisation:** §<section> p.<N> | <timestamp>
**Explication:** <2–4 phrases, français simple>
**Question:** <exact question posée>
**Ta réponse:** <mots exacts de l'utilisateur>

## Tranche 2 — …

(repeat per tranche)

---

## Synthèse de séance

**Wedge couvert:** oui | partiel | non

**Ce qu'on a compris ensemble:**
- <bullet — langage simple, ancré dans les réponses utilisateur>

**Surprises vs croyances:**
- <Confirmed | Shaken | New | Unresolved> — <lien belief + tranche>

**Questions ouvertes:**
- <partially answered | still open | new> — <question>

**Ce que l'auteur ne dit pas:**
- <gaps explicites pour le wedge>

**Critères de réussite** (depuis brief):
- [x] ou [ ] <criterion> — <one-line evidence>
```

## Step 5: Update brief.md (study mode)

1. Anchor `[x]` in `## Source material` + `<!-- read YYYY-MM-DD via /dense-read -->`
2. Met `[x]` on met `## Success criteria` with one-line evidence in chat.
3. Do **not** rewrite `## Open questions` — status lives in notes only.

## Step 6: Append learning

One line to `~/.ours-stack/learnings.jsonl`:

```json
{"ts":"<ISO8601>","skill":"dense-read","slug":"<slug>","source":"<anchor>","insight":"<durable sentence — prefer user's words>"}
```

## Step 7: Handoff — passation et enchaînement

Tone like `bear-hours` Step 4 / `source-scout` handoff — personalized, direct, no ceremony.

**Anti-slop:** cite wedge + anchor + one user phrase; no « Félicitations ! », no filler. GOOD: « Sur [wedge], [N] tranches de [anchor]. Tu as dit : « … ». » BAD: template alone.

### Beat 1 — Ce qui vient d'être fait

Short paragraph — lecture guidée, trace in `notes.md` with **tes réponses**, verdict wedge (oui/partiel). If partial/need sources/beliefs shaken → mention `/dense-read` (next source), `/source-scout`, or `/dialogue` in passing (not default handoff).

### Beat 2 — Carte du parcours

```
✅ /bear-hours — cadrage (fait)
✅ /source-scout — sources trouvées (fait)
✅ /dense-read — lecture guidée de l'anchor (fait)
→ /mind-map — carte mentale depuis brief + notes
  /layout-html · /infographic · /dialogue — selon besoin
  /study-status — à tout moment
```

Adjust checkmarks if bear-hours or source-scout skipped (ad-hoc).

### Beat 3 — Enchaînement direct

**Next skill:** `/mind-map` (default). `AskUserQuestion` title `Dense Read — On enchaîne ?` — e.g. « On enchaîne sur /mind-map pour <slug> ? » Options: **Oui — lance /mind-map maintenant** | **Plus tard — je m'arrête ici**. **If Oui:** `Read` + follow `mind-map/SKILL.md` same session. **If Plus tard:** one line — `Quand tu veux : /mind-map <slug>`.

## Escape hatches

| User says | Action |
|-----------|--------|
| `lis tout seul` / `en solo` | [Mode solo](#mode-solo--lis-tout-seul) |
| `vas-y` / `go` | Smart-skip Step 1; first unchecked anchor |
| `abstract only` | One tranche; thin notes; partial wedge |
| `strict wedge` | Drop tranches off wedge |
| `one claim only` | One tranche + one question |
| `overwrite` | Replace notes without confirmation |

---

## Mode solo — « lis tout seul »

Agent reads alone, writes `notes.md` **without** question loop. Trigger: `lis tout seul`, `en solo`, or Step 1 option.

**Extract in order (do not merge):** Pass A Claims (wedge, location + confidence) → Pass B Feynman (plain language) → Pass C Surprises vs `## Current beliefs` (Confirmed/Shaken/New/Unresolved) → Pass D Open questions → Pass E What the author does not say. **Stop** when wedge covered.

**notes.md:** same header fields as Step 4; `**Read:** <date> — mode solo` instead of Séance; body = `## Claims` · `## Feynman` · `## Surprises` · `## Open questions` · `## What the author does not say` · `## Verdict` (wedge + success criteria) — field meanings match **Synthèse de séance** in Step 4.

**After write:** débrief chat — 3 idées clés. Step 7 identical; Beat 1 says « extraction solo ».

## Self-check before delivery

- [ ] Guided: 3–6 tranches (or fewer if wedge covered); each has explain + one question + user reply in notes
- [ ] Claims located; wedge verdict honest; no summary-theater; anchor `[x]` (study mode)
- [ ] `learnings.jsonl` appended; Handoff 3 beats + On enchaîne ? (unless cancelled)
- [ ] Stopped when wedge covered — not full document