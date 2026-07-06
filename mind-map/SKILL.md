---
name: mind-map
description: |
  Carte mentale interactive — extraction hiérarchique depuis brief/notes/report vers
  mind-map.json éditable + mind-map.html autonome (pan/zoom, expand/collapse, liens
  sources). Zero CDN. Presets partagés avec layout-html. Pas de recherche.
  Déclencheurs : "mind map", "carte mentale", "mind-map", "vue hiérarchique".
  Commande : /mind-map.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Mind Map

Carte mentale cliquable — plus rapide à parcourir qu'un article linéaire, moins immersif qu'un palais 3D.

## When to use (vs other skills)

| Skill | Responsibility | Does NOT |
|-------|----------------|----------|
| `/layout-html` | Article linéaire + SVG figures | Arbre hiérarchique |
| **`/mind-map`** | **This skill** — carte mentale interactive | Nouvelle recherche |
| `/deep-research` | Synthèse + sources-index | Carte mentale |

**Optional pipeline** (never auto-chained):

```
/bear-hours → notes / dense-read → /mind-map
/deep-research → /mind-map
```

## Hard rules

1. **No research** — never `WebSearch` / `WebFetch`. Work only from provided text/files.
2. **Zero external assets** — no CDN, no Google Fonts, no external scripts/images/stylesheets, no `fetch()`.
3. **JSON is source of truth** — `mind-map.json` editable; HTML regenerated from JSON.
4. **Faithful to source** — never invent URLs, claims, or nodes absent from input.
5. **Limits** — max **80 nodes**, depth **5**. Overflow → merge siblings into one `detail` with bullet `note` (deterministic, no ask).
6. **Escape output** — embed JSON via structured serialization only; never inject raw markdown HTML into template.
7. **Open browser** — `open <path>` on macOS after write.

## Step 0: Style — AskUserQuestion

**Title:** `Mind Map — Style`

Offer exactly these 4 options (AskUserQuestion max): `warm`, `editorial`, `minimal`, `creative`. Custom style goes through the automatic "Other" option — treat the free text as a custom preset per `references/presets.md` § Custom. Smart-skip if one of these presets is named in message.

Default when skipped: `warm` for all inputs.

Load `references/presets.md` and token blocks from `references/html-template.md`.

## Step 1: Intake — detect input mode

| Mode | Trigger | Source | Output |
|------|---------|--------|--------|
| **A — Study** | `studies/<slug>/` or slug | `brief.md` + optional `notes.md` | `studies/<slug>/mind-map.{json,html}` |
| **B — Research** | `research/<slug>/` | `report.md` + optional `sources-index.md` | `research/<slug>/mind-map.{json,html}` |
| **C — File** | path to `.md` | that file | `<dir>/mind-map.{json,html}` |
| **D — Pasted** | text in chat | message body | `output/mind-map/<slug>/map.{json,html}` |
| **E — Regenerate** | `regenerate` / existing JSON | `mind-map.json` only | regen HTML only |

**Invocation examples:**

```
/mind-map biomimetisme-locomotion-chantier
/mind-map studies/biomimetisme-locomotion-chantier/brief.md
/mind-map research/robots-assemblage-structurel-chantier
/mind-map regenerate studies/foo/mind-map.json
```

**Guard:** no text and no resolvable slug → ask for content or path.

## Step 2: Extract hierarchy

Load `references/extraction-rules.md` and `references/node-schema.md`.

Parse markdown headings, bullets, source lines. Assign `id`, `type`, `label`, `summary`, `note`, `href`, `collapsed`, and optional `importance`.

Use `importance` only for visual hierarchy: `5` root / central thesis, `4` major branches, `3` supporting concepts, `2` details or examples, `1` sources or minor leaves. Omit it when unsure; the HTML renderer infers a safe size.

Leave top-level `layout` omitted or `"auto"` by default. Set `"centered"` only when the source is clearly wide/exploratory and shallow; set `"tree"` only when the user explicitly wants the classic hierarchy.

Run validation:

```bash
python3 mind-map/scripts/validate-map.py "<path>/mind-map.json"
```

On validation error → fix JSON before composing HTML.

## Step 3: Write JSON then HTML

1. Write `mind-map.json` with accurate `meta.nodeCount`
2. Compose HTML:

```bash
python3 mind-map/scripts/compose-html.py "<path>/mind-map.json"
```

Or hand-compose from `references/html-template.md` if script unavailable.

Overwrite without asking unless file modified <1h ago and user didn't say `overwrite`.

## Step 4: Deliver

```bash
open "<absolute-path>/mind-map.html"
```

Tell the user:

1. Output paths (json + html)
2. Style preset used
3. Input mode
4. Node count by type (`concept`, `detail`, `example`, `source`); mention `summary` / `note` coverage when present
5. Reminder: edit `mind-map.json` then `/mind-map regenerate <path>`

## Errors (deterministic)

| Condition | Action |
|-----------|--------|
| Empty / unparseable markdown | Stop — ask for clearer structure or paste headings |
| No brief (study mode) | Suggest `/bear-hours` first |
| >80 nodes after extraction | Merge deepest siblings into grouped `detail` until ≤80 |
| Duplicate `id` | Regenerate ids with slug prefix |
| `source` without `href` | Keep node; panel shows label only |
| Invalid JSON (regenerate) | Stop — show `validate-map.py` error |
| `compose-html.py` missing | Fall back to template in `references/html-template.md` |

## Escape hatches

| User says | Action |
|-----------|--------|
| `regenerate` | Mode E — JSON → HTML only |
| `overwrite` | Replace without confirmation |
| `warm` / `editorial` / `minimal` / `creative` | Smart-skip style question |
| Described style ("sombre néon", "pastel"…) | Smart-skip — custom preset per `references/presets.md` § Custom (`meta.customTokens`) |
| slug only | Try `studies/<slug>/` then `research/<slug>/` |

## Self-check before delivery

- [ ] No WebSearch / WebFetch
- [ ] All nodes traceable to input
- [ ] ≤80 nodes, depth ≤5
- [ ] `validate-map.py` passes
- [ ] HTML offline-ready (no external URLs in assets)
- [ ] JSON + HTML written + browser opened

## References

- `references/node-schema.md` — JSON contract
- `references/extraction-rules.md` — markdown → tree
- `references/html-template.md` — manual compose fallback
- `references/presets.md` — layout-html token alignment
- `references/design-decisions.md` — design decision log
- `scripts/validate-map.py` — schema check
- `scripts/compose-html.py` — JSON → HTML
