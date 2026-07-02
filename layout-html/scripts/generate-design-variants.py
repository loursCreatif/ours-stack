#!/usr/bin/env python3
"""Generate alternative design variants for academic, minimal, creative presets."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research/robots-assemblage-structurel-chantier/report.html"
OUT_DIR = ROOT / "research/robots-assemblage-structurel-chantier"

BASE_REMAP = {
    "#8b2942": "#8b2942", "#b85c72": "#b85c72", "#2d5a3d": "#2d5a3d", "#3d6b4d": "#3d6b4d",
    "#8b6914": "#8b6914", "#6b6560": "#6b6560", "#f5e8ec": "#f5e8ec", "#edd5dc": "#edd5dc",
    "#faf3e0": "#faf3e0", "#ede8e0": "#ede8e0", "#f5edd0": "#f5edd0",
}

REMAP = {
    "academic-manuscript": {
        **BASE_REMAP,
        "#8b2942": "#2c5282", "#b85c72": "#4a6fa5", "#2d5a3d": "#2f6f4e", "#3d6b4d": "#2f6f4e",
        "#8b6914": "#8b6914", "#6b6560": "#64748b", "#f5e8ec": "#f1f5f9", "#edd5dc": "#e2e8f0",
        "#faf3e0": "#f8fafc", "#ede8e0": "#f1f5f9", "#f5edd0": "#f8fafc",
    },
    "academic-lab": {
        **BASE_REMAP,
        "#8b2942": "#0d6e6e", "#b85c72": "#14a3a3", "#2d5a3d": "#1a7a4a", "#3d6b4d": "#1a7a4a",
        "#8b6914": "#c47d0e", "#6b6560": "#5a6b6b", "#f5e8ec": "#e8f4f4", "#edd5dc": "#d4ecec",
        "#faf3e0": "#faf8f5", "#ede8e0": "#f0f4f4", "#f5edd0": "#faf8f5",
    },
    "academic-night": {
        **BASE_REMAP,
        "#8b2942": "#58a6ff", "#b85c72": "#79b8ff", "#2d5a3d": "#3fb950", "#3d6b4d": "#3fb950",
        "#8b6914": "#d29922", "#6b6560": "#8b949e", "#f5e8ec": "#161b22", "#edd5dc": "#21262d",
        "#faf3e0": "#0d1117", "#ede8e0": "#161b22", "#f5edd0": "#0d1117",
    },
    "minimal-swiss": {
        **BASE_REMAP,
        "#8b2942": "#111", "#b85c72": "#333", "#2d5a3d": "#111", "#3d6b4d": "#111",
        "#8b6914": "#e63946", "#6b6560": "#666", "#f5e8ec": "#fff", "#edd5dc": "#f5f5f5",
        "#faf3e0": "#fff", "#ede8e0": "#fafafa", "#f5edd0": "#fff",
    },
    "minimal-quiet": {
        **BASE_REMAP,
        "#8b2942": "#37352f", "#b85c72": "#6b6b6b", "#2d5a3d": "#448361", "#3d6b4d": "#448361",
        "#8b6914": "#cb912f", "#6b6560": "#9b9a97", "#f5e8ec": "#f7f7f5", "#edd5dc": "#ededeb",
        "#faf3e0": "#f7f7f5", "#ede8e0": "#f1f1ef", "#f5edd0": "#f7f7f5",
    },
    "minimal-brutal": {
        **BASE_REMAP,
        "#8b2942": "#000", "#b85c72": "#000", "#2d5a3d": "#000", "#3d6b4d": "#000",
        "#8b6914": "#000", "#6b6560": "#444", "#f5e8ec": "#fff", "#edd5dc": "#fff",
        "#faf3e0": "#fff", "#ede8e0": "#fff", "#f5edd0": "#fff",
    },
    "creative-pop": {
        **BASE_REMAP,
        "#8b2942": "#ff4757", "#b85c72": "#ff6b81", "#2d5a3d": "#2ed573", "#3d6b4d": "#2ed573",
        "#8b6914": "#ffa502", "#6b6560": "#57606f", "#f5e8ec": "#fff5f6", "#edd5dc": "#ffe8ea",
        "#faf3e0": "#fff9f0", "#ede8e0": "#f8f9fa", "#f5edd0": "#fff9f0",
    },
    "creative-aurora": {
        **BASE_REMAP,
        "#8b2942": "#7c3aed", "#b85c72": "#a78bfa", "#2d5a3d": "#06b6d4", "#3d6b4d": "#22d3ee",
        "#8b6914": "#f59e0b", "#6b6560": "#64748b", "#f5e8ec": "#faf5ff", "#edd5dc": "#ede9fe",
        "#faf3e0": "#f0fdfa", "#ede8e0": "#f8fafc", "#f5edd0": "#fffbeb",
    },
    "creative-riso": {
        **BASE_REMAP,
        "#8b2942": "#2b4c7e", "#b85c72": "#e8488a", "#2d5a3d": "#2b4c7e", "#3d6b4d": "#2b4c7e",
        "#8b6914": "#f4d35e", "#6b6560": "#5c4d3c", "#f5e8ec": "#fff8e7", "#edd5dc": "#fde8f0",
        "#faf3e0": "#fff8e7", "#ede8e0": "#f5f0e8", "#f5edd0": "#fff8e7",
    },
}

VARIANTS = {
    "academic-manuscript": {
        "label": "Manuscript",
        "body": ' class="variant-manuscript"',
        "layout": "layout layout-manuscript",
        "hero": """      <header class="hero">
        <p class="hero-meta">Recherche · 179 sources · 20 lectures · 1 juillet 2026</p>
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="hero-deck">Confiance moyenne-haute — synthèse structurée pour lecture longue.</p>
      </header>""",
        "css": r"""
