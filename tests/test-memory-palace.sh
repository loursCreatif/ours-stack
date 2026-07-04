#!/usr/bin/env bash
# Integration tests: memory-palace compose-html (visual plan, path, fallback).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE="$ROOT/memory-palace/scripts/compose-html.py"
MATERIALIZE="$ROOT/memory-palace/scripts/materialize-biomimetisme-study.sh"
FIXTURE="$ROOT/tests/fixtures/biomimetisme-memory-palace.json"
STUDY_DIR="$ROOT/studies/biomimetisme-locomotion-chantier"
STUDY_JSON="$STUDY_DIR/memory-palace.json"
SCRATCH="${MEMORY_PALACE_TEST_SCRATCH:-/var/folders/nb/hms4jttd77xfdkwyqtwbx79w0000gn/T/grok-goal-c77839e7534a/implementer}"
mkdir -p "$SCRATCH"

[ -f "$COMPOSE" ] || { echo "FAIL: missing $COMPOSE"; exit 1; }
[ -x "$MATERIALIZE" ] || { echo "FAIL: missing $MATERIALIZE"; exit 1; }
[ -f "$FIXTURE" ] || { echo "FAIL: missing $FIXTURE"; exit 1; }

pass=0
fail() { echo "FAIL: $*"; exit 1; }
ok() { echo "PASS: $*"; pass=$((pass + 1)); }

HTML_3D="$SCRATCH/palace-3d.html"
HTML_2D="$SCRATCH/palace-2d.html"
LOG="$SCRATCH/memory-palace-tests.log"
exec > >(tee "$LOG") 2>&1

STUDY_HTML="$STUDY_DIR/memory-palace.html"
bash "$MATERIALIZE" >"$SCRATCH/regen-study.log" 2>&1
[ -s "$STUDY_HTML" ] || { cat "$SCRATCH/regen-study.log" >&2; fail "materialize-biomimetisme-study.sh failed"; }
grep -q 'const PALACE_DATA' "$STUDY_HTML" || fail "study HTML missing PALACE_DATA"
ok "materialize-biomimetisme-study.sh: fixture → study json+html"

python3 "$COMPOSE" "$FIXTURE" -o "$HTML_3D" >/dev/null
python3 "$COMPOSE" "$FIXTURE" -o "$HTML_2D" --2d-only >/dev/null

[ -s "$HTML_3D" ] || fail "3D HTML empty"
[ -s "$HTML_2D" ] || fail "2D HTML empty"
ok "compose generates non-empty HTML from biomimetisme fixture"

if ! grep -q 'const PALACE_DATA' "$HTML_3D"; then
  fail "PALACE_DATA missing"
fi
ok "PALACE_DATA embedded"

# Shadows
for token in 'shadowMap.enabled' 'PCFSoftShadowMap' 'castShadow' 'receiveShadow'; do
  if ! grep -q "$token" "$HTML_3D"; then
    fail "missing shadow token: $token"
  fi
done
ok "soft shadows enabled in scene JS"

# Light scene (no old dark night background)
if grep -q 'scene\.fog = new THREE\.Fog' "$COMPOSE"; then
  fail "scene.fog must be removed per VISUAL-PLAN"
fi
if grep -q 'renderer\.setSize(window\.innerWidth' "$COMPOSE"; then
  fail "renderer must size to canvas client rect, not window"
fi
if ! grep -q 'resizeCanvas' "$COMPOSE" || ! grep -q 'canvas\.clientWidth' "$COMPOSE"; then
  fail "missing canvas clientWidth/clientHeight sizing"
fi
if grep -q '0x4a5568' "$HTML_3D"; then
  fail "old dark night background 0x4a5568 still present"
fi
if grep -q 'fill="#2a3040"' "$HTML_3D"; then
  fail "old dark iso fill #2a3040 still present"
fi
if ! grep -q 'pal.sky' "$HTML_3D"; then
  fail "light sky palette not used"
fi
ok "light architect-model palette (no night/dark iso fill)"

# Distinct archetype palettes in source
for theme in construction museum corridor library; do
  if ! grep -q "${theme}:" "$COMPOSE"; then
    fail "missing THEME entry: $theme"
  fi
done
ok "THEME palettes per archetype in compose source"

# Silhouette variety
for geom in 'ConeGeometry' 'roofVariant' 'addArchetypeDetail'; do
  if ! grep -q "$geom" "$HTML_3D"; then
    fail "missing silhouette logic: $geom"
  fi
done
ok "differentiated building silhouettes (roof variants + archetype details)"

# Memory path
for token in 'buildPathRoute' 'makeNumberSprite' 'stroke-dasharray' 'polyline'; do
  if ! grep -q "$token" "$HTML_3D"; then
    fail "missing path token: $token"
  fi
done
ok "numbered memory path in 3D and iso-SVG"

# Fit-to-bounds site framing
for token in 'computeSiteBoundsRaw' 'pathSpriteWorldPos' 'projectSiteExtents' 'fitSiteCamera' 'siteFitDist' 'preserveAspectRatio="xMidYMid meet"'; do
  if ! grep -q "$token" "$COMPOSE"; then
    fail "missing fit-to-bounds token: $token"
  fi
done
if ! grep -q 'allSpritesInView' "$COMPOSE"; then
  fail "missing sprite viewport metrics"
fi
ok "fit-to-bounds camera + iso viewBox in compose source"

# Fallback boot
for token in 'enableIsoMode' 'buildIsoSvg' 'WebGL relief failed'; do
  if ! grep -q "$token" "$HTML_3D"; then
    fail "missing fallback token: $token"
  fi
