# ours-stack

Agent skills for autodidacts — **deep learning**, **dense papers**, **public proof**.

By [School of the Bear](https://github.com/loursCreatif).

Inspired by [gstack](https://github.com/garrytan/gstack), for learning instead of shipping code.

## Install

```bash
git clone https://github.com/loursCreatif/ours-stack.git ~/.claude/skills/ours-stack
~/.claude/skills/ours-stack/setup
```

Works in **Claude Code** and **Grok Build**. Run `./setup` once — it links skills to `~/.grok/skills/` (required for `/source-scout` in Grok).

**Grok workspace:** open this repo (or any repo with `studies/`), not `/`. If `/source-scout` spins on Glob with 0 matches, run `./setup` and restart the session.

## Use

```
/bear-hours         → frame the topic      → studies/<slug>/brief.md
/source-scout       → find sources         → updates ## Source material in brief.md
/dense-read         → read anchor source   → studies/<slug>/notes.md
/deep-research      → research + summary   → research/<slug>/report.md (standalone)
/layout-html        → page HTML autonome   → report.html / article.html (typo + SVG fidèles)
/mind-map           → carte mentale        → mind-map.json + mind-map.html
/memory-palace      → carte relief oblique  → studies/<slug>/memory-palace.html
/infographic        → visuel mémorable     → visual-proof.png or infographic-prompt.md
/council            → advisory panel       → studies/<slug>/council.md
/dialogue → talk with a figure  → studies/<slug>/dialogue/<persona>/
/study-status      → study dashboard      → chat only (read-only)
```

`/deep-research` is **standalone** — invoke it directly on any question; no pipeline required.
`/layout-html` turns **finished text** into one self-contained HTML page — editorial typography, SVG figures built only from source data; opens offline (`file://`). No new research.
`/infographic` (alias `/visual-proof`) turns study notes or reports into **one** poster-style visual — generates PNG when an image model is connected, otherwise exports a paste-ready prompt for Midjourney, DALL·E, or Flux.
`/dialogue` is **standalone** — 1-on-1 Socratic dialogue; use `/council` for multi-agent panels. Alias: `/dialogue-historique`.
`/study-status` is **read-only** — criteria, artifacts, and suggested next step per study; no file output.

Cross-project memory lives in `~/.ours-stack/studies-index.jsonl`. `./setup` backfills existing `studies/` into the index.

Examples:

```
/bear-hours I want to understand how gstack structures its skills
/source-scout robotique-assemblage-structurel
/dense-read biomimetisme-locomotion-chantier
/deep-research What are the best approaches for structural assembly robots on construction sites?
/layout-html robots-assemblage-structurel-chantier
/layout-html studies/biomimetisme-locomotion-chantier/notes.md
/mind-map biomimetisme-locomotion-chantier
/mind-map regenerate studies/biomimetisme-locomotion-chantier/mind-map.json
/memory-palace biomimetisme-locomotion-chantier
/memory-palace research/robots-assemblage-structurel-chantier theme construction
/infographic biomimetisme-locomotion-chantier
/council robotique-assemblage-structurel
/council critique this plan: <paste>
/dialogue discuter de l'évolution avec Darwin
/dialogue robotique-assemblage-structurel
/study-status
/study-status robotique-assemblage-structurel
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