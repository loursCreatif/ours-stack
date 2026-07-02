#!/usr/bin/env python3
"""Generate 3 v3 examples: palette-safe templates, claim atlas, animation budget."""
from pathlib import Path
import importlib.util
import re

_SCRIPTS = Path(__file__).resolve().parent


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, _SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_val = _load("val", "generate-validation-reports.py")
_var = _load("var", "generate-design-variants.py")
_ft = _load("ft", "figure_templates.py")

CSS = _val.CSS
BODY_CLASS = _val.BODY_CLASS
LAYOUT_CLASS = _val.LAYOUT_CLASS
HERO_DEFAULT = _val.HERO_DEFAULT
extract_parts = _val.extract_parts
remap_colors = _val.remap_colors
enhance_article = _val.enhance_article
POP_VARIANTS = _var.VARIANTS
remap_variant = _var.remap_colors
EXTRA_CSS = _ft.EXTRA_CSS

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research/robots-assemblage-structurel-chantier/report.html"
OUT_DIR = ROOT / "research/robots-assemblage-structurel-chantier"

ANIM_CSS = r"""
/* ── Figure animations (svg-graphics.md) ── */
.fig-animate .fig-layer { opacity:0; transform:translateY(12px); animation:fig-enter .6s cubic-bezier(.22,1,.36,1) forwards; }
.fig-animate .fig-layer-1 { animation-delay:.05s; }
.fig-animate .fig-layer-2 { animation-delay:.15s; }
.fig-animate .fig-layer-3 { animation-delay:.25s; }
.fig-animate .fig-layer-4 { animation-delay:.35s; }
@keyframes fig-enter { to { opacity:1; transform:translateY(0); } }
.fig-bar-fill { width:0 !important; animation:bar-grow 1s cubic-bezier(.22,1,.36,1) .3s forwards; }
@keyframes bar-grow { to { width:var(--target,50%); } }
.visual-beat.fig-animate { animation:beat-in .5s cubic-bezier(.22,1,.36,1) both; }
@keyframes beat-in { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
.stat-row { display:flex; flex-wrap:wrap; gap:.75rem; margin:.5rem 0; }
.stat-card { flex:1; min-width:110px; padding:1rem; background:var(--accent-light); border-radius:var(--radius,8px); text-align:center; }
.stat-num { display:block; font-size:2rem; font-weight:700; color:var(--accent); line-height:1.1; }
.stat-label { font-size:.72rem; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }
@media (prefers-reduced-motion:reduce) {
  .fig-animate .fig-layer,.fig-bar-fill,.visual-beat.fig-animate {
    animation:none!important; opacity:1!important; transform:none!important; width:var(--target,inherit)!important;
  }
}
"""

EXAMPLES = [
    ("editorial", "report-enhanced-editorial.html", "Editorial Ink — graphiques v3"),
    ("warm", "report-enhanced-warm.html", "Warm Bear — graphiques v3"),
    ("creative-pop", "report-enhanced-creative-pop.html", "Editorial Pop — graphiques v3"),
]

def _visual_beat_bounds(html: str, start: int) -> tuple[int, int] | None:
    if start < 0:
        return None
    depth = 0
    i = start
    while i < len(html):
        o = html.find("<div", i)
        c = html.find("</div>", i)
        if c == -1:
            return None
        if o != -1 and o < c:
            depth += 1
            i = o + 4
        else:
            depth -= 1
            end = c + 6
            i = end
            if depth == 0:
                return start, end
    return None


def _replace_visual_at(article: str, marker: str, replacement: str) -> str:
    pos = article.find(marker)
    if pos < 0:
        return article
    vb = article.find('<div class="visual-beat', pos)
    bounds = _visual_beat_bounds(article, vb)
    if not bounds:
        return article
    return article[: bounds[0]] + replacement + article[bounds[1] :]


def _replace_visual_before(article: str, marker: str, replacement: str) -> str:
    pos = article.find(marker)
    if pos < 0:
        return article
    vb = article.rfind('<div class="visual-beat', 0, pos)
    bounds = _visual_beat_bounds(article, vb)
    if not bounds:
        return article
    return article[: bounds[0]] + replacement + article[bounds[1] :]


def _replace_visual_containing(article: str, needle: str, replacement: str) -> str:
    pos = article.find(needle)
    if pos < 0:
        return article
    vb = article.rfind('<div class="visual-beat', 0, pos)
    bounds = _visual_beat_bounds(article, vb)
    if not bounds:
        return article
    return article[: bounds[0]] + replacement + article[bounds[1] :]


def _merge_insight_figures(article: str) -> str:
    s1 = article.find('<div class="visual-beat">\n          <div class="insights-grid">')
    if s1 < 0:
        return article
    b1 = _visual_beat_bounds(article, s1)
    if not b1:
        return article
    s2 = article.find('<div class="visual-beat">', b1[1])
    b2 = _visual_beat_bounds(article, s2) if s2 >= 0 else None
    if not b2:
        return article
    return article[: b1[0]] + _ft.insights_merged() + article[b2[1] :]


def _replace_section(article: str, start_marker: str, end_marker: str, replacement: str) -> str:
    s = article.find(start_marker)
    if s < 0:
        return article
    e = article.find(end_marker, s + len(start_marker))
    if e < 0:
        return article
    return article[:s] + replacement + article[e:]


