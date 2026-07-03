# Design inspiration — rapport intégré

> Le sous-agent de recherche n’a pas pu finir (WebSearch en panne). Ce fichier consolide la recherche manuelle + avis consultatif + patterns volés dans les repos open source.

## Top 15 — classés par pertinence

| # | Source | URL | À voler | Preset(s) |
|---|--------|-----|---------|-----------|
| 1 | **Tufte CSS** | https://github.com/edwardtufte/tufte-css | Sidenotes, figures + légendes latérales, compteurs, densité typo | `academic` |
| 2 | **Pico CSS** | https://github.com/picocss/pico | Variables CSS, landmarks sémantiques, reset classless | `minimal` |
| 3 | **Water.css** | https://github.com/kognise/water.css | Zéro classe obligatoire, tokens `:root` | `minimal` |
| 4 | **Gwern.net** | https://gwern.net | Long-form dense, liens soulignés fins, notes de bas de page | `editorial`, `academic` |
| 5 | **Bear Blog** | https://github.com/HermanMartinus/bearblog | Lisibilité, minimal chrome, ton humain | `warm` |
| 6 | **Stripe Press** | https://press.stripe.com | Opener magazine, serif display, rythme large | `editorial` |
| 7 | **Neo-brutalism** | https://brutalist-web.design | Bordures épaisses, ombres dures, clash coloré contrôlé | `creative` |
| 8 | **HyperFrames / Pretext** | skill `gstack-design-html` | HTML autonome, layouts calculés, zéro deps | tous |
| 9 | **frontend-design** | skill de design frontend | Éviter AI slop, hiérarchie typo forte | tous |
| 10 | **Academic Markdown CSS** | https://github.com/sindresorhus/github-markdown-css | Tables, code blocks pro (extraits utiles) | `academic` |
| 11 | **Sakura** | https://github.com/oxalorg/sakura | Micro-framework classless, serif doux | `warm`, `editorial` |
| 12 | **MVP.css** | https://github.com/andybrewer/mvp | Article HTML minimal sans classes | `minimal` |
| 13 | **Rough Notation** | ❌ JS — hors scope | Idée : bordures « soulignées » en SVG statique | `creative` |
| 14 | **SVG Pan** | https://github.com/arp242/svg-graph | Graphes SVG purs sans D3 | `academic`, `minimal` |
| 15 | **layout-html** (ce skill) | `ours-stack/layout-html` | Alternance prose/SVG, entonnoir PRISMA | pipeline |
| 16 | **svg-graphics.md** | `references/svg-graphics.md` | Qualité figures, defs, animations CSS/SMIL sans JS | tous |

## Idées concrètes par preset (intégrées)

### `academic`
- [x] Hero rapport blanc + `metric-pill` (pas gradient marketing)
- [x] Sections numérotées `01 ·` via CSS counter
- [x] `.visual-beat` type exhibit (`border-left` accent)
- [x] **`.sidenote`** — note méthodo en marge (pattern Tufte, statique sans JS)
- [x] Légendes figures alignées gauche, non italiques

### `editorial`
- [x] Nav horizontale, article transparent
- [x] Drop cap sur `.lead`
- [x] **`.pullquote`** — citation large entre sections
- [x] **`.section-kicker`** — label uppercase au-dessus des `h2`
- [x] **`.epigraph`** — épigraphe italic avant une section (CSS prêt)

### `minimal`
- [x] Mono nav, zéro ombre, hero bandeau
- [x] `h2` uppercase mono
- [x] Liens `text-underline-offset` + `text-decoration-thickness` (Gwern/Tufte)
- [x] SVG monochrome `fill:none` prioritaire (grammaire documentée)

### `warm`
- [x] Nav numérotée, hero field-note
- [x] **`.takeaway`** — encadré apprentissage
- [x] **`.open-question`** — question ouverte en italique amber (CSS prêt)

### `creative`
- [x] Neo-brutal stickers, hero skew, figures inclinées
- [x] **`.spicy-callout`** — constat choc (fond magenta)

## Skills agent à consulter en composition

| Skill | Quand |
|-------|-------|
| `gstack-design-html` | Valider structure HTML autonome, spacing |
| `frontend-design` | Audit anti-slop avant livraison |
| `layout-html` | Ce skill — ne pas WebSearch pendant compose |

## Règles transverses

1. Un preset = personnalité **structurelle**, pas palette seule.
2. SVG : grammaire active dans `diagram-menu.md`.
3. Lisibilité d'abord — `creative` inclus.
4. Pas de JS / CDN / Google Fonts.
5. Sidenotes Tufte interactives → hors scope ; version statique `.sidenote` OK.
