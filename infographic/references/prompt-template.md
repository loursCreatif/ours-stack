# Prompt template — PROMPT mode

Fill from `visual-proof.spec.md` and write to `{output_dir}/infographic-prompt.md`.

Also print the **Universal** block in chat for immediate copy-paste.

---

## File structure

```markdown
# Infographic prompt — {{SLUG}}

**Visual type:** {{TYPE}} · **Preset:** {{PRESET}} · **Source:** {{SOURCE_PATH}}
**Aspect:** {{ASPECT}} · **Lang:** {{LANG}}

---

## Universal (paste anywhere)

{{UNIVERSAL_BODY}}

---

## Midjourney

{{MIDJOURNEY_BODY}}

---

## DALL·E / GPT Image

{{DALLE_BODY}}

---

## Flux / Stable Diffusion

**Positive:**
{{FLUX_POSITIVE}}

**Negative:**
photo, realistic human face, illegible text, busy texture, watermark, logo, meme style, 3D render, gore, NSFW, blurry text, cluttered background
```

---

## Universal body template

```
Create a single professional infographic, {{ASPECT}}, no photorealistic clutter.

**Scene:** {{VISUAL_METAPHOR}} — this concrete scene IS the composition; do not replace it with generic boxes and arrows.

**Hero element:** {{HERO}} — render it huge, ~1/3 of the canvas; everything else smaller and supporting.

**Title (exact text):** "{{TITLE}}"
**Thesis:** {{THESIS}}

**Layout skeleton:** {{TYPE_LAYOUT_INSTRUCTION}} — merged into the scene above.

**Labels (exact text, 1–2 words each, legible sans-serif, spell correctly):**
1. {{NODE_1}}
2. {{NODE_2}}
…

**Legend:**
- {{LEGEND_1}}
- {{LEGEND_2}}

**Palette:** primary {{PRIMARY}}, secondary {{SECONDARY}}, accent {{ACCENT}}, surface {{SURFACE}}, muted {{MUTED}}

**Style:** {{PRESET_STYLE_PHRASE}} — flat vector, crisp edges, generous whitespace, educational poster.

**Constraints:**
- All text spelled correctly, accents included; high contrast; no watermark; no stock photo faces.
- Exactly the labels listed above — do not invent extra text.
- No copyrighted logos or exact reproduction of published figures.
- Maximum 7 text labels on canvas.
- Language on canvas: {{LANG}}.

**Negative:** blurry text, cluttered background, 3D render, meme style, illegible typography, uniform same-size elements
```

---

## Midjourney body

Condense Universal to 2–4 sentences, then append:

```
--ar {{AR_NUM}} --style raw --v 6
```

| Aspect | --ar |
|--------|------|
| 16:9 | 16:9 |
| 1:1 | 1:1 |
| 9:16 | 9:16 |

---

## DALL·E body

Universal body + append:

```
Use a clean vector infographic style suitable for a technical blog. Ensure all text is legible and correctly spelled.
```

---

## Flux positive

Condensed Universal (subject → layout → palette → style phrase). One coherent scene.

---

## IMAGE mode prompt (shorter)

For `image_gen` / `GenerateImage` — front-load subject, 2–5 sentences:

```
{{PRESET_STYLE_PHRASE}} infographic, {{ASPECT}}.

Scene: {{VISUAL_METAPHOR}}.
Hero element: {{HERO}}, rendered huge (~1/3 of canvas); everything else small.
Title text: "{{TITLE}}".
Layout skeleton: {{TYPE_LAYOUT_INSTRUCTION}}.
Labels (exact text, nothing more): {{NODE_1}}, {{NODE_2}}, {{NODE_3}}.
Colors: {{PRIMARY}}, {{SECONDARY}}, {{ACCENT}} on {{SURFACE}} background.
Flat vector, crisp edges, educational poster, high contrast, legible sans-serif text, correct spelling with accents.
No photorealistic faces, no watermarks, no logos, no invented extra labels.
```