done
if ! grep -q 'try {' "$HTML_3D" || ! grep -q 'initRelief();' "$HTML_3D"; then
  fail "initRelief not wrapped in try/catch"
fi
ok "WebGL try/catch + enableIsoMode fallback"

# FORCE_2D flag in 2D build
if ! grep -q 'window.FORCE_2D = true' "$HTML_2D"; then
  fail "2D build must set FORCE_2D true"
fi
ok "FORCE_2D set in --2d-only output"

# Path numbering wired to fixture path[] (dynamic idx+1, not hardcoded)
python3 -c "
import json, re
from pathlib import Path
fixture = json.loads(Path('$FIXTURE').read_text())
path_len = len(fixture['path'])
html = Path('$HTML_3D').read_text()
assert 'buildPathRoute' in html
assert 'makeNumberSprite(idx + 1)' in html
assert \"(idx + 1) + '</text>'\" in html
assert html.count('data.path.forEach') >= 2
# PALACE_DATA path length must match fixture (embedded JSON, not mocked)
m = re.search(r'const PALACE_DATA = (\{.*?\});\s*window\.FORCE_2D', html, re.S)
data = json.loads(m.group(1))
assert len(data['path']) == path_len
" || fail "path numbering wiring mismatch"
ok "path numbering driven by fixture path[]"

# WebGL failure simulation — stub THREE.WebGLRenderer at runtime, assert iso fallback boots
WEBGL_LOG="$SCRATCH/webgl-fallback.log"
if command -v npx >/dev/null 2>&1 && npx playwright --version >/dev/null 2>&1; then
  if [ ! -d "$SCRATCH/node_modules/playwright" ]; then
    (cd "$SCRATCH" && npm init -y >/dev/null 2>&1 && npm install playwright@1.61.1 >/dev/null 2>&1)
  fi
  cat >"$SCRATCH/webgl-fallback-boot.mjs" <<'MJS'
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const html = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage();
const consoleLines = [];
const errors = [];
page.on("console", msg => consoleLines.push(`[${msg.type()}] ${msg.text()}`));
page.on("pageerror", e => errors.push(String(e)));
await page.addInitScript(() => {
  const origGetContext = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, attrs) {
    const t = String(type || "").toLowerCase();
    if (t === "webgl" || t === "webgl2" || t === "experimental-webgl") {
      throw new Error("STUB: WebGL context creation failed");
    }
    return origGetContext.call(this, type, attrs);
  };
  window.__palaceWebglStubbed = true;
});
await page.goto(pathToFileURL(html).href, { waitUntil: "domcontentloaded" });
await page.click("#overlay-first");
await page.waitForTimeout(400);
const state = await page.evaluate(() => {
  const canvas = document.getElementById("relief-canvas");
  const iso = document.getElementById("iso-map");
  const svg = iso?.querySelector("svg");
  return {
    force2d: window.FORCE_2D,
    canvasHidden: canvas?.classList.contains("hidden"),
    canvasDisplay: canvas ? getComputedStyle(canvas).display : null,
    isoHidden: iso?.classList.contains("hidden"),
    isoDisplay: iso ? getComputedStyle(iso).display : null,
    hasSvg: !!svg,
    polylines: iso?.querySelectorAll("polyline").length ?? 0,
    numbers: [...(iso?.querySelectorAll("text") ?? [])].filter(t => /^\d+$/.test(t.textContent.trim())).length,
    buildings: iso?.querySelectorAll(".iso-bld").length ?? 0,
    stubbed: !!window.__palaceWebglStubbed
  };
});
const report = { state, consoleLines, errors, html };
console.log(JSON.stringify(report, null, 2));
await browser.close();
if (!state.stubbed) process.exit(2);
if (state.force2d) process.exit(3);
if (!state.canvasHidden) process.exit(4);
if (state.isoHidden || state.isoDisplay === "none") process.exit(5);
if (!state.hasSvg || state.polylines < 1) process.exit(6);
if (state.numbers < 7) process.exit(7);
if (state.buildings < 7) process.exit(8);
if (!consoleLines.some(l => l.includes("WebGL relief failed"))) process.exit(9);
MJS
  {
    echo "=== WebGL fallback runtime boot ==="
    (cd "$SCRATCH" && node webgl-fallback-boot.mjs "$HTML_3D")
  } >"$WEBGL_LOG" 2>&1 || {
    cat "$WEBGL_LOG" >&2
    fail "WebGL stub runtime fallback boot failed"
  }
  python3 -c "
import json
from pathlib import Path
raw = Path('$WEBGL_LOG').read_text()
start = raw.index('{')
report = json.loads(raw[start:])
s = report['state']
assert s['stubbed'], 'getContext webgl stub not applied'
assert s['canvasHidden'], 'canvas must be hidden after fallback'
assert not s['isoHidden'] and s['isoDisplay'] != 'none', 'iso-map must be visible'
assert s['hasSvg'] and s['polylines'] >= 1, 'iso SVG route missing'
assert s['numbers'] >= 7, 'path numbers missing in iso fallback'
assert s['buildings'] >= 7, 'buildings missing in iso fallback'
assert any('WebGL relief failed' in l for l in report.get('consoleLines', [])), 'missing fallback console warn'
" || fail "webgl-fallback.log state assertions failed"
  ok "WebGL stub throws → hidden canvas + populated iso-map (runtime)"
