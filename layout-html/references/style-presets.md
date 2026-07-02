# Style presets — layout-html

Apply **one** preset profile. Each preset = full design system (shell, hero, nav, prose, figures, SVG grammar).

**Load:** `references/presets/{{PRESET_ID}}.md` — paste full CSS from validation HTML or profile spec.

**Custom:** user-described style → map to `:root` + typography; document in `<!-- style: custom — … -->`

---

## Index

| id | label | Profile |
|----|-------|---------|
| `academic` | Academic Blue — rapport recherche *(défaut)* | [presets/academic.md](presets/academic.md) |
| `editorial` | Editorial Ink — magazine, serif, crème & encre | [presets/editorial.md](presets/editorial.md) |
| `minimal` | Minimal Mono — technique, neutre, épuré | [presets/minimal.md](presets/minimal.md) |
| `warm` | Warm Bear — earthy, amber & vert | [presets/warm.md](presets/warm.md) |
| `creative` | Creative Spicy — coloré, original, un peu WTF | [presets/creative.md](presets/creative.md) |
| `custom` | User-defined | § Custom below |

Validation HTML (same source, 5 looks): `research/robots-assemblage-structurel-chantier/report-{preset}.html`

---

## Smart-skip

Skip the style question if the user's message already contains:

- preset id: `academic`, `editorial`, `minimal`, `warm`, `creative`
- French aliases: `académique`, `éditorial`, `minimal`, `chaleureux`, `bear`, `créatif`, `spicy`, `wtf`, `pop`, `coloré`, `original`
- explicit style description ≥5 words (treat as `custom`, no question)
- "default" / "comme d'habitude" → `academic`

---

## 5. `custom` — User-defined

When user picks **Custom** or describes a style in their message:

1. Parse: mood (serious/playful/dark), primary color, background feel, font (serif/sans/mono)
2. Build `:root` — define all variables from `academic` profile
3. System font stacks only (no CDN)
4. Pick closest preset shell as starting point, then override tokens
5. If vague → one follow-up: "Couleur dominante et ambiance ?"

Document: `<!-- style: custom — {one-line summary} -->`

| User says | Map to |
|-----------|--------|
| "sombre, tech, cyan" | dark bg, `--accent: #22d3ee`, sans |
| "médical, blanc, bleu clair" | `--bg: #f0f9ff`, `--accent: #0284c7` |
| "brutaliste, noir et jaune" | `--radius: 0`, `--shadow: 4px 4px 0`, creative-like shell |