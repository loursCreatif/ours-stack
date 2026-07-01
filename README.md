# ours-stack

Agent skills for autodidacts — **deep learning**, **dense papers**, **public proof**.

By [School of the Bear](https://github.com/loursCreatif).

Inspired by [gstack](https://github.com/garrytan/gstack), for learning instead of shipping code.

## Install

```bash
git clone https://github.com/loursCreatif/ours-stack.git ~/.claude/skills/ours-stack
~/.claude/skills/ours-stack/setup
```

Works in **Claude Code** and **Grok Build** (Grok reads `~/.claude/skills/` automatically).

## Use

```
/bear-hours      → frame the topic      → studies/<slug>/brief.md
/source-scout    → find sources         → updates ## Source material in brief.md
/deep-research   → research + summary   → research/<slug>/report.md (standalone)
```

`/deep-research` is **standalone** — invoke it directly on any question; no pipeline required.

Cross-project memory lives in `~/.ours-stack/studies-index.jsonl`. `./setup` backfills existing `studies/` into the index.

Examples:

```
/bear-hours I want to understand how gstack structures its skills
/source-scout robotique-assemblage-structurel
/deep-research What are the best approaches for structural assembly robots on construction sites?
```

Test v1: open `studies/robotique-assemblage-structurel/brief.md` — `## Source material` should list an anchor + core sources after scout.

Details: [AGENTS.md](AGENTS.md)

## Develop

Clone anywhere, run `./setup` — it symlinks this repo to `~/.claude/skills/ours-stack`. Edit a `*/SKILL.md`, test in your agent, commit.

Add a skill: copy a folder, write `SKILL.md`, add one line to `AGENTS.md` and this README.

## Ethos

- **Deep over wide** — one wedge at a time
- **Dense over shallow** — explain it simply or you don't know it yet
- **Proof over consumption** — publish something
- **Show your work** — everything lives in `studies/`

## License

MIT — [LICENSE](LICENSE)