else
  {
    echo "playwright unavailable — cannot run WebGL stub runtime boot"
    grep -q 'enableIsoMode' "$COMPOSE" || exit 1
    grep -q 'catch' "$HTML_3D" || exit 1
  } >"$WEBGL_LOG" 2>&1 || fail "webgl fallback unavailable and no structural fallback"
  ok "WebGL fallback structural only (playwright unavailable)"
fi

# FORCE_2D DOM boot via playwright
FORCE2D_DOM="$SCRATCH/force2d-dom.txt"
if command -v npx >/dev/null 2>&1 && npx playwright --version >/dev/null 2>&1; then
  if [ ! -d "$SCRATCH/node_modules/playwright" ]; then
    (cd "$SCRATCH" && npm init -y >/dev/null 2>&1 && npm install playwright@1.61.1 >/dev/null 2>&1)
  fi
  cat >"$SCRATCH/force2d-boot.mjs" <<'MJS'
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const html = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage();
const errors = [];
page.on("pageerror", e => errors.push(String(e)));
await page.goto(pathToFileURL(html).href, { waitUntil: "domcontentloaded" });
await page.click("#overlay-first");
const iso = await page.$eval("#iso-map", el => ({
  hidden: el.classList.contains("hidden"),
  display: getComputedStyle(el).display,
  svg: el.querySelector("svg") !== null,
  polylines: el.querySelectorAll("polyline").length,
  numbers: [...el.querySelectorAll("text")].filter(t => /^\d+$/.test(t.textContent.trim())).length
}));
console.log(JSON.stringify({ errors, iso }));
await browser.close();
if (errors.length) process.exit(2);
if (iso.hidden || iso.display === "none" || !iso.svg || iso.polylines < 1 || iso.numbers < 7) process.exit(3);
MJS
  (cd "$SCRATCH" && node force2d-boot.mjs "$HTML_2D") >"$FORCE2D_DOM" 2>&1 || {
    cat "$FORCE2D_DOM" >&2
    fail "FORCE_2D playwright boot failed"
  }
  ok "FORCE_2D populates visible iso-map with path (playwright)"
else
  echo "playwright unavailable — structural fallback only" >"$FORCE2D_DOM"
  if ! grep -q 'iso-map' "$HTML_2D" && ! grep -q 'buildIsoSvg' "$HTML_2D"; then
    fail "2D HTML missing iso-map logic"
  fi
  ok "FORCE_2D structural check (no playwright)"
fi

