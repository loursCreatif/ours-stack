# Privacy strip — before spec finalization

Apply **before** writing `visual-proof.spec.md`. Aligns with AGENTS.md § Privacy.

## Strip from on-image text

- Long copyrighted quotes (paraphrase to ≤5 words max on canvas)
- Full paper titles — shorten to topic label
- Abstract verbatim
- Author names as hero text (cite in `visual-proof.alt.md` only if needed)
- Personal emails, phone numbers, addresses
- Unreleased employer or client names
- Internal project codenames unless user explicitly requests

## Visual content rules

- **No trademark logos** — use generic icons (gear, box, arrow)
- **No exact reproduction** of published figures ("Figure 3 from Smith 2019") — recreate the *idea* with new abstract layout
- **No photorealistic faces** unless user supplies reference and `image_edit` is appropriate
- **Principles only** when source is paywalled PDF notes — do not paste proprietary diagrams

## Numbers and claims

- Only numbers **verbatim** in source appear on the visual
- If source has conflicting numbers → omit numbers; use qualitative labels
- Never invent statistics, citations, or "studies show" claims

## Language

- On-image text matches source language (`lang` field in spec)
- Prompt instructions in same language as source

## Public proof reminder

Before sharing the visual publicly: strip copyrighted long quotes, personal data, unreleased work. Summarize in your own words.