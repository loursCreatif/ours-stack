# Palace archetypes — relief site layouts

Each theme defines a **parcel grid** of buildings (not interior corridor rooms).

## construction *(robotics, BTP, field)*

**Best for:** biomimetisme, robotique chantier, hardware.

| Building | Label pattern | Position hint |
|----------|---------------|---------------|
| Site entrance | Entrée chantier | `[0, 0, 10, 8]` |
| Terrain bay | Zone terrain | `[12, 0, 10, 8]` |
| Workshop | Atelier mécanismes | `[24, 0, 10, 8]` |
| Hangar | Hangar robots / démos | `[0, 10, 12, 8]` |
| Office trailer | Bureau croyances | `[14, 10, 10, 8]` |
| Proof trailer | Trailer preuve | `[26, 10, 8, 8]` |
| Scaffold (blocked) | Questions ouvertes | `[36, 4, 6, 6]` `blocked: true` |

**Colors:** light sand ground (`#e8dcc8`), cream buildings (`#f2e8d8`), amber roofs/pins; procedural crane on alternating buildings.

## corridor

**Best for:** linear teaching, first palace.

Buildings as **row of houses** along X: `footprint [i*12, 0, 8, 6]`.
Labels: Maison 1…N. Path = left to right.
**Colors:** warm pastel ground (`#e8e2d8`), cream facades, terracotta roofs; chimney details.

## museum

**Best for:** research synthesis, themed clusters.

Hub building at center `[16, 8, 12, 10]`; wings at corners (NE, NW, SE, SW).
Wing = synthesis theme; vitrines = zones inside.
**Colors:** cream ground (`#e8e4dc`), ivory buildings, brass roofs/pins; pediment details on facades.

## library

**Best for:** source-heavy studies.

Central reading room + shelf buildings along south row.
Hotspots = citation pins on shelf zones.
**Colors:** wood-tone ground (`#d8cfc0`), parchment buildings, dark-green roofs; book-stack details.

## custom

User describes place → map to nearest grid; store `theme_notes` in manifest.