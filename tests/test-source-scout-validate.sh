#!/usr/bin/env bash
# Integration tests: signal-based engine on noisy + live WebSearch cassettes.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUN="$ROOT/bin/ours-stack-source-scout-run"
LIVE="$ROOT/bin/ours-stack-source-scout-live-harness"
VALIDATE="$ROOT/bin/ours-stack-source-scout-validate"
PREFLIGHT="$ROOT/bin/ours-stack-source-scout-preflight"
TRANSCRIPT_CHECK="$ROOT/bin/ours-stack-source-scout-transcript-check"
EVIDENCE="$ROOT/bin/ours-stack-source-scout-evidence-check"
SYNC="$ROOT/bin/ours-stack-source-scout-sync-transcript-from-raw"
LOG="$ROOT/bin/ours-stack-source-scout-log-tool"
CASSETTES="$ROOT/tests/fixtures/source-scout-cassettes"
TEMPLATE="$ROOT/tests/fixtures/brief-home-energy-template.md"
SCRATCH="${SOURCE_SCOUT_TEST_SCRATCH:-$(mktemp -d)}"
mkdir -p "$SCRATCH"

for bin in "$RUN" "$LIVE" "$VALIDATE" "$PREFLIGHT" "$TRANSCRIPT_CHECK" "$EVIDENCE" "$SYNC" "$LOG"; do
  [ -x "$bin" ] || { echo "FAIL: missing or not executable: $bin"; exit 1; }
done
[ -f "$TEMPLATE" ] || { echo "FAIL: missing $TEMPLATE"; exit 1; }

pass=0
fail() { echo "FAIL: $*"; exit 1; }
ok() { echo "PASS: $*"; pass=$((pass + 1)); }

assert_manifest() {
  local man="$1" label="$2"
  jq -e '.wedge_coverage.on_wedge_picks == true' "$man" >/dev/null || fail "$label: picks not on-wedge"
  jq -e '[.scores[]] | all(. >= 9)' "$man" >/dev/null || fail "$label: score < 9"
  jq -e '.pool_size >= 3' "$man" >/dev/null || fail "$label: pool too small"
  # Anchor must not be arXiv (units doc, not paper)
  anchor="$(jq -r '.anchor' "$man")"
  case "$anchor" in *arxiv*) fail "$label: anchor must be units doc, not arXiv (got $anchor)" ;; esac
}

run_cassette() {
  local name="$1" run_id="$2"
  local cassette="$CASSETTES/${name}.jsonl"
  [ -f "$cassette" ] || fail "missing $cassette"
  local rb="$SCRATCH/${name}-brief.md"
  local man="$SCRATCH/${name}-manifest.json"
  cp "$TEMPLATE" "$rb"
  "$RUN" --brief "$rb" --cassette "$cassette" --run-id "$run_id" \
    --out "$rb" --raw "$SCRATCH/${name}-raw.jsonl" \
    --transcript "$SCRATCH/${name}-tr.jsonl" --manifest "$man" \
    >"$SCRATCH/${name}-run.log" 2>&1 || { cat "$SCRATCH/${name}-run.log" >&2; fail "run $name"; }
  "$VALIDATE" "$rb" >"$SCRATCH/${name}-validate.log" 2>&1 || fail "validate $name"
  assert_manifest "$man" "$name"
  jq -r '.primary_queries | join("|")' "$man"
}

# 0 — anti-overfit: engine must not hardcode study topics or URL/video IDs
ENGINE="$ROOT/source-scout/scripts/scout-engine.py"
if grep -inE 'bitcoin|genesis|satoshi|nakamoto|coinbase|7ujlqilwy84|3tknrphc140|4090|gpu' "$ENGINE" >/dev/null; then
  fail "engine contains hardcoded domain or URL tokens"
fi
if grep -inE 'kilowatt|kwh|inference|workload|homelab|vllm|batter|storage|energy.gov|pnnl|sandia|eia\.gov' "$ENGINE" >/dev/null; then
  fail "engine contains hardcoded energy-study tokens"
