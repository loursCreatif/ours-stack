#!/usr/bin/env bash
# Contract tests: council SKILL.md — live round-table design, cross-file coherence.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/council/SKILL.md"
[ -f "$SKILL" ] || { echo "FAIL: missing $SKILL"; exit 1; }

pass=0
fail() { echo "FAIL: $*"; exit 1; }
ok() { echo "PASS: $*"; pass=$((pass + 1)); }

# 1 — frontmatter intact
grep -q "^name: council$" "$SKILL" || fail "frontmatter must declare name: council"
ok "frontmatter declares name: council"

# 2 — live-meeting contract: never simulate the whole meeting, wait for user
grep -qi "never generate the whole meeting in one message" "$SKILL" || fail "missing live-meeting rule"
grep -q "STOP" "$SKILL" || fail "missing STOP-and-wait instruction"
ok "live-meeting rule present (no one-shot simulation, waits for user)"

# 3 — user participation: floor returns to user, user turns logged
grep -qi "3 figure turns" "$SKILL" || fail "missing max-figure-turns-before-user rule"
grep -q '\*\*Toi :\*\*' "$SKILL" || fail "user turns must be logged in transcript"
ok "user participation enforced (floor cadence + transcript)"

# 4 — real people only (incl. host) + built-in disagreement
grep -qi "real historical or public contemporary figure" "$SKILL" || fail "missing real-figures rule"
grep -qi "No invented personas, no generic roles" "$SKILL" || fail "missing no-invented-personas rule"
grep -qi "Real host" "$SKILL" || fail "missing real-host rule"
grep -qi "panel that agrees is a failed panel" "$SKILL" || fail "missing built-in-conflict rule"
ok "real figures only (host included), no invented personas, mandatory disagreement"

# 5 — honest fiction + no research + era limits
grep -qi "réunion pédagogique fictive" "$SKILL" || fail "missing fiction disclaimer"
grep -qi "never .WebSearch" "$SKILL" || fail "missing no-research rule"
EPI="dialogue/references/epistemic-modes.md"
grep -q "$EPI" "$SKILL" || fail "must reference shared epistemic modes"
[ -f "$ROOT/$EPI" ] || fail "referenced $EPI does not exist"
ok "fiction disclaimer, no-research rule, epistemic modes reference resolves"

# 6 — artifact contract matches AGENTS.md paths
grep -q 'studies/<slug>/council.md' "$SKILL" || fail "missing study-linked artifact path"
grep -q 'output/council/<slug>/council.md' "$SKILL" || fail "missing standalone artifact path"
grep -q 'output/council/<slug>/' "$ROOT/AGENTS.md" || fail "AGENTS.md lost council output path"
ok "artifact paths match AGENTS.md contract"

# 7 — close protocol: synthesis + learnings
grep -q "learnings.jsonl" "$SKILL" || fail "missing learnings.jsonl append"
grep -q "## Synthèse" "$SKILL" || fail "missing synthesis section in template"
ok "close protocol (synthèse + learnings.jsonl)"

# 8 — legacy machinery removed
for legacy in "Independent consult" "score(persona)" "Fuse plans" "Final fusion" "bear-hours first"; do
  if grep -qF "$legacy" "$SKILL"; then fail "legacy machinery still present: $legacy"; fi
done
ok "legacy plan-fusion machinery removed"

# 9 — no stale cross-references to the old design
if grep -rn "fused study plan\|final fusion" "$ROOT/AGENTS.md" "$ROOT/README.md" "$ROOT/dialogue" "$ROOT/study-status" >/dev/null 2>&1; then
  fail "stale council cross-reference (fusion-era wording) outside council/"
fi
ok "cross-references updated (AGENTS, README, dialogue, study-status)"

echo "OK: $pass tests passed"
