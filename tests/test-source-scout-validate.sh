#!/usr/bin/env bash
# Tests for ours-stack-source-scout-validate — the single source-scout gate.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATE="$ROOT/bin/ours-stack-source-scout-validate"
SCRATCH="${SOURCE_SCOUT_TEST_SCRATCH:-$(mktemp -d)}"
mkdir -p "$SCRATCH"

[ -x "$VALIDATE" ] || { echo "FAIL: missing or not executable: $VALIDATE"; exit 1; }

pass=0
fail() { echo "FAIL: $*"; exit 1; }
ok() { echo "PASS: $*"; pass=$((pass + 1)); }

# ── Fixture builders ────────────────────────────────────────────────

brief_head() {
  cat <<'EOF'
# Study brief — test

## Narrow wedge

Comment un hexapode garde son équilibre sur terrain irrégulier.

## Success criteria

- [ ] Expliquer la marche tripode sans notes

EOF
}

source_block() {
  # $1 = score
  cat <<EOF
- [ ] **Author (2024)** — *Titre dense* — https://example.org/paper
  - Format: article
  - Tier: 1 · ~45 min · open access
  - Why: unlocks the wedge — figure 3 montre la séquence tripode mesurée
  - Targets: Expliquer la marche tripode
  - Score: ${1}/10 — dense, on-wedge, auteur identifié
EOF
}

valid_section() {
  # $1 = anchor score, $2/$3 = core scores, $4 = set score
  cat <<EOF
## Source material

Scouted 2026-07-03 via \`/source-scout\` :

### Read first (anchor)
$(source_block "${1:-9}")

### Core
$(source_block "${2:-9}")
$(source_block "${3:-10}")

### Skipped (wedge boundary)
- *Teaser YouTube anonyme* — autorité non identifiable, hors bar.

### Scout scores
- Set: ${4:-9}/10 — 3 slots on-wedge, anchor Tier 1.
EOF
}

# ── Cases ───────────────────────────────────────────────────────────

# 1. Valid brief passes
b="$SCRATCH/valid.md"
{ brief_head; valid_section; } >"$b"
"$VALIDATE" "$b" >/dev/null || fail "valid brief should pass"
ok "valid brief passes"

# 2. Missing ## Source material fails
b="$SCRATCH/missing-section.md"
brief_head >"$b"
! "$VALIDATE" "$b" 2>/dev/null || fail "missing section should fail"
ok "missing section fails"

# 3. Wrong header fails
b="$SCRATCH/bad-header.md"
{ brief_head; valid_section | sed 's/^Scouted .*/Scouted hier :/'; } >"$b"
! "$VALIDATE" "$b" 2>/dev/null || fail "bad header should fail"
ok "bad header fails"

# 4. Only 2 sources fails
b="$SCRATCH/two-sources.md"
{
  brief_head
  cat <<EOF
## Source material

Scouted 2026-07-03 via \`/source-scout\` :

### Read first (anchor)
$(source_block 9)

### Core
$(source_block 9)

### Skipped (wedge boundary)
- *X* — hors wedge.

### Scout scores
- Set: 9/10 — set réduit.
EOF
} >"$b"
! "$VALIDATE" "$b" 2>/dev/null || fail "2 sources should fail"
ok "2 sources fails"

# 5. Score below minimum fails (default MIN 9)
b="$SCRATCH/low-score.md"
{ brief_head; valid_section 8 9 9 9; } >"$b"
! "$VALIDATE" "$b" 2>/dev/null || fail "score 8/10 should fail at MIN 9"
ok "score below minimum fails"

# 6. SOURCE_SCOUT_MIN_SCORE override lowers the gate
SOURCE_SCOUT_MIN_SCORE=8 "$VALIDATE" "$b" >/dev/null \
  || fail "score 8/10 should pass with MIN_SCORE=8"
ok "MIN_SCORE override works"

# 7. Low set score fails
b="$SCRATCH/low-set.md"
{ brief_head; valid_section 9 9 9 7; } >"$b"
! "$VALIDATE" "$b" 2>/dev/null || fail "set 7/10 should fail"
ok "low set score fails"

# 8. Missing Targets: line fails
b="$SCRATCH/no-targets.md"
{ brief_head; valid_section | grep -v '  - Targets:'; } >"$b"
! "$VALIDATE" "$b" 2>/dev/null || fail "missing Targets should fail"
ok "missing Targets fails"

# 9. Missing ### Scout scores fails
b="$SCRATCH/no-set.md"
{ brief_head; valid_section | sed '/### Scout scores/,$d'; } >"$b"
! "$VALIDATE" "$b" 2>/dev/null || fail "missing Scout scores should fail"
ok "missing Scout scores fails"

echo
echo "All $pass source-scout-validate tests passed."