# Launch screenshots 3D + 2D
if command -v npx >/dev/null 2>&1 && npx playwright --version >/dev/null 2>&1; then
  if [ ! -d "$SCRATCH/node_modules/playwright" ]; then
    (cd "$SCRATCH" && npm init -y >/dev/null 2>&1 && npm install playwright@1.61.1 >/dev/null 2>&1)
  fi
  cat >"$SCRATCH/launch-3d-verify.mjs" <<'MJS'
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const [html, outPng] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
const errors = [];
page.on("pageerror", e => errors.push(String(e)));
await page.goto(pathToFileURL(html).href, { waitUntil: "domcontentloaded" });
const panelClosed = await page.evaluate(() => {
  const panel = document.getElementById("detail-panel");
  return panel.hidden || getComputedStyle(panel).display === "none";
});
await page.click("#overlay-first");
await page.waitForTimeout(900);
const report = await page.evaluate(() => {
  const canvas = document.getElementById("relief-canvas");
  const panel = document.getElementById("detail-panel");
  const metrics = typeof window.__palaceMetrics === "function" ? window.__palaceMetrics() : null;
  return {
    metrics,
    panelClosed: panel.hidden || getComputedStyle(panel).display === "none",
    canvasVisible: canvas && canvas.clientWidth > 200 && canvas.clientHeight > 200,
    canvasFullWidth: canvas && canvas.clientWidth >= window.innerWidth - 320
  };
});
const pixels = await page.evaluate(() => {
  const canvas = document.getElementById("relief-canvas");
  const gl = canvas.getContext("webgl") || canvas.getContext("webgl2");
  const samples = [];
  if (gl && canvas.width > 0 && canvas.height > 0) {
    const buf = new Uint8Array(4);
    const fracs = [[0.5, 0.5], [0.25, 0.4], [0.75, 0.55], [0.4, 0.7]];
    for (const [fx, fy] of fracs) {
      const x = Math.floor(canvas.width * fx);
      const y = Math.floor(canvas.height * (1 - fy));
      gl.readPixels(x, y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, buf);
      samples.push([buf[0], buf[1], buf[2]]);
    }
  }
  const uniq = new Set(samples.map(s => s.join(",")));
  return {
    samples,
    paintedVaried: uniq.size >= 2,
    notBlack: samples.some(s => s[0] + s[1] + s[2] > 60),
    lightPalette: samples.some(s => s[0] > 140 && s[1] > 130)
  };
});
report.pixels = pixels;
report.panelClosedBeforeOverlay = panelClosed;
await page.screenshot({ path: outPng, fullPage: false });
console.log(JSON.stringify({ errors, report, outPng }));
await browser.close();
if (errors.length) process.exit(2);
const m = report.metrics;
if (!m) process.exit(4);
if (!report.panelClosedBeforeOverlay || !report.panelClosed) process.exit(5);
if (!report.canvasVisible || !report.canvasFullWidth) process.exit(6);
if (!m.usesClientSizing) process.exit(7);
if (m.hasFog) process.exit(8);
if (m.pathSprites < m.pathSteps) process.exit(9);
if (!m.allSpritesInView || m.spritesInView < m.pathSteps) process.exit(10);
const ext = m.siteExtents;
if (!ext) process.exit(12);
if (ext.spanNx < 0.63 || ext.spanNy < 0.55) process.exit(13);
if (ext.minNx < 0.07 || ext.maxNx > 0.93 || ext.minNy < 0.07 || ext.maxNy > 0.93) process.exit(14);
if (ext.minNx > 0.20 || ext.maxNx < 0.80) process.exit(15);
if (ext.minNy > 0.12 || ext.maxNy < 0.85) process.exit(16);
if (m.spriteSpreadNx < 0.45 || m.spriteSpreadNy < 0.45) process.exit(17);
const px = report.pixels;
if (!px.paintedVaried || !px.notBlack || !px.lightPalette) process.exit(11);
MJS
  cat >"$SCRATCH/iso-fit-verify.mjs" <<'MJS'
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const html = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
await page.goto(pathToFileURL(html).href, { waitUntil: "domcontentloaded" });
await page.click("#overlay-first");
await page.waitForTimeout(400);
const iso = await page.evaluate(() => {
  const wrap = document.getElementById("iso-map");
  const svg = wrap.querySelector("svg");
  const vb = svg?.viewBox?.baseVal;
  const wrapRect = wrap.getBoundingClientRect();
  const inWrap = r => r.right > wrapRect.left && r.left < wrapRect.right && r.bottom > wrapRect.top && r.top < wrapRect.bottom;
  const nums = [...wrap.querySelectorAll("text")].filter(t => /^\d+$/.test(t.textContent.trim()));
  const bids = new Set([...wrap.querySelectorAll(".iso-bld[data-bid]")].map(el => el.dataset.bid));
  const bidRects = [...bids].map(bid => {
    const els = [...wrap.querySelectorAll('.iso-bld[data-bid="' + bid + '"]')];
    let minL = Infinity, minT = Infinity, maxR = -Infinity, maxB = -Infinity;
    els.forEach(el => {
      const r = el.getBoundingClientRect();
      minL = Math.min(minL, r.left); minT = Math.min(minT, r.top);
      maxR = Math.max(maxR, r.right); maxB = Math.max(maxB, r.bottom);
    });
    return { bid, rect: { left: minL, top: minT, right: maxR, bottom: maxB } };
  });
  return {
    viewBox: vb ? { x: vb.x, y: vb.y, w: vb.width, h: vb.height } : null,
    distinctBuildings: bids.size,
    buildingsVisible: bidRects.filter(b => inWrap(b.rect)).length,
    numbersVisible: nums.filter(n => inWrap(n.getBoundingClientRect())).length,
    numbersTotal: nums.length
  };
});
console.log(JSON.stringify(iso));
await browser.close();
if (!iso.viewBox || iso.distinctBuildings < 7) process.exit(2);
if (iso.numbersVisible !== 7 || iso.numbersTotal !== 7) process.exit(3);
if (iso.buildingsVisible < 7) process.exit(4);
MJS
  cat >"$SCRATCH/panel-resize-verify.mjs" <<'MJS'
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const html = process.argv[2];
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
await page.goto(pathToFileURL(html).href, { waitUntil: "domcontentloaded" });
await page.click("#overlay-first");
await page.waitForTimeout(600);
const opened = await page.evaluate(() => {
  document.getElementById("detail-panel").hidden = false;
  return new Promise(resolve => {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const m = window.__palaceMetrics();
        resolve({
          narrowerWithPanel: m.clientW < window.innerWidth - 150,
          usesClientSizing: m.usesClientSizing,
          aspectMatch: Math.abs(m.aspectCanvas - m.aspectClient) < 0.02
        });
      });
    });
  });
});
console.log(JSON.stringify(opened));
await browser.close();
if (!opened.narrowerWithPanel || !opened.usesClientSizing) process.exit(2);
MJS
  cat >"$SCRATCH/launch-2d-verify.mjs" <<'MJS'
import { chromium } from "playwright";
import { pathToFileURL } from "url";
const [html, outPng] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
const errors = [];
page.on("pageerror", e => errors.push(String(e)));
await page.goto(pathToFileURL(html).href, { waitUntil: "domcontentloaded" });
await page.click("#overlay-first");
await page.waitForTimeout(400);
const iso = await page.$eval("#iso-map", el => ({
  hidden: el.classList.contains("hidden"),
  display: getComputedStyle(el).display,
  svg: el.querySelector("svg") !== null,
  polylines: el.querySelectorAll("polyline").length,
  numbers: [...el.querySelectorAll("text")].filter(t => /^\d+$/.test(t.textContent.trim())).length,
  svgWidth: el.querySelector("svg")?.getBoundingClientRect().width ?? 0
}));
await page.screenshot({ path: outPng, fullPage: false });
console.log(JSON.stringify({ errors, iso, outPng }));
await browser.close();
if (errors.length) process.exit(2);
if (iso.hidden || iso.display === "none" || !iso.svg || iso.polylines < 1 || iso.numbers < 7 || iso.svgWidth < 100) process.exit(3);
MJS
  (cd "$SCRATCH" && node launch-3d-verify.mjs "$HTML_3D" "$SCRATCH/launch-3d-framed.png") >"$SCRATCH/launch-3d.log" 2>&1 || {
    cat "$SCRATCH/launch-3d.log" >&2
    fail "3D launch verification failed"
  }
  (cd "$SCRATCH" && node launch-2d-verify.mjs "$HTML_2D" "$SCRATCH/launch-2d.png") >"$SCRATCH/launch-2d.log" 2>&1 || {
    cat "$SCRATCH/launch-2d.log" >&2
    fail "2D launch verification failed"
  }
  (cd "$SCRATCH" && node iso-fit-verify.mjs "$HTML_2D") >"$SCRATCH/iso-fit-dom.txt" 2>&1 || {
    cat "$SCRATCH/iso-fit-dom.txt" >&2
    fail "iso fit verification failed"
  }
  (cd "$SCRATCH" && node panel-resize-verify.mjs "$HTML_3D") >"$SCRATCH/panel-closed-dom.txt" 2>&1 || {
    cat "$SCRATCH/panel-closed-dom.txt" >&2
    fail "panel resize scenario failed"
  }
  [ -f "$SCRATCH/launch-3d-framed.png" ] && [ -s "$SCRATCH/launch-3d-framed.png" ] || fail "launch-3d-framed.png missing"
  [ -f "$SCRATCH/launch-2d.png" ] && [ -s "$SCRATCH/launch-2d.png" ] || fail "launch-2d.png missing"
  python3 -c "
