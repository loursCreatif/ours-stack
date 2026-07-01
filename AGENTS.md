# ours-stack

Install: `git clone … ~/.claude/skills/ours-stack && ./setup`

Skills live in subfolders (`bear-hours/`, etc.). Grok Build discovers them via Claude compat.

## Ethos

- **Deep over wide** — one narrow wedge, mastered
- **Dense over shallow** — Feynman extraction, open questions, no summary theater
- **Proof over consumption** — every session tends toward a publishable artifact
- **Show your work** — notes live in `studies/<slug>/`, traceable and revisitable

## Artifact contract

Every study uses the same layout:

```
studies/<slug>/
├── brief.md        # /bear-hours
└── research.md     # /deep-research (optional, when linked to study)
```

Standalone deep research (no brief required):

```
research/<slug>/
└── report.md       # /deep-research
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
| `/bear-hours` | New topic, "what should I learn?", scope unclear — optional scan via `studies-index.jsonl`, 7 framing questions (incl. source material), confirm slug before reuse |
| `/source-scout` | Brief exists, `## Source material` is TBD or thin — wedge-locked parallel search, ranked anchor + core list written to brief |
| `/deep-research` | Standalone — any research question; finds best sources, reads them, writes synthesis report. No brief required. Optional link to `studies/<slug>/` |

## Routing

- User shares a learning goal without a plan → `/bear-hours`
- User shares paper/chapter/URL without a brief → `/bear-hours` first
- Brief exists, sources missing or "TBD" → `/source-scout`
- User wants depth + summary on a topic (not framed as a study wedge) → `/deep-research` — **not** auto-chained from other skills
- User has anchor source and wants dense extraction → future `/dense-read`
- User has a brief and wants to publish → future `/proof-draft`

## Privacy

Before any public proof: strip copyrighted long quotes, personal data, unreleased work. Summarize in your own words.