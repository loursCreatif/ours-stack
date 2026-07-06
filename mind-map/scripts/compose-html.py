#!/usr/bin/env python3
"""Compose mind-map.html from mind-map.json (offline, zero CDN)."""
import html
import json
import re
import sys
from pathlib import Path

# Custom preset: only these token names, values restricted to safe CSS characters
# (no ; } < " ') so meta.customTokens can never break out of the <style> block.
TOKEN_NAMES = ("bg", "surface", "text", "muted", "border", "accent",
               "accent-light", "secondary", "success", "warning", "radius")
SAFE_TOKEN_VALUE = re.compile(r"^[#a-zA-Z0-9 .,%()-]+$")

PRESET_CSS = {
    "academic": """:root {
  --bg: #f0f4f8; --surface: #fff; --text: #1a2332; --muted: #5c6370; --border: #d4e4f7;
  --accent: #1e4d8c; --accent-light: #e8f0fa; --secondary: #2d6cb5; --success: #1a6b4a; --warning: #9a6b00;
  --radius: 8px;
}""",
    "editorial": """:root {
  --bg: #faf8f5; --surface: #fff; --text: #1c1917; --muted: #6b6560; --border: #e8e4df;
  --accent: #8b2942; --accent-light: #f5e8ec; --secondary: #b85c72; --success: #2d5a3d; --warning: #8b6914;
  --radius: 4px;
}""",
    "minimal": """:root {
  --bg: #fafafa; --surface: #fff; --text: #18181b; --muted: #71717a; --border: #e4e4e7;
  --accent: #18181b; --accent-light: #f4f4f5; --secondary: #3f3f46; --success: #166534; --warning: #a16207;
  --radius: 4px;
}""",
    "warm": """:root {
  --bg: #f5f0e8; --surface: #fffaf3; --text: #2c2416; --muted: #6b5c4a; --border: #e5d9c8;
  --accent: #8b5a2b; --accent-light: #f0e6d6; --secondary: #c49a6c; --success: #3d5c3a; --warning: #b45309;
  --radius: 14px;
}""",
    "creative": """:root {
  --bg: #0f0a1a; --surface: #1a1228; --text: #f0e6ff; --muted: #9a8ab0; --border: #3d2a5c;
  --accent: #ff2d6a; --accent-light: #ffe0ec; --secondary: #7b2ff7; --success: #00a878; --warning: #ffb800;
  --radius: 0;
}""",
}

