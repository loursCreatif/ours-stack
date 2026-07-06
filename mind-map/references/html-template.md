# HTML template — mind-map

Replace `{{PLACEHOLDERS}}`. Embed full `mind-map.json` in `<script id="map-data" type="application/json">`.

## Document skeleton

```html
<!DOCTYPE html>
<html lang="{{LANG}}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}} — mind map</title>
  <style>
    /* PRESET_CSS_BLOCK — see § Preset CSS below */
    /* RENDERER_CSS — see § Renderer CSS below */
  </style>
</head>
<body class="preset-{{PRESET_ID}}">
  <div class="app">
    <header class="toolbar">
      <div class="toolbar-left">
        <h1>{{TITLE}}</h1>
        <span class="meta">{{NODE_COUNT}} nœuds · {{SOURCE_FILE}}</span>
      </div>
      <div class="toolbar-right">
        <input type="search" id="search" placeholder="Rechercher…" aria-label="Rechercher un nœud">
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
      </div>
      <aside class="panel" id="panel" hidden>
        <button type="button" class="panel-close" id="panel-close" aria-label="Fermer">×</button>
        <span class="panel-type" id="panel-type"></span>
        <h2 id="panel-label"></h2>
        <p id="panel-note"></p>
        <a id="panel-link" class="panel-link" target="_blank" rel="noopener" hidden>Ouvrir la source →</a>
      </aside>
    </div>
    <footer>{{FOOTER}}</footer>
  </div>
  <script id="map-data" type="application/json">{{JSON_DATA}}</script>
  <script>
    /* RENDERER_JS — see § Renderer JS below */
  </script>
</body>
</html>
```

## Preset CSS (`:root` tokens)

Use one block per preset. Agent copies tokens from layout-html reports.

### academic
```css
:root {
  --bg: #f0f4f8; --surface: #fff; --text: #1a2332; --muted: #5c6370; --border: #d4e4f7;
  --accent: #1e4d8c; --accent-light: #e8f0fa; --secondary: #2d6cb5; --success: #1a6b4a; --warning: #9a6b00;
  --radius: 8px;
}
```

### editorial
```css
:root {
  --bg: #faf8f5; --surface: #fff; --text: #1c1917; --muted: #6b6560; --border: #e8e4df;
  --accent: #8b2942; --accent-light: #f5e8ec; --secondary: #b85c72; --success: #2d5a3d; --warning: #8b6914;
  --radius: 4px;
}
```

### minimal
```css
:root {
  --bg: #fafafa; --surface: #fff; --text: #18181b; --muted: #71717a; --border: #e4e4e7;
  --accent: #18181b; --accent-light: #f4f4f5; --secondary: #3f3f46; --success: #166534; --warning: #a16207;
  --radius: 4px;
}
```

### warm
```css
:root {
  --bg: #f5f0e8; --surface: #fffaf3; --text: #2c2416; --muted: #6b5c4a; --border: #e5d9c8;
  --accent: #8b5a2b; --accent-light: #f0e6d6; --secondary: #c49a6c; --success: #3d5c3a; --warning: #b45309;
  --radius: 14px;
}
```

### creative
```css
:root {
  --bg: #0f0a1a; --surface: #1a1228; --text: #f0e6ff; --muted: #9a8ab0; --border: #3d2a5c;
  --accent: #ff2d6a; --accent-light: #ffe0ec; --secondary: #7b2ff7; --success: #00a878; --warning: #ffb800;
  --radius: 0;
}
```

### custom

Build the `:root` block from `meta.customTokens` merged over the `warm` defaults (same 11 var names). Only inject values matching `^[#a-zA-Z0-9 .,%()-]+$` — drop anything with `;`, `}` or quotes.

