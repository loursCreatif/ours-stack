# HTML template — layout-html

Copy this structure. Replace `{{PLACEHOLDERS}}`. Quality references: `research/robots-assemblage-structurel-chantier/report-{academic,editorial,minimal,warm,creative}.html`

## Document skeleton

```html
<!DOCTYPE html>
<html lang="{{LANG}}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>
  <style>
    /* ── paste full CSS block below ── */
  </style>
</head>
<body class="preset-{{PRESET_ID}}">
  <div class="layout layout-{{PRESET_ID}}">
    <nav>
      <h2>{{TOC_LABEL}}</h2>
      <!-- <a href="#anchor">Label</a> × 6–12 -->
    </nav>
    <main>
      <!-- Research hero -->
      <header class="hero">
        <h1>{{TITLE}}</h1>
        <p class="subtitle">{{DISCOVERED}} sources · {{READ}} lectures · {{DATE}}</p>
        <span class="badge">Confiance {{CONFIDENCE}}</span>
      </header>

      <!-- Generic article hero (use when no funnel counts) -->
      <!--
      <header class="hero">
        <h1>{{TITLE}}</h1>
        <p class="subtitle">{{DATE_OR_READING_TIME}} · {{TOPIC_TAG}}</p>
        <span class="badge">{{BADGE}}</span>
      </header>
      -->
      <article>
        <!-- alternating .prose-beat / .visual-beat -->
      </article>
      <footer>{{FOOTER}}</footer>
    </main>
  </div>
</body>
</html>
```

`{{TOC_LABEL}}` = `Sommaire` (FR) or `Contents` (EN) — match report language.

**Style:** load the active preset profile from `references/presets/{{PRESET_ID}}.md`. Paste its **full CSS** into `<style>`. Apply preset-specific shell (body class, layout class, hero variant, nav pattern). Beat class names stay shared (`.prose-beat`, `.visual-beat`) but preset CSS redefines their look.

Optional HTML comment after `<html>`: `<!-- style: {{PRESET_ID}} -->`

**Preset shell variants:**

| Preset | `body` | `.layout` | Nav | Article |
|--------|--------|-----------|-----|---------|
| `academic` | default | `.layout` grid 260px | sticky sidebar | card |
| `editorial` | `.preset-editorial` | `.layout.layout-editorial` block | top strip | transparent |
| `minimal` | `.preset-minimal` | `.layout.layout-minimal` | mono sidebar | flat border |
| `warm` | `.preset-warm` | `.layout.layout-warm` | numbered path | soft card |
| `creative` | `.preset-creative` | `.layout.layout-creative` | sticker nav | brutal shadow |

## Full CSS (inline, required — default = academic preset)

