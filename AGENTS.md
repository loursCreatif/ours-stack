# ours-stack

Install: `git clone … ~/.claude/skills/ours-stack && ./setup`

Skills live in subfolders (`bear-hours/`, etc.). Grok Build discovers them via Claude compat.

## Ethos

- **Deep over wide** — one narrow wedge, mastered
- **Dense over shallow** — Feynman extraction, open questions, no summary theater
- **Explain over consume** — every session tends toward something you can explain
- **Show your work** — notes live in `studies/<slug>/`, traceable and revisitable

## Artifact contract

Every study uses the same layout:

```
studies/<slug>/
├── brief.md        # /bear-hours
├── notes.md        # /dense-read (session trace — guided tranches + tes réponses)
├── council.md      # /council (optional)
├── dialogue/       # /dialogue (optional)
│   └── <persona>/
│       ├── persona.md
│       └── dialogue.md
├── research.md           # /deep-research (optional, when linked to study)
├── sources-index.md
├── report.html           # /layout-html (optional)
├── mind-map.json         # /mind-map (optional, editable)
├── mind-map.html         # /mind-map (optional)
├── visual-proof.spec.md  # /infographic (when run)
├── visual-proof.png      # /infographic (optional — image_gen)
├── visual-proof.alt.md   # /infographic (optional)
├── infographic-prompt.md # /infographic (optional — no image tool)
├── memory-palace.json    # /memory-palace (optional)
└── memory-palace.html    # /memory-palace (optional)
```

No `proof.md` in the default layout. A standalone proof draft file is created **only** when the user explicitly runs `/proof-draft` (future skill).

Standalone deep research (no brief required):

```
research/<slug>/
├── report.md             # /deep-research — synthesis
├── sources-index.md      # /deep-research — full screening log (150–250+ in literature-review mode)
├── report.html           # /layout-html — mise en page HTML (optional)
├── mind-map.json         # /mind-map (optional, editable)
├── mind-map.html         # /mind-map (optional)
├── visual-proof.*        # /infographic — same pattern as studies/
├── memory-palace.json    # /memory-palace (optional)
└── memory-palace.html    # /memory-palace (optional)
```

Ad-hoc outputs (pasted text or standalone, no existing study folder):

```
output/layout/<slug>/
├── article.html        # /layout-html
└── visual-proof.*      # /infographic (pasted text mode)

output/council/<slug>/
└── council.md          # /council

output/dialogue/<slug>/
├── persona.md
└── dialogue.md         # /dialogue

output/mind-map/<slug>/
├── map.json            # /mind-map
└── map.html            # /mind-map

output/dense-read/<slug>/
└── notes.md            # /dense-read (ad-hoc, no brief)
```

### Cross-session memory

```
~/.ours-stack/
├── studies-index.jsonl   # registered studies (slug, path, title, wedge, repo)
└── learnings.jsonl       # durable insights across sessions
```

Register on each `brief.md` write: `bin/ours-stack-register-study`. Backfill existing studies: `./setup` (or `bin/ours-stack-backfill-index`).

### Slug rules

- Lowercase letters, digits, hyphens only (`transformer-attention`, `gstack-overview`)
- Derive from the topic title; ask before reusing an existing slug
- One slug = one study thread; fork with suffix if scope diverges (`gstack-skills-v2`)

## Skills

| Skill | When to use |
|-------|-------------|
| `/bear-hours` | New topic, "what should I learn?", scope unclear — optional scan via `studies-index.jsonl`, 5 framing questions (entry angle → wedge); `## Source material` defaults to TBD — run /source-scout, confirm slug before reuse |
| `/source-scout` | Brief exists, `## Source material` is TBD or thin — wedge-locked search; exactly 3 sources (article + YouTube + joker), anchor + core in brief; URLs opened in browser |
| `/dense-read` | Anchor + brief — lecture guidée tranche par tranche (3–6), une question par tranche, `notes.md` = trace avec tes réponses ; « lis tout seul » = mode extraction solo ; handoff → `/mind-map` |
| `/deep-research` | Standalone — classic funnel: 150–250+ sources discovered & screened (default), 15–25 read in depth, synthesis report + `sources-index.md`. No brief required |
| `/layout-html` | Finished text → self-contained HTML (editorial typography, 3–7 inline SVG figures quoted from source) — `report.md`, notes, any `.md`/`.txt`, pasted text; opens offline; fidelity over beauty; no new research |
| `/mind-map` | Interactive mind map from brief/notes/report — `mind-map.json` (editable) + `mind-map.html` (pan/zoom, expand/collapse, source links); no new research |
| `/memory-palace` | Oblique relief map (method of loci) — click buildings, drill-down interiors, concept panel; `memory-palace.json` + `.html`; no FPS movement |
| `/infographic` | One memorable visual from existing study/research text — `image_gen` when available, else export prompt (`/visual-proof` alias) |
| `/council` | Multi-agent council for a study wedge or learning plan — dynamic panel, disagreement, synthesis, Codex fusion, `council.md` artifact |
| `/dialogue` | 1-on-1 Socratic dialogue with a historical/public figure — persona card + transcript; challenges beliefs; informed epistemic mode default (alias `/dialogue-historique`) |
| `/study-status` | Read-only dashboard — criteria checked, artifacts on disk, suggested next step per study; local `studies/` + optional `~/.ours-stack/studies-index.jsonl`; no file writes |

## Routing

- User shares a learning goal without a plan → `/bear-hours`
- User shares paper/chapter/URL without a brief → `/bear-hours` first
- Brief exists, sources missing or "TBD" → `/source-scout`
- User wants depth + summary on a topic (not framed as a study wedge) → `/deep-research` — **not** auto-chained from other skills
- User wants HTML layout / infographics on any text or after deep research → `/layout-html` — **not** auto-chained
- User wants mind map / carte mentale / hierarchical overview → `/mind-map` — **not** auto-chained; complement to `/layout-html`
- User wants spatial memory / relief map / palais cliquable (not FPS) → `/memory-palace` — **not** auto-chained
- User wants **one** shareable visual summary (poster, thread hook, slide) from notes/report/brief → `/infographic` (alias `/visual-proof`) — **not** auto-chained
- After `/infographic` in PROMPT mode, user pastes result back → re-run with attachment + `image_edit` if available
- User wants multi-agent critique, advisor panel, study strategy, plan pressure-test, or `/council` → `/council` — **not** auto-chained
- `brief.md` exists and user asks "what should I do next?" with real ambiguity → `/council` (not `/source-scout` or `/deep-research`)
- User wants sources only → `/source-scout`, not `/council`
- User wants full research answer → `/deep-research`, not `/council`
- User wants 1-on-1 dialogue with a figure (Darwin, Tesla, …), "discuter avec", belief testing in character → `/dialogue` — **not** auto-chained
- User wants multi-agent panel or study plan debate → `/council`, not `/dialogue`
- User has anchor source and wants dense extraction → `/dense-read` — **not** auto-chained
- Brief exists, sources listed, user wants to read anchor against wedge → `/dense-read` (after `/source-scout` if sources TBD)
- User has a brief and **explicitly** wants to publish → future `/proof-draft` (never auto-create `proof.md`)
- User asks where studies stand, "où j'en suis", statut, tableau de bord, or "what's next" (status view) → `/study-status` — **not** auto-chained; use `/council` when strategy debate is the goal, not a dashboard

## Privacy

Before any public proof: strip copyrighted long quotes, personal data, unreleased work. Summarize in your own words.