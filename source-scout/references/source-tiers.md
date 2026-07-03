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

**Authority signals (Accept):** named conference speaker; institutional channel (university, lab, standards body, established technical media); site/channel whose **corpus is specialized** in the wedge domain.

**Authority signals (Reject):** anonymous or unverifiable channel; channel whose main corpus is **off-wedge**; narration likely generated without citable sources.

**Use when:** wedge needs "what exists today" or maker-accessible reference. Never as sole anchor unless wedge is purely applied survey. `/source-scout` screens a **pool** of YouTube candidates (~10 on-wedge if available, **timebox 2 min / 3 WebFetch**) before picking slot 2; rejects teasers, trailers, SEO tutorials, superficial recaps. Log channel/speaker identity on every Pool V `WebFetch`. Honest **article/site Tier 1–3 fallback** if no video passes the bar — never a weak off-wedge or anonymous video.

**Swap preference (energy / GPU wedges):** third-party **measured** power (review lab, Powenetics-style) **>** vendor spec sheet **>** homelab blog for final picks when scoring for ≥9/10.

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
| YouTube teaser / trailer / hype clip | No density; wastes slot 2 |
| YouTube generalist primer | Vocabulary only; not wedge mechanism |
| Anonymous / unidentifiable author or channel | No traceability; engine caps ≤6/10 → article fallback |
| Off-domain channel corpus | Speaker identity known but content habitually outside wedge |

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