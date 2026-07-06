#!/usr/bin/env bash
# Integration tests: mind-map validate + compose-html (escape, round-trip, UX).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATE="$ROOT/mind-map/scripts/validate-map.py"
COMPOSE="$ROOT/mind-map/scripts/compose-html.py"
FIXTURES="$ROOT/tests/fixtures"
SCRATCH="${MIND_MAP_TEST_SCRATCH:-/tmp/ours-stack-mind-map-test}"
mkdir -p "$SCRATCH"

for script in "$VALIDATE" "$COMPOSE"; do
  [ -f "$script" ] || { echo "FAIL: missing $script"; exit 1; }
done

pass=0
fail() { echo "FAIL: $*"; exit 1; }
ok() { echo "PASS: $*"; pass=$((pass + 1)); }

VALID="$FIXTURES/mind-map-valid.json"
TRAP="$FIXTURES/mind-map-trap.json"
WIDE="$FIXTURES/mind-map-wide.json"
[ -f "$VALID" ] || fail "missing $VALID"
[ -f "$TRAP" ] || fail "missing $TRAP"
[ -f "$WIDE" ] || fail "missing $WIDE"

# 1 — validate accepts valid fixture
python3 "$VALIDATE" "$VALID" >"$SCRATCH/valid.log" 2>&1 || { cat "$SCRATCH/valid.log" >&2; fail "valid map rejected"; }
ok "validate-map accepts valid fixture"

# 2 — reject duplicate id
DUP="$SCRATCH/dup-id.json"
cat >"$DUP" <<'EOF'
{"meta":{"title":"dup","slug":"dup","source":"x","preset":"warm","lang":"fr","generated":"2026-07-03","nodeCount":2},
 "root":{"id":"root","label":"R","type":"concept","children":[{"id":"a","label":"A","type":"detail","children":[{"id":"a","label":"B","type":"detail"}]}]}}
EOF
if python3 "$VALIDATE" "$DUP" >/dev/null 2>&1; then fail "must reject duplicate id"; else ok "rejects duplicate id"; fi

# 3 — reject invalid type
BAD_TYPE="$SCRATCH/bad-type.json"
cat >"$BAD_TYPE" <<'EOF'
{"meta":{"title":"t","slug":"t","source":"x","preset":"warm","lang":"fr","generated":"2026-07-03","nodeCount":2},
 "root":{"id":"root","label":"R","type":"concept","children":[{"id":"x","label":"X","type":"bogus","children":[]}]}}
EOF
if python3 "$VALIDATE" "$BAD_TYPE" >/dev/null 2>&1; then fail "must reject invalid type"; else ok "rejects invalid type"; fi

# 4 — reject depth > 5
DEEP="$SCRATCH/deep.json"
python3 -c "
import json
from pathlib import Path
node = {'id': 'leaf', 'label': 'L', 'type': 'detail', 'children': []}
for i in range(6):
    node = {'id': f'n{i}', 'label': f'N{i}', 'type': 'detail', 'children': [node]}
root = {'id': 'root', 'label': 'R', 'type': 'concept', 'children': [node]}
data = {'meta': {'title': 'd', 'slug': 'd', 'source': 'x', 'preset': 'warm', 'lang': 'fr',
                 'generated': '2026-07-03', 'nodeCount': 8}, 'root': root}
Path('$DEEP').write_text(json.dumps(data))
"
if python3 "$VALIDATE" "$DEEP" >/dev/null 2>&1; then fail "must reject depth > 5"; else ok "rejects depth > 5"; fi

# 5 — reject > 80 nodes
MANY="$SCRATCH/many.json"
python3 -c "
import json
from pathlib import Path
kids = [{'id': f'n{i}', 'label': f'N{i}', 'type': 'detail', 'children': []} for i in range(81)]
root = {'id': 'root', 'label': 'R', 'type': 'concept', 'children': kids}
data = {'meta': {'title': 'm', 'slug': 'm', 'source': 'x', 'preset': 'warm', 'lang': 'fr',
                 'generated': '2026-07-03', 'nodeCount': 82}, 'root': root}
Path('$MANY').write_text(json.dumps(data))
"
if python3 "$VALIDATE" "$MANY" >/dev/null 2>&1; then fail "must reject > 80 nodes"; else ok "rejects > 80 nodes"; fi