RENDERER_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; }
.app { display: flex; flex-direction: column; height: 100vh; }
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: .6rem 1rem; background: var(--surface); border-bottom: 1px solid var(--border); flex-shrink: 0; flex-wrap: wrap; }
.toolbar h1 { font-size: 1rem; font-weight: 700; }
.toolbar .meta { font-size: .75rem; color: var(--muted); display: block; }
.toolbar-right { display: flex; gap: .4rem; align-items: center; flex-wrap: wrap; }
.toolbar input[type=search] { padding: .35rem .6rem; border: 1px solid var(--border); border-radius: var(--radius); font-size: .82rem; min-width: 140px; background: var(--bg); color: var(--text); }
.search-count { font-size: .75rem; color: var(--muted); white-space: nowrap; }
.toolbar button { padding: .35rem .65rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface); color: var(--text); font-size: .78rem; cursor: pointer; }
.toolbar button:hover { background: var(--accent-light); border-color: var(--accent); }
.toolbar button[aria-pressed="true"] { background: var(--accent-light); border-color: var(--accent); }
.workspace { display: flex; flex: 1; min-height: 0; }
.canvas-wrap { flex: 1; overflow: hidden; cursor: grab; background: var(--bg); touch-action: none; position: relative; }
.tooltip { position: absolute; pointer-events: none; background: var(--surface); border: 1px solid var(--border); box-shadow: 0 2px 8px rgba(0,0,0,.12); max-width: 280px; border-radius: var(--radius); padding: .5rem .65rem; font-size: .82rem; line-height: 1.4; color: var(--text); z-index: 10; display: none; }
.tooltip.visible { display: block; }
.canvas-wrap.dragging { cursor: grabbing; }
#map-svg { width: 100%; height: 100%; display: block; }
.panel { width: 280px; flex-shrink: 0; background: var(--surface); border-left: 1px solid var(--border); padding: 1rem; overflow-y: auto; position: relative; }
.panel[hidden] { display: none; }
.panel-close { position: absolute; top: .5rem; right: .5rem; border: none; background: none; font-size: 1.2rem; cursor: pointer; color: var(--muted); }
.panel-type { font-size: .68rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
.panel h2 { font-size: 1rem; margin: .35rem 0; color: var(--accent); }
.panel-summary { font-size: .88rem; line-height: 1.5; color: var(--muted); font-style: italic; margin-bottom: .5rem; }
.panel p { font-size: .88rem; line-height: 1.5; color: var(--text); }
.panel-empty { color: var(--muted); font-style: italic; }
.panel-link { display: inline-block; margin-top: .75rem; color: var(--secondary); font-size: .85rem; }
.node rect { cursor: pointer; transition: filter .15s; }
.node:hover rect { filter: brightness(1.08); }
.node.highlight rect { stroke: var(--warning); stroke-width: 3; }
.node.collapsed .toggle { fill: var(--muted); }
.node text { pointer-events: none; }
.link { fill: none; stroke: var(--border); stroke-width: 1.5; }
.link-source { stroke: var(--secondary); stroke-dasharray: 4 3; }
footer { text-align: center; font-size: .72rem; color: var(--muted); padding: .35rem; border-top: 1px solid var(--border); flex-shrink: 0; }
@media (max-width: 700px) {
  .workspace { flex-direction: column; }
  .panel { width: 100%; max-height: 35vh; border-left: none; border-top: 1px solid var(--border); }
}
"""

RENDERER_JS = r"""
(function () {
  const data = JSON.parse(document.getElementById('map-data').textContent);
  const svg = document.getElementById('map-svg');
  const g = document.getElementById('map-root');
  const panel = document.getElementById('panel');
  const tooltip = document.getElementById('tooltip');
  const BASE_NODE_W = 166, BASE_NODE_H = 32, GAP_Y = 14, GAP_X = 84;
  const MIN_SCALE = 0.4, MAX_SCALE = 4;
  const MIN_IMPORTANCE = 1, MAX_IMPORTANCE = 5;
  const MAX_NODE_W = BASE_NODE_W + (MAX_IMPORTANCE - 1) * 22;
  const STEP_X = MAX_NODE_W + GAP_X;
  const collapsed = new Set();
  const state = { x: 0, y: 0, scale: 1, vw: 1, vh: 1, layout: chooseLayout(data), fit: true, dragging: false, dx: 0, dy: 0, sx: 0, sy: 0 };

  function maxDepth(node) {
    const kids = node.children || [];
    if (!kids.length) return 1;
    return 1 + Math.max(...kids.map(maxDepth));
  }

  function chooseLayout(mapData) {
    if (mapData.layout === 'tree' || mapData.layout === 'centered') return mapData.layout;
    const rootKids = (mapData.root.children || []).length;
    return rootKids >= 4 && maxDepth(mapData.root) <= 3 ? 'centered' : 'tree';
  }

  function initCollapsed(node) {
    if (node.collapsed && node.children && node.children.length) collapsed.add(node.id);
    (node.children || []).forEach(initCollapsed);
  }
  initCollapsed(data.root);

  function visibleChildren(node) {
    return collapsed.has(node.id) ? [] : (node.children || []);
  }

  function descendantCount(node) {
    return (node.children || []).reduce((sum, c) => sum + 1 + descendantCount(c), 0);
  }

  function explicitImportance(value) {
    const n = Number(value);
    if (!Number.isFinite(n)) return null;
    const rounded = Math.round(n);
    if (rounded < MIN_IMPORTANCE || rounded > MAX_IMPORTANCE) return null;
    return rounded;
  }

  function nodeImportance(node, depth) {
    const explicit = explicitImportance(node.importance);
    if (explicit) return explicit;
    if (depth === 0) return 5;
    if (node.type === 'source') return 1;
    if (node.type === 'example') return 2;
    if (node.type === 'concept') return depth === 1 ? 4 : 3;
    if (visibleChildren(node).length >= 2) return 3;
    return depth <= 1 ? 3 : 2;
  }

  function nodeMetrics(node, depth) {
    const importance = nodeImportance(node, depth);
    const step = importance - MIN_IMPORTANCE;
    const h = BASE_NODE_H + step * 6;
    return {
      importance,
      w: BASE_NODE_W + step * 22,
      h,
      radius: h / 2,
      font: 10 + step,
      pad: 12 + step * 2
    };
  }

  function nodeX(depth, side) {
    return side === 'left' ? -depth * STEP_X : depth * STEP_X;
  }

  function layoutTree(node, depth, y, side) {
    const metrics = nodeMetrics(node, depth);
    const kids = visibleChildren(node);
    if (!kids.length) {
      return { node, x: nodeX(depth, side), y, w: metrics.w, boxH: metrics.h, h: metrics.h, metrics, depth, side };
    }
    let cy = y;
    const childLayouts = kids.map(k => {
      const l = layoutTree(k, depth + 1, cy, side);
      cy = l.y + l.h + GAP_Y;
      return l;
    });
    const h = Math.max(metrics.h, cy - y - GAP_Y);
    const yMid = y + h / 2 - metrics.h / 2;
    return { node, x: nodeX(depth, side), y: yMid, w: metrics.w, boxH: metrics.h, h, metrics, depth, children: childLayouts, side };
  }

  function visibleLeafCount(node) {
    const kids = visibleChildren(node);
    if (!kids.length) return 1;
    return kids.reduce((sum, child) => sum + visibleLeafCount(child), 0);
  }

  function splitCenteredBranches(root) {
    const branches = visibleChildren(root)
      .map((node, index) => ({ node, index, leaves: visibleLeafCount(node) }))
      .sort((a, b) => b.leaves - a.leaves || a.index - b.index);
    const sides = { left: [], right: [] };
    const load = { left: 0, right: 0 };
    branches.forEach(branch => {
      const side = load.right <= load.left ? 'right' : 'left';
      sides[side].push(branch);
      load[side] += branch.leaves;
    });
    sides.left.sort((a, b) => a.index - b.index);
    sides.right.sort((a, b) => a.index - b.index);
    return {
      left: sides.left.map(branch => branch.node),
      right: sides.right.map(branch => branch.node)
    };
  }

  function shiftLayout(layout, dy) {
    layout.y += dy;
    (layout.children || []).forEach(child => shiftLayout(child, dy));
  }

  function layoutSide(branches, side) {
    let cy = 0;
    const layouts = branches.map(branch => {
      const l = layoutTree(branch, 1, cy, side);
      cy = l.y + l.h + GAP_Y;
      return l;
    });
    const h = layouts.length ? cy - GAP_Y : 0;
    const rootMetrics = nodeMetrics(data.root, 0);
    const shift = rootMetrics.h / 2 - h / 2;
    layouts.forEach(layout => shiftLayout(layout, shift));
    return layouts;
  }

  function layoutCentered(root) {
    const split = splitCenteredBranches(root);
    const metrics = nodeMetrics(root, 0);
    return {
      node: root,
      x: 0,
      y: 0,
      w: metrics.w,
      boxH: metrics.h,
      h: metrics.h,
      metrics,
      depth: 0,
      side: 'root',
      children: layoutSide(split.left, 'left').concat(layoutSide(split.right, 'right'))
    };
  }

  function layoutMap() {
    return state.layout === 'centered' ? layoutCentered(data.root) : layoutTree(data.root, 0, 0, 'right');
  }

  function flatten(layout, acc) {
    acc.push(layout);
    (layout.children || []).forEach(c => flatten(c, acc));
    return acc;
  }

  let lastLayouts = new Map();

  function render() {
    const tree = layoutMap();
    const nodes = flatten(tree, []);
    lastLayouts = new Map(nodes.map(l => [l.node.id, l]));
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    nodes.forEach(n => {
      minX = Math.min(minX, n.x);
      minY = Math.min(minY, n.y);
      maxX = Math.max(maxX, n.x + n.w);
      maxY = Math.max(maxY, n.y + n.boxH);
    });
    const pad = 80;
    if (state.fit) {
      state.x = minX - pad;
      state.y = minY - pad;
      state.scale = 1;
      state.fit = false;
    }
    const vw = Math.max(1, maxX - minX + pad * 2) / state.scale;
    const vh = Math.max(1, maxY - minY + pad * 2) / state.scale;
    state.vw = vw;
    state.vh = vh;
    svg.setAttribute('viewBox', `${state.x} ${state.y} ${vw} ${vh}`);
    updateLayoutButton();
    g.innerHTML = '';

    function drawLinks(layout) {
      const ny = layout.y + layout.boxH / 2;
      (layout.children || []).forEach(c => {
        const leftSide = c.side === 'left';
        const nx = leftSide ? layout.x : layout.x + layout.w;
        const cx = leftSide ? c.x + c.w : c.x;
        const cy = c.y + c.boxH / 2;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const mx = (nx + cx) / 2;
        path.setAttribute('d', `M${nx},${ny} C${mx},${ny} ${mx},${cy} ${cx},${cy}`);
        path.setAttribute('class', 'link' + (c.node.type === 'source' ? ' link-source' : ''));
        g.appendChild(path);
        drawLinks(c);
      });
    }
    drawLinks(tree);

    nodes.forEach(({ node, x, y, w, boxH, metrics }) => {
      const hasKids = (node.children || []).length > 0;
      const isCollapsed = collapsed.has(node.id);
      const toggleLabel = hasKids ? (isCollapsed ? '+' + descendantCount(node) : '−') : '';
      const toggleW = hasKids ? Math.max(18, toggleLabel.length * (metrics.font + 1) * 0.62 + 6) : 0;
      const grp = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      grp.setAttribute('class', 'node' + (isCollapsed ? ' collapsed' : '') + (node._hl ? ' highlight' : ''));
      grp.setAttribute('data-importance', String(metrics.importance));
      grp.setAttribute('tabindex', '0');
      grp.setAttribute('role', 'button');
      grp.setAttribute('aria-label', node.label);
      const fill = node.type === 'concept' ? 'var(--accent)' :
        node.type === 'example' ? 'var(--accent-light)' :
        node.type === 'source' ? 'var(--secondary)' : 'var(--surface)';
      const stroke = node.type === 'detail' ? 'var(--accent)' : node.type === 'example' ? 'var(--success)' : 'var(--border)';
      const textFill = node.type === 'concept' || node.type === 'source' ? '#fff' : 'var(--text)';
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', x); rect.setAttribute('y', y);
      rect.setAttribute('width', w); rect.setAttribute('height', boxH);
      rect.setAttribute('rx', metrics.radius); rect.setAttribute('fill', fill); rect.setAttribute('stroke', stroke);
      rect.setAttribute('stroke-width', 1 + metrics.importance * 0.22);
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', x + (hasKids ? metrics.pad + toggleW : metrics.pad));
      text.setAttribute('y', y + boxH / 2 + metrics.font * 0.35);
      text.setAttribute('fill', textFill); text.setAttribute('font-size', String(metrics.font));
      text.setAttribute('font-weight', metrics.importance >= 4 ? '700' : '500');
      const maxChars = Math.max(12, Math.floor((w - (hasKids ? metrics.pad + toggleW + 16 : metrics.pad * 2)) / (metrics.font * 0.58)));
      const label = node.label.length > maxChars ? node.label.slice(0, Math.max(1, maxChars - 1)) + '…' : node.label;
      text.textContent = label;
      grp.appendChild(rect); grp.appendChild(text);
      if (hasKids) {
        const tg = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        tg.setAttribute('class', 'toggle'); tg.setAttribute('x', x + metrics.pad); tg.setAttribute('y', y + boxH / 2 + metrics.font * 0.35);
        tg.setAttribute('fill', textFill); tg.setAttribute('font-size', String(metrics.font + 1)); tg.setAttribute('font-weight', '700');
        tg.textContent = toggleLabel;
        grp.appendChild(tg);
      }
      function onActivate(e, toggleOnly) {
        if (toggleOnly && hasKids) {
          const expanding = collapsed.has(node.id);
          if (expanding) collapsed.delete(node.id); else collapsed.add(node.id);
          render();
          if (expanding) focusOn(node);
          return;
        }
        if (node.type === 'source' && node.href) window.open(node.href, '_blank');
        showPanel(node);
        focusOn(node);
      }
      grp.addEventListener('click', e => {
        const toggleOnly = hasKids && (e.target.classList?.contains('toggle') || isToggleHit(e, x, y, boxH, metrics.pad + toggleW));
        onActivate(e, toggleOnly);
      });
      grp.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onActivate(e, e.shiftKey && hasKids); }
      });
      grp.addEventListener('mouseenter', e => showTooltip(node, e));
      grp.addEventListener('mousemove', e => {
        if (tooltip.classList.contains('visible')) positionTooltip(e.clientX, e.clientY);
      });
      grp.addEventListener('mouseleave', hideTooltip);
      g.appendChild(grp);
    });
  }

  function subtreeBBox(node) {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity, found = false;
    (function visit(n) {
      const l = lastLayouts.get(n.id);
      if (l) {
        found = true;
        minX = Math.min(minX, l.x); minY = Math.min(minY, l.y);
        maxX = Math.max(maxX, l.x + l.w); maxY = Math.max(maxY, l.y + l.boxH);
      }
      visibleChildren(n).forEach(visit);
    })(node);
    return found ? { minX, minY, maxX, maxY } : null;
  }

  let anim = null;
  function cancelAnim() {
    if (anim) { cancelAnimationFrame(anim); anim = null; }
  }

  function animateTo(tx, ty, tscale) {
    cancelAnim();
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      state.x = tx; state.y = ty; state.scale = tscale;
      render();
      return;
    }
    const from = { x: state.x, y: state.y, scale: state.scale };
    const start = performance.now(), dur = 380;
    function step(now) {
      const t = Math.min(1, (now - start) / dur);
      const e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      state.x = from.x + (tx - from.x) * e;
      state.y = from.y + (ty - from.y) * e;
      state.scale = from.scale + (tscale - from.scale) * e;
      render();
      anim = t < 1 ? requestAnimationFrame(step) : null;
    }
    anim = requestAnimationFrame(step);
  }

  function focusOn(node) {
    const box = subtreeBBox(node);
    if (!box) return;
    const bw = Math.max(box.maxX - box.minX, 1);
    const bh = Math.max(box.maxY - box.minY, 1);
    const cw = state.vw * state.scale, ch = state.vh * state.scale;
    const rect = wrap.getBoundingClientRect();
    const eW = Math.max(rect.width, 1), eH = Math.max(rect.height, 1);
    // Screen px per map unit: target = subtree fills ~65% of the canvas,
    // capped at 1.6 px/unit so a single leaf never becomes gigantic.
    const wanted = Math.min(0.65 * Math.min(eW / bw, eH / bh), 1.6);
    const current = Math.min(eW / cw, eH / ch);
    const tscale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, wanted / current));
    const vw = cw / tscale, vh = ch / tscale;
    const cx = (box.minX + box.maxX) / 2, cy = (box.minY + box.maxY) / 2;
    animateTo(cx - vw / 2, cy - vh / 2, tscale);
  }

  function overview() {
    hideTooltip();
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    lastLayouts.forEach(l => {
      minX = Math.min(minX, l.x); minY = Math.min(minY, l.y);
      maxX = Math.max(maxX, l.x + l.w); maxY = Math.max(maxY, l.y + l.boxH);
    });
    if (!isFinite(minX)) return;
    animateTo(minX - 80, minY - 80, 1);
  }

  function svgPoint(e) {
    const point = svg.createSVGPoint();
    point.x = e.clientX;
    point.y = e.clientY;
    const ctm = svg.getScreenCTM();
    return ctm ? point.matrixTransform(ctm.inverse()) : { x: e.offsetX, y: e.offsetY };
  }

  function isToggleHit(e, x, y, boxH, zone) {
    const point = svgPoint(e);
    return point.x >= x && point.x <= x + (zone || 32) && point.y >= y && point.y <= y + boxH;
  }

  function tooltipText(node) {
    if (node.summary) return node.summary;
    if (node.note) {
      const first = node.note.split('. ')[0];
      if (first) return first.endsWith('.') ? first : first + '.';
    }
    if (node.label.length > 28) return node.label;
    return '';
  }

  function positionTooltip(clientX, clientY) {
    const pad = 12;
    let left = clientX + pad;
    let top = clientY + pad;
    tooltip.style.left = left + 'px';
    tooltip.style.top = top + 'px';
    tooltip.classList.add('visible');
    const rect = tooltip.getBoundingClientRect();
    if (rect.right > window.innerWidth - 8) {
      left = Math.max(8, clientX - rect.width - pad);
      tooltip.style.left = left + 'px';
    }
    if (rect.bottom > window.innerHeight - 8) {
      top = Math.max(8, clientY - rect.height - pad);
      tooltip.style.top = top + 'px';
    }
  }

  function hideTooltip() {
    tooltip.classList.remove('visible');
    tooltip.textContent = '';
  }

  function showTooltip(node, e) {
    const text = tooltipText(node);
    if (!text) { hideTooltip(); return; }
    tooltip.textContent = text;
    positionTooltip(e.clientX, e.clientY);
  }

  function showPanel(node) {
    panel.hidden = false;
    document.getElementById('panel-type').textContent = node.type;
    document.getElementById('panel-label').textContent = node.label;
    const summaryEl = document.getElementById('panel-summary');
    const noteEl = document.getElementById('panel-note');
    const summary = node.summary || '';
    const note = node.note || '';
    if (summary) {
      summaryEl.textContent = summary;
      summaryEl.hidden = false;
    } else {
      summaryEl.textContent = '';
      summaryEl.hidden = true;
    }
    noteEl.classList.remove('panel-empty');
    if (note) {
      noteEl.textContent = note;
      noteEl.hidden = false;
    } else if (!summary) {
      noteEl.textContent = 'Pas de détail pour ce nœud';
      noteEl.classList.add('panel-empty');
      noteEl.hidden = false;
    } else {
      noteEl.textContent = '';
      noteEl.hidden = true;
    }
    const link = document.getElementById('panel-link');
    if (node.href) { link.href = node.href; link.hidden = false; } else link.hidden = true;
  }

  function walk(node, fn) { fn(node); (node.children || []).forEach(c => walk(c, fn)); }

  function resetView() {
    hideTooltip();
    cancelAnim();
    state.fit = true;
    state.scale = 1;
    render();
  }

  function updateLayoutButton() {
    const btn = document.getElementById('btn-layout');
    btn.textContent = state.layout === 'centered' ? '⇆ Centrée' : '⇆ Arbre';
    btn.setAttribute('aria-pressed', state.layout === 'centered' ? 'true' : 'false');
  }

  document.getElementById('btn-expand-all').onclick = () => { collapsed.clear(); render(); };
  document.getElementById('btn-collapse-all').onclick = () => {
    walk(data.root, n => { if (n.children && n.children.length) collapsed.add(n.id); });
    render();
  };
  document.getElementById('btn-layout').onclick = () => {
    state.layout = state.layout === 'centered' ? 'tree' : 'centered';
    resetView();
  };
  document.getElementById('btn-reset').onclick = overview;
  document.getElementById('panel-close').onclick = () => { panel.hidden = true; };
  const searchEl = document.getElementById('search');
  const searchCount = document.getElementById('search-count');
  let preSearchCollapsed = null;
  let searchMatches = [], searchIdx = -1;
  searchEl.oninput = e => {
    const q = e.target.value.toLowerCase().trim();
    if (q && !preSearchCollapsed) preSearchCollapsed = new Set(collapsed);
    if (!q && preSearchCollapsed) {
      collapsed.clear();
      preSearchCollapsed.forEach(id => collapsed.add(id));
      preSearchCollapsed = null;
    }
    searchMatches = [];
    searchIdx = -1;
    function mark(n, ancestors) {
      n._hl = !!q && (n.label.toLowerCase().includes(q) || (n.note || '').toLowerCase().includes(q) || (n.summary || '').toLowerCase().includes(q));
      if (n._hl) {
        searchMatches.push(n);
        ancestors.forEach(id => collapsed.delete(id));
      }
      (n.children || []).forEach(c => mark(c, ancestors.concat(n.id)));
    }
    mark(data.root, []);
    const m = searchMatches.length;
    searchCount.textContent = q ? m + (m > 1 ? ' résultats' : ' résultat') + (m ? ' · Entrée ↵' : '') : '';
    searchCount.hidden = !q;
    render();
  };
  searchEl.addEventListener('keydown', e => {
    if (e.key === 'Enter' && searchMatches.length) {
      e.preventDefault();
      searchIdx = (searchIdx + (e.shiftKey ? -1 : 1) + searchMatches.length) % searchMatches.length;
      focusOn(searchMatches[searchIdx]);
      searchCount.textContent = (searchIdx + 1) + '/' + searchMatches.length;
    } else if (e.key === 'Escape') {
      searchEl.value = '';
      searchEl.dispatchEvent(new Event('input'));
    }
  });
  window.addEventListener('keydown', e => {
    if (e.key === 'Escape' && document.activeElement !== searchEl) overview();
  });

  const wrap = document.getElementById('canvas-wrap');
  wrap.addEventListener('wheel', e => {
    hideTooltip();
    cancelAnim();
    e.preventDefault();
    const rect = wrap.getBoundingClientRect();
    const fx = (e.clientX - rect.left) / rect.width;
    const fy = (e.clientY - rect.top) / rect.height;
    const cx = state.x + fx * state.vw;
    const cy = state.y + fy * state.vh;
    const oldScale = state.scale;
    state.scale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, oldScale * (e.deltaY > 0 ? 0.92 : 1.08)));
    const ratio = oldScale / state.scale;
    state.x = cx - fx * state.vw * ratio;
    state.y = cy - fy * state.vh * ratio;
    render();
  }, { passive: false });
  wrap.addEventListener('mousedown', e => {
    hideTooltip();
    cancelAnim();
    if (e.target === wrap || e.target === svg || e.target.tagName === 'path') {
      state.dragging = true; state.sx = e.clientX; state.sy = e.clientY; wrap.classList.add('dragging');
    }
  });
  window.addEventListener('mousemove', e => {
    if (!state.dragging) return;
    state.x -= (e.clientX - state.sx) / state.scale;
    state.y -= (e.clientY - state.sy) / state.scale;
    state.sx = e.clientX; state.sy = e.clientY;
    render();
  });
  window.addEventListener('mouseup', () => { state.dragging = false; wrap.classList.remove('dragging'); });
  wrap.addEventListener('dblclick', e => {
    if (e.target === wrap || e.target === svg || e.target.tagName === 'path') overview();
  });

  render();
})();
"""


def _custom_css(tokens: dict) -> str:
    base = dict(re.findall(r"(--[a-z-]+):\s*([^;]+);", PRESET_CSS["warm"]))
    for name in TOKEN_NAMES:
        value = tokens.get(name)
        if value is None:
            continue
        if not isinstance(value, str) or not SAFE_TOKEN_VALUE.match(value.strip()):
            print(f"warn: ignoring unsafe custom token --{name}", file=sys.stderr)
            continue
        base[f"--{name}"] = value.strip()
    lines = " ".join(f"{k}: {v};" for k, v in base.items())
    return ":root {\n  " + lines + "\n}"


def _preset_css(meta: dict) -> tuple[str, str]:
    preset = meta.get("preset", "warm")
    if preset == "custom":
        tokens = meta.get("customTokens")
        if isinstance(tokens, dict) and tokens:
            return "custom", _custom_css(tokens)
        print("warn: preset custom without meta.customTokens, falling back to warm",
              file=sys.stderr)
        return "warm", PRESET_CSS["warm"]
    if preset not in PRESET_CSS:
        print(f"warn: unknown preset {preset!r}, falling back to warm", file=sys.stderr)
        return "warm", PRESET_CSS["warm"]
    return preset, PRESET_CSS[preset]


def _count_nodes(node: dict) -> int:
    return 1 + sum(_count_nodes(child) for child in node.get("children") or [])


def _tree_depth(node: dict) -> int:
    children = node.get("children") or []
    if not children:
        return 1
    return 1 + max(_tree_depth(child) for child in children)


def _initial_layout(data: dict) -> str:
    requested = data.get("layout")
    if requested in {"tree", "centered"}:
        return requested
    root = data["root"]
    return "centered" if len(root.get("children") or []) >= 4 and _tree_depth(root) <= 3 else "tree"


def compose(json_path: Path, out_path: Path | None = None) -> Path:
    data = json.loads(json_path.read_text())
    meta = data["meta"]
    preset, preset_css = _preset_css(meta)
    lang = html.escape(meta.get("lang", "fr"))
    title = html.escape(meta["title"])
    node_count = html.escape(str(_count_nodes(data["root"])))
    source = html.escape(meta.get("source", json_path.name))
    generated = html.escape(meta.get("generated", ""))
    json_embed = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    footer = html.escape(f"mind-map.json · généré {meta.get('generated', '')} · ours-stack /mind-map")
    initial_layout = html.escape(_initial_layout(data))

    html_out = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — mind map</title>
  <style>
{preset_css}
body.preset-{preset} {{ }}
{RENDERER_CSS}
  </style>
</head>
<body class="preset-{preset}" data-initial-layout="{initial_layout}">
  <div class="app">
    <header class="toolbar">
      <div class="toolbar-left">
        <h1>{title}</h1>
        <span class="meta">{node_count} nœuds · {source}</span>
      </div>
      <div class="toolbar-right">
        <input type="search" id="search" placeholder="Rechercher…" aria-label="Rechercher un nœud">
        <span class="search-count" id="search-count" aria-live="polite" hidden></span>
        <button type="button" id="btn-layout" aria-label="Basculer la vue" aria-pressed="false">⇆ Vue</button>
        <button type="button" id="btn-expand-all">Tout ouvrir</button>
        <button type="button" id="btn-collapse-all">Tout fermer</button>
        <button type="button" id="btn-reset">Reset vue</button>
      </div>
    </header>
    <div class="workspace">
      <div class="canvas-wrap" id="canvas-wrap">
        <svg id="map-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Carte mentale">
          <g id="map-root"></g>
        </svg>
        <div class="tooltip" id="tooltip" role="tooltip"></div>
      </div>
      <aside class="panel" id="panel" hidden>
        <button type="button" class="panel-close" id="panel-close" aria-label="Fermer">×</button>
        <span class="panel-type" id="panel-type"></span>
        <h2 id="panel-label"></h2>
        <p class="panel-summary" id="panel-summary" hidden></p>
        <p id="panel-note"></p>
        <a id="panel-link" class="panel-link" target="_blank" rel="noopener" hidden>Ouvrir la source →</a>
      </aside>
    </div>
    <footer>{footer}</footer>
  </div>
  <script id="map-data" type="application/json">{json_embed}</script>
  <script>
{RENDERER_JS}
  </script>
</body>
</html>
"""
    out = out_path or json_path.with_suffix(".html")
    if out.name.endswith(".json.html"):
        out = json_path.parent / "mind-map.html"
    out.write_text(html_out)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: compose-html.py <mind-map.json> [output.html]", file=sys.stderr)
        sys.exit(2)
    jp = Path(sys.argv[1])
    op = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    out = compose(jp, op)
    print(out)
