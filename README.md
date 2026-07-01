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
/bear-hours          → frame the topic      → studies/<slug>/brief.md
/dense-read          → read deeply          → notes.md + proof.md
/checkpoint-learnings → save & remember     → checkpoint.md + ~/.ours-stack/learnings.jsonl
```

Example:

```
/bear-hours I want to understand how gstack structures its skills
/dense-read https://github.com/garrytan/gstack
/checkpoint-learnings
```

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