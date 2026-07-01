# Extreme mode — 20 sub-agent discovery

**Target:** ~2 000 unique candidates discovered, screened, top 40–60 read in depth.

**Cost honesty:** this mode is designed for maximum coverage within a single session. Tell the user upfront:
- **Tokens:** high — often **500k–2M+** depending on tool results and screening volume
- **Time:** **1–3 hours** wall-clock (20 parallel discovery agents + batched screening)
- **Not guaranteed:** search APIs and rate limits may cap discovery below 2k — report actual counts

## File layout

```
research/<slug>/
├── discovery/
│   ├── shard-01.md … shard-20.md   # raw per-agent logs
│   └── merge-log.md                # dedup stats
├── screening/
│   └── batch-01.md … batch-10.md   # optional parallel screen shards
├── sources-index.md                # merged canonical index
└── report.md
```

## Orchestrator workflow

### 1. Partition query angles

From the research plan, assign **20 non-overlapping angle clusters** (one per sub-agent). Examples of clusters:

| Agent | Angle cluster |
|-------|----------------|
| 01 | Surveys / systematic reviews / meta-analyses |
| 02 | arXiv preprints (recent 3y) |
| 03 | IEEE / ACM proceedings |
| 04 | Industry reports + whitepapers |
| 05 | Government / standards (ISO, NIST, EU) |
| 06 | Seminal authors (set A) |
| 07 | Seminal authors (set B) |
| 08 | Mechanism / theory keywords |
| 09 | Applied / deployment / case studies |
| 10 | Critique / limitations / failures |
| 11–20 | Synonyms, adjacent subfields, venues, languages, grey lit — **no overlap with 01–10** |

Write `discovery/plan.md` with one line per agent: `Agent NN — <cluster> — seed queries: …`

### 2. Launch 20 discovery sub-agents (single parallel batch)

Use the **`Task`** tool — **one message, 20 calls**, `subagent_type: generalPurpose`, `model: composer-2.5-fast`.

**Per-agent target:** **~100 unique candidates** logged to `research/<slug>/discovery/shard-NN.md`.

**Sub-agent prompt template:**

```
Deep Research EXTREME — discovery shard {NN}/20.

Question: {QUESTION}
Your angle cluster: {CLUSTER}
Seed queries: {SEEDS}
Output file: research/{slug}/discovery/shard-{NN}.md

Rules:
- WebSearch ONLY for discovery — no WebFetch yet
- Run 8–12 search rounds, 4–6 NEW queries per round (no query reuse across rounds)
- Target ~100 unique URLs/papers; stop at 100 or when angles exhausted
- Dedup within shard by URL / DOI / arXiv ID
- Append after each round

Shard format:
# Discovery shard {NN}
**Agent:** {NN}
**Cluster:** {CLUSTER}
**Candidates:** <running count>

| Local # | Title | URL | Found via | Screen |
|---------|-------|-----|-----------|--------|
| 1 | ... | ... | query | pending |

Return ONLY: candidate count, top 3 angles that worked, any rate-limit issues.
```

### 3. Merge shards → `sources-index.md`

Orchestrator (parent agent):

1. Read all 20 shard files
2. Dedup globally (URL, DOI, arXiv ID, normalized title)
3. Assign global `#` — write `sources-index.md` header with **Mode: extreme**, real discovered count
4. Write `discovery/merge-log.md`: raw rows per shard, duplicates removed, final unique count

**Honesty:** if merged unique count **< 1 500**, document shortfall; if **< 1 000**, tell user extreme target was not met and why.

### 4. Parallel screening (recommended)

Launch **up to 10 screening sub-agents** in one parallel batch.

Each processes a slice of `pending` rows (~200 per agent):

- Use search snippet first
- `WebFetch` abstract **only** when title/snippet ambiguous
- Set `include` / `exclude` + reason code
- Write to `screening/batch-NN.md`

Orchestrator merges screen results back into `sources-index.md`.

**Screen targets (extreme):** ~300–500 `include` from ~2 000 discovered (exclude 60–85%).

### 5. Eligible + deep read (orchestrator)

Parent agent ranks eligible pool; promote **40–60** to `read`.

Do **not** spawn sub-agents for full-text read — parent reads top picks sequentially or in small batches to control token burn.

### 6. Report

Same template as other modes. Funnel table must show **actual** counts. Add section:

```markdown
## Extreme run metadata

| Metric | Value |
|--------|-------|
| Discovery sub-agents | 20 |
| Raw rows (pre-dedup) | <N> |
| Unique discovered | <N> |
| Screening sub-agents | <N or 0> |
| Est. token cost | high — user acknowledged |
```

## Abort / escape

| User says | Action |
|-----------|--------|
| `stop` / `arrête` | Halt new sub-agents; merge what exists; report partial funnel |
| `skip screening` | Merge discovery only; screen top 200 by title heuristics |
| `downgrade` | Stop extreme; continue as `literature-review` on current index |

## Self-check (extreme)

- [ ] User passed **two** confirmations (picker + extreme gate)
- [ ] 20 shard files attempted (note failures per shard)
- [ ] `merge-log.md` exists with dedup stats
- [ ] `sources-index.md` reflects merged reality — not inflated counts
- [ ] 40–60 deep-reads OR documented capacity shortfall
- [ ] Report cites only deep-read sources