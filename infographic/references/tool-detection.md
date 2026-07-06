# Tool detection — IMAGE vs PROMPT mode

## Decision tree

```
BEFORE Step 5 (generate or export):

IF user says "I'll generate myself" / "prompt only" / "pas d'image"
  → MODE = PROMPT (skip tool probe)

ELSE IF image_gen OR GenerateImage appears in this session's callable tool set
  → MODE = IMAGE

ELSE IF only image_edit available AND user attached visual-proof.png
  → MODE = IMAGE (edit path)

ELSE
  → MODE = PROMPT
```

**Do not** burn a generation on a probe image — introspect tools only.

## Tool shapes

Use whichever image generation tool is actually exposed in the current session.

**Aliases to check:** `image_gen`, `generate_image`, `create_image`, `GenerateImage`, `dalle`

## IMAGE mode — before calling

1. Apply labeled-infographic verification rules:
   - Image models garble text — limit to ≤7 labels of 1–2 words on canvas
   - If >7 precise labels or exact numeric data required → suggest `/layout-html` instead

## IMAGE mode — fidelity loop (after every generate)

Read the generated image back and check **against the spec**, in order:

| # | Check | Fail → |
|---|-------|--------|
| 1 | Text legible + correctly spelled (accents included) | retry with fewer/shorter labels |
| 2 | Label count = spec nodes (no invented extra text) | retry adding "exactly these labels, nothing more" |
| 3 | Hero element clearly dominant (~1/3 of canvas) | retry emphasizing hero size |
| 4 | Palette roughly matches preset (dominant colors) | retry restating hex values |

**Budget: 2 retries total** (not per check) — fix the worst failure first. Still failing → fallback PROMPT, tell the user which check failed.

## IMAGE mode — generation

**`prompt`-style image tools:**
- `prompt` — composed from spec (shorter than external prompt)
- `aspect_ratio` — `16:9` default; `1:1` if square/Instagram; `9:16` if story

**`description` + `filename` image tools:**
- `description` — same semantic content as the prompt
- `filename` — `visual-proof.png` in output dir

## IMAGE failure → PROMPT fallback

On timeout, policy block, or illegible text after 2 attempts:

1. Keep `visual-proof.spec.md`
2. Write `infographic-prompt.md`
3. Tell user generation failed; prompt is ready for external tools

## Edit / iterate path

When user says "iterate", "refine", "v2":

- `image_edit` with existing `visual-proof.png` as source
- Save as `visual-proof.v2.png` (or increment)
- Describe only what changes (imagine principle)

## Listing in allowed-tools

Listing `image_gen` / `GenerateImage` in skill frontmatter is **necessary but not sufficient** — confirm tool is exposed in **this** session before Step 5a.
