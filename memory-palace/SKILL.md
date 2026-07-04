---
name: memory-palace
description: |
  Carte en relief oblique (style Google Maps 3D) — cliquer bâtiments et zones pour
  ancrer concepts (method of loci). Drill-down site → intérieur, panneau latéral.
  Pas de déplacement FPS. Reads brief.md, notes.md, research.md, report.md.
  Outputs memory-palace.json + HTML (Three.js vendored). Triggers: "memory palace",
  "palais de mémoire", "relief map", "carte oblique", /memory-palace. No new research.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Memory Palace

Transform study concepts into an **oblique relief map** (method of loci) — click buildings, drill into interiors, read concepts in a side panel. **No FPS movement. No research.**

## When to use (vs other skills)

| Skill | Responsibility | Does NOT |
|-------|----------------|----------|
| `/mind-map` | 2D tree, editable JSON | Spatial relief map |
| `/layout-html` | Linear article + SVG | Spatial map |
| `/memory-palace` | **This skill** — relief map + drill-down loci | New sources, WASD navigation |

**Optional pipeline (manual only — never auto-chain):**

```
/bear-hours → [dense read] → /memory-palace
/deep-research → /memory-palace
```

## Hard rules

1. **No research** — never `WebSearch` / `WebFetch`. Concepts must trace to input files.
2. **Wedge lock** — if `brief.md` exists, exclude `out-of-wedge` concepts from default `path[]`.
3. **Provenance** — every concept: `source.file`, `source.section`, optional `anchor`.
4. **Cap** — default **8–16 loci**; `AskUserQuestion` before exceeding 20.
5. **Two artifacts** — `memory-palace.json` (manifest) + `memory-palace.html` (experience).
6. **Self-contained HTML** — Three.js from `references/vendor/three.min.js`, inlined; **no CDN**.
7. **Iso-SVG fallback** — isometric click map (same drill-down) when no WebGL, mobile, or `prefers-reduced-motion`.
8. **Relief UX** — oblique map by default; optional **guided ground tour** on rails (`Visite guidée`); pan/zoom on site level only; click building → interior; no WASD / pointer-lock / free movement.
9. **Language** — match source (`lang` on `<html>`).
10. **Open browser** — `open <path>` on macOS after write.
11. **Theme first** — `AskUserQuestion` before reading content (unless smart-skip).

## Step 0: Theme — AskUserQuestion (always first)

Use **`AskUserQuestion`** — one call, wait for answer before continuing.

**Title:** `Memory Palace — Theme`

**Hard rules:**
- **Never** list theme options as plain chat bullets — always `AskUserQuestion`
- **STOP** after the call; wait for answer
- **Smart-skip** — if user already named a theme (`museum`, `chantier`, `corridor`, `library`, or ≥5 words describing a place), skip this step

**Question:** "Quel décor pour ancrer tes concepts ? (method of loci — un parcours fixe aide la mémoire)"

**Options (exactly 5):**

| id | label |
|----|-------|
| `corridor` | Corridor classique — pièces en ligne, portes numérotées *(défaut)* |
| `museum` | Musée — salles thématiques, vitrines = sous-concepts |
| `construction` | Chantier / atelier — zones, équipements *(robotique, BTP)* |
| `library` | Bibliothèque — rayons = thèmes, livres = citations |
| `custom` | Custom — je décris le lieu dans le prochain message |

**If `custom` selected:** wait for user's next message. Map to nearest archetype topology; store description in manifest `theme_notes`.

Default when skipped: `corridor`.

Load `references/palace-archetypes.md` for topology before Step 3.

## Step 1: Intake — detect input mode

Resolve input in this priority order:

| Mode | Trigger | Source | Default output |
|------|---------|--------|----------------|
| **A — Study slug** | slug or `studies/<slug>/` | `brief.md` → `notes.md` → `research.md` | `studies/<slug>/memory-palace.{json,html}` |
| **B — Research slug** | `research/<slug>/` | `report.md` (+ `brief.md` via Study link) | `research/<slug>/memory-palace.{json,html}` |
| **C — File path** | path to `.md` | that file | `<dir>/memory-palace.{json,html}` |
| **D — Pasted concepts** | user lists concepts in chat | message body | `output/layout/<slug>/memory-palace.{json,html}` |

**Slug derivation (mode D):** lowercase-hyphen from title or first heading; ask once if ambiguous.

**Custom output:** user may specify `→ out.html` — write HTML there; JSON alongside with same basename unless user says otherwise.