# 6 — reject root.type != concept
BAD_ROOT="$SCRATCH/bad-root.json"
cat >"$BAD_ROOT" <<'EOF'
{"meta":{"title":"t","slug":"t","source":"x","preset":"warm","lang":"fr","generated":"2026-07-03","nodeCount":1},
 "root":{"id":"root","label":"R","type":"detail","children":[]}}
EOF
if python3 "$VALIDATE" "$BAD_ROOT" >/dev/null 2>&1; then fail "must reject root.type != concept"; else ok "rejects root.type != concept"; fi

# 7 — reject href non-http on source
BAD_HREF="$SCRATCH/bad-href.json"
cat >"$BAD_HREF" <<'EOF'
{"meta":{"title":"t","slug":"t","source":"x","preset":"warm","lang":"fr","generated":"2026-07-03","nodeCount":2},
 "root":{"id":"root","label":"R","type":"concept","children":[{"id":"s","label":"S","type":"source","href":"ftp://bad.example/x","children":[]}]}}
EOF
if python3 "$VALIDATE" "$BAD_HREF" >/dev/null 2>&1; then fail "must reject non-http href"; else ok "rejects non-http href on source"; fi

# 8 — compose: trap string must not appear literally in HTML
TRAP_HTML="$SCRATCH/trap.html"
python3 "$COMPOSE" "$TRAP" "$TRAP_HTML" >/dev/null
if grep -q '</script><script>alert' "$TRAP_HTML"; then
  fail "trap </script><script> leaked into HTML"
fi
ok "compose-html blocks script-breakout in embedded JSON"

# 9 — title HTML-escaped
if ! grep -q '<title>&lt;b&gt;&amp;&lt;/b&gt; Titre piégé — mind map</title>' "$TRAP_HTML"; then
  fail "title not HTML-escaped"
fi
ok "compose-html escapes title in <title>"

# 10 — JSON round-trip from generated HTML
python3 -c "
import json, re, sys
from pathlib import Path
html = Path('$TRAP_HTML').read_text()
m = re.search(r'<script id=\"map-data\" type=\"application/json\">(.*?)</script>', html, re.S)
assert m, 'map-data script block missing'
raw = m.group(1)
parsed = json.loads(raw)
expected = json.loads(Path('$TRAP').read_text())
assert parsed == expected, 'round-trip mismatch'
trap = parsed['root']['children'][0]['note']
assert '</script><script>alert(1)</script>' in trap, 'trap note corrupted'
" || fail "JSON round-trip failed"
ok "JSON round-trip intact (trap note preserved)"

# 11 — zero external assets (inline SVG namespace + source hrefs allowed)
python3 -c "
import re, sys
from pathlib import Path
text = Path('$TRAP_HTML').read_text()
bad = []
for pat in [r'cdn', r'fonts\.googleapis', r'unpkg', r'jsdelivr', r'<script[^>]+src=', r'@import']:
    if re.search(pat, text, re.I):
        bad.append(pat)
# Any other http(s) URL must be w3.org SVG namespace or a source href inside map-data
for m in re.finditer(r'https?://[^\s\"\\'>]+', text):
    url = m.group(0)
    if 'w3.org/2000/svg' in url:
        continue
    if re.search(r'<script id=\"map-data\"[^>]*>.*' + re.escape(url), text, re.S):
        continue
    bad.append(url)
if bad:
    print('found:', bad, file=sys.stderr)
    sys.exit(1)
" || fail "external asset detected"
ok "zero CDN / external script assets"

# 12 — UX: cursor-centered wheel zoom in compose-html source
if ! grep -qE 'getBoundingClientRect|clientX.*rect\.left' "$COMPOSE"; then
  fail "missing cursor-centered zoom logic"
fi
ok "UX: wheel zoom anchored to cursor"

# 13 — UX: label truncation adapts to bubble width
if ! grep -q 'maxChars' "$COMPOSE" || ! grep -q 'node.label.slice(0, Math.max(1, maxChars - 1))' "$COMPOSE"; then
  fail "missing width-aware label truncation"
fi
ok "UX: labels truncate from computed bubble width"

# 14 — validate accepts summary in valid fixture
if ! python3 "$VALIDATE" "$VALID" >"$SCRATCH/valid-summary.log" 2>&1; then
  cat "$SCRATCH/valid-summary.log" >&2
  fail "valid fixture with summary rejected"