def enhance_editorial_prose(article: str, preset: str, enhance_preset: str | None = None) -> str:
    ep = enhance_preset or preset
    if ep == "creative-pop":
        ep = "creative"
    out = enhance_article(article, ep)
    if preset == "editorial":
        out = out.replace(
            '<div class="pullquote">Chaque pilier a un rôle précis. Le <strong>design</strong> réduit ce que le robot doit improviser.</div>\n          Chaque pilier a un rôle précis.',
            '<div class="pullquote">Le <strong>design</strong> réduit ce que le robot doit improviser — pas l\'inverse.</div>\n          Chaque pilier a un rôle précis.',
            1,
        )
    return out


def apply_v3(article: str, preset: str, enhance_preset: str | None = None) -> str:
    """Rebuild figures from templates; max 3 animated beats (atlas, funnel, maturity)."""
    out = enhance_editorial_prose(article, preset, enhance_preset)
    out = remap_colors(out, preset)

    # Fig 1 — claim atlas after lead
    if 'id="atlas"' not in out:
        out = out.replace(
            "</div>\n\n        <div class=\"prose-beat\">\n          Le vrai goulot",
            f"</div>\n\n{_ft.claim_atlas(preset, animate=True)}\n\n        <div class=\"prose-beat\">\n          Le vrai goulot",
            1,
        )

    out = _replace_section(
        out,
        "<!-- ═══ VISUEL 1 : 3 piliers ═══ -->",
        "<!-- ═══ HORIZON ═══ -->",
        f"<!-- ═══ VISUEL 1 : 3 piliers ═══ -->\n{_ft.pillars(preset)}\n\n        ",
    )

    out = _replace_visual_at(out, '<div class="prose-beat" id="horizon">', _ft.timeline_beat())

    out = _replace_visual_before(out, "<!-- ═══ CONSTATS ═══ -->", _ft.funnel(preset, animate=True))

    out = _merge_insight_figures(out)

    out = _replace_visual_before(out, "<!-- ═══ TAXONOMIE ═══ -->", _ft.maturity(preset, animate=True))

    out = _replace_visual_at(out, 'id="taxonomie"', _ft.taxonomy_wheel(preset))

    out = _replace_visual_at(out, "<!-- ═══ STACK ═══ -->", _ft.stack_layers(preset))

    out = _replace_visual_containing(out, 'aria-label="Workflow co-robotique"', _ft.workflow_hrc(preset))

    out = _replace_visual_at(out, "<!-- ═══ DÉCISION ═══ -->", _ft.decision_tree(preset))

    # Contradictions: unnumbered appendix
    out = out.replace(
        '<p class="caption">Fig. 10 — Trois contradictions non résolues</p>',
        '<p class="caption">Annexe — Trois contradictions non résolues</p>',
    )

    # CTA references updated figure number
    out = out.replace("l'arbre de décision (Fig. 9)", "l'arbre de décision (Fig. 10)")

    return out


def main():
    html = SRC.read_text(encoding="utf-8")
    nav, article, footer = extract_parts(html)

    for preset, outfile, label in EXAMPLES:
        if preset == "creative-pop":
            cfg = POP_VARIANTS["creative-pop"]
            art = apply_v3(remap_variant(article, "creative-pop"), "creative-pop", enhance_preset="creative")
            art = art.replace('class="cta-box"', 'class="cta-box pop-callout"', 1)
            css = cfg["css"].strip() + "\n" + ANIM_CSS + EXTRA_CSS
            doc = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[{label}] Robots d'assemblage structurel</title>
  <style>
{css}
  </style>
</head>
<body{cfg["body"]}>
  <div class="{cfg["layout"]}">
    <nav>{nav}</nav>
    <main>
{cfg["hero"]}
      <article>{art}</article>
      <footer>{footer}</footer>
    </main>
  </div>
</body>
</html>"""
        else:
            art = apply_v3(article, preset)
            css = CSS[preset].strip() + "\n" + ANIM_CSS + EXTRA_CSS
            doc = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[{label}] Robots d'assemblage structurel</title>
  <style>
{css}
  </style>
</head>
<body{BODY_CLASS[preset]}>
  <div class="{LAYOUT_CLASS[preset]}">
    <nav>{nav}</nav>
    <main>
{HERO_DEFAULT}
      <article>{art}</article>
      <footer>{footer}</footer>
    </main>
  </div>
</body>
</html>"""

        path = OUT_DIR / outfile
        path.write_text(doc, encoding="utf-8")
        print(f"wrote {path}")

    hub = OUT_DIR / "report-enhanced-gallery.html"
    hub.write_text(
        """<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Exemples graphiques v3</title>
<style>body{font-family:system-ui;background:#0f1419;color:#e8eaed;padding:2rem;max-width:700px;margin:0 auto}
a{display:block;margin:1rem 0;padding:1rem;background:#1a2332;border-radius:10px;color:#7eb8ff;text-decoration:none;font-weight:600}
a:hover{background:#243044} h1{font-size:1.4rem} p{color:#9aa0a6}
.links{display:flex;flex-direction:column;gap:.5rem}</style></head>
<body>
<h1>3 exemples — graphiques v3</h1>
<p>Claim atlas · palettes strictes · funnel animé · validateur · max 3 animations</p>
<div class="links">
<a href="report-enhanced-editorial.html" target="_blank" rel="noopener">Editorial Ink v3 →</a>
<a href="report-enhanced-warm.html" target="_blank" rel="noopener">Warm Bear v3 →</a>
<a href="report-enhanced-creative-pop.html" target="_blank" rel="noopener">Editorial Pop v3 →</a>
</div>
</body></html>""",
        encoding="utf-8",
    )
    print(f"wrote {hub}")


if __name__ == "__main__":
    main()