# Preset: `editorial` — Magazine Ink

**Shell:** `<body class="preset-editorial">` · `.layout.layout-editorial` — **no sidebar grid**  
**Nav:** horizontal strip above main (`border-bottom`, inline links)  
**Hero:** no gradient; large serif `h1` `clamp(2rem, 5vw, 3.2rem)`; `border-bottom: 2px solid accent`  
**Article:** transparent — no card, no shadow, no border  
**Prose:** `max-width: 68ch`; `.lead::first-letter` drop cap; sans-serif for `.prose-beat`  
**Figures:** thin borders, cream surface, captions italic left  
**SVG grammar:** thin strokes `stroke-width: 1`, serif-friendly, minimal gradients

## SVG palette

`#8b2942` `#b85c72` `#2d5a3d` `#8b6914` `#6b6560` `#f5e8ec` `#faf3e0`

## Document skeleton

```html
<body class="preset-editorial">
  <div class="layout layout-editorial">
    <nav>...</nav>
    <main>
      <header class="hero">...</header>
      <article>...</article>
      <footer>...</footer>
    </main>
  </div>
</body>
```

## Optional (magazine)

```html
<span class="section-kicker">Synthèse</span>
<h2>Section title</h2>
<div class="pullquote">One strong sentence from the source.</div>
<div class="epigraph">Epigraph before a section — italic, muted.</div>
```

## Full CSS

Reference: `research/robots-assemblage-structurel-chantier/report-editorial.html` `<style>` block.