fi
ok "validate-map accepts summary in valid fixture"

# 15 — reject summary > 200 chars
LONG_SUM="$SCRATCH/long-summary.json"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['root']['summary'] = 'x' * 201
Path('$LONG_SUM').write_text(json.dumps(data))
"
if python3 "$VALIDATE" "$LONG_SUM" >/dev/null 2>&1; then
  fail "must reject summary > 200 chars"
else
  ok "rejects summary > 200 chars"
fi

# 16 — reject non-string summary
BAD_SUM="$SCRATCH/bad-summary.json"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['root']['summary'] = 42
Path('$BAD_SUM').write_text(json.dumps(data))
"
if python3 "$VALIDATE" "$BAD_SUM" >/dev/null 2>&1; then
  fail "must reject non-string summary"
else
  ok "rejects non-string summary"
fi

# 17 — compose: tooltip logic present, data via textContent not innerHTML
VALID_HTML="$SCRATCH/valid.html"
python3 "$COMPOSE" "$VALID" "$VALID_HTML" >/dev/null
if ! grep -q 'tooltip' "$VALID_HTML" || ! grep -q 'tooltipText' "$COMPOSE"; then
  fail "missing tooltip logic in compose-html"
fi
if grep -qE 'tooltip\.innerHTML|panel-summary.*innerHTML|panel-note.*innerHTML' "$COMPOSE"; then
  fail "data fields must not use innerHTML"
fi
if ! grep -q 'tooltip.textContent' "$COMPOSE"; then
  fail "tooltip must use textContent"
fi
ok "compose-html tooltip via textContent (no data innerHTML)"

# 18 — trap summary with script breakout stays in JSON, not literal in HTML
python3 "$COMPOSE" "$TRAP" "$TRAP_HTML" >/dev/null
if grep -q '</script><script>alert' "$TRAP_HTML"; then
  fail "trap summary leaked into HTML"
fi
python3 -c "
import json, re, sys
from pathlib import Path
html = Path('$TRAP_HTML').read_text()
m = re.search(r'<script id=\"map-data\" type=\"application/json\">(.*?)</script>', html, re.S)
assert m, 'map-data missing'
parsed = json.loads(m.group(1))
trap_sum = parsed['root']['children'][0]['summary']
assert '</script><script>alert(2)' in trap_sum, 'trap summary corrupted'
" || fail "trap summary round-trip failed"
ok "trap summary preserved in JSON, not literal in HTML"

# 19 — search includes summary field
if ! grep -q 'n.summary' "$COMPOSE"; then
  fail "search must include summary field"
fi
ok "search covers summary field"

# 20 — validate accepts layout auto and centered
for mode in auto centered; do
  LAYOUT_OK="$SCRATCH/layout-${mode}.json"
  python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['layout'] = '$mode'
Path('$LAYOUT_OK').write_text(json.dumps(data, ensure_ascii=False))
"
  if ! python3 "$VALIDATE" "$LAYOUT_OK" >"$SCRATCH/layout-${mode}.log" 2>&1; then
    cat "$SCRATCH/layout-${mode}.log" >&2
    fail "valid layout=$mode rejected"
  fi
done
ok "validate-map accepts layout auto and centered"

# 21 — reject unknown layout value
BAD_LAYOUT="$SCRATCH/layout-radial.json"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['layout'] = 'radial'
Path('$BAD_LAYOUT').write_text(json.dumps(data, ensure_ascii=False))
"
if python3 "$VALIDATE" "$BAD_LAYOUT" >/dev/null 2>&1; then
  fail "must reject layout=radial"
else
  ok "rejects unknown layout value"
fi

# 22 — existing JSON without layout remains valid and composes as tree
NO_LAYOUT_HTML="$SCRATCH/no-layout.html"
python3 "$VALIDATE" "$VALID" >"$SCRATCH/no-layout-validate.log" 2>&1 || { cat "$SCRATCH/no-layout-validate.log" >&2; fail "valid no-layout rejected"; }
python3 "$COMPOSE" "$VALID" "$NO_LAYOUT_HTML" >/dev/null
if ! grep -q 'data-initial-layout="tree"' "$NO_LAYOUT_HTML"; then
  fail "existing fixture without layout should default to tree"
fi
ok "existing no-layout fixture composes in tree mode"

