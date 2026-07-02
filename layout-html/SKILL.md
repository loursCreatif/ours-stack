---
name: layout-html
description: |
  Turn one finished text — deep-research report.md, study notes.md, any .md/.txt file,
  or pasted content — into a single self-contained HTML page: editorial typography plus
  inline SVG figures built only from data already present in the text. No new research,
  no invented numbers, no external dependency; the page opens offline from file://.
  Use when the user says "layout", "mise en page", "HTML version", "rends ça lisible",
  "turn this into a page", or runs /layout-html.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
---

# Layout HTML

One text in, one `.html` file out. The page must survive three tests:

1. It opens from `file://`, network unplugged, and looks finished.
2. Every figure traces back to a sentence of the source text.
3. A reader who never sees the original loses **no claim, no caveat, no number**.

**Time budget:** one reading pass, one question, one file. No research detours.

## Hard rules

- **No new research.** The source text is the entire knowledge base. Never WebFetch, never fill a gap from memory. Missing context stays missing (see Failure modes).
- **Figures are quotations.** Every SVG visualizes data that exists in the source. A number absent from the text never appears in a figure. No numbers in the text → structure figures only (flow, timeline, hierarchy) or none. Never a decorative fake chart.
- **Self-contained or nothing.** One file: inline CSS, inline SVG, system font stack. No CDN, no webfont, no `<script src>`, no external image. The only outbound links are sources the text already cites.
- **Fidelity over beauty.** Never alter a claim, drop a caveat, soften a hedge, or reorder an argument. Abridge only with a visible `[abridged — full text in source]` marker.
- **Zero JavaScript by default.** CSS does the layout. Single exception: Magazine mode may embed ≤30 lines of vanilla JS for a collapsible TOC.
- **AskUserQuestion:** one question per call; title `Layout — {label}`.

## Step 0: Locate the text

First match wins:

| Input | Source read | Output (AGENTS.md contract) |
|-------|-------------|------------------------------|
| Study slug named or inferable | `studies/<slug>/notes.md` (default) | `studies/<slug>/report.html` |
| Research slug | `research/<slug>/report.md` | `research/<slug>/report.html` |
| Explicit file path (.md/.txt) | that file | `output/layout/<slug>/article.html` |
| Pasted text | the paste | `output/layout/<slug>/article.html` |

- Study has several layoutable texts (`notes.md`, `council.md`, `research.md`) → one `AskUserQuestion` (`Layout — Source`) listing them; never guess.
- Ad-hoc slug: derive from title, lowercase-hyphens (AGENTS.md slug rules); if `output/layout/<slug>/` exists, ask before overwriting.
- Source under ~300 words → warn: typography-only card, no figures (a figure needs material).

## Step 1: Figure ledger

One reading pass. While reading, hunt figure candidates:

| Pattern in the text | Candidate figure |
|---------------------|------------------|
| Two+ numbers compared (A vs B, before/after) | Bar pair / slope |
| Values over time | Timeline / sparkline |
| Parts of a whole | Stacked proportion bar |
| Process, pipeline, causality | Flow diagram |
| Taxonomy, options, trade-offs | Matrix or tree |
| One striking number | Stat callout |
| One striking sentence | Pull-quote card |

For **each** candidate, record in a working ledger (in conversation, not a file): the exact source sentence, its section, the figure type. Then cut hard: keep **3–7**, ranked by "would the reader remember this tomorrow?". Fewer than 2 solid candidates → the page is typography-only; say so rather than forcing weak figures.

The ledger is the traceability contract: at delivery, every figure cites its ledger line.

## Step 2: Art direction — one question

`AskUserQuestion` — title `Layout — Direction`:

- **Éditorial** *(recommended)* — calm single column (68ch), strong typographic hierarchy, figures interleaved at their reference point. For reading and rereading.
- **Magazine** — full-bleed header, standfirst, pull quotes, denser figure rhythm, collapsible TOC (the one JS exception). For sharing and skimming.
- `other`

Never ask about colors, fonts, or spacing — that is the skill's job, not the user's.

## Step 3: Design tokens

