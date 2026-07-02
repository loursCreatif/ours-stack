# Diagram menu — SVG catalogue

Pick diagrams based on **source content** (research report, article, notes, pasted text). Max 10 figures total. Adapt all labels to the topic — never copy placeholder text verbatim.

**Research-only:** funnel PRISMA, contradiction cards (require matching sections in source).

**Universal:** insight cards, timeline, pillars, workflow, decision tree, concept map, comparison, numbered steps — use for any text.

**Qualité & animations :** lire **`svg-graphics.md`** avant de composer — barre de qualité, boîte à outils `<defs>`, patterns node/connector, stat callouts, CSS animations sans JS.

## SVG color rules

Never hardcode one palette in output. Use the **active preset palette** from `presets/{{PRESET_ID}}.md` § SVG palette.

Semantic roles when composing SVG:

| Role | Use for |
|------|---------|
| `--fig-primary` / accent | main shapes, headers, arrows |
| `--fig-secondary` | gradients, secondary boxes |
| `--fig-success` | positive / mature / OK nodes |
| `--fig-warning` | caution / mid-term nodes |
| `--fig-muted` | labels, grid, captions in SVG |
| `--fig-surface` | light fills (funnel tiers, backgrounds) |

Replace placeholder hex in templates below with preset values before writing HTML.

## Grammaires par preset

| Preset | Stroke | Fill | Radius | Labels |
|--------|--------|------|--------|--------|
| `academic` | 1.5, crisp | light gradients | 6–10 | sans-serif |
| `editorial` | 1, thin | cream, flat | 4–6 | serif optional |
| `minimal` | 1, mono | none or white | 0–4 | monospace |
| `warm` | 1.5–2 | earthy soft | 10–14 | sans-serif |
| `creative` | 2.5, bold | saturated multi | 0–8 | sans bold 700+ |

---

## 1. Funnel PRISMA (almost always)

**When:** funnel counts exist in report.

**Params:** `{{DISCOVERED}}`, `{{INCLUDED}}`, `{{READ}}`, `{{EXCLUDED}}`

```html
<div class="visual-beat fig-animate">
  <svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Entonnoir méthodologie" class="fig-svg">
    <defs>
      <linearGradient id="figN-grad-1" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{{SURFACE}}"/><stop offset="100%" stop-color="{{SURFACE_2}}"/></linearGradient>
      <marker id="figN-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{{MUTED}}"/></marker>
    </defs>
    <polygon class="fig-layer fig-layer-1" points="240,16 400,52 400,70 240,70 80,70 80,52" fill="url(#figN-grad-1)" stroke="{{SECONDARY}}" stroke-width="1.5"/>
    <text x="240" y="46" text-anchor="middle" font-size="13" font-weight="700" fill="{{PRIMARY}}">{{DISCOVERED}} découvertes</text>
    <line x1="400" y1="46" x2="430" y2="46" stroke="{{MUTED}}" stroke-width="1" marker-end="url(#figN-arrow)"/>
    <text x="438" y="49" font-size="10" fill="{{MUTED}}">{{EXCLUDED}} exclues</text>
    <polygon class="fig-layer fig-layer-2" points="240,78 360,108 360,126 240,126 120,126 120,108" fill="{{SURFACE_2}}" stroke="{{SECONDARY}}" stroke-width="1.5"/>
    <text x="240" y="111" text-anchor="middle" font-size="12" font-weight="600" fill="{{PRIMARY}}">{{INCLUDED}} retenues → {{READ}} lues</text>
    <polygon class="fig-layer fig-layer-3" points="240,138 300,168 300,186 240,186 180,186 180,168" fill="{{PRIMARY}}" stroke="{{PRIMARY}}" stroke-width="1.5"/>
    <text x="240" y="168" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Synthèse</text>
  </svg>
  <p class="caption">Fig. N — Méthodologie : entonnoir PRISMA</p>
</div>
```

---

## 2. Architecture / pillars

**When:** report describes hybrid architecture, multiple complementary pillars.

**Params:** 3 pillar labels + base context label + apex label.