# 23 — compose: two layout modes and toolbar toggle are present
if ! grep -q 'function chooseLayout' "$COMPOSE" || ! grep -q 'layoutCentered' "$COMPOSE" || ! grep -q 'btn-layout' "$COMPOSE"; then
  fail "missing layout selection or toggle logic"
fi
if ! grep -q "state.layout === 'centered'" "$COMPOSE"; then
  fail "missing centered/tree render branch"
fi
ok "compose-html includes auto layout and toggle logic"

# 24 — wide shallow fixture opens centered and round-trips intact
WIDE_HTML="$SCRATCH/wide.html"
python3 "$VALIDATE" "$WIDE" >"$SCRATCH/wide-validate.log" 2>&1 || { cat "$SCRATCH/wide-validate.log" >&2; fail "wide fixture rejected"; }
python3 "$COMPOSE" "$WIDE" "$WIDE_HTML" >/dev/null
if ! grep -q 'data-initial-layout="centered"' "$WIDE_HTML"; then
  fail "wide fixture should auto-select centered layout"
fi
python3 -c "
import json, re
from pathlib import Path
html = Path('$WIDE_HTML').read_text()
m = re.search(r'<script id=\"map-data\" type=\"application/json\">(.*?)</script>', html, re.S)
assert m, 'map-data missing'
parsed = json.loads(m.group(1))
expected = json.loads(Path('$WIDE').read_text())
assert parsed == expected, 'wide round-trip mismatch'
" || fail "wide fixture round-trip failed"
ok "wide fixture auto-centers and round-trips"

# 25 — deep auto fixture stays in tree mode
DEEP_AUTO="$SCRATCH/deep-auto.json"
python3 -c "
import json
from pathlib import Path
leaf = {'id': 'leaf', 'label': 'Leaf', 'type': 'detail', 'children': []}
node = leaf
for i in range(3, 0, -1):
    node = {'id': f'level-{i}', 'label': f'Level {i}', 'type': 'detail', 'children': [node]}
data = {
    'meta': {'title': 'Deep generic', 'slug': 'deep-generic', 'source': 'scratch',
             'preset': 'warm', 'lang': 'fr', 'generated': '2026-07-03', 'nodeCount': 5},
    'root': {'id': 'root', 'label': 'Root', 'type': 'concept', 'children': [node]}
}
Path('$DEEP_AUTO').write_text(json.dumps(data, ensure_ascii=False))
"
DEEP_HTML="$SCRATCH/deep-auto.html"
python3 "$VALIDATE" "$DEEP_AUTO" >"$SCRATCH/deep-auto-validate.log" 2>&1 || { cat "$SCRATCH/deep-auto-validate.log" >&2; fail "deep auto rejected"; }
python3 "$COMPOSE" "$DEEP_AUTO" "$DEEP_HTML" >/dev/null
if ! grep -q 'data-initial-layout="tree"' "$DEEP_HTML"; then
  fail "deep fixture should auto-select tree layout"
fi
ok "deep fixture auto-selects tree"

# 26 — explicit layout forces generated initial mode
for mode in tree centered; do
  FORCED="$SCRATCH/forced-${mode}.json"
  FORCED_HTML="$SCRATCH/forced-${mode}.html"
  python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['layout'] = '$mode'
Path('$FORCED').write_text(json.dumps(data, ensure_ascii=False))
"
  python3 "$VALIDATE" "$FORCED" >"$SCRATCH/forced-${mode}.log" 2>&1 || { cat "$SCRATCH/forced-${mode}.log" >&2; fail "forced $mode rejected"; }
  python3 "$COMPOSE" "$FORCED" "$FORCED_HTML" >/dev/null
  if ! grep -q "data-initial-layout=\"$mode\"" "$FORCED_HTML"; then
    fail "layout=$mode did not force generated initial mode"
  fi
done
ok "explicit layout forces tree or centered"

# 27 — validate accepts explicit importance 1..5
IMPORTANCE_OK="$SCRATCH/importance-ok.json"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['root']['importance'] = 5
data['root']['children'][0]['importance'] = 3
data['root']['children'][1]['importance'] = 1
Path('$IMPORTANCE_OK').write_text(json.dumps(data, ensure_ascii=False))
"
python3 "$VALIDATE" "$IMPORTANCE_OK" >"$SCRATCH/importance-ok.log" 2>&1 || { cat "$SCRATCH/importance-ok.log" >&2; fail "valid importance rejected"; }
ok "validate-map accepts explicit importance 1..5"