## Renderer CSS

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; }
.app { display: flex; flex-direction: column; height: 100vh; }
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: .6rem 1rem; background: var(--surface); border-bottom: 1px solid var(--border); flex-shrink: 0; }
.toolbar h1 { font-size: 1rem; font-weight: 700; }
.toolbar .meta { font-size: .75rem; color: var(--muted); display: block; }
.toolbar-right { display: flex; gap: .4rem; align-items: center; flex-wrap: wrap; }
.toolbar input[type=search] { padding: .35rem .6rem; border: 1px solid var(--border); border-radius: var(--radius); font-size: .82rem; min-width: 140px; background: var(--bg); color: var(--text); }
.toolbar button { padding: .35rem .65rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface); color: var(--text); font-size: .78rem; cursor: pointer; }
.toolbar button:hover { background: var(--accent-light); border-color: var(--accent); }
.workspace { display: flex; flex: 1; min-height: 0; }
.canvas-wrap { flex: 1; overflow: hidden; cursor: grab; background: var(--bg); touch-action: none; }
.canvas-wrap.dragging { cursor: grabbing; }
#map-svg { width: 100%; height: 100%; display: block; }
.panel { width: 280px; flex-shrink: 0; background: var(--surface); border-left: 1px solid var(--border); padding: 1rem; overflow-y: auto; position: relative; }
.panel[hidden] { display: none; }
.panel-close { position: absolute; top: .5rem; right: .5rem; border: none; background: none; font-size: 1.2rem; cursor: pointer; color: var(--muted); }
.panel-type { font-size: .68rem; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); }
.panel h2 { font-size: 1rem; margin: .35rem 0; color: var(--accent); }
.panel p { font-size: .88rem; line-height: 1.5; color: var(--text); }
.panel-link { display: inline-block; margin-top: .75rem; color: var(--secondary); font-size: .85rem; }
.node rect { cursor: pointer; transition: filter .15s; }
.node:hover rect { filter: brightness(1.08); }
.node.highlight rect { stroke: var(--warning); stroke-width: 3; }
.node.collapsed .toggle { fill: var(--muted); }
.link { fill: none; stroke: var(--border); stroke-width: 1.5; }
.link-source { stroke: var(--secondary); stroke-dasharray: 4 3; }
footer { text-align: center; font-size: .72rem; color: var(--muted); padding: .35rem; border-top: 1px solid var(--border); flex-shrink: 0; }
@media (max-width: 700px) {
  .workspace { flex-direction: column; }
  .panel { width: 100%; max-height: 35vh; border-left: none; border-top: 1px solid var(--border); }
}
```

## Renderer JS

**Minimal offline fallback only.** The embedded renderer in `scripts/compose-html.py` is the source of truth and is richer: importance-based bubble sizing, centered/tree layout toggle, search that auto-expands collapsed matches with a result counter, and animated zoom-to-branch on node click. Prefer regenerating with the script whenever python3 is available.

Copy this block verbatim into every generated HTML. Reads `#map-data` JSON.