fi
if grep -inE 'youtube\.com/watch/[a-zA-Z0-9_-]{8,}|youtu\.be/[a-zA-Z0-9_-]{8,}' "$ENGINE" >/dev/null; then
  fail "engine contains hardcoded YouTube video IDs"
fi
ok "anti-overfit: no hardcoded study topics or URL IDs in engine"

# 1 — noisy synthetic pools (alternate URLs: energy.gov, pnnl — not EIA measuring.php)
queries_all=""
for name in noisy-mixed-pool noisy-gpu-measured noisy-inference-first; do
  qset="$(run_cassette "$name" "noisy-${name}")"
  case "$queries_all" in *"$qset"*) fail "$name duplicates queries" ;; esac
  queries_all="${queries_all}##${qset}"
done
ok "noisy ×3: dynamic pick from alternate URLs, scores >=9, non-arXiv anchor"

# 2 — two live WebSearch captures (agent session 2026-07-03, distinct query sets)
qa="$(run_cassette provider-live-a 10)"
qb="$(run_cassette provider-live-b 11)"
[ "$qa" != "$qb" ] || fail "live-a and live-b must have distinct queries"
ok "live WebSearch ×2: provider-live-{a,b}.jsonl → engine → validate"

# 3 — junk-only cassette rejected
JUNK="$SCRATCH/junk-only.jsonl"
cat >"$JUNK" <<'EOF'
{"tool":"WebSearch","query":"top 10 best electricity blogs","provider_status":"ok","results":["https://www.howtogeek.com/self-hosting-isnt-free/","https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/"]}
{"tool":"WebFetch","url":"https://www.howtogeek.com/self-hosting-isnt-free/","status":"ok","snippet_chars":3000}
EOF
junk_brief="$SCRATCH/junk-brief.md"
cp "$TEMPLATE" "$junk_brief"
if "$RUN" --brief "$junk_brief" --cassette "$JUNK" --run-id junk \
    --out "$junk_brief" --raw "$SCRATCH/junk-raw.jsonl" --transcript "$SCRATCH/junk-tr.jsonl" \
    >"$SCRATCH/junk-run.log" 2>&1; then
  fail "junk cassette must fail"
else
  ok "rejects junk-only cassette"
fi

# 4 — preflight
"$PREFLIGHT" "$TEMPLATE" >"$SCRATCH/preflight.log" 2>&1 || { cat "$SCRATCH/preflight.log" >&2; fail "preflight"; }
ok "preflight OK"

# 5 — production live-harness (provider.log = live-a capture)
PROD_BRIEF="$ROOT/studies/home-energy-ai-lab/brief.md"
PROD_CASSETTE="$ROOT/studies/home-energy-ai-lab/provider.log"
[ -f "$PROD_CASSETTE" ] || fail "missing $PROD_CASSETTE"
"$LIVE" "$PROD_BRIEF" "$PROD_CASSETTE" >"$SCRATCH/live-harness.log" 2>&1 || { cat "$SCRATCH/live-harness.log" >&2; fail "live-harness"; }
assert_manifest "${PROD_CASSETTE%.log}.manifest.json" "production"
ok "live-harness production"

# 6 — evidence chain
PROD_RAW="$ROOT/studies/home-energy-ai-lab/scout-raw.jsonl"
PROD_TR="$ROOT/studies/home-energy-ai-lab/scout-transcript.jsonl"
"$EVIDENCE" "$PROD_RAW" "$PROD_TR" >"$SCRATCH/evidence-prod.log" 2>&1 || fail "evidence"
"$TRANSCRIPT_CHECK" "$PROD_TR" "$PROD_BRIEF" >"$SCRATCH/transcript-prod.log" 2>&1 || fail "transcript"
ok "production evidence + transcript-check"