import json
from pathlib import Path
raw = Path('$SCRATCH/launch-3d.log').read_text()
log = json.loads(raw[raw.index('{'):])
m = log['report']['metrics']
assert log['report']['panelClosed'], 'panel must stay closed on load'
assert m['allSpritesInView'], 'all path sprites must be in viewport'
assert m['spritesInView'] == m['pathSteps'], 'sprite count mismatch'
ext = m['siteExtents']
assert ext and ext['spanNx'] >= 0.63, 'site must fill viewport width'
assert ext['minNy'] <= 0.12 and ext['maxNy'] >= 0.85, 'vertical ~10% margin binds'
assert ext['minNx'] <= 0.20, 'not excess horizontal letterboxing'
assert m['spriteSpreadNx'] >= 0.42, 'sprites must span frame'
px = log['report']['pixels']
assert px['paintedVaried'] and px['lightPalette'], '3D must show varied light render'
iso = json.loads(Path('$SCRATCH/iso-fit-dom.txt').read_text())
assert iso['distinctBuildings'] == 7 and iso['numbersVisible'] == 7, 'iso must show 7 distinct buildings'
" || fail "framing verification logs insufficient"
  ok "playwright 3D: all path sprites in viewport, panel closed, framed screenshot"
  ok "playwright iso-SVG fit shows all 7 buildings and numbers"
  ok "panel resize scenario separate from closed-on-load"
else
  echo "playwright unavailable" >"$SCRATCH/launch-fallback.log"
  ok "launch fallback logged (no playwright)"
fi

# --- Baseline count before immersion extension (regression suite) ---
EXISTING_PASSES=$pass
echo "EXISTING_BASELINE: $EXISTING_PASSES tests passed before immersion checks"

# --- Immersion: structural tokens in compose source ---
[ -x "$MATERIALIZE" ] || fail "materialize script not executable"
grep -q 'biomimetisme-memory-palace.json' "$MATERIALIZE" || fail "materialize script must reference canonical fixture"
for token in 'Visite guidée' 'btn-tour' 'tour-nav' 'scene-block' 'scene.image' 'startTour' 'endTour' 'computeTourPose' 'buildingBBoxCorners' 'getTourFramingMetrics' 'setPathSpritesVisible' 'buildingColors' 'makeSkyTexture' 'foliageAnim' 'iso-tree' 'skyGrad'; do
  if ! grep -q "$token" "$COMPOSE"; then
    fail "missing immersion token in compose: $token"
  fi
done
if ! grep -q 'sun.position.set(58, 9, 32)' "$COMPOSE"; then
  fail "low afternoon sun position missing in compose source"
fi
ok "immersion structural tokens in compose source (incl. low sun)"

# --- Immersion: 7 scenes in biomimetisme fixture ---
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$FIXTURE').read_text())
path = data['path']
loci = {l['id']: l for l in data['loci']}
scenes = 0
for bid in path:
    loc = loci[bid]
    assert 'scene' in loc, f'missing scene on {bid}'
    assert loc['scene'].get('image'), f'empty scene.image on {bid}'
    senses = loc['scene'].get('senses', [])
    assert 2 <= len(senses) <= 3, f'senses count on {bid}: {len(senses)}'
    scenes += 1
assert scenes == 7, f'expected 7 scenes, got {scenes}'
" || fail "biomimetisme fixture scene validation"
ok "biomimetisme fixture has 7 mental scenes"

# --- Study evidence (verification plan step 3) — fixture → study sync + audit ---
python3 -c "
import json, hashlib
from pathlib import Path
fixture = Path('$FIXTURE')
study_json = Path('$STUDY_JSON')
study_html = Path('$STUDY_HTML')
data = json.loads(fixture.read_text())
loci = {l['id']: l for l in data['loci']}
scenes = []
for bid in data['path']:
    loc = loci[bid]
    sc = loc.get('scene', {})
    scenes.append({
        'locus': bid,
        'image_len': len(sc.get('image', '')),
        'senses_count': len(sc.get('senses', [])),
        'image_preview': sc.get('image', '')[:60]
    })
