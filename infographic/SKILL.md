---
name: infographic
description: |
  Visual proof — transforme un extrait d'étude (brief, notes, dense-read, report)
  en une infographie mémorable (schéma, timeline, comparaison, flux). Utilise
  un outil de génération d'image si connecté ; sinon exporte un prompt prêt à coller.
  Déclencheurs : "infographic", "visual proof",
  "schéma visuel", "une image qui résume", /infographic, /visual-proof.
  Aucune recherche. Sorties : visual-proof.png ou infographic-prompt.md.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - image_gen
  - image_edit
  - GenerateImage
---

# Infographic (alias `/visual-proof`)

Transforme **un extrait d'étude** en **un visuel mémorable** — poster, slide, thread hook. **Aucune recherche, aucun WebSearch.**

Also invoked as **`/visual-proof`** — same skill, same outputs.

## When to use (vs other skills)

| Skill | Responsibility | Does NOT |
|-------|----------------|----------|
| `/layout-html` | Article HTML + 5–10 SVG inline | Raster poster, external prompts |
| `/infographic` | **This skill** — one memorable visual from *existing* text | New sources, multi-page layout |
| `/deep-research` | Discovery + synthesis | Visuals |
| `/bear-hours` | Topic framing | Visuals |

**Optional pipeline (never auto-chained):**

```
/bear-hours → notes/dense-read → /infographic (optional shareable visual)
/deep-research → /infographic (hook) OU /layout-html (rapport complet)
```

## Hard rules

1. **No research** — never `WebSearch` / `WebFetch`. Work only from provided text/files.
2. **One visual** — single PNG or single prompt export per run (iterations → `visual-proof.v2.png`).
3. **Faithful to source** — never invent sources, numbers, quotes, or claims absent from input.
4. **Spec always** — write `visual-proof.spec.md` before generate or prompt export.
5. **Privacy strip** — apply `references/privacy-strip.md` before spec finalization.
6. **Language** — on-image text matches source (`lang` in spec).
7. **≤7 labels** on canvas — image models garble text; if more needed → suggest `/layout-html`.
8. **Style first** — ask style via `AskUserQuestion` before reading content (unless smart-skip).
9. **No silent brief edits** — mention output paths in chat; do not append to `brief.md` without consent.
10. **Metaphor + hero** — every spec names one concrete visual metaphor (a drawable scene, never "boxes and lines") and one hero element that dominates the canvas. See Step 2.

## Step 0: Style — AskUserQuestion (always first)

Use **`AskUserQuestion`** — one call, wait for answer before continuing.

**Title:** `Infographic — Style`

**Hard rules:**
- **Never** list style options as plain chat bullets — always `AskUserQuestion`
- **STOP** after the call; wait for answer
- **Smart-skip** — if user already named a preset or described custom style (≥5 words), skip (see `references/palettes.md`)

**Question:** "Quel style visuel pour cette infographie ?"

**Options (exactly 4 — AskUserQuestion max; custom style goes through the automatic "Other" option):**

| id | label |
|----|-------|
| `warm` | Warm Bear — earthy, amber & vert, School of the Bear *(défaut)* |
| `academic` | Academic Blue — rapport recherche, bleu pro |
| `minimal` | Minimal Mono — technique, neutre, épuré |
| `creative` | Creative Spicy — coloré, original, un peu WTF |

**If user answers via "Other":** treat the free text as a custom style. Map to palette per `references/palettes.md`. One short follow-up only if too vague.

**If preset selected:** load palette from `layout-html/references/presets/{{PRESET_ID}}.md` via `references/palettes.md`.

Default when skipped: **`warm`**.

## Step 1: Intake — detect input mode

Resolve input in this priority order:

| Mode | Trigger | Source (first with substance) | Default output dir |
|------|---------|-------------------------------|-------------------|
| **A — Research slug** | slug or `research/<slug>/` | `report.md` (exec summary if long) | `research/<slug>/` |
| **B — Study slug** | `studies/<slug>/` | `notes.md` → `research.md` → `brief.md` | `studies/<slug>/` |
| **C — File path** | path to `.md`, `.txt` | that file | same directory |
| **D — Pasted text** | user pastes in chat | message body | `output/layout/<slug>/` |
| **E — Notes** | `notes.md` present | `studies/<slug>/notes.md` | `studies/<slug>/` |

**Slug derivation (mode D):** lowercase-hyphen from title or first heading; ask once if ambiguous.

**Guards:**
- No resolvable text → ask for slug, path, or paste
- Multiple substantive files in study → `AskUserQuestion` "Which file is the source of truth?"
- Source < ~150 words → warn; still allow `card` type
- If `brief.md` exists → read `## Narrow wedge`; reject visual elements outside wedge (one question if excerpt spans topics)

Load `references/visual-types.md`, `references/spec-schema.md`, `references/palettes.md`, `references/privacy-strip.md` before extracting.

## Step 2: Extract visual kernel (no invention)

From source, produce fields for `visual-proof.spec.md`:

| Field | Rule |
|-------|------|
| `title` | ≤8 words, from H1 or wedge |
| `thesis` | One sentence — the "so what" |
| `metaphor` | **One concrete, drawable scene** embodying the thesis (e.g. "un ours qui grimpe 4 paliers de montagne", not "timeline with 4 phases"). Tied to the source's domain. Never a diagram description. |
| `hero` | The single dominant element — the thesis phrase or THE killer number. Rendered huge (~1/3 of canvas); everything else stays small. |
| `nodes` | 3–7 labels, **1–2 words each**. FR: prefer accent-free synonyms when natural (image models garble é/è/ç) |
| `relations` | Optional: `A → B`, `A vs B` |
| `numbers` | Only if verbatim in source |
| `legend` | 2–5 entries max |
| `forbidden` | Long quotes, logos, copyrighted figures |

**Metaphor quality bar:** if you can't picture the scene in one sentence without the words "box", "diagram", "chart" or "section", it's not a metaphor — pick a composition variant from `references/visual-types.md` and make it concrete with the source's own imagery.

Apply `references/privacy-strip.md` **before** spec is finalized.

For long reports: use executive summary / key findings section only — never the whole report.

## Step 3: Select visual type

Auto-score per `references/visual-types.md`. Types: `schema`, `timeline`, `comparison`, `flow`, `card` (fallback).

If top two scores within tie threshold → `AskUserQuestion`:

**Title:** `Infographic — Layout`

**Options (max 4):** Schema | Timeline | Comparison | Flow — put the auto-scored winner first, labeled *(recommandé)*; picking it = agent's choice

User override always wins. Record `type_rationale` in spec.

**Escape:** If source needs >7 precise labels or exact numeric data on canvas → warn user; suggest `/layout-html` for SVG reliability. Proceed with simplified visual or PROMPT only if user confirms.

## Step 4: Build spec — always write

Write `{output_dir}/visual-proof.spec.md` per `references/spec-schema.md`.

This file is the audit trail and source for both IMAGE and PROMPT modes.

## Step 5: Generate or export

Load `references/tool-detection.md`. Determine MODE before acting.

### Step 5a: IMAGE mode

**When:** `image_gen` or `GenerateImage` available in this session (unless user asked prompt-only).

**Before generate:** Apply the labeled-infographic verification loop from `references/tool-detection.md`.

1. Compose prompt from spec + `references/prompt-template.md` § IMAGE mode
2. If using a `prompt`-style image tool: pass the composed prompt and aspect ratio (`16:9` default; `1:1` if square/Instagram; `9:16` if story)
3. If using a `description` + `filename` image tool: write `visual-proof.png` in the output dir
4. Verify (fidelity loop, see `references/tool-detection.md`): read generated image back — check text legible **and** label count/palette/hero match the spec; one targeted retry, then fallback PROMPT
5. Write `{output_dir}/visual-proof.png`
6. Write `{output_dir}/visual-proof.alt.md` — 2–3 sentence alt text + caption for posts

**Iterate:** `image_edit` on existing PNG → `visual-proof.v2.png`

```bash
open "{output_dir}/visual-proof.png"   # macOS, IMAGE mode
```

### Step 5b: PROMPT mode

**When:** No image tool, user requested prompt-only, or IMAGE failed.

1. Fill `references/prompt-template.md` → write `{output_dir}/infographic-prompt.md`
2. Include blocks: Universal, Midjourney, DALL·E, Flux/SD
3. Print **Universal** block in chat for immediate copy-paste

## Step 6: Deliver

Tell the user:

1. **Mode** used (IMAGE | PROMPT)
2. **Visual type** + preset
3. **Output paths** (spec always; png or prompt)
4. **Source file** + wedge (if any)
5. Reminder: spec = source of truth; image = illustrative proof, not new research
6. Suggest pairing: `/layout-html` for full article — do not create `proof.md` unless user asks

Do **not** silently edit `brief.md`. Optional on consent: add `## Visual proof` section with paths and date.

## Escape hatches

| User says | Action |
|-----------|--------|
| slug only | Try `research/<slug>/` then `studies/<slug>/` |
| file path | Mode C — outputs alongside source |
| pasted text | Mode D — `output/layout/<slug>/` |
| `overwrite` | Replace PNG/prompt without confirmation |
| `warm` / `academic` / etc. in message | Smart-skip style question |
| `prompt only` / `pas d'image` | Force PROMPT mode |
| `square` / `Instagram` | aspect `1:1` |
| `story` / `vertical` | aspect `9:16` |
| wants multi-diagram article | Suggest `/layout-html` |
| attaches generated image + `iterate` | `image_edit` path |
| wants research but no notes | Suggest `/deep-research` or `/bear-hours` first |

## Self-check before delivery

- [ ] No WebSearch / WebFetch
- [ ] All labels/numbers traceable to input
- [ ] `visual-proof.spec.md` written with `type_rationale`
- [ ] Spec has a concrete `metaphor` (drawable scene) + `hero` element
- [ ] Privacy strip applied
- [ ] ≤7 on-image labels, 1–2 words each (or user warned + confirmed)
- [ ] IMAGE: PNG + alt.md OR PROMPT: `infographic-prompt.md` with 4 blocks
- [ ] Universal block printed in chat (PROMPT mode)
- [ ] Clear differentiation from `/layout-html` in delivery message
- [ ] IMAGE mode: browser opened (`open` on macOS)