```html
<svg viewBox="0 0 720 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Architecture">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2d6cb5"/><stop offset="100%" stop-color="#1e4d8c"/></linearGradient>
    <linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#2d9a6a"/><stop offset="100%" stop-color="#1a6b4a"/></linearGradient>
    <linearGradient id="g3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#c9a227"/><stop offset="100%" stop-color="#9a6b00"/></linearGradient>
  </defs>
  <rect x="40" y="195" width="640" height="45" rx="8" fill="#e8ecf2" stroke="#c5cdd8"/>
  <text x="360" y="224" text-anchor="middle" font-size="13" font-weight="600" fill="#5c6370">{{BASE}}</text>
  <rect x="60" y="75" width="180" height="110" rx="10" fill="url(#g1)"/>
  <text x="150" y="115" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">{{PILLAR_1}}</text>
  <rect x="270" y="75" width="180" height="110" rx="10" fill="url(#g2)"/>
  <text x="360" y="115" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">{{PILLAR_2}}</text>
  <rect x="480" y="75" width="180" height="110" rx="10" fill="url(#g3)"/>
  <text x="570" y="115" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">{{PILLAR_3}}</text>
  <polygon points="360,25 660,65 60,65" fill="none" stroke="#1e4d8c" stroke-width="2" stroke-dasharray="5,4"/>
  <text x="360" y="52" text-anchor="middle" font-size="11" font-weight="700" fill="#1e4d8c">{{APEX}}</text>
</svg>
```

---

## 3. Insight cards (key findings)

**When:** report has numbered key findings. Split in grids of 4 if >4 items.

```html
<div class="insights-grid">
  <div class="insight-card">
    <span class="num">1</span><strong>{{HEADLINE}}</strong> — {{ONE_LINE}}<span class="src">{{SOURCE}}</span>
  </div>
  <!-- repeat -->
</div>
```

---

## 4. Timeline (short / medium / long)

**When:** report distinguishes deployment horizons or maturity over time.

```html
<div class="timeline">
  <div class="timeline-phase">
    <div class="timeline-dot">NOW</div>
    <h4>{{PHASE_1_TITLE}}</h4>
    <ul><li>{{ITEM}}</li></ul>
  </div>
  <div class="timeline-phase">
    <div class="timeline-dot">2–5 ans</div>
    <h4>{{PHASE_2_TITLE}}</h4>
    <ul><li>{{ITEM}}</li></ul>
  </div>
  <div class="timeline-phase">
    <div class="timeline-dot">R&D</div>
    <h4>{{PHASE_3_TITLE}}</h4>
    <ul><li>{{ITEM}}</li></ul>
  </div>
</div>
```

---

## 5. Maturity bars

**When:** taxonomy table includes maturity column. Use **only** percentages present in report; otherwise use qualitative width (high=80%, medium=55%, low=30%) and label qualitatively.

```html
<div class="maturity-grid fig-animate">
  <div class="maturity-row">
    <span class="label">{{NAME}}</span>
    <div class="maturity-bar"><div class="maturity-fill fig-bar-fill" style="--target:{{PCT}}%; background:linear-gradient(90deg,{{PRIMARY}},{{SECONDARY}});">{{PCT}}%</div></div>
    <span class="maturity-tag">{{TAG}}</span>
  </div>
</div>
```

---

## 6. Taxonomy wheel

**When:** report defines named families (A–F, categories) around a central concept.

**Params:** center label + 4–6 satellite nodes with letter + short name. Place nodes evenly on a circle (cx=320, cy=150, r≈108).

```html
<svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Taxonomie">
  <circle cx="320" cy="150" r="48" fill="#1e4d8c"/>
  <text x="320" y="155" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">{{CENTER}}</text>
  <!-- satellite: <circle cx cy r="34" fill="COLOR"/> + letter + name -->
</svg>
```

---

## 7. Tech stack (layers)

**When:** report describes layered stack (e.g. BIM → perception → robot).

```html
<svg viewBox="0 0 560 185" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Stack technique">
  <polygon points="280,8 520,38 40,38" fill="#e8f0fa" stroke="#1e4d8c" stroke-width="1.5"/>
  <text x="280" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="#1e4d8c">{{GAP_LABEL}}</text>
  <rect x="95" y="48" width="370" height="32" rx="6" fill="#3d8fd4"/>
  <text x="280" y="68" text-anchor="middle" font-size="11" font-weight="600" fill="#fff">{{LAYER_3}}</text>
  <rect x="70" y="88" width="420" height="32" rx="6" fill="#2d6cb5"/>
  <text x="280" y="108" text-anchor="middle" font-size="11" font-weight="600" fill="#fff">{{LAYER_2}}</text>
  <rect x="45" y="128" width="470" height="38" rx="6" fill="#1e4d8c"/>
  <text x="280" y="152" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">{{LAYER_1}}</text>
</svg>
```