evidence = {
    'contract': {
        'canonical_source_tracked': 'tests/fixtures/biomimetisme-memory-palace.json',
        'materialize_script': 'memory-palace/scripts/materialize-biomimetisme-study.sh',
        'study_target_gitignored': True,
        'study_target_note': 'studies/biomimetisme-locomotion-chantier/ is gitignored; not in CHANGED_FILES — materialized at test/runtime only'
    },
    'canonical_fixture': str(fixture),
    'study_json': str(study_json),
    'study_html': str(study_html),
    'fixture_sha256': hashlib.sha256(fixture.read_bytes()).hexdigest(),
    'study_json_sha256': hashlib.sha256(study_json.read_bytes()).hexdigest(),
    'study_html_bytes': study_html.stat().st_size if study_html.is_file() else 0,
    'path_len': len(data['path']),
    'scene_count': len(scenes),
    'scenes': scenes,
    'materialize_verified': True
}
out = Path('$SCRATCH/study-evidence.json')
out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2))
assert evidence['scene_count'] == 7
assert evidence['study_json_sha256'] == evidence['fixture_sha256']
assert evidence['study_html_bytes'] > 100000
" || fail "study-evidence.json generation failed"
[ -s "$SCRATCH/study-evidence.json" ] || fail "study-evidence.json missing"
ok "materialize study evidence: fixture sha matches study json on disk"

# --- Immersion: scenes embedded in generated HTML ---
python3 -c "
import json, re
from pathlib import Path
fixture = json.loads(Path('$FIXTURE').read_text())
html = Path('$STUDY_HTML').read_text()
m = re.search(r'const PALACE_DATA = (\{.*?\});\s*window\.FORCE_2D', html, re.S)
data = json.loads(m.group(1))
for bid in data['path']:
    loc = next(l for l in data['loci'] if l['id'] == bid)
    assert loc.get('scene', {}).get('image'), f'scene missing in PALACE_DATA for {bid}'
    assert loc['scene']['image'] in html, f'scene.image not in HTML for {bid}'
" || fail "PALACE_DATA scenes not embedded in study HTML"
ok "mental scenes embedded in study HTML"

# --- Immersion: retrocompat JSON without scene ---
RETRO_JSON="$SCRATCH/retro-no-scene.json"
RETRO_HTML="$SCRATCH/retro-no-scene.html"
python3 -c "
import json
from pathlib import Path
data = json.loads(Path('$FIXTURE').read_text())
for loc in data['loci']:
    loc.pop('scene', None)
Path('$RETRO_JSON').write_text(json.dumps(data, ensure_ascii=False, indent=2))
" 
python3 "$COMPOSE" "$RETRO_JSON" -o "$RETRO_HTML" >/dev/null
grep -q 'if (scene && scene.image)' "$COMPOSE" || fail "showPanel scene guard missing"
grep -q 'showPanel(concepts, title, subtitle, scene)' "$COMPOSE" || fail "showPanel scene param missing"
ok "retrocompat: scene-block gated on scene.image in compose source"

# --- Immersion Playwright: guided tour + iso parity + screenshots ---
IMMERSION_LOG="$SCRATCH/immersion-tour.log"
if command -v npx >/dev/null 2>&1 && npx playwright --version >/dev/null 2>&1; then
  if [ ! -d "$SCRATCH/node_modules/playwright" ]; then
    (cd "$SCRATCH" && npm init -y >/dev/null 2>&1 && npm install playwright@1.61.1 >/dev/null 2>&1)
  fi
  cat >"$SCRATCH/immersion-tour.mjs" <<'MJS'
import { chromium } from "playwright";
import { pathToFileURL } from "url";
import { readFileSync } from "fs";

const [html3d, html2d, outCarte, outStop1, outIso, fixturePath] = process.argv.slice(2);
const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));
const loci = Object.fromEntries(fixture.loci.map(l => [l.id, l]));
const pathLen = fixture.path.length;
const firstSceneImage = loci[fixture.path[0]].scene.image;

const browser = await chromium.launch();
const errors = [];

async function run3d() {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on("pageerror", e => errors.push(String(e)));
  await page.goto(pathToFileURL(html3d).href, { waitUntil: "domcontentloaded" });
  await page.click("#overlay-first");
  await page.waitForTimeout(500);
  await page.screenshot({ path: outCarte, fullPage: false });
  const before = await page.evaluate(() => window.__palaceMetrics());
  await page.click("#btn-tour");
  await page.waitForTimeout(200);
  const midDescent = await page.evaluate(() => window.__palaceMetrics().cameraY);
  await page.waitForTimeout(1000);
  await page.screenshot({ path: outStop1, fullPage: false });
  const afterStart = await page.evaluate(() => {
    const m = window.__palaceMetrics();
    const panel = document.getElementById("detail-panel");
    const sceneImg = document.querySelector(".scene-image");
    return {
      m,
      tourActive: m.tourActive,
      cameraY: m.cameraY,
      tourStop: m.tourStop,
      tourFraming: m.tourFraming,
      panelOpen: !panel.hidden,
      sceneText: sceneImg?.textContent || "",
      btnMapVisible: !document.getElementById("btn-map-view").hidden
    };
  });
  for (let i = 0; i < pathLen - 1; i++) {
    await page.click("#tour-next");
    await page.waitForTimeout(700);
  }
  const atEnd = await page.evaluate(() => window.__palaceMetrics().tourStop);
  await page.keyboard.press("Escape");
  await page.waitForTimeout(900);
  const afterEsc = await page.evaluate(() => window.__palaceMetrics());
  await page.close();
  return { before, midDescent, afterStart, atEnd, afterEsc, firstSceneImage };
}