```css
:root {
  --bg: #f4f6f9;
  --surface: #fff;
  --text: #1a1d23;
  --muted: #5c6370;
  --border: #dde2ea;
  --accent: #1e4d8c;
  --accent-light: #e8f0fa;
  --success: #1a6b4a;
  --success-bg: #e8f5ee;
  --warning: #9a6b00;
  --warning-bg: #fff8e6;
  --radius: 12px;
  --shadow: 0 2px 8px rgba(30,77,140,.06), 0 8px 24px rgba(0,0,0,.05);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.65; font-size: 16px; }

.layout { display: grid; grid-template-columns: 220px 1fr; min-height: 100vh; }
nav { position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--surface); border-right: 1px solid var(--border); padding: 1.2rem .75rem; }
nav h2 { font-size: .68rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: .75rem; padding-left: .4rem; }
nav a { display: block; padding: .35rem .6rem; color: var(--text); text-decoration: none; border-radius: 6px; font-size: .82rem; }
nav a:hover { background: var(--accent-light); color: var(--accent); }

main { max-width: 740px; padding: 2rem 1.5rem 4rem; }

header.hero {
  background: linear-gradient(135deg, #163d6e, #2d6cb5 60%, #3d8fd4);
  color: #fff; border-radius: var(--radius); padding: 1.75rem 1.85rem; margin-bottom: 1.5rem; box-shadow: var(--shadow);
}
header.hero h1 { font-size: 1.55rem; margin-bottom: .4rem; }
header.hero .subtitle { opacity: .92; font-size: .92rem; margin-bottom: .85rem; }
.badge { background: rgba(255,255,255,.18); padding: .2rem .55rem; border-radius: 20px; font-size: .75rem; font-weight: 600; margin-right: .4rem; display: inline-block; }

article { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.75rem 1.85rem; box-shadow: var(--shadow); }

.prose-beat { margin: 1.5rem 0; font-size: .98rem; line-height: 1.72; color: var(--text); }
.prose-beat:first-child { margin-top: 0; }
.prose-beat strong { color: var(--accent); font-weight: 600; }
.prose-beat.lead {
  font-size: 1.05rem; background: var(--accent-light); border-left: 4px solid var(--accent);
  padding: 1rem 1.15rem; border-radius: 0 8px 8px 0; margin: 0 0 1.25rem;
}
.prose-beat.tight { margin: 1rem 0; font-size: .94rem; color: var(--muted); }
.prose-beat h2 { font-size: 1.2rem; color: var(--accent); margin-bottom: .5rem; padding-top: .5rem; border-top: 1px solid var(--border); }
.prose-beat h2:first-child { border-top: none; padding-top: 0; }
.prose-beat ul { margin: .4rem 0 .2rem 1.1rem; }
.prose-beat li { margin-bottom: .25rem; }

.visual-beat { margin: 1.25rem 0 1.5rem; background: var(--bg); border-radius: 10px; padding: 1.1rem 1rem; overflow-x: auto; }
.visual-beat svg { display: block; max-width: 100%; height: auto; margin: 0 auto; }
.caption { text-align: center; font-size: .78rem; color: var(--muted); margin-top: .55rem; font-style: italic; }

/* ── Figure animations (include when using .fig-animate — see svg-graphics.md) ── */
.fig-animate .fig-layer { opacity:0; transform:translateY(12px); animation:fig-enter .6s cubic-bezier(.22,1,.36,1) forwards; }
.fig-animate .fig-layer-1 { animation-delay:.05s; }
.fig-animate .fig-layer-2 { animation-delay:.15s; }
.fig-animate .fig-layer-3 { animation-delay:.25s; }
@keyframes fig-enter { to { opacity:1; transform:translateY(0); } }
.fig-bar-fill { width:0 !important; animation:bar-grow 1s cubic-bezier(.22,1,.36,1) .3s forwards; }
@keyframes bar-grow { to { width:var(--target,50%); } }
.visual-beat.fig-animate { animation:beat-in .5s cubic-bezier(.22,1,.36,1) both; }
@keyframes beat-in { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
.insight-card.fig-stagger { opacity:0; animation:fig-enter .45s cubic-bezier(.22,1,.36,1) forwards; }
.insights-grid .insight-card:nth-child(1) { animation-delay:.05s; }
.insights-grid .insight-card:nth-child(2) { animation-delay:.12s; }
.insights-grid .insight-card:nth-child(3) { animation-delay:.19s; }
.insights-grid .insight-card:nth-child(4) { animation-delay:.26s; }
.stat-row { display:flex; flex-wrap:wrap; gap:.75rem; }
.stat-card { flex:1; min-width:120px; padding:1rem; background:var(--accent-light); border-radius:var(--radius,8px); text-align:center; }
.stat-num { display:block; font-size:2rem; font-weight:700; color:var(--accent); line-height:1.1; }
.stat-label { font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
@media (prefers-reduced-motion:reduce) {
  .fig-animate .fig-layer,.fig-bar-fill,.visual-beat.fig-animate,.insight-card.fig-stagger { animation:none!important; opacity:1!important; transform:none!important; width:var(--target,inherit)!important; }
}

.insights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; }
.insight-card { padding: .85rem; border-radius: 8px; border-left: 3px solid var(--accent); background: var(--bg); font-size: .86rem; }
.insight-card .num { display: inline-block; width: 22px; height: 22px; background: var(--accent); color: #fff; border-radius: 50%; text-align: center; line-height: 22px; font-size: .7rem; font-weight: 700; margin-right: .35rem; }
.insight-card strong { color: var(--accent); }
.insight-card .src { display: block; font-size: .72rem; color: var(--muted); margin-top: .3rem; }

.timeline { display: flex; gap: 0; margin: 0; position: relative; }
.timeline::before { content: ''; position: absolute; top: 26px; left: 8%; right: 8%; height: 3px; background: linear-gradient(90deg, var(--success), var(--warning), #6c757d); border-radius: 2px; z-index: 0; }
.timeline-phase { flex: 1; text-align: center; position: relative; z-index: 1; padding: 0 .35rem; }
.timeline-dot { width: 50px; height: 50px; border-radius: 50%; margin: 0 auto .5rem; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .68rem; color: #fff; border: 3px solid var(--surface); box-shadow: var(--shadow); }
.timeline-phase:nth-child(1) .timeline-dot { background: var(--success); }
.timeline-phase:nth-child(2) .timeline-dot { background: var(--warning); }
.timeline-phase:nth-child(3) .timeline-dot { background: #6c757d; }
.timeline-phase h4 { font-size: .8rem; margin-bottom: .3rem; }
.timeline-phase ul { list-style: none; font-size: .74rem; color: var(--muted); text-align: left; }
.timeline-phase li { padding: .1rem 0 .1rem .8rem; position: relative; }
.timeline-phase li::before { content: '→'; position: absolute; left: 0; color: var(--accent); }

.maturity-grid { display: grid; gap: .55rem; }
.maturity-row { display: grid; grid-template-columns: 130px 1fr 82px; align-items: center; gap: .6rem; font-size: .82rem; }
.maturity-row .label { font-weight: 600; }
.maturity-bar { height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }
.maturity-fill { height: 100%; border-radius: 10px; font-size: .65rem; font-weight: 600; color: #fff; display: flex; align-items: center; padding-left: .45rem; }

.contradiction-card { display: grid; grid-template-columns: 1fr auto 1fr auto; gap: .45rem; align-items: center; background: var(--bg); padding: .75rem .9rem; border-radius: 8px; margin-bottom: .55rem; font-size: .84rem; }
.contra-side { padding: .45rem .55rem; border-radius: 6px; background: var(--surface); border: 1px solid var(--border); }
.contra-side strong { display: block; font-size: .68rem; color: var(--muted); text-transform: uppercase; margin-bottom: .15rem; }
.contra-vs { font-weight: 800; color: var(--accent); font-size: .85rem; }
.tag { display: inline-block; padding: .1rem .4rem; border-radius: 4px; font-size: .68rem; font-weight: 600; }
.tag-mixed { background: #f8d7da; color: #721c24; }
.tag-weak { background: #e2e3e5; color: #6c757d; }

.sources-compact { font-size: .88rem; list-style: none; }
.sources-compact a { color: var(--accent); }
.sources-compact li { margin-bottom: .35rem; }

.cta-box { background: linear-gradient(135deg, var(--accent-light), #fff); border: 2px solid var(--accent); border-radius: 10px; padding: 1rem 1.15rem; margin-top: 1rem; font-size: .92rem; }
.confidence { display: flex; gap: .85rem; align-items: center; padding: .9rem; background: var(--accent-light); border-radius: 8px; margin-top: 1rem; font-size: .88rem; }
.confidence .level { font-size: 1.2rem; font-weight: 700; color: var(--accent); white-space: nowrap; }

footer { text-align: center; color: var(--muted); font-size: .8rem; padding: 1.25rem 0 0; }

@media (max-width: 800px) {
  .layout { grid-template-columns: 1fr; }
  nav { position: static; height: auto; }
  main { padding: 1rem; }
  .insights-grid { grid-template-columns: 1fr; }
  .timeline { flex-direction: column; gap: .85rem; }
  .timeline::before { display: none; }
  .maturity-row { grid-template-columns: 1fr; }
  .contradiction-card { grid-template-columns: 1fr; text-align: center; }
}
```

