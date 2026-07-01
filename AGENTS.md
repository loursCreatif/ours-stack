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
├── notes.md        # /dense-read
├── proof.md        # /dense-read (final section)
└── checkpoint.md   # /checkpoint-learnings
```

Cross-session memory: `~/.ours-stack/learnings.jsonl`

### Slug rules

- Lowercase letters, digits, hyphens only (`transformer-attention`, `gstack-overview`)
- Derive from the topic title; ask before reusing an existing slug
- One slug = one study thread; fork with suffix if scope diverges (`gstack-skills-v2`)

## Skills

| Skill | When to use |
|-------|-------------|
| `/bear-hours` | New topic, "what should I learn?", scope unclear — optional bounded local scan, 7 framing questions (incl. source material), confirm slug before reuse |
| `/dense-read` | Paper, chapter, dense doc, URL, PDF, or pasted text |
| `/checkpoint-learnings` | End of session, pause, resume, "where was I?" |

## Routing

- User shares a learning goal without a plan → `/bear-hours`
- User shares paper/chapter/URL/dense material → `/dense-read` (create `brief.md` first if missing)
- User says pause, resume, checkpoint, "what did I retain?" → `/checkpoint-learnings`
- User wants public proof only → `/dense-read` (focus on `proof.md` section)

## Privacy

Before any public proof: strip copyrighted long quotes, personal data, unreleased work. Summarize in your own words. `proof.md` is a draft — user publishes manually.

## Quick loop

```
/bear-hours → /dense-read → /checkpoint-learnings
```

Repeat until `proof.md` is ready to publish.