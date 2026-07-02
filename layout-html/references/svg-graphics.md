# SVG graphics — qualité & animations

Référence obligatoire pour toute figure du skill. Complète `diagram-menu.md` (quoi dessiner) avec **comment** le dessiner bien.

**Contraintes inchangées :** HTML autonome · CSS inline · zéro CDN · zéro JS.

---

## Barre de qualité (non négociable)

Chaque figure doit passer ces 8 critères avant livraison :

| # | Critère | Mauvais | Bon |
|---|---------|---------|-----|
| 1 | **IDs uniques** | `id="g1"` réutilisé Fig.2–10 | `id="fig3-grad-a"` par figure |
| 2 | **Padding viewBox** | Éléments collés aux bords | 24–40px de marge interne |
| 3 | **Hiérarchie** | Tout même taille/poids | 3 niveaux : titre 13–15px bold · label 11–12px · note 9–10px muted |
| 4 | **Connecteurs** | Flèches `→` en texte seul | `<line>` + `<marker>` ou `<path>` avec `marker-end` |
| 5 | **Palette preset** | Bleu academic codé en dur | Hex de `preset-palettes.md` pour le preset actif |
| 6 | **Accessibilité** | SVG nu | `role="img"` + `aria-label` descriptif + `.caption` |
| 7 | **Lisibilité mobile** | viewBox 1200×800 illisible | `max-width:100%` · viewBox compact · texte ≥9px |
| 8 | **Motion safe** | Animation infinie agressive | Entrée unique · `prefers-reduced-motion` respecté |

**Anti-patterns à éviter :** rectangles génériques empilés · dégradés arc-en-ciel sans sens · texte sur fond de même luminosité · diagrammes « wireframe » vides (workflow avec un seul `<text>`).

---

## Boîte à outils SVG — copier dans chaque figure

Préfixer tous les IDs avec `fig{N}-` (N = numéro de figure). Adapter les hex au preset actif.

```html
<svg viewBox="0 0 640 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{{DESCRIPTION}}" class="fig-svg">
  <defs>
    <!-- Gradients -->
    <linearGradient id="fig1-grad-primary" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{{SECONDARY}}"/>
      <stop offset="100%" stop-color="{{PRIMARY}}"/>
    </linearGradient>
    <linearGradient id="fig1-grad-success" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{{SUCCESS}}"/>
      <stop offset="100%" stop-color="{{SUCCESS}}" stop-opacity="0.7"/>
    </linearGradient>
    <!-- Arrow marker -->
    <marker id="fig1-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="{{PRIMARY}}"/>
    </marker>
    <!-- Soft shadow (academic, warm, creative — skip minimal) -->
    <filter id="fig1-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="{{PRIMARY}}" flood-opacity="0.12"/>
    </filter>
    <!-- Subtle grid (optional, academic/minimal) -->
    <pattern id="fig1-grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="{{MUTED}}" stroke-width="0.5" opacity="0.25"/>
    </pattern>
  </defs>
  <!-- <rect width="100%" height="100%" fill="url(#fig1-grid)"/> optional background -->
  <!-- content -->
</svg>
```

### Grammaire visuelle par preset

| Preset | Fills | Strokes | Radius | Shadow | Font |
|--------|-------|---------|--------|--------|------|
| `academic` | gradients légers + surface | 1.5px | 6–10 | `feDropShadow` léger | system-ui |
| `editorial` | flat cream/surface | 1px | 4–6 | none | Georgia labels optionnel |
| `minimal` | white/none | 1px mono | 0–4 | none | ui-monospace |
| `warm` | earthy soft | 1.5–2px | 10–14 | shadow doux | system-ui |
| `creative` | saturé, 2–3 couleurs max | 2–2.5px | 0–8 | offset ou glow | bold 700+ |

---

## Patterns graphiques améliorés

### Node + connector (base réutilisable)

