# Loci mapping — relief map

Map concepts to **buildings** on an oblique site map. Method of loci = fixed path across buildings.

## Site level (`level: site`)

| Building role | Content | Interior |
|---------------|---------|----------|
| Entrée / foyer | Wedge + why now | 2 zones |
| Terrain / zone A | Core mechanism #1 | 1 zone + 0–1 hotspot |
| Atelier / zone B | Core mechanism #2 | 2 zones |
| Hangar / preuve terrain | Examples (robots, demos) | 1 zone per example |
| Bureau | Beliefs + questions to test | 2 zones |
| Trailer / fin | Success criteria + proof | 2 zones |
| Grisé (`blocked`) | Open questions | no interior — panel on click |

## Interior level

Per building, `interior`:

```json
{
  "zones": [{ "id", "label", "footprint": [x, z, w, d], "concepts": ["c-id"] }],
  "hotspots": [{ "id", "label", "concept": "c-id", "at": [x, y, z] }]
}
```

- **Zones** — floor pads (click → panel with all zone concepts)
- **Hotspots** — pins for one precise concept (compliance, statistic, named robot)
- Footprints relative to building origin (0,0 = corner of building footprint)

## Path order

`path[]` = building ids in **teaching order** (not file order):

1. Problem / wedge
2. Core mechanisms
3. Examples
4. Beliefs
5. Success / proof
6. Blocked = open questions (optional, end)

## Footprint grid (construction theme)

```
[row 0] entree(0,0)   terrain(12,0)   mecanismes(24,0)
[row 1] robots(0,10)  croyances(14,10) preuve(26,10)
[blocked] questions(36,4) — smaller, dashed
```

Spacing: ~10–12 units between building origins. See `palace-archetypes.md` per theme.

## Caps

- 5–12 site buildings on `path[]`
- ≤4 zones + ≤4 hotspots per interior
- 1–3 concepts per zone max