# 7 — validate cwd
"$VALIDATE" "$PROD_BRIEF" >"$SCRATCH/validate-root.log" 2>&1 || fail "validate root"
( cd "$ROOT/source-scout" && "$VALIDATE" "$PROD_BRIEF" ) >"$SCRATCH/validate-subdir.log" 2>&1 || fail "validate subdir"
ok "validate root + subdir"

# 8 — log-tool round-trip
ROUND_RAW="$SCRATCH/roundtrip-raw.jsonl"
ROUND_TR="$SCRATCH/roundtrip-transcript.jsonl"
: >"$ROUND_RAW"
"$LOG" --raw "$ROUND_RAW" --run 99 --tool WebSearch --query "roundtrip probe" \
  --urls "https://www.energy.gov/energysaver/electric-meters"
"$LOG" --raw "$ROUND_RAW" --run 99 --tool WebFetch \
  --url "https://www.energy.gov/energysaver/electric-meters" --status ok --snippet-chars 100
"$SYNC" "$ROUND_RAW" "$ROUND_TR" >/dev/null
head -1 "$ROUND_TR" | jq -e '.raw_seq == 1' >/dev/null || fail "sync"
ok "log-tool + sync round-trip"

# 9 — reject score <9
FIXTURE="$SCRATCH/brief-low-score.md"
cat >"$FIXTURE" <<'EOF'
# Test
## Source material
Scouted 2026-07-02 via `/source-scout` :
### Read first (anchor)
- [ ] **A** — *T* — https://example.com/a
  - Format: article
  - Tier: 1 · ~15 min · open access
  - Why: test
  - Targets: test
  - Score: 7/10 — too low
### Core
- [ ] **B** — *T* — https://example.com/b
  - Format: article
  - Tier: 1 · ~15 min · open access
  - Why: test
  - Targets: test
  - Score: 9/10 — ok
- [ ] **C** — *T* — https://example.com/c
  - Format: article
  - Tier: 1 · ~15 min · open access
  - Why: test
  - Targets: test
  - Score: 9/10 — ok
### Skipped (wedge boundary)
- *X* — off wedge
### Scout scores
- Set: 9/10 — inconsistent
EOF
if "$VALIDATE" "$FIXTURE" >/dev/null 2>&1; then fail "must reject 7/10"; else ok "rejects score 7/10"; fi

# 10 — anonymous YouTube on-wedge → score ≤6, article fallback
AUTH_ANON="$CASSETTES/authority-anonymous-video.jsonl"
anon_brief="$SCRATCH/authority-anon-brief.md"
anon_man="$SCRATCH/authority-anon-manifest.json"
cp "$TEMPLATE" "$anon_brief"
"$RUN" --brief "$anon_brief" --cassette "$AUTH_ANON" --run-id auth-anon \
  --out "$anon_brief" --raw "$SCRATCH/authority-anon-raw.jsonl" \
  --transcript "$SCRATCH/authority-anon-tr.jsonl" --manifest "$anon_man" \
  >"$SCRATCH/authority-anon-run.log" 2>&1 || { cat "$SCRATCH/authority-anon-run.log" >&2; fail "authority-anon run"; }
jq -e '.video_fallback == true' "$anon_man" >/dev/null || fail "anonymous video must trigger article fallback"
grep -q "youtube.com" "$anon_brief" && fail "anonymous video must not appear in final picks"
python3 -c "
import json, runpy
from pathlib import Path
ns = runpy.run_path('$ENGINE')
signals = ns['parse_brief'](Path('$anon_brief'))
cassette = ns['load_cassette'](Path('$AUTH_ANON'))
cands, _ = ns['build_candidates'](cassette, signals)
videos = [c for c in cands if c.is_youtube]
assert videos, 'missing youtube candidate'
score = ns['rubric_score'](videos[0], set())
assert score <= 6, f'anonymous video score {score} > 6'
"
ok "anonymous on-wedge video ≤6/10 and article fallback"

