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
└── brief.md        # /bear-hours
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

## Routing

- User shares a learning goal without a plan → `/bear-hours`
- User shares paper/chapter/URL without a brief → `/bear-hours` first
- User has a brief and wants to publish → future `/proof-draft`

## Privacy

Before any public proof: strip copyrighted long quotes, personal data, unreleased work. Summarize in your own words.