# 28 — reject invalid importance values
for bad in 0 6 true; do
  BAD_IMPORTANCE="$SCRATCH/importance-${bad}.json"
  python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['root']['importance'] = json.loads('$bad')
Path('$BAD_IMPORTANCE').write_text(json.dumps(data, ensure_ascii=False))
"
  if python3 "$VALIDATE" "$BAD_IMPORTANCE" >/dev/null 2>&1; then
    fail "must reject importance=$bad"
  fi
done
ok "rejects invalid importance values"

# 29 — compose: variable bubble sizing is present
if ! grep -q 'function nodeMetrics' "$COMPOSE" || ! grep -q 'function nodeImportance' "$COMPOSE"; then
  fail "missing importance-to-metrics logic"
fi
if ! grep -q 'data-importance' "$COMPOSE" || ! grep -q 'metrics.radius' "$COMPOSE" || ! grep -q 'boxH' "$COMPOSE"; then
  fail "missing variable bubble dimensions"
fi
ok "compose-html maps importance to variable bubble size"

# 30 — explicit importance survives HTML JSON round-trip
IMPORTANCE_HTML="$SCRATCH/importance.html"
python3 "$COMPOSE" "$IMPORTANCE_OK" "$IMPORTANCE_HTML" >/dev/null
python3 -c "
import json, re
from pathlib import Path
html = Path('$IMPORTANCE_HTML').read_text()
m = re.search(r'<script id=\"map-data\" type=\"application/json\">(.*?)</script>', html, re.S)
assert m, 'map-data missing'
parsed = json.loads(m.group(1))
assert parsed['root']['importance'] == 5
assert parsed['root']['children'][0]['importance'] == 3
assert parsed['root']['children'][1]['importance'] == 1
" || fail "importance round-trip failed"
ok "importance round-trip intact"

# 31 — style proposal no longer offers academic
python3 -c "
from pathlib import Path
text = Path('$ROOT/mind-map/SKILL.md').read_text()
step0 = text.split('## Step 0: Style', 1)[1].split('## Step 1:', 1)[0].lower()
assert 'academic' not in step0, 'academic still appears in style proposal'
assert 'default when skipped:' in text.lower() and 'for all inputs' in text.lower()
" || fail "style proposal still offers academic"
ok "style proposal excludes academic"

# 32 — style question capped at 4 options (AskUserQuestion max), custom via Other
python3 -c "
import re
from pathlib import Path
text = Path('$ROOT/mind-map/SKILL.md').read_text()
step0 = text.split('## Step 0: Style', 1)[1].split('## Step 1:', 1)[0]
opts = re.findall(r'\`(\w+)\`', step0.split('Smart-skip', 1)[0].split('Custom style', 1)[0])
opts = [o for o in opts if o not in ('AskUserQuestion',)]
assert len(opts) == 4, f'expected 4 style options, got {len(opts)}: {opts}'
assert 'custom' not in opts, 'explicit custom option still offered'
assert 'Other' in step0, 'no automatic Other handling for custom style'
" || fail "style question exceeds 4 options"
ok "style question: exactly 4 options, custom via automatic Other"

# 33 — custom preset: tokens injected, missing ones fall back to warm
CUSTOM="$SCRATCH/custom.json"
CUSTOM_HTML="$SCRATCH/custom.html"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['meta']['preset'] = 'custom'
data['meta']['customTokens'] = {'accent': '#123abc', 'bg': '#101418', 'radius': '10px'}
Path('$CUSTOM').write_text(json.dumps(data, ensure_ascii=False))
"
python3 "$VALIDATE" "$CUSTOM" >"$SCRATCH/custom-validate.log" 2>&1 || { cat "$SCRATCH/custom-validate.log" >&2; fail "valid custom preset rejected"; }
python3 "$COMPOSE" "$CUSTOM" "$CUSTOM_HTML" >/dev/null 2>"$SCRATCH/custom-compose.log"
grep -q -- '--accent: #123abc;' "$CUSTOM_HTML" || fail "custom accent token not injected"
grep -q -- '--bg: #101418;' "$CUSTOM_HTML" || fail "custom bg token not injected"
grep -q -- '--radius: 10px;' "$CUSTOM_HTML" || fail "custom radius token not injected"
grep -q -- '--surface: #fffaf3;' "$CUSTOM_HTML" || fail "missing token must fall back to warm"
ok "custom preset: tokens injected, missing tokens fall back to warm"

