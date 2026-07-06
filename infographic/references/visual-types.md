# Visual type taxonomy

Four primary types + fallback `card`. Map heuristics from `layout-html/references/diagram-menu.md` — inform raster composition only, never emit SVG.

## 1. Schema (`schema`)

**Looks like:** Labeled blocks, hierarchy, pillars-on-base, taxonomy wheel, stack layers.

**Select when:** Architecture, "3 pillars", categories, system components, layered stack.

**Source signals:** "consists of", numbered families, parallel H2 sections, "mécanismes", "piliers".

**Layout:** Center or base anchor + 3–6 satellites; clear legend.

**Avoid:** >7 nodes — collapse into groups.

**Composition variants (pick the one matching the source's domain, make it concrete):**
- *Temple* — pillars standing on a labeled foundation, roof = thesis
- *Tree* — trunk = core concept, branches = components, roots = prerequisites
- *Orbit* — hero element as sun, satellites orbiting with short labels

**Fallback layout instruction:** centered hierarchy, hero element large in the middle, 3–6 labeled satellites.

---

## 2. Timeline (`timeline`)

**Looks like:** Horizontal or vertical phases, NOW → near → far.

**Select when:** Maturity horizons, historical evolution, roadmap, short/medium/long term.

**Source signals:** dates, phases, "today / in 5 years", deployment stages, "court terme".

**Max:** 4 phases, 1–2 word labels each.

**Composition variants:**
- *Mountain path* — trail climbing ledge by ledge, summit = end state
- *Road* — milestones along a road vanishing toward the horizon
- *Growth* — seed → sprout → tree stages for maturity narratives

**Fallback layout instruction:** horizontal timeline, 3–4 labeled phases left to right, final phase visually largest.

---

## 3. Comparison (`comparison`)

**Looks like:** Split panel A vs B, before/after, wheels vs legs.

**Select when:** Explicit contrast, tradeoffs, "X better than Y on Z".

**Source signals:** "vs", "compared to", "however", "roues" / "pattes", "avant/après".

**Rule:** Both sides must appear in source — no strawman.

**Composition variants:**
- *Balance scale* — two pans, heavier side = source's verdict
- *Split scene* — one landscape, day/night or terrain split down the middle
- *Mirror* — same object drawn twice with the differing traits highlighted

**Fallback layout instruction:** split-screen with bold divider, A/B headers, verdict element largest.

---

## 4. Flow (`flow`)

**Looks like:** Left-to-right or top-down process, decision diamond, feedback loop.

**Select when:** Workflow, algorithm steps, causal chain, numbered methodology.

**Source signals:** numbered steps, "first … then … finally", "d'abord … ensuite".

**Max:** 5 steps + optional loop-back.

**Composition variants:**
- *River* — stream flowing through labeled waypoints, loop = tributary rejoining
- *Assembly line* — object visibly transformed at each station
- *Trail map* — numbered path across a stylized landscape

**Fallback layout instruction:** linear flow with arrows, 4–5 steps, outcome element largest at the end.

---

## 5. Fallback: Insight card (`card`)

**When:** Short notes, single killer finding, <300 words, no strong signal for 1–4.

**Looks like:** One bold thesis + 3 supporting chips + tiny legend.

**Composition variants:**
- *Big number* — the killer stat at ~1/3 of canvas, chips beneath
- *Object hero* — one illustrated object from the source's domain carrying the headline

**Fallback layout instruction:** single hero card, headline dominant, three callout chips below.

---

## Metaphor before layout

The layout instruction is the **skeleton**; the spec's `metaphor` is the **skin**. Always merge them: pick a composition variant, then replace its generic imagery with the source's own domain (construction site, forest, robot, lab…). A generic instruction alone produces a forgettable corporate diagram.

---

## Selection scoring

```
score[type] = keyword_hits + 2 * section_heading_match + 3 * user_override
pick max score
if max - second_max < 2 → AskUserQuestion "Infographic — Layout"
```

### Keyword hints

| Type | Keywords (FR/EN) |
|------|------------------|
| schema | architecture, piliers, composants, consists of, stack, layers |
| timeline | phase, roadmap, maturité, horizon, évolution, court/moyen/long |
| comparison | vs, versus, comparé, tradeoff, roues/pattes, avant/après |
| flow | étape, workflow, process, d'abord, then, finally, causal |
| card | (default when no strong signal) |

### AskUserQuestion (tie-break)

**Title:** `Infographic — Layout`

**Question:** "Quel type de visuel pour cette idée ?"

**Options (exactly 4 — AskUserQuestion max; auto-scored winner first, labeled *(recommandé)*; picking it = agent's choice):**

| id | label |
|----|-------|
| `schema` | Schéma — blocs, hiérarchie, piliers |
| `timeline` | Timeline — phases, maturité |
| `comparison` | Comparaison — A vs B |
| `flow` | Flux — étapes, workflow |

User override always wins.