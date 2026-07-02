# Preset: `academic` — Research Dashboard

**Shell:** `body` default · `.layout` sidebar 260px + main `max-width: 920px`  
**Hero:** white report header, `border-top: 6px solid var(--accent)`, `.metric-pill` row (no gradient)  
**Nav:** sticky left, border-left highlight on hover  
**Prose:** `h2` numbered via CSS counter (`01 ·`, `02 ·`…)  
**Figures:** `.visual-beat` exhibit — white, `border-left: 4px solid var(--accent)`  
**SVG grammar:** gradients légers, `rx: 6–10`, `stroke-width: 1.5`, sans-serif labels

## SVG palette

`#1e4d8c` `#2d6cb5` `#3d8fd4` `#1a6b4a` `#9a6b00` `#5c6370` `#e8f0fa` `#d4e4f7`

## Hero HTML (research)

```html
<header class="hero">
  <h1>{{TITLE}}</h1>
  <div class="hero-metrics">
    <span class="metric-pill">{{DISCOVERED}} sources</span>
    <span class="metric-pill">{{READ}} lectures</span>
    <span class="metric-pill">{{DATE}}</span>
    <span class="badge">Confiance {{CONFIDENCE}}</span>
  </div>
</header>
```

## Optional (Tufte-inspired)

```html
<div class="prose-beat sidenote">Note méthodologique — 179 sources, 20 lues…</div>
```

## Full CSS

Reference: `research/robots-assemblage-structurel-chantier/report-academic.html` `<style>` block.