# 34 — custom preset: unsafe token value dropped, no style breakout
EVIL="$SCRATCH/custom-evil.json"
EVIL_HTML="$SCRATCH/custom-evil.html"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['meta']['preset'] = 'custom'
data['meta']['customTokens'] = {'accent': 'red;} body{background:url(//evil)', 'bg': '#101418'}
Path('$EVIL').write_text(json.dumps(data, ensure_ascii=False))
"
python3 "$COMPOSE" "$EVIL" "$EVIL_HTML" >/dev/null 2>"$SCRATCH/evil-compose.log"
python3 -c "
from pathlib import Path
html = Path('$EVIL_HTML').read_text()
style = html.split('<style>', 1)[1].split('</style>', 1)[0]
assert 'url(//evil)' not in style, 'unsafe token value leaked into <style>'
assert '--accent: #8b5a2b;' in style, 'dropped token must fall back to warm accent'
assert '--bg: #101418;' in style, 'safe sibling token must still be injected'
" || fail "unsafe custom token handling"
grep -q 'ignoring unsafe custom token' "$SCRATCH/evil-compose.log" || fail "no stderr warning for unsafe token"
ok "custom preset: unsafe token dropped with warning, no CSS breakout"

# 35 — validate enforces the customTokens contract
for case in missing unknown unsafe; do
  BAD_CUSTOM="$SCRATCH/custom-$case.json"
  python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['meta']['preset'] = 'custom'
case = '$case'
if case == 'unknown':
    data['meta']['customTokens'] = {'font': 'serif'}
elif case == 'unsafe':
    data['meta']['customTokens'] = {'accent': 'red;} body{}'}
Path('$BAD_CUSTOM').write_text(json.dumps(data, ensure_ascii=False))
"
  if python3 "$VALIDATE" "$BAD_CUSTOM" >/dev/null 2>&1; then
    fail "validate must reject custom preset with $case customTokens"
  fi
done
ok "validate rejects custom preset with missing/unknown/unsafe tokens"

# 36 — search UX: auto-expand of collapsed ancestors + match counter
grep -q 'preSearchCollapsed' "$COMPOSE" || fail "search must snapshot/restore collapsed state"
grep -q 'ancestors.forEach(id => collapsed.delete(id))' "$COMPOSE" || fail "search must expand ancestors of matches"
grep -q 'search-count' "$COMPOSE" || fail "missing match counter"
grep -q 'id="search-count"' "$SCRATCH/valid.html" 2>/dev/null || python3 "$COMPOSE" "$VALID" "$SCRATCH/valid.html" >/dev/null
grep -q 'id="search-count"' "$SCRATCH/valid.html" || fail "search-count element absent from composed HTML"
ok "search auto-expands collapsed matches and shows a result counter"

# 37 — validate rejects label > 80 and note > 600
for field in label note; do
  LONG="$SCRATCH/long-$field.json"
  python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['root']['$field'] = 'x' * (81 if '$field' == 'label' else 601)
Path('$LONG').write_text(json.dumps(data))
"
  if python3 "$VALIDATE" "$LONG" >/dev/null 2>&1; then fail "must reject oversized $field"; fi
done
ok "rejects label > 80 chars and note > 600 chars"