**Guard:** if no resolvable text and no pasted concepts → ask for slug, path, or concept list. Do **not** suggest `/deep-research` unless user wanted more content first.

## Step 2: Extract concepts

Load `references/concept-extraction.md`. Read source files. Extract only what exists.

**Minimum:** ≥5 concepts or abort with guidance ("add `notes.md` or paste concepts").

**Pre-flight:** if only `brief.md` with no notes → warn palace will be thin; proceed only if ≥5 extractable concepts.

**If >16 concepts extracted** — `AskUserQuestion`:

**Title:** `Memory Palace — Density`

**Options:**
- Trim to top 12 by importance
- Keep all (warn larger file)
- I'll pick concepts in chat

## Step 3: Map loci (relief site)

Load `references/loci-mapping.md` + `references/palace-archetypes.md`.

- `path[]` = ordered **building** ids on the site map (5–12)
- Each locus: `kind: building`, `footprint: [x, z, w, d]`, `height`, `interior.zones`, `interior.hotspots`
- Each locus: optional `scene` — vivid mental image (`scene.image`, 1–2 sentences) + 2–3 sensory hooks (`scene.senses`: « Son — … », « Odeur — … », « Texture — … ») encoding the concept for method-of-loci recall
- Entrée = wedge + why now; zones terrain/mécanismes/robots = findings; bureau = beliefs
- `blocked: true` buildings = open questions (click → panel only, no interior)
- Zone footprints relative to building interior (0…building size)

## Step 4: Write `memory-palace.json`

Follow `references/palace-schema.json` (`view_mode: relief`). Write to resolved output dir.

Overwrite without asking unless file modified &lt;1h ago and user didn't say `overwrite`.

Show user a compact summary: concept count, loci count, path order (one line).

## Step 5: Compose `memory-palace.html`

Load `references/navigation-ux.md`. Compose via script (preferred).

**Before composing:**

```bash
bash memory-palace/scripts/fetch-three.sh
```

Pinned version: **Three.js 0.160.0** (last npm release with `build/three.min.js` IIFE). Override: `THREE_VERSION=0.160.0 bash …/fetch-three.sh`.

If fetch fails (no network), fall back to **iso-SVG** HTML (`--2d-only`) and tell user to run fetch later for relief 3D.

**Compose** (agent-authored **or** helper script):

```bash
python3 memory-palace/scripts/compose-html.py studies/<slug>/memory-palace.json
# 2D only: python3 memory-palace/scripts/compose-html.py … --2d-only
```

Manual path:

1. `Read` `memory-palace/references/vendor/three.min.js` → inline in first `<script>` block
2. Embed full JSON as `const PALACE_DATA = …`
3. Inline scene bootstrap from `html-template.md` § Scene JS
4. Add room objects from `loci[].objects` (simple `BoxGeometry` props)
5. Theme colors from archetype table
6. HUD, overlays, 2D plan, footer with source files + study path

**If user said `2d only`:** `--2d-only` or `window.FORCE_2D = true`; skip Three.js inline (smaller file).

## Step 6: Deliver

```bash
open "<absolute-path>/memory-palace.html"
```

Tell the user:

1. Output paths (`.json` + `.html`)
2. Theme used
3. Locus count + concept count
4. **Memory walk script** — 30-second verbal path through buildings in `path[]` order
5. Source files used
6. Reminder: recall the **path**, not just the visuals
7. Optional: `/layout-html` for 2D report; re-run with `overwrite` after new notes

## Escape hatches

| User says | Action |
|-----------|--------|
| `2d only` | Iso-SVG map only (no Three.js) |
| `overwrite` | Replace JSON/HTML without confirmation |
| slug only | Try `studies/<slug>/` then `research/<slug>/` |
| file path | Mode C |
| pasted concepts | Mode D — `output/layout/<slug>/` |
| theme in message | Smart-skip Step 0 |
| `museum` / `construction` / etc. | Smart-skip theme question |

## Self-check before delivery

- [ ] No WebSearch / WebFetch
- [ ] Every concept label grep-able in source files
- [ ] `path[]` length ≥ 5 and ≤ 20
- [ ] `out-of-wedge` excluded from path (if brief exists)
- [ ] JSON validates against `palace-schema.json` structure
- [ ] HTML offline-ready (no CDN links)
- [ ] `view_mode: relief` in JSON; buildings have `footprint` + `interior`
- [ ] Iso-SVG fallback OR Three.js relief inlined
- [ ] No WASD / pointer-lock in composed HTML
- [ ] `lang` matches source
- [ ] Files written + browser opened