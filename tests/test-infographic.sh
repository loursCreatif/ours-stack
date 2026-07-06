#!/usr/bin/env bash
# Contract tests: infographic skill — AskUserQuestion limits, metaphor/hero pipeline,
# prompt templates, fidelity loop, layout-html preset coupling.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/infographic/SKILL.md"
REFS="$ROOT/infographic/references"

pass=0
fail() { echo "FAIL: $*"; exit 1; }
ok() { echo "PASS: $*"; pass=$((pass + 1)); }

# 1 — all skill files exist
for f in "$SKILL" "$REFS/palettes.md" "$REFS/privacy-strip.md" "$REFS/prompt-template.md" \
         "$REFS/spec-schema.md" "$REFS/tool-detection.md" "$REFS/visual-types.md"; do
  [ -f "$f" ] || fail "missing $f"
done
ok "all skill files present"

# 2 — Step 0 style question has exactly 4 options (AskUserQuestion max)
python3 -c "
import re
from pathlib import Path
text = Path('$SKILL').read_text()
step0 = text.split('## Step 0', 1)[1].split('## Step 1', 1)[0]
rows = re.findall(r'^\|\s*\`(\w+)\`\s*\|', step0, re.M)
assert len(rows) == 4, f'expected 4 style options, got {len(rows)}: {rows}'
assert rows[0] == 'warm', f'warm must be first (default), got {rows[0]}'
" || fail "Step 0 style options"
ok "Step 0: exactly 4 style options, warm first"

# 3 — no editorial preset anywhere in the skill
if grep -rqi 'editorial' "$ROOT/infographic/"; then
  fail "editorial still referenced in infographic/"
fi
ok "editorial preset fully removed"

# 4 — no explicit custom option row; custom handled via automatic Other
python3 -c "
import re
from pathlib import Path
text = Path('$SKILL').read_text()
step0 = text.split('## Step 0', 1)[1].split('## Step 1', 1)[0]
assert not re.search(r'^\|\s*\`custom\`', step0, re.M), 'explicit custom row present'
assert 'Other' in step0, 'no mention of automatic Other handling'
" || fail "custom option handling"
ok "custom style routed through automatic Other option"

# 5 — layout tie-break capped at 4 options everywhere (no fifth auto row)
python3 -c "
import re
from pathlib import Path
vt = Path('$REFS/visual-types.md').read_text()
section = vt.split('### AskUserQuestion', 1)[1]
rows = re.findall(r'^\|\s*\`(\w+)\`\s*\|', section, re.M)
assert len(rows) == 4, f'expected 4 layout options, got {len(rows)}: {rows}'
assert 'auto' not in rows, 'explicit auto row still present'
skill = Path('$SKILL').read_text()
step3 = skill.split('## Step 3', 1)[1].split('## Step 4', 1)[0]
assert 'max 4' in step3, 'Step 3 missing max-4 constraint'
" || fail "layout tie-break options"
ok "layout tie-break: 4 options max, no explicit auto row"

# 6 — spec schema has visual metaphor + hero element sections
python3 -c "
from pathlib import Path
spec = Path('$REFS/spec-schema.md').read_text()
assert '## Visual metaphor' in spec, 'missing Visual metaphor section'
assert 'Hero element' in spec, 'missing Hero element'
assert 'VISUAL_METAPHOR' in spec.upper() or 'DRAWABLE_SCENE' in spec.upper(), 'no metaphor placeholder'
" || fail "spec schema metaphor/hero"
ok "spec schema: visual metaphor + hero element required"

# 7 — spec rules ban diagram-speak in the metaphor
python3 -c "
from pathlib import Path
spec = Path('$REFS/spec-schema.md').read_text().lower()
for word in ['box', 'diagram']:
    assert word in spec, f'metaphor rules must mention forbidden word: {word}'
assert 'drawable' in spec, 'metaphor must be described as drawable'
" || fail "metaphor quality bar in spec rules"
ok "spec rules: metaphor quality bar (drawable, no box/diagram-speak)"

# 8 — SKILL.md Step 2 extracts metaphor + hero; hard rule exists
python3 -c "
from pathlib import Path
text = Path('$SKILL').read_text()
step2 = text.split('## Step 2', 1)[1].split('## Step 3', 1)[0]
assert '\`metaphor\`' in step2, 'Step 2 missing metaphor field'
assert '\`hero\`' in step2, 'Step 2 missing hero field'
rules = text.split('## Hard rules', 1)[1].split('## Step 0', 1)[0]
assert 'Metaphor + hero' in rules, 'missing metaphor+hero hard rule'
" || fail "SKILL.md metaphor/hero extraction"
ok "SKILL.md: Step 2 extracts metaphor + hero, hard rule present"

# 9 — prompt templates inject metaphor + hero (Universal and IMAGE mode)
python3 -c "
from pathlib import Path
pt = Path('$REFS/prompt-template.md').read_text()
assert pt.count('{{VISUAL_METAPHOR}}') >= 2, 'metaphor missing from Universal or IMAGE prompt'
assert pt.count('{{HERO}}') >= 2, 'hero missing from Universal or IMAGE prompt'
assert '1/3 of' in pt or '1/3 of the canvas' in pt, 'hero size guidance missing'
" || fail "prompt template metaphor/hero injection"
ok "prompt templates: metaphor + hero in Universal and IMAGE prompts"