:root { --bg:#fafaf8; --text:#1c1917; --muted:#78716c; --border:#e7e5e4; --accent:#2c5282; --accent-light:#f1f5f9; --success:#2f6f4e; --warning:#8b6914; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-manuscript { font-family: Charter, "Bitstream Charter", Georgia, serif; background:var(--bg); color:var(--text); line-height:1.75; font-size:18px; }
.layout-manuscript { max-width:1100px; margin:0 auto; padding:2rem 1.5rem 4rem; }
.layout-manuscript nav { display:flex; flex-wrap:wrap; gap:.35rem .6rem; padding-bottom:1rem; margin-bottom:2rem; border-bottom:1px solid var(--border); font-family:system-ui,sans-serif; font-size:.75rem; }
.layout-manuscript nav h2 { display:none; }
.layout-manuscript nav a { color:var(--muted); text-decoration:none; }
.layout-manuscript nav a:hover { color:var(--accent); text-decoration:underline; }
header.hero { margin-bottom:2.5rem; max-width:42rem; }
.hero-meta { font-family:system-ui,sans-serif; font-size:.72rem; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); margin-bottom:.75rem; }
header.hero h1 { font-size:clamp(1.8rem,4vw,2.6rem); font-weight:400; line-height:1.2; margin-bottom:.75rem; }
.hero-deck { font-size:1.05rem; color:var(--muted); font-style:italic; }
article { display:grid; grid-template-columns:minmax(0,42rem) minmax(0,14rem); gap:2rem 3rem; align-items:start; }
.prose-beat { margin:1.5rem 0; font-size:1rem; max-width:42rem; grid-column:1; }
.prose-beat strong { color:var(--accent); }
.prose-beat.lead { font-size:1.12rem; margin:0 0 2rem; }
.prose-beat.lead::first-letter { float:left; font-size:3.5rem; line-height:.8; padding-right:.1em; color:var(--accent); font-weight:700; }
.prose-beat h2 { font-size:1.25rem; font-weight:600; margin-top:2.5rem; margin-bottom:.5rem; color:var(--text); border-top:1px solid var(--border); padding-top:1.5rem; }
.prose-beat.tight, .sidenote { grid-column:2; font-family:system-ui,sans-serif; font-size:.82rem; line-height:1.55; color:var(--muted); padding:.5rem 0 .5rem 1rem; border-left:2px solid var(--border); margin:0; }
.visual-beat { grid-column:1 / -1; margin:2rem 0; padding:1.25rem 0; border-top:1px solid var(--border); border-bottom:1px solid var(--border); overflow-x:auto; }
.caption { font-family:system-ui,sans-serif; font-size:.76rem; color:var(--muted); margin-top:.6rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.65rem; font-family:system-ui,sans-serif; font-size:.86rem; }
.insight-card { padding:.75rem; border-top:2px solid var(--accent); background:var(--accent-light); }
.insight-card .num { color:var(--accent); font-weight:700; margin-right:.3rem; }
.timeline { display:flex; gap:1rem; font-family:system-ui,sans-serif; }
.timeline-dot { width:44px; height:44px; border-radius:50%; border:1px solid var(--border); display:flex; align-items:center; justify-content:center; font-size:.65rem; font-weight:600; margin:0 auto .4rem; background:#fff; }
.timeline-phase:nth-child(1) .timeline-dot { background:var(--success); color:#fff; border-color:var(--success); }
.timeline-phase:nth-child(2) .timeline-dot { background:var(--warning); color:#fff; border-color:var(--warning); }
.timeline-phase:nth-child(3) .timeline-dot { background:var(--muted); color:#fff; }
.maturity-row { display:grid; grid-template-columns:120px 1fr 70px; gap:.5rem; font-size:.8rem; font-family:system-ui,sans-serif; margin-bottom:.35rem; }
.maturity-bar { height:14px; background:var(--border); }
.maturity-fill { height:100%; background:var(--accent); font-size:.6rem; color:#fff; display:flex; align-items:center; padding-left:.35rem; }
.mat-f .maturity-fill,.mat-a .maturity-fill { background:var(--success); }
.mat-e .maturity-fill { background:var(--warning); }
.contradiction-card { display:grid; grid-template-columns:1fr auto 1fr auto; gap:.4rem; font-size:.82rem; font-family:system-ui,sans-serif; margin-bottom:.4rem; }
.contra-side { border:1px solid var(--border); padding:.4rem; }
.cta-box,.confidence { font-family:system-ui,sans-serif; font-size:.9rem; grid-column:1; max-width:42rem; }
.cta-box { border-left:3px solid var(--accent); padding:.75rem 1rem; margin-top:1rem; background:var(--accent-light); }
.confidence { border-top:1px solid var(--border); padding-top:1rem; margin-top:1.5rem; }
footer { grid-column:1 / -1; font-family:system-ui,sans-serif; font-size:.78rem; color:var(--muted); margin-top:2rem; padding-top:1rem; border-top:1px solid var(--border); }
@media (max-width:900px) { article { grid-template-columns:1fr; } .prose-beat.tight,.sidenote { grid-column:1; border-left:none; border-top:1px solid var(--border); padding-left:0; padding-top:.75rem; } }
""",
    },
    "academic-lab": {
        "label": "Lab Notebook",
        "body": ' class="variant-lab"',
        "layout": "layout layout-lab",
        "hero": """      <header class="hero">
        <span class="lab-tag">Rapport de synthèse</span>
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <div class="lab-stats"><span>179 sources</span><span>20 lectures</span><span>01/07/2026</span><span class="conf-badge">Confiance moyenne-haute</span></div>
      </header>""",
        "css": r"""
:root { --bg:#faf8f5; --surface:#fff; --text:#1a2e2e; --muted:#5a6b6b; --border:#d4e0e0; --accent:#0d6e6e; --accent-light:#e8f4f4; --success:#1a7a4a; --warning:#c47d0e; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-lab { font-family:system-ui,-apple-system,sans-serif; background:var(--bg); color:var(--text); line-height:1.65; font-size:16px; }
.layout-lab { display:grid; grid-template-columns:220px 1fr; min-height:100vh; }
nav { position:sticky; top:0; height:100vh; overflow-y:auto; background:var(--surface); border-right:1px dashed var(--border); padding:1.25rem .75rem; }
nav h2 { font-size:.65rem; text-transform:uppercase; letter-spacing:.1em; color:var(--accent); margin-bottom:.75rem; }
nav a { display:block; padding:.3rem .5rem; color:var(--text); text-decoration:none; font-size:.8rem; border-radius:4px; }
nav a:hover { background:var(--accent-light); color:var(--accent); }
main { max-width:860px; padding:2rem 1.75rem 4rem; }
header.hero { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1.5rem; margin-bottom:1.5rem; position:relative; }
header.hero::after { content:''; position:absolute; top:12px; right:12px; width:48px; height:48px; border:2px dashed var(--border); border-radius:50%; opacity:.5; }
.lab-tag { display:inline-block; font-size:.68rem; text-transform:uppercase; letter-spacing:.12em; color:var(--accent); font-weight:700; margin-bottom:.5rem; }
header.hero h1 { font-size:1.5rem; margin-bottom:.75rem; color:var(--accent); }
.lab-stats { display:flex; flex-wrap:wrap; gap:.5rem; font-size:.78rem; color:var(--muted); }
.lab-stats span { background:var(--accent-light); padding:.2rem .55rem; border-radius:4px; }
.conf-badge { background:var(--success)!important; color:#fff!important; font-weight:600; }
article { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1.75rem; }
.prose-beat { margin:1.4rem 0; }
.prose-beat strong { color:var(--accent); }
.prose-beat.lead { background:var(--accent-light); border-radius:6px; padding:1rem 1.15rem; margin:0 0 1.25rem; border-left:4px solid var(--accent); }
.prose-beat h2 { font-size:1.1rem; color:var(--accent); margin-top:1.75rem; padding-bottom:.35rem; border-bottom:1px dotted var(--border); }
.prose-beat.tight { font-size:.88rem; color:var(--muted); font-style:italic; background:var(--bg); padding:.75rem; border-radius:4px; border:1px dashed var(--border); }
.visual-beat { margin:1.25rem 0; background:var(--bg); border:1px solid var(--border); border-radius:6px; padding:1.1rem; overflow-x:auto; }
.caption { font-size:.76rem; color:var(--muted); margin-top:.5rem; }
.caption::before { content:'Fig. · '; font-weight:600; color:var(--accent); }
.insight-card { padding:.75rem; border:1px solid var(--border); border-radius:6px; background:var(--bg); font-size:.84rem; }
.insight-card .num { display:inline-block; width:20px; height:20px; background:var(--accent); color:#fff; border-radius:50%; text-align:center; line-height:20px; font-size:.65rem; font-weight:700; margin-right:.3rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.55rem; }
.maturity-bar { height:18px; background:var(--accent-light); border-radius:9px; overflow:hidden; }
.maturity-fill { height:100%; border-radius:9px; font-size:.65rem; color:#fff; display:flex; align-items:center; padding-left:.4rem; }
.mat-f .maturity-fill,.mat-a .maturity-fill { background:var(--success); }
.mat-c .maturity-fill,.mat-d .maturity-fill { background:var(--accent); }
.mat-e .maturity-fill { background:var(--warning); }
.mat-b .maturity-fill { background:var(--muted); }
.cta-box { border:1px solid var(--accent); border-radius:6px; padding:1rem; background:var(--accent-light); margin-top:1rem; }
.confidence { display:flex; gap:.75rem; padding:.85rem; background:var(--accent-light); border-radius:6px; margin-top:1rem; font-size:.88rem; }
footer { text-align:center; color:var(--muted); font-size:.78rem; padding:1.25rem 0 0; }
@media (max-width:800px) { .layout-lab { grid-template-columns:1fr; } nav { position:static; height:auto; } .insights-grid { grid-template-columns:1fr; } }
""",
    },
    "academic-night": {
        "label": "Night Research",
        "body": ' class="variant-night"',
        "layout": "layout layout-night",
        "hero": """      <header class="hero">
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="subtitle">179 sources · 20 lectures · 1 juillet 2026 · <strong>Confiance moyenne-haute</strong></p>
      </header>""",
        "css": r"""
:root { --bg:#0d1117; --surface:#161b22; --text:#e6edf3; --muted:#8b949e; --border:#30363d; --accent:#58a6ff; --accent-light:#1f2937; --success:#3fb950; --warning:#d29922; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-night { font-family:system-ui,-apple-system,sans-serif; background:var(--bg); color:var(--text); line-height:1.65; font-size:16px; }
.layout-night { display:grid; grid-template-columns:240px 1fr; min-height:100vh; }
nav { position:sticky; top:0; height:100vh; overflow-y:auto; background:var(--surface); border-right:1px solid var(--border); padding:1.2rem .75rem; }
nav h2 { font-size:.65rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin-bottom:.75rem; }
nav a { display:block; padding:.35rem .55rem; color:var(--muted); text-decoration:none; font-size:.82rem; border-radius:6px; }
nav a:hover { background:var(--accent-light); color:var(--accent); }
main { max-width:900px; padding:2rem 1.5rem 4rem; }
header.hero { margin-bottom:1.5rem; padding-bottom:1.25rem; border-bottom:1px solid var(--border); }
header.hero h1 { font-size:1.65rem; color:var(--text); margin-bottom:.5rem; }
header.hero .subtitle { font-size:.88rem; color:var(--muted); }
header.hero .subtitle strong { color:var(--success); }
article { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1.75rem; }
.prose-beat { margin:1.4rem 0; }
.prose-beat strong { color:var(--accent); }
.prose-beat.lead { background:var(--accent-light); border-left:3px solid var(--accent); padding:1rem 1.15rem; border-radius:0 6px 6px 0; margin:0 0 1.25rem; }
.prose-beat h2 { font-size:1.15rem; color:var(--text); margin-top:1.75rem; padding-top:.75rem; border-top:1px solid var(--border); }
.prose-beat.tight { font-size:.88rem; color:var(--muted); font-family:ui-monospace,monospace; background:#0d1117; padding:.65rem .85rem; border-radius:6px; border:1px solid var(--border); }
.visual-beat { margin:1.25rem 0; background:#0d1117; border:1px solid var(--border); border-radius:8px; padding:1.1rem; overflow-x:auto; }
.caption { font-size:.76rem; color:var(--muted); margin-top:.5rem; }
.insight-card { padding:.75rem; background:var(--bg); border:1px solid var(--border); border-radius:6px; font-size:.84rem; }
.insight-card .num { color:var(--accent); font-weight:700; margin-right:.3rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.55rem; }
.maturity-bar { height:16px; background:var(--border); border-radius:8px; overflow:hidden; }
.maturity-fill { height:100%; background:var(--accent); font-size:.65rem; color:#fff; display:flex; align-items:center; padding-left:.4rem; }
.mat-f .maturity-fill,.mat-a .maturity-fill { background:var(--success); }
.mat-e .maturity-fill { background:var(--warning); }
.cta-box { border:1px solid var(--accent); border-radius:6px; padding:1rem; background:rgba(88,166,255,.08); margin-top:1rem; }
.confidence { display:flex; gap:.75rem; padding:.85rem; border:1px solid var(--border); border-radius:6px; margin-top:1rem; }
.confidence .level { color:var(--success); font-weight:700; }
footer { text-align:center; color:var(--muted); font-size:.78rem; padding:1.25rem 0 0; }
@media (max-width:800px) { .layout-night { grid-template-columns:1fr; } nav { position:static; height:auto; } .insights-grid { grid-template-columns:1fr; } }
""",
    },
    "minimal-swiss": {
        "label": "Swiss Grid",
        "body": ' class="variant-swiss"',
        "layout": "layout layout-swiss",
        "hero": """      <header class="hero">
        <div class="hero-rule"></div>
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="subtitle">179 sources / 20 lectures / 1 juillet 2026</p>
      </header>""",
        "css": r"""
:root { --bg:#fff; --text:#111; --muted:#666; --border:#ddd; --accent:#e63946; --accent-light:#fff; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-swiss { font-family:system-ui,-apple-system,"Helvetica Neue",sans-serif; background:var(--bg); color:var(--text); line-height:1.55; font-size:15px; }
.layout-swiss { max-width:960px; margin:0 auto; padding:3rem 2rem 5rem; }
nav { display:flex; flex-wrap:wrap; gap:.25rem 1.25rem; margin-bottom:3rem; padding-bottom:1rem; border-bottom:2px solid var(--accent); }
nav h2 { font-size:.6rem; text-transform:uppercase; letter-spacing:.15em; color:var(--muted); width:100%; margin-bottom:.25rem; }
nav a { color:var(--text); text-decoration:none; font-size:.75rem; font-weight:500; text-transform:uppercase; letter-spacing:.04em; }
nav a:hover { color:var(--accent); }
.hero-rule { width:60px; height:4px; background:var(--accent); margin-bottom:1.5rem; }
header.hero h1 { font-size:clamp(2rem,5vw,3.5rem); font-weight:700; letter-spacing:-.03em; line-height:1.05; margin-bottom:1rem; max-width:14ch; }
header.hero .subtitle { font-size:.8rem; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }
article { margin-top:2.5rem; }
.prose-beat { margin:2rem 0; max-width:65ch; }
.prose-beat strong { font-weight:700; }
.prose-beat.lead { font-size:1.15rem; font-weight:300; line-height:1.5; margin:0 0 2.5rem; max-width:55ch; }
.prose-beat h2 { font-size:.7rem; text-transform:uppercase; letter-spacing:.12em; color:var(--accent); margin-top:3rem; margin-bottom:.75rem; font-weight:700; }
.prose-beat.tight { font-size:.85rem; color:var(--muted); }
.visual-beat { margin:2.5rem 0; padding:1.5rem 0; border-top:1px solid var(--border); border-bottom:1px solid var(--border); overflow-x:auto; }
.caption { font-size:.7rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); margin-top:.75rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:1px; background:var(--border); border:1px solid var(--border); }
.insight-card { padding:1rem; background:var(--bg); font-size:.85rem; }
.insight-card .num { color:var(--accent); font-weight:700; margin-right:.35rem; }
.maturity-row { display:grid; grid-template-columns:100px 1fr 60px; gap:.75rem; font-size:.78rem; margin-bottom:.5rem; align-items:center; }
.maturity-bar { height:8px; background:var(--border); }
.maturity-fill { height:100%; background:var(--text); }
.mat-f .maturity-fill,.mat-a .maturity-fill { background:var(--accent); }
.cta-box { border-left:4px solid var(--accent); padding:.75rem 0 .75rem 1.25rem; margin-top:2rem; font-size:.95rem; }
.confidence { margin-top:2rem; padding-top:1.5rem; border-top:2px solid var(--text); font-size:.85rem; }
footer { margin-top:3rem; font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
@media (max-width:700px) { .insights-grid { grid-template-columns:1fr; } }
""",
    },
    "minimal-quiet": {
        "label": "Quiet Doc",
        "body": ' class="variant-quiet"',
        "layout": "layout layout-quiet",
        "hero": """      <header class="hero">
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="subtitle">179 sources · 20 lectures · 1 juillet 2026 · Confiance moyenne-haute</p>
      </header>""",
        "css": r"""
:root { --bg:#f7f7f5; --surface:#fff; --text:#37352f; --muted:#9b9a97; --border:#ededeb; --accent:#37352f; --accent-light:#f1f1ef; --success:#448361; --warning:#cb912f; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-quiet { font-family:system-ui,-apple-system,sans-serif; background:var(--bg); color:var(--text); line-height:1.7; font-size:16px; }
.layout-quiet { display:grid; grid-template-columns:240px 1fr; min-height:100vh; }
nav { position:sticky; top:0; height:100vh; overflow-y:auto; padding:2rem 1rem 2rem 1.5rem; }
nav h2 { font-size:.7rem; color:var(--muted); margin-bottom:.75rem; font-weight:400; }
nav a { display:block; padding:.25rem .5rem; margin-left:-.5rem; color:var(--muted); text-decoration:none; font-size:.85rem; border-radius:4px; }
nav a:hover { background:var(--accent-light); color:var(--text); }
main { max-width:720px; padding:3rem 2rem 4rem 0; }
header.hero { margin-bottom:2rem; }
header.hero h1 { font-size:2.25rem; font-weight:700; letter-spacing:-.02em; line-height:1.2; margin-bottom:.5rem; }
header.hero .subtitle { font-size:.9rem; color:var(--muted); }
article { background:transparent; }
.prose-beat { margin:1.25rem 0; }
.prose-beat strong { font-weight:600; }
.prose-beat.lead { font-size:1.05rem; color:var(--text); margin:0 0 1.5rem; padding:1rem; background:var(--surface); border-radius:4px; box-shadow:0 1px 2px rgba(0,0,0,.04); }
.prose-beat h2 { font-size:1.3rem; font-weight:600; margin-top:2rem; margin-bottom:.35rem; }
.prose-beat.tight { font-size:.9rem; color:var(--muted); padding:.5rem 0; }
.visual-beat { margin:1.5rem 0; background:var(--surface); border-radius:4px; padding:1.25rem; box-shadow:0 1px 3px rgba(0,0,0,.06); overflow-x:auto; }
.caption { font-size:.78rem; color:var(--muted); margin-top:.5rem; }
.insight-card { padding:.85rem; background:var(--surface); border-radius:4px; font-size:.88rem; box-shadow:0 1px 2px rgba(0,0,0,.04); }
.insight-card .num { display:inline-block; width:22px; height:22px; background:var(--accent-light); color:var(--text); border-radius:4px; text-align:center; line-height:22px; font-size:.72rem; font-weight:600; margin-right:.35rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.65rem; }
.maturity-bar { height:12px; background:var(--border); border-radius:6px; overflow:hidden; }
.maturity-fill { height:100%; background:var(--success); border-radius:6px; font-size:.6rem; color:#fff; display:flex; align-items:center; padding-left:.35rem; }
.mat-c .maturity-fill,.mat-d .maturity-fill { background:var(--accent); opacity:.7; }
.mat-e .maturity-fill { background:var(--warning); }
.cta-box { background:var(--surface); border-radius:4px; padding:1rem 1.15rem; margin-top:1.25rem; box-shadow:0 1px 3px rgba(0,0,0,.06); font-size:.92rem; }
.confidence { display:flex; gap:.75rem; padding:1rem; background:var(--surface); border-radius:4px; margin-top:1rem; font-size:.88rem; box-shadow:0 1px 2px rgba(0,0,0,.04); }
footer { color:var(--muted); font-size:.8rem; padding:2rem 0 0; }
@media (max-width:800px) { .layout-quiet { grid-template-columns:1fr; } nav { position:static; height:auto; padding:1rem; } main { padding:1.5rem; } .insights-grid { grid-template-columns:1fr; } }
""",
    },
    "minimal-brutal": {
        "label": "Brutal Type",
        "body": ' class="variant-brutal"',
        "layout": "layout layout-brutal",
        "hero": """      <header class="hero">
        <h1>ROBOTS D'ASSEMBLAGE STRUCTUREL SUR CHANTIER</h1>
        <p class="subtitle">179 SOURCES — 20 LECTURES — JUILLET 2026</p>
      </header>""",
        "css": r"""
:root { --bg:#fff; --text:#000; --muted:#444; --border:#000; --accent:#000; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-brutal { font-family:system-ui,sans-serif; background:var(--bg); color:var(--text); line-height:1.45; font-size:16px; }
.layout-brutal { max-width:800px; margin:0 auto; padding:2rem 1.5rem 4rem; }
nav { margin-bottom:2rem; }
nav h2 { font-size:1rem; font-weight:900; text-transform:uppercase; margin-bottom:.5rem; }
nav a { display:inline-block; margin-right:1rem; color:var(--text); text-decoration:none; font-weight:700; font-size:.85rem; text-transform:uppercase; }
nav a:hover { text-decoration:underline; }
header.hero { border:4px solid var(--border); padding:2rem; margin-bottom:2rem; }
header.hero h1 { font-size:clamp(1.5rem,6vw,2.8rem); font-weight:900; line-height:1; letter-spacing:-.02em; text-transform:uppercase; }
header.hero .subtitle { font-size:.85rem; font-weight:700; margin-top:1rem; text-transform:uppercase; letter-spacing:.05em; }
article { border:4px solid var(--border); padding:1.5rem; }
.prose-beat { margin:1.5rem 0; }
.prose-beat strong { font-weight:900; text-decoration:underline; }
.prose-beat.lead { font-size:1.2rem; font-weight:700; margin:0 0 1.5rem; line-height:1.35; }
.prose-beat h2 { font-size:1.5rem; font-weight:900; text-transform:uppercase; margin-top:2rem; border-top:4px solid var(--border); padding-top:1rem; }
.prose-beat.tight { font-size:.9rem; font-weight:600; }
.visual-beat { margin:1.5rem 0; border:2px solid var(--border); padding:1rem; overflow-x:auto; }
.caption { font-size:.75rem; font-weight:700; text-transform:uppercase; margin-top:.5rem; }
.insight-card { border:2px solid var(--border); padding:.75rem; font-size:.85rem; font-weight:600; }
.insight-card .num { font-weight:900; margin-right:.3rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.5rem; }
.maturity-bar { height:20px; border:2px solid var(--border); background:#fff; }
.maturity-fill { height:100%; background:var(--text); color:#fff; font-weight:900; font-size:.65rem; display:flex; align-items:center; padding-left:.4rem; }
.cta-box { border:4px solid var(--border); padding:1rem; margin-top:1.5rem; font-weight:700; }
.confidence { border:4px solid var(--border); padding:1rem; margin-top:1rem; font-weight:700; }
footer { margin-top:2rem; font-weight:900; text-transform:uppercase; font-size:.75rem; }
@media (max-width:700px) { .insights-grid { grid-template-columns:1fr; } }
""",
    },
    "creative-pop": {
        "label": "Editorial Pop",
        "body": ' class="variant-pop"',
        "layout": "layout layout-pop",
        "hero": """      <header class="hero">
        <span class="pop-label">Recherche</span>
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="subtitle">179 sources · 20 lectures · Confiance moyenne-haute</p>
      </header>""",
        "css": r"""
:root { --bg:#fff9f0; --surface:#fff; --text:#2d3436; --muted:#636e72; --border:#dfe6e9; --accent:#ff4757; --accent-light:#fff5f6; --success:#2ed573; --warning:#ffa502; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-pop { font-family:Georgia,serif; background:var(--bg); color:var(--text); line-height:1.75; font-size:17px; }
.layout-pop { max-width:780px; margin:0 auto; padding:2rem 1.5rem 4rem; }
nav { display:flex; flex-wrap:wrap; gap:.35rem; margin-bottom:2rem; font-family:system-ui,sans-serif; }
nav h2 { display:none; }
nav a { padding:.35rem .75rem; background:var(--surface); border:2px solid var(--text); color:var(--text); text-decoration:none; font-size:.78rem; font-weight:600; border-radius:50px; }
nav a:hover { background:var(--accent); color:#fff; border-color:var(--accent); }
.pop-label { display:inline-block; background:var(--accent); color:#fff; font-family:system-ui,sans-serif; font-size:.7rem; font-weight:700; text-transform:uppercase; letter-spacing:.1em; padding:.25rem .65rem; border-radius:4px; margin-bottom:1rem; }
header.hero h1 { font-size:clamp(2.2rem,6vw,3.5rem); font-weight:400; line-height:1.1; margin-bottom:.75rem; color:var(--text); }
header.hero .subtitle { font-family:system-ui,sans-serif; font-size:.88rem; color:var(--muted); }
article { background:var(--surface); border-radius:12px; padding:2rem; box-shadow:0 4px 24px rgba(0,0,0,.06); }
.prose-beat { margin:1.5rem 0; font-family:system-ui,sans-serif; font-size:.98rem; }
.prose-beat strong { color:var(--accent); font-weight:700; }
.prose-beat.lead { font-family:Georgia,serif; font-size:1.25rem; line-height:1.5; margin:0 0 2rem; color:var(--text); }
.prose-beat h2 { font-family:Georgia,serif; font-size:1.6rem; color:var(--accent); margin-top:2rem; }
.pop-callout { background:var(--accent); color:#fff; font-family:system-ui,sans-serif; font-weight:700; padding:.85rem 1.15rem; border-radius:8px; margin:1.25rem 0; font-size:.95rem; }
.visual-beat { margin:1.75rem 0; border-radius:10px; overflow:hidden; border:1px solid var(--border); padding:1.15rem; background:var(--bg); }
.caption { font-family:system-ui,sans-serif; font-size:.76rem; color:var(--muted); margin-top:.55rem; }
.insight-card { padding:.85rem; border-radius:8px; background:var(--accent-light); font-family:system-ui,sans-serif; font-size:.86rem; border-left:4px solid var(--accent); }
.insight-card .num { color:var(--accent); font-weight:800; margin-right:.3rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.6rem; }
.maturity-bar { height:14px; background:var(--border); border-radius:7px; overflow:hidden; }
.maturity-fill { height:100%; background:var(--accent); border-radius:7px; font-size:.65rem; color:#fff; font-weight:600; display:flex; align-items:center; padding-left:.4rem; }
.mat-f .maturity-fill,.mat-a .maturity-fill { background:var(--success); }
.mat-e .maturity-fill { background:var(--warning); }
.cta-box { background:var(--accent-light); border:2px solid var(--accent); border-radius:10px; padding:1rem; margin-top:1.25rem; font-family:system-ui,sans-serif; }
.cta-box.pop-callout { background:var(--accent); color:#fff; }
.confidence { display:flex; gap:.75rem; padding:1rem; background:var(--bg); border-radius:8px; margin-top:1rem; font-family:system-ui,sans-serif; font-size:.88rem; }
footer { text-align:center; font-family:system-ui,sans-serif; color:var(--muted); font-size:.8rem; padding:2rem 0 0; }
@media (max-width:700px) { .insights-grid { grid-template-columns:1fr; } }
""",
    },
    "creative-aurora": {
        "label": "Soft Aurora",
        "body": ' class="variant-aurora"',
        "layout": "layout layout-aurora",
        "hero": """      <header class="hero">
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="subtitle">179 sources · 20 lectures · 1 juillet 2026</p>
        <span class="badge">Confiance moyenne-haute</span>
      </header>""",
        "css": r"""
:root { --text:#1e1b4b; --muted:#64748b; --border:rgba(124,58,237,.15); --accent:#7c3aed; --accent-2:#06b6d4; --success:#10b981; --warning:#f59e0b; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-aurora {
  font-family:system-ui,-apple-system,sans-serif; color:var(--text); line-height:1.65; font-size:16px;
  background:linear-gradient(135deg,#faf5ff 0%,#f0fdfa 40%,#fffbeb 100%);
  min-height:100vh;
}
.layout-aurora { display:grid; grid-template-columns:200px 1fr; min-height:100vh; }
nav { position:sticky; top:0; height:100vh; padding:1.5rem 1rem; background:rgba(255,255,255,.6); backdrop-filter:blur(12px); border-right:1px solid var(--border); }
nav h2 { font-size:.65rem; text-transform:uppercase; letter-spacing:.1em; color:var(--muted); margin-bottom:.75rem; }
nav a { display:block; padding:.35rem .5rem; color:var(--muted); text-decoration:none; font-size:.8rem; border-radius:8px; }
nav a:hover { background:rgba(124,58,237,.08); color:var(--accent); }
main { max-width:820px; padding:2rem 1.75rem 4rem; }
header.hero { margin-bottom:1.75rem; }
header.hero h1 { font-size:1.85rem; font-weight:700; background:linear-gradient(135deg,var(--accent),var(--accent-2)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:.5rem; }
header.hero .subtitle { font-size:.88rem; color:var(--muted); margin-bottom:.5rem; }
.badge { display:inline-block; background:linear-gradient(135deg,var(--accent),var(--accent-2)); color:#fff; padding:.2rem .65rem; border-radius:20px; font-size:.72rem; font-weight:600; }
article { background:rgba(255,255,255,.75); backdrop-filter:blur(8px); border:1px solid var(--border); border-radius:16px; padding:1.75rem; box-shadow:0 8px 32px rgba(124,58,237,.08); }
.prose-beat { margin:1.35rem 0; }
.prose-beat strong { color:var(--accent); }
.prose-beat.lead { font-size:1.05rem; padding:1rem 1.15rem; background:linear-gradient(135deg,rgba(124,58,237,.06),rgba(6,182,212,.06)); border-radius:12px; margin:0 0 1.25rem; }
.prose-beat h2 { font-size:1.2rem; color:var(--accent); margin-top:1.75rem; }
.visual-beat { margin:1.25rem 0; background:rgba(255,255,255,.9); border:1px solid var(--border); border-radius:12px; padding:1.1rem; overflow-x:auto; }
.caption { font-size:.76rem; color:var(--muted); margin-top:.5rem; }
.insight-card { padding:.8rem; border-radius:10px; background:linear-gradient(135deg,rgba(124,58,237,.05),rgba(6,182,212,.05)); font-size:.85rem; border:1px solid var(--border); }
.insight-card .num { display:inline-block; width:22px; height:22px; background:linear-gradient(135deg,var(--accent),var(--accent-2)); color:#fff; border-radius:6px; text-align:center; line-height:22px; font-size:.68rem; font-weight:700; margin-right:.3rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.55rem; }
.maturity-bar { height:16px; background:rgba(124,58,237,.1); border-radius:8px; overflow:hidden; }
.maturity-fill { height:100%; background:linear-gradient(90deg,var(--accent),var(--accent-2)); border-radius:8px; font-size:.65rem; color:#fff; display:flex; align-items:center; padding-left:.4rem; }
.mat-f .maturity-fill,.mat-a .maturity-fill { background:linear-gradient(90deg,var(--success),#34d399); }
.mat-e .maturity-fill { background:linear-gradient(90deg,var(--warning),#fbbf24); }
.cta-box { border:1px solid var(--border); border-radius:12px; padding:1rem; background:linear-gradient(135deg,rgba(124,58,237,.08),rgba(6,182,212,.08)); margin-top:1rem; }
.confidence { display:flex; gap:.75rem; padding:.9rem; border-radius:12px; background:rgba(255,255,255,.8); border:1px solid var(--border); margin-top:1rem; font-size:.88rem; }
footer { text-align:center; color:var(--muted); font-size:.78rem; padding:1.25rem 0 0; }
@media (max-width:800px) { .layout-aurora { grid-template-columns:1fr; } nav { position:static; height:auto; } .insights-grid { grid-template-columns:1fr; } }
""",
    },
    "creative-riso": {
        "label": "Risograph",
        "body": ' class="variant-riso"',
        "layout": "layout layout-riso",
        "hero": """      <header class="hero">
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="subtitle">179 sources · 20 lectures · 1 juillet 2026</p>
      </header>""",
        "css": r"""
:root { --bg:#fff8e7; --surface:#fff; --text:#2b2118; --muted:#5c4d3c; --border:#2b4c7e; --accent:#2b4c7e; --accent-2:#e8488a; --accent-3:#f4d35e; --success:#2b4c7e; }
* { box-sizing:border-box; margin:0; padding:0; }
body.variant-riso {
  font-family:Georgia,serif; background:var(--bg); color:var(--text); line-height:1.7; font-size:17px;
  background-image:radial-gradient(circle,#2b4c7e12 1px,transparent 1px); background-size:12px 12px;
}
.layout-riso { display:grid; grid-template-columns:210px 1fr; min-height:100vh; }
nav { position:sticky; top:0; height:100vh; background:var(--accent-3); border-right:3px solid var(--border); padding:1rem .65rem; font-family:system-ui,sans-serif; }
nav h2 { font-size:.65rem; text-transform:uppercase; letter-spacing:.1em; color:var(--border); margin-bottom:.65rem; font-weight:800; }
nav a { display:block; padding:.3rem .45rem; margin-bottom:.25rem; color:var(--border); text-decoration:none; font-size:.78rem; font-weight:600; background:var(--surface); border:2px solid var(--border); }
nav a:hover { background:var(--accent-2); color:#fff; border-color:var(--accent-2); transform:translate(-2px,-2px); box-shadow:2px 2px 0 var(--border); }
main { max-width:760px; padding:1.75rem 1.5rem 4rem; }
header.hero { margin-bottom:1.5rem; position:relative; }
header.hero h1 { font-size:1.75rem; font-weight:700; line-height:1.15; color:var(--border); text-shadow:2px 2px 0 var(--accent-2); margin-bottom:.5rem; }
header.hero .subtitle { font-family:system-ui,sans-serif; font-size:.85rem; color:var(--muted); }
article { background:var(--surface); border:3px solid var(--border); padding:1.5rem; box-shadow:4px 4px 0 var(--accent-2); }
.prose-beat { margin:1.35rem 0; font-family:system-ui,sans-serif; font-size:.96rem; }
.prose-beat strong { color:var(--accent-2); font-weight:700; }
.prose-beat.lead { font-family:Georgia,serif; font-size:1.1rem; background:var(--accent-3); padding:1rem; border:2px solid var(--border); margin:0 0 1.25rem; }
.prose-beat h2 { font-size:1.2rem; color:var(--border); margin-top:1.5rem; text-decoration:underline; text-decoration-color:var(--accent-2); text-underline-offset:4px; }
.riso-stamp { display:inline-block; background:var(--accent-2); color:#fff; font-family:system-ui,sans-serif; font-size:.72rem; font-weight:800; text-transform:uppercase; padding:.3rem .6rem; border:2px solid var(--border); transform:rotate(-2deg); margin:.5rem 0; }
.visual-beat { margin:1.25rem 0; border:2px solid var(--border); padding:1rem; background:var(--bg); overflow-x:auto; }
.visual-beat:nth-child(even) { box-shadow:3px 3px 0 var(--accent); }
.caption { font-family:system-ui,sans-serif; font-size:.74rem; color:var(--muted); margin-top:.5rem; font-weight:600; }
.insight-card { padding:.75rem; border:2px solid var(--border); background:var(--accent-3); font-family:system-ui,sans-serif; font-size:.84rem; }
.insight-card .num { color:var(--accent-2); font-weight:900; margin-right:.3rem; }
.insights-grid { display:grid; grid-template-columns:1fr 1fr; gap:.5rem; }
.maturity-bar { height:18px; border:2px solid var(--border); background:var(--surface); }
.maturity-fill { height:100%; background:var(--accent); font-size:.65rem; color:#fff; font-weight:700; display:flex; align-items:center; padding-left:.4rem; }
.mat-a .maturity-fill { background:var(--accent-2); }
.mat-e .maturity-fill { background:var(--accent-3); color:var(--border); }
.cta-box { border:3px solid var(--border); padding:1rem; margin-top:1rem; background:var(--accent-3); font-family:system-ui,sans-serif; font-weight:600; }
.cta-box.riso-stamp { display:block; text-align:center; }
.confidence { display:flex; gap:.75rem; border:2px solid var(--border); padding:.85rem; margin-top:1rem; background:var(--surface); font-family:system-ui,sans-serif; font-size:.86rem; }
footer { text-align:center; font-family:system-ui,sans-serif; color:var(--muted); font-size:.78rem; font-weight:600; padding:1.25rem 0 0; }
@media (max-width:800px) { .layout-riso { grid-template-columns:1fr; } nav { position:static; height:auto; } .insights-grid { grid-template-columns:1fr; } }
""",
    },
}


def extract_parts(html: str):
    nav_m = re.search(r"<nav>(.*?)</nav>", html, re.DOTALL)
    article_m = re.search(r"<article>(.*?)</article>", html, re.DOTALL)
    footer_m = re.search(r"<footer>(.*?)</footer>", html, re.DOTALL)
    return nav_m.group(1), article_m.group(1), footer_m.group(1)


def remap_colors(fragment: str, variant: str) -> str:
    out = fragment
    for old, new in REMAP.get(variant, {}).items():
        out = out.replace(old, new)
    return out


def enhance_article(article: str, variant: str) -> str:
    out = article
    if variant == "academic-manuscript":
        out = out.replace('class="prose-beat tight"', 'class="prose-beat sidenote"', 1)
    if variant == "creative-pop":
        out = out.replace('class="cta-box"', 'class="cta-box pop-callout"', 1)
    if variant == "creative-riso":
        out = out.replace('class="cta-box"', 'class="cta-box riso-stamp"', 1)
    return out


def build(variant: str, nav: str, article: str, footer: str) -> str:
    cfg = VARIANTS[variant]
    article = enhance_article(remap_colors(article, variant), variant)
    return f"""<!DOCTYPE html>
<html lang="fr">
<!-- variant: {variant} -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[{cfg['label']}] Robots d'assemblage structurel sur chantier</title>
  <style>
{cfg['css'].strip()}
  </style>
</head>
<body{cfg['body']}>
  <div class="{cfg['layout']}">
    <nav>{nav}</nav>
    <main>
{cfg['hero']}
      <article>{article}</article>
      <footer>{footer}</footer>
    </main>
  </div>
</body>
</html>
"""


def write_gallery():
    gallery = OUT_DIR / "report-variants-gallery.html"
    sections = [
        ("✓ Validés", [
            ("report-editorial.html", "Editorial Ink", "Magazine serif — validé", "#8b2942"),
            ("report-warm.html", "Warm Bear", "Carnet d'étude — validé", "#8b5a2b"),
        ]),
        ("Academic — 3 propositions", [
            ("report-academic.html", "Academic Blue (actuel)", "Dashboard bleu — à rejeter ?", "#1e4d8c"),
            ("report-academic-manuscript.html", "Manuscript", "Tufte/Gwern · colonne étroite · sidenotes", "#2c5282"),
            ("report-academic-lab.html", "Lab Notebook", "Carnet scientifique · teal · figures numérotées", "#0d6e6e"),
            ("report-academic-night.html", "Night Research", "Dark mode · docs techniques", "#58a6ff"),
        ]),
        ("Minimal — 3 propositions", [
            ("report-minimal.html", "Minimal Mono (actuel)", "Manuel technique mono — à rejeter ?", "#18181b"),
            ("report-minimal-swiss.html", "Swiss Grid", "Style suisse · rouge · typo pure", "#e63946"),
            ("report-minimal-quiet.html", "Quiet Doc", "Notion-like · doux · sans fioritures", "#37352f"),
            ("report-minimal-brutal.html", "Brutal Type", "Manifeste · noir & blanc · caps", "#000"),
        ]),
        ("Creative — 3 propositions", [
            ("report-creative.html", "Creative Spicy (actuel)", "Neo-brutal rainbow — à rejeter ?", "#ff2d6a"),
            ("report-creative-pop.html", "Editorial Pop", "Lisible + punch · une couleur forte", "#ff4757"),
            ("report-creative-aurora.html", "Soft Aurora", "Gradients doux · glass moderne", "#7c3aed"),
            ("report-creative-riso.html", "Risograph", "Zine imprimé · 3 couleurs · offset", "#2b4c7e"),
        ]),
    ]
    cards = []
    for section_title, items in sections:
        cards.append(f'<h2 class="section-title">{section_title}</h2><div class="grid">')
        for href, title, desc, color in items:
            cards.append(f"""<article class="card">
      <div class="swatch" style="background:linear-gradient(135deg,{color},{color}88)"></div>
      <h3>{title}</h3>
      <p>{desc}</p>
      <a href="{href}" target="_blank">Ouvrir →</a>
    </article>""")
        cards.append("</div>")
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Layout HTML — Galerie variantes</title>
  <style>
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    body {{ font-family:system-ui,sans-serif; background:#0f1419; color:#e8eaed; padding:2rem 1.5rem 3rem; max-width:1100px; margin:0 auto; line-height:1.5; }}
    header {{ margin-bottom:2rem; }}
    header h1 {{ font-size:1.5rem; margin-bottom:.35rem; }}
    header p {{ color:#9aa0a6; font-size:.9rem; }}
    .open-all {{ display:inline-block; margin-top:1rem; padding:.65rem 1.2rem; background:#1a6b4a; color:#fff; text-decoration:none; border-radius:8px; font-weight:600; cursor:pointer; border:none; font-size:.9rem; }}
    .section-title {{ font-size:1rem; color:#9aa0a6; margin:2rem 0 1rem; text-transform:uppercase; letter-spacing:.08em; }}
    .section-title:first-of-type {{ margin-top:0; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:1rem; margin-bottom:.5rem; }}
    .card {{ background:#1a2332; border:1px solid #2d3748; border-radius:12px; padding:1.15rem; display:flex; flex-direction:column; gap:.6rem; }}
    .card:hover {{ border-color:#4a5568; }}
    .swatch {{ height:40px; border-radius:8px; }}
    .card h3 {{ font-size:1rem; }}
    .card p {{ font-size:.82rem; color:#9aa0a6; flex:1; }}
    .card a {{ display:inline-block; text-align:center; padding:.5rem .9rem; background:#2d6cb5; color:#fff; text-decoration:none; border-radius:8px; font-size:.85rem; font-weight:600; }}
    .card a:hover {{ background:#3d8fd4; }}
  </style>
</head>
<body>
  <header>
    <h1>Layout HTML — Comparaison des styles</h1>
    <p>Editorial + Warm validés · 9 nouvelles propositions pour academic, minimal, creative</p>
    <button class="open-all" id="open-all">Ouvrir toutes les variantes (11 onglets)</button>
  </header>
  {''.join(cards)}
  <script>
    document.getElementById('open-all').addEventListener('click', function() {{
      {repr([i[0] for s in sections for i in s[1]])}.forEach(function(f) {{ window.open(f, '_blank'); }});
    }});
  </script>
</body>
</html>"""
    gallery.write_text(html, encoding="utf-8")
    print(f"wrote {gallery}")


def main():
    html = SRC.read_text(encoding="utf-8")
    nav, article, footer = extract_parts(html)
    for variant in VARIANTS:
        out = OUT_DIR / f"report-{variant}.html"
        out.write_text(build(variant, nav, article, footer), encoding="utf-8")
        print(f"wrote {out}")
    write_gallery()


if __name__ == "__main__":
    main()