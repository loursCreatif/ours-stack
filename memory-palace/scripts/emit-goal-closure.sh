#!/usr/bin/env bash
# Emit harness-safe goal closure text (tracked CHANGED_FILES only — no studies/).
set -euo pipefail

SCRATCH="${1:?usage: emit-goal-closure.sh <scratch-dir>}"
OUT="$SCRATCH/goal-closure.md"
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

Le study biomimetisme (7 scènes, HTML embarqué) est régénéré à runtime via `bash memory-palace/scripts/materialize-biomimetisme-study.sh` → cible gitignorée (absent du patch). Preuve : study-evidence.json dans le scratch du test (`scene_count: 7`, SHA fixture = SHA study_json).
EOF

# Validate tracked section is clean
if awk '/^## Fichiers modifiés/,/^## Matérialisation/' "$OUT" | grep -qE '(^|- )`?studies/'; then
  echo "emit-goal-closure: tracked section must not list studies/ paths" >&2
  exit 1
fi

echo "Wrote $OUT"