---

## 8. Workflow (linear process)

**When:** report describes a key process loop (e.g. robot → human → sensor → OK).

```html
<svg viewBox="0 0 560 120" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Workflow">
  <!-- boxes: rect rx="8" + label; arrows: text → or line marker-end -->
  <text x="280" y="22" text-anchor="middle" font-size="10" font-weight="600" fill="#5c6370">{{WORKFLOW_TITLE}}</text>
</svg>
```

Pattern: 4–5 boxes left-to-right, `#1e4d8c` → `#3d8fd4` → `#9a6b00` → `#1a6b4a` gradient progression.

---

## 9. Decision tree

**When:** report gives practitioner choice criteria (if X → approach Y).

```html
<svg viewBox="0 0 600 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Arbre de décision">
  <defs><marker id="arr" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#1e4d8c"/></marker></defs>
  <!-- root rect/polygon → branches → leaf rects -->
</svg>
```

Keep depth ≤3 levels. Leaf nodes = approach names from report taxonomy.

---

## 10. Contradiction cards

**When:** report has contradictions / uncertainty table.

```html
<div class="contradiction-card">
  <div class="contra-side"><strong>{{SIDE_A_LABEL}}</strong>{{POSITION_A}}</div>
  <span class="contra-vs">vs</span>
  <div class="contra-side"><strong>{{SIDE_B_LABEL}}</strong>{{POSITION_B}}</div>
  <span class="tag tag-mixed">{{ASSESSMENT}}</span>
</div>
```

Assessment tags: `Fort` / `Mixte` / `Preuve faible` — from report table only.

---

## Optional prose components (per preset)

Use when content supports it — see `design-inspiration.md`.

| Class | Preset | When |
|-------|--------|------|
| `.sidenote` | academic | Methodology note, caveat, source detail |
| `.section-kicker` | editorial | Label above `h2` section |
| `.pullquote` | editorial | One strong sentence pulled from prose |
| `.epigraph` | editorial | Quote before a section |
| `.takeaway` | warm | Learning takeaway |
| `.open-question` | warm | Unresolved question from source |
| `.spicy-callout` | creative | Bold callout / CTA emphasis |

Palette hex: `references/preset-palettes.md`

---

## 14. Stat callouts (HTML)

**When:** source has 2–4 headline numbers (sources, %, dates, counts).

See `svg-graphics.md` § Stat callout — prefer over a bare SVG rectangle.

---

## Selection checklist

Before composing, mark which diagrams apply:

```
[ ] Funnel (counts in report?)
[ ] Stat callouts (2–4 chiffres clés?)
[ ] Pillars (hybrid architecture?)
[ ] Insights (key findings?)
[ ] Timeline (horizons?)
[ ] Maturity (taxonomy + levels?)
[ ] Wheel (named families?)
[ ] Stack (layers?)
[ ] Workflow (key process?)
[ ] Decision tree (choice criteria?)
[ ] Contradictions (uncertainty section?)
[ ] Qualité svg-graphics.md (defs, connecteurs, ≤3 animées)
```

Total checked ≤ 10 figures. Lead prose first; funnel early only if research counts exist.

---

## 11. Concept map (generic)

**When:** article explains related concepts around a central idea.

```html
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Carte conceptuelle">
  <circle cx="300" cy="140" r="40" fill="#1e4d8c"/>
  <text x="300" y="145" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">{{CENTER}}</text>
  <!-- 4–6 nodes with lines to center -->
</svg>
```

---

## 12. Comparison (A vs B)

**When:** text contrasts two approaches, options, or viewpoints (not full contradiction table).

```html
<div class="contradiction-card">
  <div class="contra-side"><strong>{{LABEL_A}}</strong>{{POINT_A}}</div>
  <span class="contra-vs">vs</span>
  <div class="contra-side"><strong>{{LABEL_B}}</strong>{{POINT_B}}</div>
</div>
```

---

## 13. Numbered steps

**When:** how-to, process, or numbered list in source.

```html
<div class="visual-beat">
  <div class="approach-line"><span class="approach-letter">1</span><div><strong>{{STEP}}</strong> — {{DETAIL}}</div></div>
  <!-- repeat -->
</div>
```