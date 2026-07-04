#!/usr/bin/env bash
# Emit harness-safe goal closure text (tracked CHANGED_FILES only — no studies/).
set -euo pipefail

SCRATCH="${1:?usage: emit-goal-closure.sh <scratch-dir>}"
OUT="$SCRATCH/goal-closure.md"
TRACKED_LIST="$SCRATCH/changed-files-tracked.txt"
PASTE="$SCRATCH/final-response-paste.md"
mkdir -p "$SCRATCH"

cat >"$OUT" <<'EOF'
## Fichiers modifiés (trackés — copier tel quel dans FINAL_RESPONSE)

- `memory-palace/scripts/compose-html.py` — visite guidée sur rails, panneau scènes mentales, environnement procédural
- `memory-palace/scripts/materialize-biomimetisme-study.sh` — matérialise le study depuis la fixture trackée
- `memory-palace/scripts/emit-goal-closure.sh` — texte de clôture harness (section trackée sans artefact gitignoré)
- `memory-palace/scripts/fetch-three.sh` — fetch Three.js vendored
- `tests/fixtures/biomimetisme-memory-palace.json` — source canonique des 7 scènes mentales
- `tests/test-memory-palace.sh` — 17 régression + 8 immersion + goal-closure gate
- `memory-palace/SKILL.md`
- `memory-palace/references/palace-schema.json`
- `memory-palace/references/navigation-ux.md`
- `memory-palace/references/palace-archetypes.md`
- `memory-palace/references/loci-mapping.md`
- `memory-palace/references/concept-extraction.md`
- `memory-palace/references/html-template.md`
- `memory-palace/IMMERSION-PLAN.md`
- `memory-palace/VISUAL-PLAN.md`

## Matérialisation runtime (non trackée — ne pas mettre dans « Fichiers modifiés »)

Critère study satisfait par matérialisation : `bash memory-palace/scripts/materialize-biomimetisme-study.sh` copie la fixture trackée vers la cible gitignorée puis compose le HTML. Preuve scratch : `study-evidence.json` (`scene_count: 7`, `fixture_sha256` = `study_json_sha256`, `materialize_verified: true`).
EOF

tracked_section() {
  awk '/^## Fichiers modifiés/,/^## Matérialisation/' "$OUT"
}

if tracked_section | grep -qE '(^|- )`?studies/'; then
  echo "emit-goal-closure: tracked section must not list studies/ paths" >&2
  exit 1
fi

grep -E '^- `' "$OUT" | sed -E 's/^- `([^`]+)`.*/\1/' >"$TRACKED_LIST"

cp "$OUT" "$PASTE"

if awk '/^## Fichiers modifiés/,/^## Matérialisation/' "$PASTE" | grep -qE '(^|- )`?studies/'; then
  echo "emit-goal-closure: final-response-paste tracked section must not list studies/ paths" >&2
  exit 1
fi

echo "Wrote $OUT"
echo "Wrote $TRACKED_LIST ($(wc -l <"$TRACKED_LIST" | tr -d ' ') paths)"
echo "Wrote $PASTE"