## Beat patterns

**Lead answer:**

```html
<div class="prose-beat lead" id="reponse">
  <strong>{{HOOK}}.</strong> {{2–3 sentences from executive summary}}
</div>
```

**Standard prose:**

```html
<div class="prose-beat" id="{{ANCHOR}}">
  <h2>{{SECTION_TITLE}}</h2>
  {{2–4 sentences}}
</div>
```

**Visual with caption:**

```html
<div class="visual-beat" id="{{ANCHOR}}">
  <!-- SVG or HTML component -->
  <p class="caption">Fig. {{N}} — {{LEGEND}}</p>
</div>
```

**Sources compact:**

```html
<div class="visual-beat">
  <ul class="sources-compact">
    <li>⭐ <a href="{{URL}}">{{Author}} ({{YEAR}}) — {{TITLE}}</a></li>
  </ul>
  <p class="caption">Sources clés — liens directs</p>
</div>
```

**Footer:**

```html
<footer>Recherche du {{DATE}} · {{DISCOVERED}} sources · {{MODE}} · index complet : sources-index.md</footer>
```

## Print variant (`report-print.html`)

Append to `<style>`:

```css
@media print {
  .layout { display: block; }
  nav { display: none; }
  main { max-width: 100%; padding: 0; }
  article { box-shadow: none; border: none; }
  .visual-beat { page-break-inside: avoid; }
  header.hero { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
```