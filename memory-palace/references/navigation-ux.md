# Navigation UX — relief map (memory-palace)

## Paradigm

**Oblique relief map** — fixed tilt (~52°), like Google Maps 3D. **Default view** is the oblique site map; **guided ground tour** (`Visite guidée`) is a separate on-rails mode at eye height (~1.6–1.8 u) — no free WASD movement. On site load, camera **distance auto-fits** all site building footprints + path sprites via `fitSiteCamera()` (~10% viewport margin on the binding edge; tilt/azimuth fixed). Ground plane matches site span (not oversized).

| Mode | When |
|------|------|
| **relief** (default) | Desktop WebGL, motion OK |
| **iso-svg** (fallback) | Mobile narrow, no WebGL, `prefers-reduced-motion`, `--2d-only` |

Both modes share: **click buildings → drill-down → panel**.

## Relief controls (desktop)

| Input | Action |
|-------|--------|
| Drag on empty ground | Pan map (site level only) |
| Wheel | Zoom map (site level only) |
| Click building | Animated zoom → interior level |
| Click zone (interior) | Open detail panel (concepts) |
| Click hotspot (pin) | Open detail panel (one concept) |
| `Retour` / breadcrumb | Animate back to site map |
| Esc | Close panel (or exit guided tour → restore oblique map) |
| `Visite guidée` | Eye-level camera glides along `path[]`, stops at each locus, shows mental scene |
| `Précédent` / `Suivant` or ←/→ | Previous / next tour stop (while in guided tour) |
| `Vue carte` | Exit guided tour → `fitSiteCamera()` oblique view |

**Removed:** WASD, pointer-lock, E-to-enter, drag-to-look, free first-person movement.

## Two levels

```
Level 0 — Site map
  Buildings along path[] as extruded footprints
  Blocked doors = gray dashed buildings (open questions)

Level 1 — Building interior
  Cutaway: other buildings hidden
  Zones = floor pads with labels
  Hotspots = small pins for precise concepts
```

## Detail panel

Right-side `<aside id="detail-panel">`:

- **Mental scene** (if `locus.scene` present): `scene.image` first, large type on tinted background; then `scene.senses` (2–3 prefixed hooks: Son —, Odeur —, …)
- Type badge (mechanism / finding / belief / …)
- Label + gloss
- Source: `file · section`
- Multiple concepts if zone has >1

If `scene` absent, panel unchanged (concepts only).

`aria-live="polite"` on panel title.

## Breadcrumb

```
Carte du site › Entrée chantier › Zone tripod
```

Click segment → jump to that navigation level.

## First-run overlay

> Clique un **bâtiment** pour entrer. À l'intérieur, clique une **zone** ou un **repère** pour voir le concept. Pas de déplacement — seulement la carte et les clics.

French if `lang === 'fr'`.

## Iso-SVG fallback

Same `path[]` and `loci[]` data:

- Isometric parallelograms for building footprints
- Click building → SVG interior layout (zones as rects)
- Same panel + breadcrumb

No separate card grid.

## Performance

- Max 12 site buildings, 4 zones + 4 hotspots per interior
- Soft shadows on relief map (DirectionalLight + PCFSoft shadow map on ground and buildings)
- Pause render loop when tab hidden
- Camera tween ~400ms (respect `prefers-reduced-motion`: instant)