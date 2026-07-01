# ours-stack

Opinionated agent skills for AI-native autodidacts — **deep learning**, **dense papers**, **public proof**.

By [School of the Bear](https://github.com/loursCreatif).

Inspired by [gstack](https://github.com/garrytan/gstack), but for learning instead of shipping code.

## Who this is for

- Autodidacts using AI agents to learn hard material (papers, textbooks, dense docs)
- People who want **proof of understanding**, not passive consumption
- Builders studying tools like gstack, ML papers, or any topic worth going deep on

## Quick start

**Requirements:** Git, an AI agent that supports skills (Grok, Claude Code, or Cursor)

```bash
git clone https://github.com/loursCreatif/ours-stack.git ~/.ours-stack
cd ~/.ours-stack
./setup --grok          # or --cursor, --claude, or combine flags
```

Then in your agent:

1. `/bear-hours` — frame what you're learning and why
2. `/dense-read` — read deeply, take structured notes, draft public proof
3. `/checkpoint-learnings` — save progress and append durable insights

### Example: learn gstack

```
/bear-hours I want to understand how gstack structures agent skills and installs across hosts
/dense-read https://github.com/garrytan/gstack — focus on skill layout and setup
/checkpoint-learnings
```

Artifacts land in `studies/gstack-overview/` (or the slug you choose).

## Skills

| Skill | Output |
|-------|--------|
| `/bear-hours` | `studies/<slug>/brief.md` |
| `/dense-read` | `studies/<slug>/notes.md` + `proof.md` |
| `/checkpoint-learnings` | `studies/<slug>/checkpoint.md` + `~/.ours-stack/learnings.jsonl` |

See [AGENTS.md](AGENTS.md) for routing rules and the full artifact contract.

## Install options

```bash
./setup              # state dirs only (~/.ours-stack/learnings.jsonl)
./setup --grok       # symlink skills to ~/.grok/skills/<skill>/
./setup --cursor     # symlink skills to ~/.cursor/skills/<skill>/
./setup --claude     # symlink repo to ~/.claude/skills/ours-stack
./setup --grok --cursor --claude   # all of the above
```

Skills also work from this repo directly when your agent reads `*/SKILL.md` paths.

## Ethos

- **Deep over wide** — one wedge at a time
- **Dense over shallow** — explain it simply or you don't know it yet
- **Proof over consumption** — publish something: thread, gist, post, repo note
- **Show your work** — `studies/` is your paper trail

## License

MIT — see [LICENSE](LICENSE).