```html
<!-- Node -->
<g class="fig-node" filter="url(#fig1-shadow)">
  <rect x="40" y="80" width="140" height="56" rx="8" fill="url(#fig1-grad-primary)"/>
  <text x="110" y="112" text-anchor="middle" font-size="12" font-weight="600" fill="#fff">{{LABEL}}</text>
</g>
<!-- Connector -->
<line x1="180" y1="108" x2="240" y2="108" stroke="{{PRIMARY}}" stroke-width="1.5" marker-end="url(#fig1-arrow)"/>
```

### Funnel PRISMA animé (research)

Ajouter classes pour l'animation d'entrée en cascade :

```html
<div class="visual-beat fig-animate">
  <svg viewBox="0 0 480 220" ...>
    <polygon class="fig-layer fig-layer-1" points="..." fill="{{SURFACE}}" stroke="{{SECONDARY}}" stroke-width="1.5"/>
    <polygon class="fig-layer fig-layer-2" points="..." .../>
    <polygon class="fig-layer fig-layer-3" points="..." .../>
  </svg>
</div>
```

### Maturity bars animées

```html
<div class="maturity-bar">
  <div class="maturity-fill fig-bar-fill" style="--target:85%; background:linear-gradient(90deg,{{SUCCESS}},{{SECONDARY}});">85%</div>
</div>
```

La largeur finale reste en inline `style` ou attribut ; l'animation part de `0%` (voir CSS ci-dessous).

### Stat callout (HTML, pas SVG)

Pour chiffres clés du source — plus impactant qu'un rectangle SVG :

```html
<div class="stat-row">
  <div class="stat-card"><span class="stat-num">179</span><span class="stat-label">sources découvertes</span></div>
  <div class="stat-card"><span class="stat-num">20</span><span class="stat-label">lectures approfondies</span></div>
</div>
```

CSS minimal à inclure dans le preset :

```css
.stat-row { display:flex; flex-wrap:wrap; gap:.75rem; }
.stat-card { flex:1; min-width:120px; padding:1rem; background:var(--accent-light); border-radius:var(--radius,8px); text-align:center; }
.stat-num { display:block; font-size:2rem; font-weight:700; color:var(--accent); line-height:1.1; }
.stat-label { font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
```

### Pillars avec liens visuels

Ne pas laisser les piliers flotter — traits pointillés vers la base + apex :

```html
<line x1="150" y1="185" x2="360" y2="240" stroke="{{MUTED}}" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
```

### Workflow — 4+ nœuds minimum

Chaque workflow doit avoir : titre, ≥4 boîtes, flèches, légende de flux. Couleurs = progression sémantique (primary → success).

### Decision tree — feuilles colorées par issue

- Racine : `{{PRIMARY}}`
- Branches : `{{SECONDARY}}`
- Feuilles positives : `{{SUCCESS}}` · neutres : `{{WARNING}}` · incertaines : `{{MUTED}}`

### Concept map / taxonomy wheel

Satellites reliés au centre par `<line>` (pas seulement proximité visuelle). Animation optionnelle : pulse léger sur le nœud central (SVG `<animate attributeName="r" ...>`).

---

## Système d'animation (sans JavaScript)

### Quand animer

| Oui | Non |
|-----|-----|
| Entrée à l'affichage (fade, slide, draw) | Boucles infinies distrayantes |
| Barres de maturité qui se remplissent | Parallax scroll (nécessite JS) |
| Flux funnel couche par couche | Hover-only critique pour comprendre |
| Pulse subtil sur 1 nœud central | Animation sur tout le texte |

**Budget :** max **3 figures animées** par article · durée 0.4–0.9s · easing `cubic-bezier(0.22, 1, 0.36, 1)`.

### CSS — bloc à coller dans `<style>` de chaque output

