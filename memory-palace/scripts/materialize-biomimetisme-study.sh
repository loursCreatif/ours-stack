#!/usr/bin/env bash
# Materialize biomimetisme study from tracked fixture (studies/ is gitignored).
# Source of truth: tests/fixtures/biomimetisme-memory-palace.json (7 mental scenes).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FIXTURE="$REPO_ROOT/tests/fixtures/biomimetisme-memory-palace.json"
STUDY_DIR="$REPO_ROOT/studies/biomimetisme-locomotion-chantier"
STUDY_JSON="$STUDY_DIR/memory-palace.json"
COMPOSE="$SCRIPT_DIR/compose-html.py"

[ -f "$FIXTURE" ] || { echo "missing fixture: $FIXTURE" >&2; exit 1; }
[ -f "$COMPOSE" ] || { echo "missing compose: $COMPOSE" >&2; exit 1; }

mkdir -p "$STUDY_DIR"
cp "$FIXTURE" "$STUDY_JSON"
exec python3 "$COMPOSE" "$STUDY_JSON"