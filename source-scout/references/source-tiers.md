# Source tiers — scout reference

Use this to rank fast. **Default pick order: Tier 1 → Tier 2 → Tier 3.** Tier 4 only as bootstrap when Tiers 1–3 are inaccessible.

## Tier 1 — Primary (prefer)

| Type | Signals | Examples |
|------|---------|----------|
| Peer-reviewed paper | arXiv, DOI, journal PDF | Ritzmann et al. 2004 locomotion terrain |
| Official documentation | `docs.*`, manufacturer spec sheet | ROS package docs, API reference |
| Primary dataset / benchmark | Published methodology + data | Standard robotics benchmarks |
| Standards / regulations | ISO, IEEE, government `.gouv` | Building codes, safety norms |

**Density signal:** abstract mentions mechanisms, constraints, evaluation — not "overview of the field".

## Tier 2 — Authoritative secondary

| Type | Signals | Examples |
|------|---------|----------|
| Review / survey paper | "review", "survey", Annual Review | IEEE review of legged locomotion |
| Expert course notes | University `.edu`, named researcher | Kodlab lecture notes |
| Seminal book chapter | Citable chapter + page range | Correll — legged locomotion chapter |
| Technical report | Lab TR, thesis with data | UPenn GRASP reports |

**Use when:** no single Tier 1 covers the wedge; one review beats three primers.

## Tier 3 — Demonstration (supporting)

| Type | Signals | Examples |
|------|---------|----------|
| Real system demo | Named robot, measurable claim | RHex video on rubble |
| Open-source repo | README with architecture diagram | Arduino hexapod with gait code |
| Conference talk | Named speaker, technical depth | ICRA talk with results slide |
| YouTube (scout slot 2) | `site:youtube.com`, lecture/talk/demo on wedge | University course, ICRA recording |

**Use when:** wedge needs "what exists today" or maker-accessible reference. Never as sole anchor unless wedge is purely applied survey. `/source-scout` reserves one of exactly 3 picks for YouTube (or honest article/site fallback if none on-wedge).

## Tier 4 — Bootstrap only (rare)

| Type | Signals | When OK |
|------|---------|---------|
| Explainer article | "Introduction to", "What is" | User has zero domain vocabulary AND no Tier 1–2 accessible |
| Wikipedia | Lead section only | Orient terminology before anchor read |
| Listicle / roundup | "Top 10", "Best resources" | **Never recommend** |

Mark Tier 4 as `bootstrap only — read <15 min then switch to anchor`.

## Rejection patterns (always skip)

| Pattern | Why |
|---------|-----|
| SEO tutorial farms | Low density, no mechanisms |
| News without technical detail | Hype, no transferable insight |
| Adjacent topic | Interesting but outside `Hors scope` |
| Duplicate coverage | Second tripod-gait explainer when one suffices |
| Broken / gated with no alternative | Wastes user time |
| AI-generated summary sites | No primary traceability |

## Access labels

| Label | Meaning |
|-------|---------|
| `open access` | PDF or HTML readable without paywall |
| `paywall` | Abstract only; note if preprint exists on arXiv |
| `partial` | Registration required but body is free |

Always search for arXiv / author-hosted PDF when DOI is paywalled.

## Time estimates

| Label | Meaning |
|-------|---------|
| `~15 min` | Skim abstract + figures, or short demo video |
| `~45 min` | Dense read of one paper section or one doc chapter |
| `~90 min` | Full paper + notes-worthy |

Scout assigns estimates; actual read happens in a later skill.