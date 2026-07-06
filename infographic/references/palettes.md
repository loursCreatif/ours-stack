# Palettes — reuse layout-html presets

Do **not** duplicate preset definitions. Load from layout-html:

```
../layout-html/references/presets/{{PRESET_ID}}.md
```

Or from repo root when workspace is ours-stack:

```
layout-html/references/presets/{{PRESET_ID}}.md
```

## Index

| id | label | SVG palette (hex) |
|----|-------|-------------------|
| `academic` | Academic Blue | `#1e4d8c` `#2d6cb5` `#4a90d9` `#e8f0fa` `#6b7c93` `#f5f8fc` |
| `minimal` | Minimal Mono | `#111` `#444` `#888` `#f5f5f5` `#ccc` `#fff` |
| `warm` | Warm Bear *(default)* | `#8b5a2b` `#c49a6c` `#3d5c3a` `#b45309` `#6b5c4a` `#f0e6d6` |
| `creative` | Creative Spicy | `#e11d48` `#7c3aed` `#f59e0b` `#06b6d4` `#1e1b4b` `#fef3c7` |

## Style phrases for image prompts

| Preset | Phrase |
|--------|--------|
| `academic` | research poster, navy blue professional, clean sans-serif |
| `minimal` | technical diagram, monochrome, Swiss grid, sparse |
| `warm` | earthy amber and forest green, School of the Bear maker aesthetic |
| `creative` | bold saturated colors, playful but readable, high contrast |

## Smart-skip (infographic default differs from layout-html)

Skip style question if user message contains preset id or French aliases (see `layout-html/references/style-presets.md` § Smart-skip).

**Default when skipped:** `warm` (not `academic`).

**French aliases for warm:** `chaleureux`, `bear`, `warm`