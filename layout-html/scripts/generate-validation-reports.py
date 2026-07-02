#!/usr/bin/env python3
"""Generate 5 preset validation HTML files from report.html article body."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research/robots-assemblage-structurel-chantier/report.html"
OUT_DIR = ROOT / "research/robots-assemblage-structurel-chantier"

# Editorial palette in current report.html → remap per preset
REMAP = {
    "academic": {
        "#8b2942": "#1e4d8c", "#b85c72": "#2d6cb5", "#2d5a3d": "#1a6b4a", "#3d6b4d": "#1a6b4a",
        "#8b6914": "#9a6b00", "#6b6560": "#5c6370", "#f5e8ec": "#e8f0fa", "#edd5dc": "#d4e4f7",
        "#faf3e0": "#fff8e6", "#ede8e0": "#e8ecf2", "#f5edd0": "#fff8e6",
    },
    "editorial": {},
    "minimal": {
        "#8b2942": "#18181b", "#b85c72": "#3f3f46", "#2d5a3d": "#166534", "#3d6b4d": "#166534",
        "#8b6914": "#a16207", "#6b6560": "#71717a", "#f5e8ec": "#f4f4f5", "#edd5dc": "#e4e4e7",
        "#faf3e0": "#fafafa", "#ede8e0": "#f4f4f5", "#f5edd0": "#fafafa",
    },
    "warm": {
        "#8b2942": "#8b5a2b", "#b85c72": "#c49a6c", "#2d5a3d": "#3d5c3a", "#3d6b4d": "#3d5c3a",
        "#8b6914": "#b45309", "#6b6560": "#6b5c4a", "#f5e8ec": "#f0e6d6", "#edd5dc": "#e5d9c8",
        "#faf3e0": "#fff8e6", "#ede8e0": "#e5d9c8", "#f5edd0": "#f0e6d6",
    },
    "creative": {
        "#8b2942": "#ff2d6a", "#b85c72": "#7b2ff7", "#2d5a3d": "#00a878", "#3d6b4d": "#00d4aa",
        "#8b6914": "#ffb800", "#6b6560": "#5c4a7a", "#f5e8ec": "#ffe0ec", "#edd5dc": "#e8d4ff",
        "#faf3e0": "#fff3cc", "#ede8e0": "#f3f0ff", "#f5edd0": "#fff3cc",
    },
}

CSS = {
"academic": r"""
:root {
  --bg: #f4f6f9; --surface: #fff; --text: #1a1d23; --muted: #5c6370; --border: #dde2ea;
  --accent: #1e4d8c; --accent-light: #e8f0fa; --success: #1a6b4a; --success-bg: #e8f5ee;
  --warning: #9a6b00; --warning-bg: #fff8e6; --radius: 8px;
  --shadow: 0 2px 8px rgba(30,77,140,.06), 0 8px 24px rgba(0,0,0,.05);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.65; font-size: 16px; }