# 10 — prompts forbid invented labels and demand correct accents
python3 -c "
from pathlib import Path
pt = Path('$REFS/prompt-template.md').read_text().lower()
assert 'do not invent extra text' in pt or 'nothing more' in pt, 'no anti-invented-labels clause'
assert 'accents' in pt, 'no accent-spelling clause'
" || fail "prompt template anti-garble clauses"
ok "prompt templates: exact labels only, accents required"

# 11 — every visual type has composition variants + fallback layout
python3 -c "
from pathlib import Path
vt = Path('$REFS/visual-types.md').read_text()
assert vt.count('Composition variants') == 5, f'expected 5 variant blocks, got {vt.count(\"Composition variants\")}'
assert vt.count('Fallback layout instruction') == 5, 'each type needs a fallback layout'
assert 'Metaphor before layout' in vt, 'missing metaphor-before-layout principle'
" || fail "visual types composition variants"
ok "visual types: 5 composition-variant blocks + metaphor-before-layout rule"

# 12 — fidelity loop: 4 checks, 2-retry budget, PROMPT fallback
python3 -c "
from pathlib import Path
td = Path('$REFS/tool-detection.md').read_text().lower()
assert 'fidelity loop' in td, 'missing fidelity loop section'
for phrase in ['label count', 'hero', 'palette', 'legible']:
    assert phrase in td, f'fidelity loop missing check: {phrase}'
assert '2 retries' in td, 'missing retry budget'
assert 'fallback prompt' in td, 'missing PROMPT fallback'
" || fail "fidelity loop contract"
ok "fidelity loop: legibility + label count + hero + palette, 2-retry budget"

# 13 — label constraints: 1–2 words, ≤7 labels, consistent across files
python3 -c "
from pathlib import Path
skill = Path('$SKILL').read_text()
spec = Path('$REFS/spec-schema.md').read_text()
assert '1–2 words' in skill or '1-2 words' in skill, 'SKILL.md missing 1-2 word label rule'
assert '1–2 words' in spec or '1-2 words' in spec, 'spec-schema missing 1-2 word label rule'
assert skill.count('7 labels') >= 1 or '≤7 labels' in skill, 'SKILL.md missing 7-label cap'
" || fail "label constraints"
ok "label constraints: ≤7 labels, 1–2 words, consistent"

# 14 — layout-html preset coupling: every offered preset file exists
python3 -c "
import re
from pathlib import Path
text = Path('$SKILL').read_text()
step0 = text.split('## Step 0', 1)[1].split('## Step 1', 1)[0]
presets = re.findall(r'^\|\s*\`(\w+)\`\s*\|', step0, re.M)
missing = [p for p in presets
           if not Path('$ROOT/layout-html/references/presets/' + p + '.md').is_file()]
assert not missing, f'presets offered but missing in layout-html: {missing}'
" || fail "layout-html preset coupling"
ok "coupling: all offered presets exist in layout-html/references/presets/"

# 15 — palettes.md index matches Step 0 options (same 4 ids, warm default)
python3 -c "
import re
from pathlib import Path
pal = Path('$REFS/palettes.md').read_text()
index = pal.split('## Index', 1)[1].split('## Style phrases', 1)[0]
ids = set(re.findall(r'^\|\s*\`(\w+)\`\s*\|', index, re.M))
assert ids == {'warm', 'academic', 'minimal', 'creative'}, f'palette index mismatch: {ids}'
phrases = pal.split('## Style phrases', 1)[1]
pids = set(re.findall(r'^\|\s*\`(\w+)\`\s*\|', phrases, re.M))
assert pids == ids, f'style phrases mismatch: {pids}'
assert 'warm' in pal.split('Default when skipped', 1)[1][:30], 'warm not the skip default'
" || fail "palettes index consistency"
ok "palettes.md: index + style phrases match the 4 offered presets"

# 16 — no research allowed: hard rule present, WebSearch/WebFetch not in allowed-tools
python3 -c "
from pathlib import Path
text = Path('$SKILL').read_text()
fm = text.split('---', 2)[1]
assert 'WebSearch' not in fm and 'WebFetch' not in fm, 'research tools in allowed-tools'
assert 'No research' in text, 'missing no-research hard rule'
" || fail "no-research contract"
ok "no-research: WebSearch/WebFetch excluded from allowed-tools"

# 17 — self-check covers the new memorability rules
python3 -c "
from pathlib import Path
text = Path('$SKILL').read_text()
check = text.split('## Self-check', 1)[1]
assert 'metaphor' in check.lower(), 'self-check missing metaphor item'
assert 'hero' in check.lower(), 'self-check missing hero item'
assert '1–2 words' in check or '1-2 words' in check, 'self-check missing label length'
" || fail "self-check coverage"
ok "self-check: metaphor + hero + label length verified before delivery"

echo "Summary: $pass tests passed"
exit 0
