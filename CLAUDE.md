# ours-stack runtime notes

This file exists for runtimes that read `CLAUDE.md`. The portable source of truth is `AGENTS.md` plus each `*/SKILL.md`.

## Operating principles

- Follow the requested skill directly when the user invokes one.
- Prefer the capability exposed by the current runtime over a named agent or provider.
- Ask only when the missing answer changes the next action; otherwise make a conservative assumption and proceed.
- Keep edits scoped, preserve the artifact contract, and verify with the repo's available scripts/tests when relevant.
- For large work, use any available sub-agent, task, or browser capability when it improves quality, but never require a specific product.
