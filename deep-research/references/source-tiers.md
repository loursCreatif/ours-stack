# Source tiers — deep research reference

Same tier logic as `/source-scout`. **Read depth** happens here; tiers guide *which* sources deserve full attention.

## Tier 1 — Primary (read in depth first)

| Type | Signals | Examples |
|------|---------|----------|
| Peer-reviewed paper | arXiv, DOI, journal PDF | Original experiments, formal proofs |
| Official documentation | `docs.*`, manufacturer spec | API reference, technical specs |
| Primary dataset / benchmark | Published methodology + data | Standard benchmarks with code |
| Standards / regulations | ISO, IEEE, government `.gouv` | Norms, safety requirements |

## Tier 2 — Authoritative secondary

| Type | Signals | Examples |
|------|---------|----------|
| Review / survey paper | "review", "survey", meta-analysis | IEEE/Annual Review surveys |
| Expert course notes | University `.edu`, named researcher | Lecture notes from domain experts |
| Seminal book chapter | Citable chapter + page range | Foundational textbook sections |
| Technical report | Lab TR, thesis with data | Industry/lab reports with methods |

**Use when:** one review synthesizes many Tier 1 papers — often the fastest path to depth.

## Tier 3 — Demonstration (supporting skim)

| Type | Signals | Examples |
|------|---------|----------|
| Real system demo | Named product, measurable claim | Deployment case studies |
| Open-source repo | README + architecture | Reference implementations |
| Conference talk | Technical depth, named speaker | ICRA/NeurIPS talks with results |

## Tier 4 — Bootstrap only

| Type | When OK |
|------|---------|
| Explainer article | Terminology bootstrap before Tier 1–2 |
| Wikipedia lead | Orient terms only — never sole primary |
| Listicle | **Never use as evidence** |

## Rejection patterns

| Pattern | Why skip |
|---------|----------|
| SEO tutorial farms | No mechanisms, no data |
| News without technical detail | Hype |
| AI summary aggregators | No traceability |
| Adjacent topic | Interesting but off-question |
| Broken / gated with no alternative | Wastes depth budget |

## Access labels

| Label | Meaning |
|-------|---------|
| `open access` | Full text readable |
| `paywall` | Abstract only — search arXiv/author PDF |
| `partial` | Registration required, body free |