async function run2d() {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on("pageerror", e => errors.push(String(e)));
  await page.goto(pathToFileURL(html2d).href, { waitUntil: "domcontentloaded" });
  await page.click("#overlay-first");
  await page.waitForTimeout(400);
  await page.click("#btn-tour");
  await page.waitForTimeout(400);
  const iso = await page.evaluate(() => {
    const panel = document.getElementById("detail-panel");
    const sceneImg = document.querySelector(".scene-image");
    const active = document.querySelector(".iso-tour-active");
    return {
      tourNavVisible: !document.getElementById("tour-nav").hidden,
      panelOpen: !panel.hidden,
      sceneText: sceneImg?.textContent || "",
      hasHighlight: !!active,
      hasSkyGrad: !!document.querySelector("#iso-map svg defs linearGradient")
    };
  });
  await page.screenshot({ path: outIso, fullPage: false });
  await page.close();
  return iso;
}

const r3d = await run3d();
const r2d = await run2d();
await browser.close();

const report = { errors, r3d, r2d };
console.log(JSON.stringify(report, null, 2));

if (errors.length) process.exit(2);
if (!r3d.afterStart.tourActive) process.exit(3);
if (!(r3d.midDescent > 3 && r3d.midDescent < r3d.before.cameraY - 5)) process.exit(15);
if (r3d.afterStart.cameraY >= 3) process.exit(4);
if (r3d.afterStart.tourStop !== 0) process.exit(5);
if (!r3d.afterStart.panelOpen) process.exit(6);
if (!r3d.afterStart.sceneText || r3d.afterStart.sceneText.length < 20) process.exit(7);
if (r3d.atEnd !== pathLen - 1) process.exit(8);
if (r3d.afterEsc.cameraY <= r3d.afterStart.cameraY) process.exit(9);
if (!r3d.afterEsc.allSpritesInView) process.exit(10);
if (!r2d.tourNavVisible) process.exit(11);
if (!r2d.panelOpen || !r2d.sceneText) process.exit(12);
if (!r2d.hasHighlight) process.exit(13);
if (!r2d.hasSkyGrad) process.exit(14);
const fr = r3d.afterStart.tourFraming;
if (!fr) process.exit(16);
if (!fr.allCornersInView) process.exit(17);
if (fr.projectedHeightRatio < 0.35 || fr.projectedHeightRatio > 0.65) process.exit(18);
if (!fr.pathSpritesHidden) process.exit(19);
MJS
  {
    echo "=== Immersion guided tour ==="
    (cd "$SCRATCH" && node immersion-tour.mjs \
      "$STUDY_HTML" "$HTML_2D" \
      "$SCRATCH/screenshot-carte.png" \
      "$SCRATCH/screenshot-visite-stop1.png" \
      "$SCRATCH/screenshot-iso-visite.png" \
      "$FIXTURE")
  } >"$IMMERSION_LOG" 2>&1 || {
    cat "$IMMERSION_LOG" >&2
    fail "immersion tour Playwright failed"
  }
  for png in screenshot-carte.png screenshot-visite-stop1.png screenshot-iso-visite.png; do
    [ -s "$SCRATCH/$png" ] || fail "missing or empty $png"
  done
  python3 -c "
import json
from pathlib import Path
raw = Path('$IMMERSION_LOG').read_text()
report = json.loads(raw[raw.index('{'):])
assert not report.get('errors'), report.get('errors')
r = report['r3d']['afterStart']
assert r['cameraY'] < 3
assert r['tourStop'] == 0
assert report['r3d']['atEnd'] == 6
assert report['r3d']['afterEsc']['cameraY'] > r['cameraY']
assert report['r2d']['hasHighlight']
mid = report['r3d']['midDescent']
before_y = report['r3d']['before']['cameraY']
fr = report['r3d']['afterStart'].get('tourFraming') or report['r3d']['afterStart']['m'].get('tourFraming')
assert fr, 'tourFraming metrics missing'
assert fr.get('allCornersInView'), fr
assert 0.35 <= fr.get('projectedHeightRatio', 0) <= 0.65, fr
assert fr.get('pathSpritesHidden'), fr
assert mid > 3 and mid < before_y - 5, f'tour must ease mid-descent, got mid={mid} before={before_y}'
" || fail "immersion-tour.log assertions failed"
  ok "immersion Playwright: guided tour eye-level, scene panel, escape restore, iso parity"
  ok "immersion screenshots captured (carte, stop1, iso-visite)"
  ok "visual framing: tour stop bbox in view, height ratio 0.35-0.65, badges hidden"

  if [ ! -d "$SCRATCH/node_modules/pngjs" ]; then
    (cd "$SCRATCH" && npm install pngjs@7.0.0 >/dev/null 2>&1)
  fi
  cat >"$SCRATCH/analyze-visual-png.mjs" <<'MJS'
import { readFileSync, writeFileSync } from "fs";
import { PNG } from "pngjs";

const [stop1Path, cartePath, framingLog, paletteLog] = process.argv.slice(2);

function luminance(r, g, b) {
  return 0.299 * r + 0.587 * g + 0.114 * b;
}

function loadRgb(path) {
  const png = PNG.sync.read(readFileSync(path));
  const pixels = [];
  for (let i = 0; i < png.data.length; i += 4) {
    pixels.push([png.data[i], png.data[i + 1], png.data[i + 2]]);
  }
  return { w: png.width, h: png.height, pixels };
}

function pixelVariance(path) {
  const { pixels } = loadRgb(path);
  const lums = pixels.map(([r, g, b]) => luminance(r, g, b));
  const mean = lums.reduce((a, b) => a + b, 0) / lums.length;
  return lums.reduce((a, v) => a + (v - mean) ** 2, 0) / lums.length;
}