# 38 — compose displays actual node count even when meta.nodeCount is wrong
WRONG_COUNT="$SCRATCH/wrong-count.json"
WRONG_HTML="$SCRATCH/wrong-count.html"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$VALID').read_text())
data['meta']['nodeCount'] = 999
Path('$WRONG_COUNT').write_text(json.dumps(data, ensure_ascii=False))
"
python3 "$VALIDATE" "$WRONG_COUNT" >"$SCRATCH/wrong-count.log" 2>&1 || fail "nodeCount mismatch must warn, not fail"
grep -q 'warn' "$SCRATCH/wrong-count.log" || fail "missing nodeCount mismatch warning"
python3 "$COMPOSE" "$WRONG_COUNT" "$WRONG_HTML" >/dev/null
if grep -q '999 nœuds' "$WRONG_HTML"; then fail "HTML shows declared count instead of actual"; fi
ACTUAL=$(python3 -c "
import json
from pathlib import Path
def count(n): return 1 + sum(count(c) for c in n.get('children') or [])
print(count(json.loads(Path('$VALID').read_text())['root']))
")
grep -q "$ACTUAL nœuds" "$WRONG_HTML" || fail "HTML missing actual node count ($ACTUAL)"
ok "compose shows actual node count, ignores wrong meta.nodeCount"

# 39 — schema doc and validator agree on limits (200/80/600)
python3 -c "
from pathlib import Path
schema = Path('$ROOT/mind-map/references/node-schema.md').read_text()
validator = Path('$VALIDATE').read_text()
assert '≤ 200 chars' in schema and 'MAX_SUMMARY = 200' in validator, 'summary limit mismatch'
assert '140' not in schema, 'stale 140-char summary limit in schema'
assert 'MAX_LABEL = 80' in validator and 'MAX_NOTE = 600' in validator, 'label/note limits missing'
assert 'customTokens' in schema, 'customTokens undocumented in schema'
" || fail "schema/validator limits diverge"
ok "node-schema.md limits match validate-map.py (200/80/600, customTokens)"

# 40 — escape hatches: no bare custom keyword, described-style row present
python3 -c "
from pathlib import Path
text = Path('$ROOT/mind-map/SKILL.md').read_text()
hatches = text.split('## Escape hatches', 1)[1].split('## Self-check', 1)[0]
assert '\`custom\`' not in hatches, 'bare custom keyword still a smart-skip trigger'
assert 'customTokens' in hatches, 'described-style escape hatch missing customTokens path'
" || fail "escape hatches still reference bare custom"
ok "escape hatches: described style routes to customTokens, no bare custom"

# 41 — click-to-focus: animated zoom centers on clicked branch, cancellable
grep -q 'function focusOn' "$COMPOSE" || fail "missing focusOn (zoom-to-branch)"
grep -q 'function subtreeBBox' "$COMPOSE" || fail "missing subtree bounding box"
grep -q 'function animateTo' "$COMPOSE" || fail "missing animated pan/zoom"
grep -q 'prefers-reduced-motion' "$COMPOSE" || fail "focus animation must respect reduced motion"
python3 -c "
from pathlib import Path
js = Path('$COMPOSE').read_text()
assert js.count('cancelAnim()') >= 3, 'wheel/drag/reset must cancel the focus animation'
assert 'focusOn(node)' in js, 'node activation must trigger focusOn'
assert 'if (expanding) focusOn(node)' in js, 'expanding a branch must refocus on it'
" || fail "focus wiring incomplete"
FOCUS_HTML="$SCRATCH/focus.html"
python3 "$COMPOSE" "$VALID" "$FOCUS_HTML" >/dev/null
grep -q 'function focusOn' "$FOCUS_HTML" || fail "focusOn absent from composed HTML"
ok "click-to-focus: animated zoom on branch, cancellable, reduced-motion aware"

# 42 — exploration UX: +N badge, animated overview (Escape/dblclick/reset), Enter cycles results
python3 -c "
from pathlib import Path
js = Path('$COMPOSE').read_text()
assert 'descendantCount' in js and \"'+' + descendantCount(node)\" in js, 'collapsed badge must show +N'
assert 'function overview' in js, 'missing animated overview return'
assert \"btn-reset').onclick = overview\" in js, 'reset button must use animated overview'
assert js.count('overview()') >= 2, 'Escape and dblclick must call overview'
assert 'dblclick' in js, 'missing dblclick-on-background return'
assert 'searchMatches' in js and 'searchIdx' in js, 'missing Enter result navigation'
assert 'focusOn(searchMatches[searchIdx])' in js, 'Enter must zoom to the match'
assert \"e.shiftKey ? -1 : 1\" in js, 'Shift+Enter must cycle backwards'
" || fail "exploration UX contract"
UX_HTML="$SCRATCH/ux.html"
python3 "$COMPOSE" "$VALID" "$UX_HTML" >/dev/null
grep -q 'descendantCount' "$UX_HTML" || fail "badge logic absent from composed HTML"
ok "exploration UX: +N badge, Escape/dblclick/reset overview, Enter cycles matches"

echo "Summary: $pass tests passed"
exit 0