The `<style>` block starts with tokens; every later rule uses tokens only:

    :root {
      --paper: …;  --ink: …;          /* base pair, contrast ≥ 7:1 */
      --accent: …;                    /* ONE hue, chosen from content mood */
      --muted: …;                     /* captions, meta — ≥ 4.5:1 on paper */
      --step--1 … --step-3: …;        /* type scale, ratio 1.25 */
      --space: 8px;                   /* all gaps are multiples */
      --measure: 68ch;
    }
    @media (prefers-color-scheme: dark) { /* swap paper/ink, re-check accent */ }

- One accent hue. Two is a design failure.
- Fonts: system stack only (`ui-serif` headings / `ui-sans-serif` body, or the inverse per mood). No downloads.
- Accent choice comes from the content (biology → green family, hardware → steel blue…) — decide once, state it in the delivery note.

## Step 4: Page skeleton

Semantic HTML5, in order:

1. `<header>` — `<h1>` (source title), standfirst (the source's own one-line thesis — quoted, not invented), meta line (source path, date, "layout only — no new research").
2. `<nav>` TOC — only if the source has >4 `##` sections; anchor links; collapsible in Magazine mode.
3. `<main>` — sections mirror the source structure 1:1 (same order, same hierarchy). Body text in the `--measure` column, `line-height: 1.6`.
4. Each figure: `<figure>` + `<figcaption>`, placed at the point where the source discusses it — never grouped in an annex.
5. `<footer>` — provenance: source file, generation date, `/layout-html` mention, and the source's own bibliography/links if present.

## Step 5: SVG recipes

Every figure obeys:

- `viewBox` set, `width: 100%`, no fixed pixel height in the HTML.
- `role="img"` + `<title>` + `<desc>` (the desc is the ledger sentence).
- Text inside the SVG ≥ 12px at base scale; colors from tokens only (`currentColor`, `var(--accent)`).
- `<figcaption>` = one factual line + `(§ section name)` for traceability.
- Geometry hand-coded — no chart library, no generator.

| Recipe | Geometry |
|--------|----------|
| Bar pair | 2–5 horizontal bars, labels left, values right |
| Timeline | horizontal axis, dated ticks, one-line labels alternating above/below |
| Flow | boxes + arrows, left→right, max 6 nodes; wrap to two rows beyond |
| Proportion | one stacked horizontal bar, ≤5 segments, direct labels (no legend) |
| Stat callout | the number at `--step-3`, unit small, source sentence underneath |
| Pull quote | the sentence at `--step-1` italic, thick `--accent` left border |
| Matrix | 2×2 grid, axis labels on the edges, ≤2 words per cell |

## Step 6: Self-check (before Write)

Run against the finished HTML string — fix, never ship warnings:

- [ ] `<script` count → 0 (Éditorial) or exactly 1 inline TOC block (Magazine)
- [ ] `http` matches only inside the sources/footer section
- [ ] every `<svg` has `viewBox`, `<title>`, `<desc>`
- [ ] every number appearing in a figure re-greps in the source text
- [ ] every source caveat/hedge sentence is present in the page
- [ ] `[abridged]` markers everywhere content was cut
- [ ] single `<h1>`; heading levels never skip
- [ ] file ≤ 200 KB

## Step 7: Deliver

1. `Write` the file to the Step 0 contract path.
2. In chat, ≤6 lines, no theater:
   - the path + "double-clique le fichier pour l'ouvrir"
   - figures shipped: `N figures — bar pair (§2), timeline (§3), …`
   - what was abridged, or "rien coupé"
   - accent hue chosen and why (3 words)

## Failure modes

| Situation | Response |
|-----------|----------|
| No layoutable text found | Say so; route: `/dense-read` (study) or `/deep-research` (standalone) |
| Text < 300 words | Typography-only card; note "trop court pour des figures" |
| User asks to add context/research mid-layout | Refuse; finish the layout, suggest `/deep-research` then re-run |
| Output path exists | Ask before overwrite; offer a `-v2` slug |
| Source has zero structure (wall of text) | Derive sections from paragraph topics; mark `[structure added by layout]` in the footer |

## What this skill never does

- Research, fact-fill, or "improve" claims
- Decorative charts with invented data
- Multi-file output, external assets, JS frameworks
- Summary theater in the delivery message