function analyzePalette(path) {
  const { w, h, pixels } = loadRgb(path);
  const building = [];
  const hueBins = new Set();
  for (let y = Math.floor(h * 0.12); y < Math.floor(h * 0.92); y++) {
    for (let x = 0; x < w; x++) {
      const [r, g, b] = pixels[y * w + x];
      const lum = luminance(r, g, b);
      const sat = Math.max(r, g, b) - Math.min(r, g, b);
      if (lum > 215 && sat < 28) continue;
      if (lum < 95) continue;
      building.push(lum);
      hueBins.add(`${Math.floor(r / 40)},${Math.floor(g / 40)},${Math.floor(b / 40)}`);
    }
  }
  const meanLum = building.length ? building.reduce((a, b) => a + b, 0) / building.length : 0;
  return { meanLum, hues: hueBins.size, count: building.length };
}

const varStop = pixelVariance(stop1Path);
writeFileSync(framingLog, JSON.stringify({
  screenshot: stop1Path,
  pixelVariance: varStop,
  minVariance: 500
}, null, 2));
if (varStop < 500) process.exit(21);

const pal = analyzePalette(cartePath);
writeFileSync(paletteLog, JSON.stringify({
  screenshot: cartePath,
  meanBuildingLuminance: pal.meanLum,
  distinctHueBins: pal.hues,
  samplePixels: pal.count,
  minMeanLuminance: 140,
  minDistinctHues: 4
}, null, 2));
if (pal.count <= 1000) process.exit(22);
if (pal.meanLum <= 140) process.exit(23);
if (pal.hues < 4) process.exit(24);
MJS
  (cd "$SCRATCH" && node analyze-visual-png.mjs \
    "$SCRATCH/screenshot-visite-stop1.png" \
    "$SCRATCH/screenshot-carte.png" \
    "$SCRATCH/visual-framing.log" \
    "$SCRATCH/visual-palette.log") || fail "visual palette/framing PNG analysis failed"
  ok "visual palette: carte buildings luminous (>140) with >=4 distinct hues"
else
  echo "playwright unavailable — immersion runtime skipped" >"$IMMERSION_LOG"
  ok "immersion structural only (playwright unavailable)"
fi

EMIT_CLOSURE="$ROOT/memory-palace/scripts/emit-goal-closure.sh"
[ -x "$EMIT_CLOSURE" ] || fail "missing emit-goal-closure.sh"
bash "$EMIT_CLOSURE" "$SCRATCH"
[ -s "$SCRATCH/goal-closure.md" ] || fail "goal-closure.md missing"
[ -s "$SCRATCH/changed-files-tracked.txt" ] || fail "changed-files-tracked.txt missing"
[ -s "$SCRATCH/final-response-paste.md" ] || fail "final-response-paste.md missing"
[ -s "$SCRATCH/FINAL_RESPONSE.md" ] || fail "FINAL_RESPONSE.md missing"
if ! cmp -s "$SCRATCH/goal-closure.md" "$SCRATCH/final-response-paste.md"; then
  fail "final-response-paste.md must equal goal-closure.md"
fi
for closure_artifact in goal-closure.md final-response-paste.md FINAL_RESPONSE.md; do
  if awk '/^## Fichiers modifiés/,/^## Matérialisation/' "$SCRATCH/$closure_artifact" | grep -qE '(^|- )`?studies/'; then
    fail "$closure_artifact tracked section must not list studies/ paths"
  fi
done
ok "goal-closure emitted (tracked section clean, FINAL_RESPONSE.md ready)"

IMMERSION_PASSES=$((pass - EXISTING_PASSES))
[ "$EXISTING_PASSES" -eq 17 ] || fail "expected 17 existing baseline passes, got $EXISTING_PASSES"
[ "$IMMERSION_PASSES" -eq 10 ] || fail "expected 10 immersion passes, got $IMMERSION_PASSES"
echo "EXISTING_TESTS: $EXISTING_PASSES passed (regression baseline)"
echo "IMMERSION_TESTS: $IMMERSION_PASSES passed"
echo "STUDY_CONTRACT: canonical=tests/fixtures/biomimetisme-memory-palace.json materialize=memory-palace/scripts/materialize-biomimetisme-study.sh target=gitignored-study-dir (runtime only, not in CHANGED_FILES)"
echo "Summary: $pass tests passed ($EXISTING_PASSES existing + $IMMERSION_PASSES immersion, study-evidence in scratch)"
{
  echo "verification_plan_step1: memory-palace-tests.log zero FAIL"
  echo "verification_plan_step2: immersion-tour.log midDescent easing + visual-framing.log"
  echo "verification_plan_step3: study-evidence.json scene_count=7 fixture_sha=study_json_sha"
  echo "verification_plan_step4: screenshot-carte.png screenshot-visite-stop1.png screenshot-iso-visite.png"
  echo "verification_plan_palette: visual-palette.log mean_lum>140 hues>=4"
  echo "changed_files_tracked: $SCRATCH/changed-files-tracked.txt"
  echo "goal_closure: $SCRATCH/goal-closure.md"
  echo "final_response_paste: $SCRATCH/final-response-paste.md"
  echo "final_response_md: $SCRATCH/FINAL_RESPONSE.md"
  echo "study_criterion: satisfied via fixture+materialize (scratch study-evidence.json), not in CHANGED_FILES"
} >"$SCRATCH/verification-summary.txt"
exit 0