.layout { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }
nav { position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--surface); border-right: 1px solid var(--border); padding: 1.2rem .75rem; }
nav h2 { font-size: .68rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: .75rem; padding-left: .4rem; }
nav a { display: block; padding: .35rem .6rem; color: var(--text); text-decoration: none; border-radius: 4px; font-size: .82rem; border-left: 2px solid transparent; }
nav a:hover { background: var(--accent-light); color: var(--accent); border-left-color: var(--accent); }
main { max-width: 920px; padding: 2rem 1.5rem 4rem; }
header.hero { background: var(--surface); color: var(--text); border-radius: var(--radius); padding: 1.5rem 1.85rem; margin-bottom: 1.5rem; box-shadow: var(--shadow); border-top: 6px solid var(--accent); border: 1px solid var(--border); border-top: 6px solid var(--accent); }
header.hero h1 { font-size: 1.65rem; margin-bottom: .5rem; color: var(--accent); }
header.hero .subtitle { font-size: .92rem; color: var(--muted); margin-bottom: .85rem; }
.hero-metrics { display: flex; flex-wrap: wrap; gap: .4rem; }
.badge, .metric-pill { background: var(--accent-light); color: var(--accent); padding: .2rem .55rem; border-radius: 4px; font-size: .75rem; font-weight: 600; display: inline-block; }
article { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.75rem 1.85rem; box-shadow: var(--shadow); counter-reset: section; }
.prose-beat { margin: 1.5rem 0; font-size: .98rem; line-height: 1.72; }
.prose-beat strong { color: var(--accent); font-weight: 600; }
.prose-beat.lead { font-size: 1.05rem; background: var(--accent-light); border-left: 4px solid var(--accent); padding: 1rem 1.15rem; border-radius: 0 8px 8px 0; margin: 0 0 1.25rem; }
.prose-beat.tight { margin: 1rem 0; font-size: .94rem; color: var(--muted); }
.sidenote { float: right; clear: right; width: 36%; margin: 0 0 1rem 1.25rem; padding: .7rem .8rem; font-size: .82rem; line-height: 1.55; color: var(--muted); background: var(--accent-light); border-left: 2px solid var(--accent); border-radius: 0 4px 4px 0; }
@media (max-width: 900px) { .sidenote { float: none; width: 100%; margin: 1rem 0; } }
.prose-beat h2 { font-size: 1.2rem; color: var(--accent); margin-bottom: .5rem; padding-top: .5rem; border-top: 1px solid var(--border); counter-increment: section; }
.prose-beat h2::before { content: counter(section, decimal-leading-zero) " · "; color: var(--muted); font-weight: 700; }
.prose-beat h2:first-child { border-top: none; padding-top: 0; }
.prose-beat ul { margin: .4rem 0 .2rem 1.1rem; }
.visual-beat { margin: 1.25rem 0 1.5rem; background: #fff; border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 4px; padding: 1.1rem 1rem; overflow-x: auto; }
.visual-beat svg { display: block; max-width: 100%; height: auto; margin: 0 auto; }
.caption { text-align: left; font-size: .78rem; color: var(--muted); margin-top: .55rem; font-style: normal; font-weight: 500; }
.insights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; }
.insight-card { padding: .85rem; border-radius: 6px; border-left: 3px solid var(--accent); background: var(--bg); font-size: .86rem; }
.insight-card .num { display: inline-block; width: 22px; height: 22px; background: var(--accent); color: #fff; border-radius: 50%; text-align: center; line-height: 22px; font-size: .7rem; font-weight: 700; margin-right: .35rem; }
.timeline { display: flex; gap: 0; margin: 0; position: relative; }
.timeline::before { content: ''; position: absolute; top: 26px; left: 8%; right: 8%; height: 3px; background: linear-gradient(90deg, var(--success), var(--warning), var(--muted)); border-radius: 2px; z-index: 0; }
.timeline-phase { flex: 1; text-align: center; position: relative; z-index: 1; padding: 0 .35rem; }
.timeline-dot { width: 50px; height: 50px; border-radius: 50%; margin: 0 auto .5rem; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .68rem; color: #fff; border: 3px solid var(--surface); box-shadow: var(--shadow); }
.timeline-phase:nth-child(1) .timeline-dot { background: var(--success); }
.timeline-phase:nth-child(2) .timeline-dot { background: var(--warning); }
.timeline-phase:nth-child(3) .timeline-dot { background: var(--muted); }
.maturity-grid { display: grid; gap: .55rem; }
.maturity-row { display: grid; grid-template-columns: 130px 1fr 82px; align-items: center; gap: .6rem; font-size: .82rem; }
.maturity-bar { height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }
.maturity-fill { height: 100%; border-radius: 10px; font-size: .65rem; font-weight: 600; color: #fff; display: flex; align-items: center; padding-left: .45rem; }
.mat-f .maturity-fill { background: linear-gradient(90deg,#1a6b4a,#2d9a6a); width:85%; }
.mat-a .maturity-fill { background: linear-gradient(90deg,#1a6b4a,#3daa7a); width:78%; }
.mat-c .maturity-fill { background: linear-gradient(90deg,#1e4d8c,#3d8fd4); width:65%; }
.mat-d .maturity-fill { background: linear-gradient(90deg,#2d6cb5,#5a9fd4); width:55%; }
.mat-b .maturity-fill { background: linear-gradient(90deg,#5c6370,#8a9199); width:35%; }
.mat-e .maturity-fill { background: linear-gradient(90deg,#9a6b00,#c9a227); width:30%; }
.contradiction-card { display: grid; grid-template-columns: 1fr auto 1fr auto; gap: .45rem; align-items: center; background: var(--bg); padding: .75rem .9rem; border-radius: 6px; margin-bottom: .55rem; font-size: .84rem; }
.contra-side { padding: .45rem .55rem; border-radius: 6px; background: var(--surface); border: 1px solid var(--border); }
.contra-vs { font-weight: 800; color: var(--accent); }
.tag-mixed { background: #f8d7da; color: #721c24; padding: .1rem .4rem; border-radius: 4px; font-size: .68rem; font-weight: 600; }
.tag-weak { background: #e2e3e5; color: #6c757d; padding: .1rem .4rem; border-radius: 4px; font-size: .68rem; font-weight: 600; }
.sources-compact { font-size: .88rem; list-style: none; }
.sources-compact a { color: var(--accent); }
.cta-box { background: linear-gradient(135deg, var(--accent-light), var(--surface)); border: 2px solid var(--accent); border-radius: 8px; padding: 1rem 1.15rem; margin-top: 1rem; font-size: .92rem; }
.confidence { display: flex; gap: .85rem; align-items: center; padding: .9rem; background: var(--accent-light); border-radius: 8px; margin-top: 1rem; font-size: .88rem; }
.confidence .level { font-size: 1.2rem; font-weight: 700; color: var(--accent); white-space: nowrap; }
footer { text-align: center; color: var(--muted); font-size: .8rem; padding: 1.25rem 0 0; }
@media (max-width: 800px) { .layout { grid-template-columns: 1fr; } nav { position: static; height: auto; } main { padding: 1rem; } .insights-grid { grid-template-columns: 1fr; } .timeline { flex-direction: column; } .timeline::before { display: none; } .maturity-row { grid-template-columns: 1fr; } .contradiction-card { grid-template-columns: 1fr; text-align: center; } }
""",

"editorial": r"""
:root {
  --bg: #f7f3eb; --surface: #fffdf8; --text: #1c1917; --muted: #6b6560; --border: #e8e0d4;
  --accent: #8b2942; --accent-light: #f5e8ec; --success: #2d5a3d; --warning: #8b6914;
  --radius: 4px; --shadow: none;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body.preset-editorial { font-family: Georgia, "Times New Roman", serif; background: var(--bg); color: var(--text); line-height: 1.78; font-size: 17px; }
.layout-editorial { display: block; min-height: 100vh; }
.layout-editorial nav { position: static; height: auto; background: transparent; border: none; border-bottom: 1px solid var(--border); padding: 1rem 0; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; gap: .25rem .5rem; align-items: center; max-width: 760px; margin-left: auto; margin-right: auto; }
.layout-editorial nav h2 { font-family: "Segoe UI", system-ui, sans-serif; font-size: .65rem; text-transform: uppercase; letter-spacing: .12em; color: var(--muted); margin: 0 .5rem 0 0; }
.layout-editorial nav a { font-family: "Segoe UI", system-ui, sans-serif; padding: .2rem .5rem; color: var(--text); text-decoration: none; font-size: .78rem; border-bottom: 1px solid transparent; }
.layout-editorial nav a:hover { color: var(--accent); border-bottom-color: var(--accent); }
.layout-editorial main { max-width: 760px; margin: 0 auto; padding: 0 1.5rem 4rem; }
header.hero { background: transparent; color: var(--text); padding: 0 0 1.5rem; margin-bottom: 2rem; border-bottom: 2px solid var(--accent); }
header.hero h1 { font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 400; line-height: 1.15; margin-bottom: .75rem; letter-spacing: -0.02em; }
header.hero .subtitle { font-family: "Segoe UI", system-ui, sans-serif; font-size: .88rem; color: var(--muted); margin-bottom: .6rem; }
.badge { font-family: "Segoe UI", system-ui, sans-serif; background: var(--accent-light); color: var(--accent); padding: .15rem .5rem; font-size: .72rem; font-weight: 600; }
article { background: transparent; border: none; box-shadow: none; padding: 0; }
.prose-beat { font-family: "Segoe UI", system-ui, sans-serif; margin: 1.75rem 0; font-size: .98rem; line-height: 1.78; max-width: 68ch; }
.prose-beat strong { color: var(--accent); }
.prose-beat.lead { font-size: 1.12rem; max-width: 68ch; border-left: 3px solid var(--accent); padding: 0 0 0 1.15rem; background: transparent; margin: 0 0 2rem; }
.prose-beat.lead::first-letter { float: left; font-family: Georgia, serif; font-size: 3.8rem; line-height: .85; padding-right: .12em; color: var(--accent); font-weight: 700; }
.prose-beat h2 { font-family: Georgia, serif; font-size: 1.35rem; color: var(--text); border-top: none; padding-top: 0; margin-top: 2rem; }
.prose-beat.tight { font-size: .9rem; color: var(--muted); font-style: italic; }
.section-kicker { font-family: "Segoe UI", system-ui, sans-serif; font-size: .68rem; text-transform: uppercase; letter-spacing: .14em; color: var(--accent); margin-bottom: .35rem; display: block; }
.pullquote { font-family: Georgia, serif; font-size: 1.35rem; line-height: 1.45; color: var(--accent); border-left: 3px solid var(--accent); padding: .5rem 0 .5rem 1.25rem; margin: 2rem 0; max-width: 72ch; }
.epigraph { font-style: italic; color: var(--muted); border-left: 2px solid var(--border); padding-left: 1rem; margin: 1.5rem 0; font-size: .95rem; }
.visual-beat { margin: 2rem 0; background: var(--surface); border: 1px solid var(--border); padding: 1.25rem; overflow-x: auto; }
.caption { font-family: "Segoe UI", system-ui, sans-serif; text-align: left; font-size: .76rem; color: var(--muted); margin-top: .6rem; font-style: italic; }
.insights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .65rem; font-family: "Segoe UI", system-ui, sans-serif; }
.insight-card { padding: .85rem; border-top: 2px solid var(--accent); background: var(--bg); font-size: .86rem; }
.insight-card .num { display: inline-block; width: 22px; height: 22px; background: var(--accent); color: #fff; border-radius: 50%; text-align: center; line-height: 22px; font-size: .7rem; font-weight: 700; margin-right: .35rem; }
.timeline { display: flex; font-family: "Segoe UI", system-ui, sans-serif; position: relative; }
.timeline::before { content: ''; position: absolute; top: 26px; left: 8%; right: 8%; height: 2px; background: var(--border); }
.timeline-dot { width: 50px; height: 50px; border-radius: 50%; margin: 0 auto .5rem; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .68rem; color: #fff; background: var(--accent); }
.timeline-phase:nth-child(1) .timeline-dot { background: var(--success); }
.timeline-phase:nth-child(2) .timeline-dot { background: var(--warning); }
.timeline-phase:nth-child(3) .timeline-dot { background: var(--muted); }
.maturity-grid, .contradiction-card, .sources-compact, .cta-box, .confidence { font-family: "Segoe UI", system-ui, sans-serif; }
.maturity-row { display: grid; grid-template-columns: 130px 1fr 82px; gap: .6rem; font-size: .82rem; margin-bottom: .4rem; }
.maturity-bar { height: 18px; background: var(--border); overflow: hidden; }
.maturity-fill { height: 100%; font-size: .65rem; font-weight: 600; color: #fff; display: flex; align-items: center; padding-left: .45rem; }
.mat-f .maturity-fill { background: var(--success); width:85%; }
.mat-a .maturity-fill { background: var(--success); width:78%; opacity:.9; }
.mat-c .maturity-fill { background: var(--accent); width:65%; }
.mat-d .maturity-fill { background: #b85c72; width:55%; }
.mat-b .maturity-fill { background: var(--muted); width:35%; }
.mat-e .maturity-fill { background: var(--warning); width:30%; }
.contradiction-card { display: grid; grid-template-columns: 1fr auto 1fr auto; gap: .45rem; align-items: center; margin-bottom: .55rem; font-size: .84rem; }
.contra-side { padding: .45rem .55rem; border: 1px solid var(--border); background: var(--surface); }
.contra-vs { font-weight: 800; color: var(--accent); }
.tag-mixed { background: var(--accent-light); color: var(--accent); padding: .1rem .4rem; font-size: .68rem; font-weight: 600; }
.tag-weak { background: var(--border); color: var(--muted); padding: .1rem .4rem; font-size: .68rem; font-weight: 600; }
.cta-box { border: 1px solid var(--accent); padding: 1rem; margin-top: 1.5rem; background: var(--accent-light); }
.confidence { display: flex; gap: .85rem; padding: .9rem; border-top: 1px solid var(--border); margin-top: 1.5rem; font-size: .88rem; }
.confidence .level { font-weight: 700; color: var(--accent); }
footer { font-family: "Segoe UI", system-ui, sans-serif; text-align: center; color: var(--muted); font-size: .8rem; padding: 2rem 0 0; }
@media (max-width: 800px) { .insights-grid { grid-template-columns: 1fr; } .timeline { flex-direction: column; gap: .85rem; } .timeline::before { display: none; } .maturity-row { grid-template-columns: 1fr; } .contradiction-card { grid-template-columns: 1fr; } }
""",

"minimal": r"""
:root {
  --bg: #fafafa; --surface: #fff; --text: #18181b; --muted: #71717a; --border: #d4d4d8;
  --accent: #18181b; --accent-light: #f4f4f5; --success: #166534; --warning: #a16207;
  --radius: 0; --shadow: none;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body.preset-minimal { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; font-size: 15px; }
.layout-minimal { display: grid; grid-template-columns: 200px 1fr; min-height: 100vh; }
nav { position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--surface); border-right: 1px solid var(--border); padding: 1rem .6rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
nav h2 { font-size: .6rem; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); margin-bottom: .6rem; }
nav a { display: block; padding: .25rem .4rem; color: var(--text); text-decoration: none; font-size: .72rem; border-radius: 0; }
nav a:hover { background: var(--accent-light); }
main { max-width: 780px; padding: 1.5rem 1.25rem 3rem; }
header.hero { background: var(--surface); color: var(--text); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); border-radius: 0; padding: 1rem 0; margin-bottom: 1.25rem; box-shadow: none; }
header.hero h1 { font-size: 1.35rem; font-weight: 700; font-family: ui-monospace, monospace; letter-spacing: -0.02em; }
header.hero .subtitle { font-family: ui-monospace, monospace; font-size: .78rem; color: var(--muted); margin-top: .35rem; }
.badge { font-family: ui-monospace, monospace; background: var(--accent); color: #fff; padding: .15rem .4rem; font-size: .68rem; font-weight: 600; border-radius: 0; }
article { background: var(--surface); border: 1px solid var(--border); border-radius: 0; padding: 1.25rem; box-shadow: none; }
.prose-beat { margin: 1.25rem 0; font-size: .94rem; }
.prose-beat strong { color: var(--text); font-weight: 700; text-decoration: underline; text-decoration-color: var(--muted); text-underline-offset: 2px; }
.prose-beat.lead { font-size: .98rem; background: var(--accent-light); border-left: 3px solid var(--accent); padding: .85rem 1rem; margin: 0 0 1rem; }
.prose-beat h2 { font-family: ui-monospace, monospace; font-size: 1rem; color: var(--text); border-top: 1px solid var(--border); padding-top: .75rem; margin-top: 1.5rem; text-transform: uppercase; letter-spacing: .04em; }
.prose-beat.tight { font-size: .82rem; color: var(--muted); font-family: ui-monospace, monospace; }
.visual-beat { margin: 1rem 0; background: var(--surface); border: 1px solid var(--border); padding: 1rem; overflow-x: auto; }
.caption { font-family: ui-monospace, monospace; text-align: left; font-size: .7rem; color: var(--muted); margin-top: .5rem; font-style: normal; }
.insight-card { padding: .75rem; border: 1px solid var(--border); background: var(--bg); font-size: .82rem; font-family: ui-monospace, monospace; }
.insight-card .num { display: inline-block; background: var(--accent); color: #fff; padding: 0 .35rem; font-size: .68rem; font-weight: 700; margin-right: .3rem; border-radius: 0; }
.insights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; }
.timeline-dot { width: 44px; height: 44px; border-radius: 0; border: 1px solid var(--border); background: var(--accent-light); color: var(--text); font-family: ui-monospace, monospace; font-size: .6rem; font-weight: 700; display: flex; align-items: center; justify-content: center; margin: 0 auto .4rem; }
.maturity-bar { height: 16px; background: var(--accent-light); border: 1px solid var(--border); border-radius: 0; }
.maturity-fill { background: var(--accent); border-radius: 0; font-family: ui-monospace, monospace; }
.contradiction-card { display: grid; grid-template-columns: 1fr auto 1fr auto; gap: .4rem; border: 1px solid var(--border); padding: .6rem; margin-bottom: .4rem; font-size: .8rem; font-family: ui-monospace, monospace; }
.contra-side { border: 1px solid var(--border); padding: .4rem; background: var(--bg); }
.sources-compact a, .prose-beat a { color: var(--text); text-decoration: underline; text-underline-offset: .15em; text-decoration-thickness: .06em; }
.cta-box { border: 2px solid var(--accent); padding: .85rem; margin-top: 1rem; font-family: ui-monospace, monospace; font-size: .85rem; background: var(--accent-light); }
.confidence { display: flex; gap: .75rem; border: 1px solid var(--border); padding: .75rem; margin-top: 1rem; font-size: .82rem; font-family: ui-monospace, monospace; }
footer { font-family: ui-monospace, monospace; text-align: left; color: var(--muted); font-size: .72rem; padding: 1rem 0 0; border-top: 1px solid var(--border); margin-top: 1rem; }
@media (max-width: 800px) { .layout-minimal { grid-template-columns: 1fr; } nav { position: static; height: auto; } .insights-grid { grid-template-columns: 1fr; } }
""",

"warm": r"""
:root {
  --bg: #f5f0e8; --surface: #fffaf3; --text: #2c2416; --muted: #6b5c4a; --border: #e5d9c8;
  --accent: #8b5a2b; --accent-light: #f0e6d6; --success: #3d5c3a; --warning: #b45309;
  --radius: 14px; --shadow: 0 2px 10px rgba(139,90,43,.08), 0 6px 20px rgba(44,36,22,.05);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body.preset-warm { font-family: "Segoe UI", system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; font-size: 16px; }
.layout-warm { display: grid; grid-template-columns: 220px 1fr; min-height: 100vh; }
nav { position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--surface); border-right: 1px solid var(--border); padding: 1.2rem .75rem; counter-reset: navstep; }
nav h2 { font-size: .68rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); margin-bottom: .75rem; }
nav a { display: flex; align-items: center; gap: .45rem; padding: .4rem .5rem; color: var(--text); text-decoration: none; border-radius: 10px; font-size: .82rem; margin-bottom: .15rem; }
nav a::before { counter-increment: navstep; content: counter(navstep); width: 22px; height: 22px; background: var(--accent-light); color: var(--accent); border-radius: 50%; font-size: .65rem; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
nav a:hover { background: var(--accent-light); color: var(--accent); }
main { max-width: 820px; padding: 2rem 1.5rem 4rem; }
header.hero { background: linear-gradient(180deg, #fffaf3, #f4eadb); color: var(--text); border: 1px solid #d8c6ad; border-radius: var(--radius); padding: 1.5rem 1.75rem; margin-bottom: 1.5rem; box-shadow: var(--shadow); }
header.hero::before { content: "Étude · School of the Bear"; display: block; font-size: .68rem; text-transform: uppercase; letter-spacing: .1em; color: var(--accent); margin-bottom: .5rem; font-weight: 700; }
header.hero h1 { font-size: 1.5rem; margin-bottom: .4rem; color: var(--text); }
header.hero .subtitle { font-size: .9rem; color: var(--muted); margin-bottom: .6rem; }
.badge { background: var(--accent); color: #fff; padding: .2rem .55rem; border-radius: 20px; font-size: .75rem; font-weight: 600; }
article { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.75rem; box-shadow: var(--shadow); }
.prose-beat { margin: 1.5rem 0; font-size: .98rem; }
.prose-beat strong { color: var(--accent); }
.prose-beat.lead { font-size: 1.05rem; background: var(--accent-light); border-left: 4px solid var(--accent); padding: 1rem 1.15rem; border-radius: 0 12px 12px 0; margin: 0 0 1.25rem; }
.takeaway { background: var(--accent-light); border-left: 4px solid var(--success); padding: .85rem 1rem; border-radius: 0 12px 12px 0; margin: 1rem 0; font-size: .92rem; }
.open-question { font-style: italic; color: var(--accent); border-bottom: 1px dashed var(--border); padding-bottom: .5rem; margin: 1rem 0; font-size: .94rem; }
.prose-beat h2 { font-size: 1.2rem; color: var(--accent); border-top: 1px dashed var(--border); padding-top: .75rem; margin-top: 1.5rem; }
.visual-beat { margin: 1.25rem 0; background: var(--bg); border-radius: 14px; padding: 1.1rem; overflow-x: auto; border: 1px solid var(--border); }
.caption { text-align: center; font-size: .78rem; color: var(--muted); margin-top: .55rem; font-style: italic; }
.insight-card { padding: .85rem; border-radius: 12px; border-left: 3px solid var(--accent); background: var(--bg); font-size: .86rem; }
.insight-card .num { display: inline-block; width: 22px; height: 22px; background: var(--accent); color: #fff; border-radius: 50%; text-align: center; line-height: 22px; font-size: .7rem; font-weight: 700; margin-right: .35rem; }
.insights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; }
.maturity-fill { border-radius: 10px; }
.mat-f .maturity-fill { background: linear-gradient(90deg,#3d5c3a,#5a8a52); width:85%; }
.mat-a .maturity-fill { background: linear-gradient(90deg,#3d5c3a,#6a9a5a); width:78%; }
.mat-c .maturity-fill { background: linear-gradient(90deg,#8b5a2b,#c49a6c); width:65%; }
.mat-d .maturity-fill { background: linear-gradient(90deg,#8b5a2b,#d4aa7a); width:55%; }
.mat-b .maturity-fill { background: linear-gradient(90deg,#6b5c4a,#9a8a72); width:35%; }
.mat-e .maturity-fill { background: linear-gradient(90deg,#b45309,#d47a2a); width:30%; }
.cta-box { border: 2px solid var(--accent); border-radius: 12px; padding: 1rem; background: linear-gradient(135deg, var(--accent-light), var(--surface)); margin-top: 1rem; }
.confidence { display: flex; gap: .85rem; padding: .9rem; background: var(--accent-light); border-radius: 12px; margin-top: 1rem; }
.confidence .level { font-weight: 700; color: var(--accent); }
footer { text-align: center; color: var(--muted); font-size: .8rem; padding: 1.25rem 0 0; }
@media (max-width: 800px) { .layout-warm { grid-template-columns: 1fr; } nav { position: static; height: auto; } .insights-grid { grid-template-columns: 1fr; } }
""",

"creative": r"""
:root {
  --bg: #f3f0ff; --surface: #fff; --text: #1a0a2e; --muted: #5c4a7a; --border: #1a0a2e;
  --accent: #ff2d6a; --accent-2: #00d4aa; --accent-3: #ffb800; --accent-light: #ffe0ec;
  --success: #00a878; --warning: #ff6b00; --radius: 0;
  --shadow: 4px 4px 0 var(--border);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body.preset-creative {
  font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.65; font-size: 16px;
  background-image: repeating-linear-gradient(45deg, transparent, transparent 12px, rgba(26,10,46,.03) 12px, rgba(26,10,46,.03) 13px);
}
.layout-creative { display: grid; grid-template-columns: 210px 1fr; min-height: 100vh; }
nav { position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--surface); border-right: 3px solid var(--border); padding: 1rem .6rem; }
nav h2 { font-size: .65rem; text-transform: uppercase; letter-spacing: .12em; color: var(--accent); margin-bottom: .65rem; font-weight: 900; }
nav a { display: block; padding: .35rem .5rem; margin-bottom: .35rem; color: var(--text); text-decoration: none; font-size: .78rem; font-weight: 600; background: #fff; border: 2px solid var(--border); box-shadow: 3px 3px 0 var(--border); transition: transform .1s, background .1s; }
nav a:hover { background: var(--accent-2); color: var(--border); transform: rotate(-1deg); }
main { max-width: 800px; padding: 1.75rem 1.25rem 3.5rem; }
header.hero { background: var(--accent-3); color: var(--border); border: 3px solid var(--border); box-shadow: 8px 8px 0 var(--border); border-radius: 0; padding: 0; margin-bottom: 1.75rem; overflow: hidden; }
header.hero h1 { font-size: 1.55rem; font-weight: 900; letter-spacing: -0.03em; background: var(--accent); color: #fff; padding: 1rem 1.25rem; margin: 0; }
.hero-deck { background: #fff; padding: .85rem 1.25rem; transform: skewX(-1deg); margin: .5rem 1rem 1rem; border: 2px solid var(--border); }
header.hero .subtitle { font-size: .88rem; color: var(--text); margin: 0; transform: skewX(1deg); }
.badge { background: var(--accent-2); color: var(--border); border: 2px solid var(--border); padding: .15rem .5rem; font-size: .72rem; font-weight: 800; display: inline-block; margin-top: .35rem; box-shadow: 2px 2px 0 var(--border); }
article { background: var(--surface); border: 3px solid var(--border); box-shadow: 6px 6px 0 var(--border); padding: 1.5rem; border-radius: 0; }
.prose-beat { margin: 1.35rem 0; font-size: .98rem; }
.prose-beat strong { color: var(--accent); font-weight: 800; }
.prose-beat strong:nth-of-type(even) { color: #7b2ff7; }
.prose-beat.lead { font-size: 1.05rem; background: #fff3cc; border: 3px solid var(--border); padding: 1rem; box-shadow: 4px 4px 0 var(--border); margin: 0 0 1.25rem; }
.spicy-callout { background: var(--accent); color: #fff; border: 2px solid var(--border); box-shadow: 4px 4px 0 var(--border); padding: .75rem 1rem; margin: 1rem 0; font-weight: 700; transform: rotate(-0.4deg); }
.prose-beat h2 { font-size: 1.15rem; color: var(--accent); font-weight: 900; border-top: 3px solid var(--border); padding-top: .65rem; margin-top: 1.5rem; text-transform: uppercase; letter-spacing: .02em; }
.visual-beat { margin: 1.25rem 0; background: #fff; border: 3px solid var(--border); box-shadow: 5px 5px 0 var(--border); padding: 1rem; overflow-x: auto; }
.visual-beat:nth-of-type(even) { transform: rotate(0.4deg); }
.visual-beat:nth-of-type(odd) { transform: rotate(-0.3deg); }
.caption { text-align: center; font-size: .76rem; color: var(--muted); margin-top: .5rem; font-weight: 700; font-style: normal; }
.insight-card { padding: .8rem; border: 2px solid var(--border); box-shadow: 3px 3px 0 var(--border); background: #fff; font-size: .84rem; }
.insight-card .num { display: inline-block; width: 24px; height: 24px; background: var(--accent); color: #fff; border: 2px solid var(--border); text-align: center; line-height: 20px; font-size: .7rem; font-weight: 900; margin-right: .35rem; }
.insights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: .55rem; }
.timeline-dot { width: 48px; height: 48px; border-radius: 0; border: 2px solid var(--border); box-shadow: 3px 3px 0 var(--border); font-weight: 900; font-size: .62rem; display: flex; align-items: center; justify-content: center; margin: 0 auto .4rem; color: var(--border); }
.timeline-phase:nth-child(1) .timeline-dot { background: var(--accent-2); }
.timeline-phase:nth-child(2) .timeline-dot { background: var(--accent-3); }
.timeline-phase:nth-child(3) .timeline-dot { background: #e8d4ff; }
.maturity-bar { height: 22px; border: 2px solid var(--border); background: #fff; border-radius: 0; }
.maturity-fill { border-radius: 0; font-weight: 800; }
.mat-f .maturity-fill { background: var(--success); width:85%; }
.mat-a .maturity-fill { background: var(--accent-2); width:78%; }
.mat-c .maturity-fill { background: var(--accent); width:65%; }
.mat-d .maturity-fill { background: #7b2ff7; width:55%; }
.mat-b .maturity-fill { background: var(--muted); width:35%; }
.mat-e .maturity-fill { background: var(--warning); width:30%; }
.contradiction-card { display: grid; grid-template-columns: 1fr auto 1fr auto; gap: .4rem; border: 2px solid var(--border); box-shadow: 3px 3px 0 var(--border); padding: .65rem; margin-bottom: .5rem; font-size: .82rem; background: #fff; }
.contra-vs { font-weight: 900; color: var(--accent); font-size: 1rem; }
.tag-mixed { background: var(--accent-light); color: var(--accent); border: 1px solid var(--border); padding: .1rem .35rem; font-size: .65rem; font-weight: 800; }
.tag-weak { background: #e8d4ff; color: var(--muted); border: 1px solid var(--border); padding: .1rem .35rem; font-size: .65rem; font-weight: 800; }
.cta-box { border: 3px solid var(--border); box-shadow: 5px 5px 0 var(--accent); padding: 1rem; margin-top: 1rem; background: linear-gradient(135deg, #ffe0ec, #fff3cc); font-weight: 600; }
.cta-box.spicy-callout { background: var(--accent); color: #fff; transform: rotate(-0.3deg); }
.cta-box.spicy-callout strong { color: #fff; }
.confidence { display: flex; gap: .75rem; border: 3px solid var(--border); box-shadow: 4px 4px 0 var(--accent-2); padding: .85rem; margin-top: 1rem; background: #fff; }
.confidence .level { font-weight: 900; color: var(--accent); font-size: 1.1rem; }
footer { text-align: center; color: var(--muted); font-size: .78rem; font-weight: 700; padding: 1.25rem 0 0; }
@media (max-width: 800px) { .layout-creative { grid-template-columns: 1fr; } nav { position: static; height: auto; } .visual-beat { transform: none !important; } .insights-grid { grid-template-columns: 1fr; } }
""",
}

BODY_CLASS = {
    "academic": "",
    "editorial": ' class="preset-editorial"',
    "minimal": ' class="preset-minimal"',
    "warm": ' class="preset-warm"',
    "creative": ' class="preset-creative"',
}

LAYOUT_CLASS = {
    "academic": "layout",
    "editorial": "layout layout-editorial",
    "minimal": "layout layout-minimal",
    "warm": "layout layout-warm",
    "creative": "layout layout-creative",
}

HERO_ACADEMIC = """      <header class="hero">
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <div class="hero-metrics">
          <span class="metric-pill">179 sources</span>
          <span class="metric-pill">20 lectures</span>
          <span class="metric-pill">1 juillet 2026</span>
          <span class="badge">Confiance moyenne-haute</span>
        </div>
      </header>"""

HERO_CREATIVE = """      <header class="hero">
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <div class="hero-deck">
          <p class="subtitle">179 sources · 20 lectures · 1 juillet 2026</p>
          <span class="badge">Confiance moyenne-haute</span>
        </div>
      </header>"""

HERO_DEFAULT = """      <header class="hero">
        <h1>Robots d'assemblage structurel sur chantier</h1>
        <p class="subtitle">179 sources · 20 lectures · 1 juillet 2026</p>
        <span class="badge">Confiance moyenne-haute</span>
      </header>"""


def extract_parts(html: str):
    nav_m = re.search(r"<nav>(.*?)</nav>", html, re.DOTALL)
    article_m = re.search(r"<article>(.*?)</article>", html, re.DOTALL)
    footer_m = re.search(r"<footer>(.*?)</footer>", html, re.DOTALL)
    return nav_m.group(1), article_m.group(1), footer_m.group(1)


def remap_colors(fragment: str, preset: str) -> str:
    out = fragment
    for old, new in REMAP.get(preset, {}).items():
        out = out.replace(old, new)
    return out


def enhance_article(article: str, preset: str) -> str:
    """Apply preset-specific optional components from open-source patterns."""
    out = article
    if preset == "academic":
        out = out.replace('class="prose-beat tight"', 'class="prose-beat sidenote"', 1)
    if preset == "editorial":
        out = out.replace(
            '<h2>8 messages à retenir</h2>',
            '<span class="section-kicker">Synthèse</span>\n          <h2>8 messages à retenir</h2>',
            1,
        )
        out = out.replace(
            'Chaque pilier a un rôle précis.',
            '<div class="pullquote">Chaque pilier a un rôle précis. Le <strong>design</strong> réduit ce que le robot doit improviser.</div>\n          Chaque pilier a un rôle précis.',
            1,
        )
    if preset == "warm":
        out = out.replace(
            'class="confidence"',
            'class="confidence takeaway"',
            1,
        )
    if preset == "creative":
        out = out.replace('class="cta-box"', 'class="cta-box spicy-callout"', 1)
    return out


def build(preset: str, nav: str, article: str, footer: str) -> str:
    article = enhance_article(remap_colors(article, preset), preset)
    hero = HERO_ACADEMIC if preset == "academic" else HERO_CREATIVE if preset == "creative" else HERO_DEFAULT
    return f"""<!DOCTYPE html>
<html lang="fr">
<!-- style: {preset} -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Robots d'assemblage structurel sur chantier</title>
  <style>
{CSS[preset].strip()}
  </style>
</head>
<body{BODY_CLASS[preset]}>
  <div class="{LAYOUT_CLASS[preset]}">
    <nav>{nav}</nav>
    <main>
{hero}
      <article>{article}</article>
      <footer>{footer}</footer>
    </main>
  </div>
</body>
</html>
"""


def main():
    html = SRC.read_text(encoding="utf-8")
    nav, article, footer = extract_parts(html)
    for preset in ("academic", "editorial", "minimal", "warm", "creative"):
        out = OUT_DIR / f"report-{preset}.html"
        out.write_text(build(preset, nav, article, footer), encoding="utf-8")
        print(f"wrote {out}")
    # academic is also default report.html
    (OUT_DIR / "report.html").write_text(
        build("academic", nav, article, footer), encoding="utf-8"
    )
    print(f"wrote {OUT_DIR / 'report.html'}")


if __name__ == "__main__":
    main()