```css
/* ── Figure animations ── */
.fig-animate .fig-layer {
  opacity: 0;
  transform: translateY(12px);
  animation: fig-enter 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.fig-animate .fig-layer-1 { animation-delay: 0.05s; }
.fig-animate .fig-layer-2 { animation-delay: 0.15s; }
.fig-animate .fig-layer-3 { animation-delay: 0.25s; }
.fig-animate .fig-layer-4 { animation-delay: 0.35s; }

@keyframes fig-enter {
  to { opacity: 1; transform: translateY(0); }
}

.fig-bar-fill {
  width: 0 !important;
  animation: bar-grow 1s cubic-bezier(0.22, 1, 0.36, 1) 0.3s forwards;
}
@keyframes bar-grow {
  to { width: var(--target, 50%); }
}

.fig-draw {
  stroke-dasharray: 400;
  stroke-dashoffset: 400;
  animation: fig-draw 1.2s cubic-bezier(0.22, 1, 0.36, 1) 0.2s forwards;
}
@keyframes fig-draw {
  to { stroke-dashoffset: 0; }
}

.visual-beat.fig-animate {
  animation: beat-in 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes beat-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.insight-card.fig-stagger {
  opacity: 0;
  animation: fig-enter 0.45s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.insights-grid .insight-card:nth-child(1) { animation-delay: 0.05s; }
.insights-grid .insight-card:nth-child(2) { animation-delay: 0.12s; }
.insights-grid .insight-card:nth-child(3) { animation-delay: 0.19s; }
.insights-grid .insight-card:nth-child(4) { animation-delay: 0.26s; }

.timeline-phase.fig-stagger {
  opacity: 0;
  animation: fig-enter 0.5s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.timeline-phase:nth-child(1) { animation-delay: 0.1s; }
.timeline-phase:nth-child(2) { animation-delay: 0.25s; }
.timeline-phase:nth-child(3) { animation-delay: 0.4s; }

/* Respect prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .fig-animate .fig-layer,
  .fig-bar-fill,
  .fig-draw,
  .visual-beat.fig-animate,
  .insight-card.fig-stagger,
  .timeline-phase.fig-stagger {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
    stroke-dashoffset: 0 !important;
    width: var(--target, inherit) !important;
  }
}
```

### SVG SMIL — pulse nœud central (optionnel)

```html
<circle cx="320" cy="150" r="40" fill="{{PRIMARY}}">
  <animate attributeName="r" values="40;42;40" dur="3s" repeatCount="indefinite"/>
</circle>
```

Désactiver en reduced-motion via classe : ne pas appliquer `<animate>` si l'agent peut ajouter `class="fig-static"` — ou préférer CSS-only pour simplicité.

### Classes à utiliser

| Classe | Où | Effet |
|--------|-----|-------|
| `.fig-animate` | `.visual-beat` | fade-in conteneur + layers enfants |
| `.fig-layer-1…4` | éléments SVG funnel/pillars | cascade entrée |
| `.fig-bar-fill` + `--target` | `.maturity-fill` | barre qui grandit |
| `.fig-draw` | `<path>` contour | trait qui se dessine |
| `.fig-stagger` | `.insight-card`, `.timeline-phase` | apparition décalée |

---

## Checklist avant écriture HTML

```
[ ] Chaque SVG a son bloc <defs> (gradients, markers, filter si preset)
[ ] IDs préfixés fig{N}-
[ ] Couleurs = preset-palettes.md (pas de bleu par défaut)
[ ] Connecteurs explicites (lines/paths + markers)
[ ] aria-label + caption Fig. N
[ ] Au moins 1 figure « riche » (pas wireframe) parmi les 3 premières visuals
[ ] Animations : ≤3 figures · reduced-motion OK
[ ] Bloc CSS animations inclus si .fig-animate utilisé
```

---

## Liens

- Types de diagrammes : `diagram-menu.md`
- Hex par preset : `preset-palettes.md`
- Inspiration : `design-inspiration.md` § SVG Pan, Tufte figures