```javascript
(function () {
  const data = JSON.parse(document.getElementById('map-data').textContent);
  const svg = document.getElementById('map-svg');
  const g = document.getElementById('map-root');
  const panel = document.getElementById('panel');
  const NODE_W = 160, NODE_H = 36, GAP_Y = 12, GAP_X = 80;
  const collapsed = new Set();
  const state = { x: 40, y: 40, scale: 1, dragging: false, dx: 0, dy: 0 };

  function initCollapsed(node, depth) {
    if (node.collapsed && node.children?.length) collapsed.add(node.id);
    (node.children || []).forEach(c => initCollapsed(c, depth + 1));
  }
  initCollapsed(data.root, 0);

  function visibleChildren(node) {
    return collapsed.has(node.id) ? [] : (node.children || []);
  }

  function layout(node, depth, y) {
    const kids = visibleChildren(node);
    if (!kids.length) {
      return { node, x: depth * (NODE_W + GAP_X), y, h: NODE_H };
    }
    let cy = y;
    const childLayouts = kids.map(k => {
      const l = layout(k, depth + 1, cy);
      cy = l.y + l.h + GAP_Y;
      return l;
    });
    const h = Math.max(NODE_H, cy - y - GAP_Y);
    const yMid = y + h / 2 - NODE_H / 2;
    return { node, x: depth * (NODE_W + GAP_X), y: yMid, h, children: childLayouts };
  }

  function flatten(layout, acc) {
    acc.push(layout);
    (layout.children || []).forEach(c => flatten(c, acc));
    return acc;
  }

  function render() {
    const tree = layout(data.root, 0, 0);
    const nodes = flatten(tree, []);
    let maxX = 0, maxY = 0;
    nodes.forEach(n => {
      maxX = Math.max(maxX, n.x + NODE_W);
      maxY = Math.max(maxY, n.y + NODE_H);
    });
    svg.setAttribute('viewBox', `${-state.x} ${-state.y} ${(maxX + 120) / state.scale} ${(maxY + 120) / state.scale}`);
    g.innerHTML = '';

    function drawLinks(layout, px, py) {
      const nx = layout.x + NODE_W, ny = layout.y + NODE_H / 2;
      (layout.children || []).forEach(c => {
        const cx = c.x, cy = c.y + NODE_H / 2;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const mx = (nx + cx) / 2;
        path.setAttribute('d', `M${nx},${ny} C${mx},${ny} ${mx},${cy} ${cx},${cy}`);
        path.setAttribute('class', 'link' + (c.node.type === 'source' ? ' link-source' : ''));
        g.appendChild(path);
        drawLinks(c, cx, cy);
      });
    }
    drawLinks(tree, 0, 0);

    nodes.forEach(({ node, x, y }) => {
      const hasKids = (node.children || []).length > 0;
      const grp = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      grp.setAttribute('class', 'node' + (collapsed.has(node.id) ? ' collapsed' : '') + (node._hl ? ' highlight' : ''));
      grp.setAttribute('data-id', node.id);
      const fill = node.type === 'concept' ? 'var(--accent)' :
        node.type === 'example' ? 'var(--accent-light)' :
        node.type === 'source' ? 'var(--secondary)' : 'var(--surface)';
      const stroke = node.type === 'detail' ? 'var(--accent)' : node.type === 'example' ? 'var(--success)' : 'var(--border)';
      const textFill = node.type === 'concept' || node.type === 'source' ? '#fff' : 'var(--text)';
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', x); rect.setAttribute('y', y);
      rect.setAttribute('width', NODE_W); rect.setAttribute('height', NODE_H);
      rect.setAttribute('rx', 8); rect.setAttribute('fill', fill); rect.setAttribute('stroke', stroke); rect.setAttribute('stroke-width', 1.5);
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', x + (hasKids ? 22 : 10)); text.setAttribute('y', y + NODE_H / 2 + 4);
      text.setAttribute('fill', textFill); text.setAttribute('font-size', '11');
      const label = node.label.length > 22 ? node.label.slice(0, 20) + '…' : node.label;
      text.textContent = label;
      grp.appendChild(rect); grp.appendChild(text);
      if (hasKids) {
        const tg = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        tg.setAttribute('class', 'toggle'); tg.setAttribute('x', x + 8); tg.setAttribute('y', y + NODE_H / 2 + 4);
        tg.setAttribute('fill', textFill); tg.setAttribute('font-size', '12'); tg.setAttribute('font-weight', '700');
        tg.textContent = collapsed.has(node.id) ? '+' : '−';
        grp.appendChild(tg);
      }
      grp.addEventListener('click', e => {
        e.stopPropagation();
        if (node.type === 'source' && node.href) window.open(node.href, '_blank');
        showPanel(node);
        if (hasKids && e.target.classList?.contains('toggle') || (hasKids && e.offsetX < 22)) {
          if (collapsed.has(node.id)) collapsed.delete(node.id); else collapsed.add(node.id);
          render();
        }
      });
      g.appendChild(grp);
    });
  }

  function showPanel(node) {
    panel.hidden = false;
    document.getElementById('panel-type').textContent = node.type;
    document.getElementById('panel-label').textContent = node.label;
    document.getElementById('panel-note').textContent = node.note || '';
    const link = document.getElementById('panel-link');
    if (node.href) { link.href = node.href; link.hidden = false; } else link.hidden = true;
  }

  function walk(node, fn) { fn(node); (node.children || []).forEach(c => walk(c, fn)); }

  document.getElementById('btn-expand-all').onclick = () => { collapsed.clear(); render(); };
  document.getElementById('btn-collapse-all').onclick = () => {
    walk(data.root, n => { if (n.children?.length) collapsed.add(n.id); });
    render();
  };
  document.getElementById('btn-reset').onclick = () => { state.x = 40; state.y = 40; state.scale = 1; render(); };
  document.getElementById('panel-close').onclick = () => { panel.hidden = true; };
  document.getElementById('search').oninput = e => {
    const q = e.target.value.toLowerCase().trim();
    walk(data.root, n => { n._hl = q && (n.label.toLowerCase().includes(q) || (n.note || '').toLowerCase().includes(q)); });
    render();
  };

  const wrap = document.getElementById('canvas-wrap');
  wrap.addEventListener('wheel', e => {
    e.preventDefault();
    state.scale = Math.min(2.5, Math.max(0.4, state.scale * (e.deltaY > 0 ? 0.92 : 1.08)));
    render();
  }, { passive: false });
  wrap.addEventListener('mousedown', e => { if (e.target === wrap || e.target === svg) { state.dragging = true; state.dx = e.clientX; state.dy = e.clientY; wrap.classList.add('dragging'); } });
  window.addEventListener('mousemove', e => {
    if (!state.dragging) return;
    state.x -= (e.clientX - state.dx) / state.scale;
    state.y -= (e.clientY - state.dy) / state.scale;
    state.dx = e.clientX; state.dy = e.clientY;
    render();
  });
  window.addEventListener('mouseup', () => { state.dragging = false; wrap.classList.remove('dragging'); });

  render();
})();
```

## Footer placeholder

`{{FOOTER}}` = `mind-map.json · généré {{DATE}} · ours-stack /mind-map`