# 11 — named expert conference video → eligible ≥9/10
AUTH_EXP="$CASSETTES/authority-named-expert.jsonl"
exp_brief="$SCRATCH/authority-exp-brief.md"
exp_man="$SCRATCH/authority-exp-manifest.json"
cp "$TEMPLATE" "$exp_brief"
"$RUN" --brief "$exp_brief" --cassette "$AUTH_EXP" --run-id auth-exp \
  --out "$exp_brief" --raw "$SCRATCH/authority-exp-raw.jsonl" \
  --transcript "$SCRATCH/authority-exp-tr.jsonl" --manifest "$exp_man" \
  >"$SCRATCH/authority-exp-run.log" 2>&1 || { cat "$SCRATCH/authority-exp-run.log" >&2; fail "authority-exp run"; }
jq -e '.video_fallback == false' "$exp_man" >/dev/null || fail "named expert video should win slot 2"
python3 -c "
import json, runpy
from pathlib import Path
ns = runpy.run_path('$ENGINE')
signals = ns['parse_brief'](Path('$exp_brief'))
cassette = ns['load_cassette'](Path('$AUTH_EXP'))
cands, _ = ns['build_candidates'](cassette, signals)
videos = [c for c in cands if c.is_youtube]
assert videos, 'missing youtube candidate'
score = ns['rubric_score'](videos[0], set())
assert score >= 9, f'named expert video score {score} < 9'
"
ok "named expert conference video ≥9/10"

# 12 — log-tool --author round-trip
AUTH_RAW="$SCRATCH/authority-log-raw.jsonl"
: >"$AUTH_RAW"
"$LOG" --raw "$AUTH_RAW" --run 101 --tool WebFetch \
  --url "https://www.youtube.com/watch?v=roundtripauth" --status ok \
  --snippet-chars 5000 --author "Dr. Sam Okonkwo — IEEE Power & Energy Society"
tail -1 "$AUTH_RAW" | jq -e '.author == "Dr. Sam Okonkwo — IEEE Power & Energy Society"' >/dev/null || fail "author not in raw log"
ok "log-tool --author round-trip"

# 13 — cross-domain regression: history-topic brief + real captured cassette
# (engine must fill slot 2 with the fetched named-expert video, not an article fallback,
#  and must not leak another study's vocabulary into the brief)
TOPIC_TEMPLATE="$ROOT/tests/fixtures/brief-topic-history-template.md"
TOPIC_CASSETTE="$CASSETTES/provider-topic-history.jsonl"
[ -f "$TOPIC_TEMPLATE" ] || fail "missing $TOPIC_TEMPLATE"
topic_brief="$SCRATCH/topic-history-brief.md"
topic_man="$SCRATCH/topic-history-manifest.json"
cp "$TOPIC_TEMPLATE" "$topic_brief"
"$RUN" --brief "$topic_brief" --cassette "$TOPIC_CASSETTE" --run-id topic \
  --out "$topic_brief" --raw "$SCRATCH/topic-history-raw.jsonl" \
  --transcript "$SCRATCH/topic-history-tr.jsonl" --manifest "$topic_man" \
  >"$SCRATCH/topic-history-run.log" 2>&1 || { cat "$SCRATCH/topic-history-run.log" >&2; fail "topic-history run"; }
"$VALIDATE" "$topic_brief" >/dev/null 2>&1 || fail "topic-history validate"
jq -e '.video_fallback == false' "$topic_man" >/dev/null || fail "fetched named video must win slot 2"
jq -e '.formats | index("video") != null' "$topic_man" >/dev/null || fail "no video format in picks"
grep -q "youtube.com/watch" "$topic_brief" || fail "video pick missing from brief"
grep -qiE "workload|inférence locale|kilowatt" "$topic_brief" && fail "energy-study vocabulary leaked into topic brief"
grep -q "auteur identifié" "$topic_brief" || fail "authority notes missing"
ok "cross-domain: real cassette → video slot filled, no vocabulary leak"

echo "Summary: $pass tests passed"
exit 0