# Preset: `creative` — Spicy Pop

**Shell:** `<body class="preset-creative">` · `.layout.layout-creative` · subtle 45° stripe `background-image` on body  
**Nav:** sticker links — `border: 2px`, `box-shadow: 3px 3px 0`, hover `rotate(-1deg)` + cyan fill  
**Hero:** neo-brutalist — yellow card, magenta title band, `.hero-deck` skewed white strip  
**Article:** `border: 3px solid`, hard shadow `6px 6px 0`  
**Prose:** `.lead` yellow + 3px border; `strong` alternates magenta / violet  
**Figures:** sticker frames, slight alternating `rotate(±0.4deg)` — disabled on mobile  
**SVG grammar:** saturated multi-color, `stroke-width: 2.5`, bold labels, Memphis geometry

## Garde-fous

- Body text stays `#1a0a2e` on light bg — readable
- No infinite CSS animations
- Funnel numbers stay plain weight (no decorative distortion)
- Content faithful to source — only habillage changes

## SVG palette

`#ff2d6a` `#7b2ff7` `#00d4aa` `#ffb800` `#00a878` `#ff6b00` `#5c4a7a` `#ffe0ec` `#f3f0ff`

## Hero HTML (research)

```html
<header class="hero">
  <h1>{{TITLE}}</h1>
  <div class="hero-deck">
    <p class="subtitle">{{DISCOVERED}} sources · {{READ}} lectures · {{DATE}}</p>
    <span class="badge">Confiance {{CONFIDENCE}}</span>
  </div>
</header>
```

## Smart-skip aliases

`créatif`, `creative`, `spicy`, `wtf`, `pop`, `coloré`, `original`

## Optional

```html
<div class="cta-box spicy-callout">…action steps…</div>
```

## Full CSS

Reference: `research/robots-assemblage-structurel-chantier/report-creative.html` `<style>` block.