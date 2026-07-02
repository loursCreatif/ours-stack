"""Palette-aware SVG/HTML figure templates for layout-html v3."""
from __future__ import annotations

PALETTES: dict[str, dict[str, str]] = {
    "editorial": {
        "primary": "#8b2942", "secondary": "#b85c72", "tertiary": "#b85c72",
        "success": "#2d5a3d", "warning": "#8b6914", "muted": "#6b6560",
        "surface": "#f5e8ec", "surface2": "#edd5dc", "bg": "#faf3e0",
        "text_on_primary": "#fff", "surface_alt": "#ede8e0",
    },
    "warm": {
        "primary": "#8b5a2b", "secondary": "#c49a6c", "tertiary": "#d4aa7a",
        "success": "#3d5c3a", "warning": "#b45309", "muted": "#6b5c4a",
        "surface": "#f0e6d6", "surface2": "#e5d9c8", "bg": "#fff8e6",
        "text_on_primary": "#fff", "surface_alt": "#e5d9c8",
    },
    "creative-pop": {
        "primary": "#ff4757", "secondary": "#ff6b81", "tertiary": "#ffa502",
        "success": "#2ed573", "warning": "#ffa502", "muted": "#57606f",
        "surface": "#fff5f6", "surface2": "#ffe8ea", "bg": "#f1f2f6",
        "text_on_primary": "#fff", "surface_alt": "#ffe8ea",
    },
    "academic": {
        "primary": "#1e4d8c", "secondary": "#2d6cb5", "tertiary": "#3d8fd4",
        "success": "#1a6b4a", "warning": "#9a6b00", "muted": "#5c6370",
        "surface": "#e8f0fa", "surface2": "#d4e4f7", "bg": "#fff8e6",
        "text_on_primary": "#fff", "surface_alt": "#e8ecf2",
    },
    "minimal": {
        "primary": "#18181b", "secondary": "#3f3f46", "tertiary": "#52525b",
        "success": "#166534", "warning": "#a16207", "muted": "#71717a",
        "surface": "#f4f4f5", "surface2": "#e4e4e7", "bg": "#fafafa",
        "text_on_primary": "#fff", "surface_alt": "#f4f4f5",
    },
}

# Academic blues that must not appear in non-academic presets
FORBIDDEN_NON_ACADEMIC = ("#1e4d8c", "#2d6cb5", "#3d8fd4", "#1a6b4a", "#e8f0fa", "#d4e4f7")

MATURITY = [
    ("F Préfab", "mat-f", "85%", "Industrie", "success"),
    ("A Dédié", "mat-a", "78%", "Commercial", "success"),
    ("C Grue/AGV", "mat-c", "65%", "Startups", "primary"),
    ("D HRC", "mat-d", "55%", "Recherche+", "secondary"),
    ("B Mobile", "mat-b", "35%", "Démo", "muted"),
    ("E Multi-IA", "mat-e", "30%", "Lab", "warning"),
]

CLAIM_ROWS = [
    ("Design > autonomie", "Fort", "F/A", "Now", "success"),
    ("Co-robotique + laser", "Fort", "D · 55%", "Now", "success"),
    ("Commercial brique/acier", "Moyen", "A · 78%", "Now", "primary"),
    ("Préfab = plus mature", "Fort", "F · 85%", "Now", "success"),
    ("VLA multi-robots", "Faible", "E · 30%", "R&D", "warning"),
]

INSIGHTS = [
    ("1", "Design > autonomie", "Modulaires auto-alignants = moins de perception.", "Tessellated Biomes"),
    ("2", "Co-robotique déployable", "Projection + laser corrige les tolérances.", "Gao & Adel 2026"),
    ("3", "Plan = structure + mouvement", "Stabilité physique dans le séquencement.", "EUPHORIA 2026"),
    ("4", "Scheduling > + de bras", "352 vis, dalle 2,4×6 m, zéro collision.", "LASER 2026"),
    ("5", "Commercial = brique + acier", "Monumental, FBR, SAM, PolyU.", "Déploiements récurrents"),
    ("6", "Robotique situationnelle", "Perception temps réel, jumeau numérique.", "Leonard / VINCI 2026"),
    ("7", "Adoption marginale", "+15 %/an mais 0,03 % du BTP.", "Zacua 2026"),
    ("8", "Sécurité HRC", "Risques mécaniques + psychosociaux.", "Earnest 2026"),
]

MAX_ANIMATED = 3


def get_palette(preset: str) -> dict[str, str]:
    return PALETTES.get(preset, PALETTES["editorial"]).copy()


def _fill(color_key: str, pal: dict[str, str]) -> str:
    return pal.get(color_key, pal["primary"])


def _wrap(beat_id: str, inner: str, fig_num: int | str, caption: str, *, animate: bool = False) -> str:
    cls = "visual-beat fig-animate" if animate else "visual-beat"
    id_attr = f' id="{beat_id}"' if beat_id else ""
    return f"""        <div class="{cls}"{id_attr}>
{inner}
          <p class="caption">Fig. {fig_num} — {caption}</p>
        </div>"""


def claim_atlas(preset: str, *, animate: bool = True) -> str:
    pal = get_palette(preset)
    p, s, su, s2, m, ok, warn = pal["primary"], pal["secondary"], pal["surface"], pal["surface2"], pal["muted"], pal["success"], pal["warning"]
    rows_svg = []
    y0 = 118
    for i, (claim, proof, mat, horizon, tone) in enumerate(CLAIM_ROWS):
        y = y0 + i * 36
        fill = {"success": ok, "primary": p, "warning": warn, "secondary": s}.get(tone, p)
        layer = f' class="fig-layer fig-layer-{min(i + 1, 4)}"' if animate else ""
        rows_svg.append(f"""
            <g{layer}>
              <rect x="12" y="{y}" width="696" height="30" rx="4" fill="{su if i % 2 == 0 else '#fff'}" stroke="{s2}" stroke-width="1"/>
              <text x="24" y="{y + 19}" font-size="11" font-weight="600" fill="{p}">{claim}</text>
              <circle cx="310" cy="{y + 15}" r="5" fill="{fill}"/>
              <text x="324" y="{y + 19}" font-size="10" fill="{m}">{proof}</text>
              <text x="430" y="{y + 19}" font-size="10" font-weight="600" fill="{p}">{mat}</text>
              <text x="560" y="{y + 19}" font-size="10" fill="{m}">{horizon}</text>
            </g>""")
    rows = "".join(rows_svg)
    svg = f"""          <svg viewBox="0 0 720 310" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Atlas des conclusions : preuve, maturité et horizon" class="fig-svg">
            <defs>
              <filter id="fig1-shadow" x="-5%" y="-5%" width="110%" height="110%">
                <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="{p}" flood-opacity="0.12"/>
              </filter>
            </defs>
            <rect width="720" height="310" rx="6" fill="{pal['surface_alt']}" stroke="{s2}"/>
            <g filter="url(#fig1-shadow)">
              <rect x="12" y="12" width="160" height="52" rx="6" fill="{su}"/><text x="92" y="36" text-anchor="middle" font-size="22" font-weight="700" fill="{p}">179</text><text x="92" y="52" text-anchor="middle" font-size="9" fill="{m}">SOURCES</text>
              <rect x="184" y="12" width="160" height="52" rx="6" fill="{su}"/><text x="264" y="36" text-anchor="middle" font-size="22" font-weight="700" fill="{p}">20</text><text x="264" y="52" text-anchor="middle" font-size="9" fill="{m}">LECTURES</text>
              <rect x="356" y="12" width="160" height="52" rx="6" fill="{su}"/><text x="436" y="36" text-anchor="middle" font-size="22" font-weight="700" fill="{p}">6</text><text x="436" y="52" text-anchor="middle" font-size="9" fill="{m}">FAMILLES A–F</text>
              <rect x="528" y="12" width="180" height="52" rx="6" fill="{su}"/><text x="618" y="36" text-anchor="middle" font-size="22" font-weight="700" fill="{p}">3</text><text x="618" y="52" text-anchor="middle" font-size="9" fill="{m}">PILIERS</text>
            </g>
            <text x="24" y="88" font-size="10" font-weight="700" fill="{m}">CONCLUSION</text>
            <text x="300" y="88" font-size="10" font-weight="700" fill="{m}">PREUVE</text>
            <text x="430" y="88" font-size="10" font-weight="700" fill="{m}">MATURITÉ</text>
            <text x="560" y="88" font-size="10" font-weight="700" fill="{m}">HORIZON</text>
            <line x1="12" y1="96" x2="708" y2="96" stroke="{s2}" stroke-width="1"/>
            {rows}
          </svg>"""
    return _wrap("atlas", svg, 1, "Atlas des conclusions — preuve, maturité, horizon", animate=animate)


def pillars(preset: str) -> str:
    pal = get_palette(preset)
    p, s, ok, warn, m, su, alt = pal["primary"], pal["secondary"], pal["success"], pal["warning"], pal["muted"], pal["surface"], pal["surface_alt"]
    svg = f"""          <svg viewBox="0 0 720 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Trois piliers sur la réalité du chantier" class="fig-svg">
            <defs>
              <linearGradient id="fig2-grad-design" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="{p}"/><stop offset="100%" stop-color="{s}"/></linearGradient>
              <linearGradient id="fig2-grad-robot" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="{ok}"/><stop offset="100%" stop-color="{ok}"/></linearGradient>
              <linearGradient id="fig2-grad-feedback" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="{warn}"/><stop offset="100%" stop-color="{warn}"/></linearGradient>
              <marker id="fig2-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{p}"/></marker>
            </defs>
            <rect x="40" y="195" width="640" height="45" rx="8" fill="{alt}" stroke="{pal['surface2']}"/>
            <text x="360" y="224" text-anchor="middle" font-size="13" font-weight="600" fill="{m}">CHANTIER — instable, imprévisible</text>
            <rect x="60" y="75" width="180" height="110" rx="10" fill="url(#fig2-grad-design)"/>
            <text x="150" y="108" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">DESIGN</text>
            <text x="150" y="128" text-anchor="middle" font-size="10" fill="{su}">Modulaire · Auto-alignant</text>
            <rect x="270" y="75" width="180" height="110" rx="10" fill="url(#fig2-grad-robot)"/>
            <text x="360" y="108" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">ROBOT</text>
            <text x="360" y="128" text-anchor="middle" font-size="10" fill="{su}">Mobile · Grue · Dédié</text>
            <rect x="480" y="75" width="180" height="110" rx="10" fill="url(#fig2-grad-feedback)"/>
            <text x="570" y="108" text-anchor="middle" font-size="12" font-weight="700" fill="#fff">FEEDBACK</text>
            <text x="570" y="128" text-anchor="middle" font-size="10" fill="{su}">Laser · BIM · Jumeau</text>
            <line x1="150" y1="185" x2="150" y2="195" stroke="{p}" stroke-width="2" marker-end="url(#fig2-arrow)"/>
            <line x1="360" y1="185" x2="360" y2="195" stroke="{ok}" stroke-width="2" marker-end="url(#fig2-arrow)"/>
            <line x1="570" y1="185" x2="570" y2="195" stroke="{warn}" stroke-width="2" marker-end="url(#fig2-arrow)"/>
            <polygon points="360,25 660,65 60,65" fill="none" stroke="{p}" stroke-width="2" stroke-dasharray="5,4"/>
            <text x="360" y="52" text-anchor="middle" font-size="11" font-weight="700" fill="{p}">ASSEMBLAGE RÉUSSI</text>
          </svg>"""
    return _wrap("piliers", svg, 2, "Architecture hybride : les trois piliers reposent sur la réalité du chantier")


def timeline_beat() -> str:
    inner = """          <div class="timeline">
            <div class="timeline-phase">
              <div class="timeline-dot">NOW</div>
              <h4>Court terme ✓</h4>
              <ul><li>HRC + laser</li><li>Robots brique</li><li>Soudage vision</li><li>Préfab (F)</li></ul>
            </div>
            <div class="timeline-phase">
              <div class="timeline-dot">2–5 ans</div>
              <h4>Moyen terme</h4>
              <ul><li>Manipulateurs mobiles</li><li>Multi-robot LASER</li><li>IA situationnelle</li></ul>
            </div>
            <div class="timeline-phase">
              <div class="timeline-dot">R&D</div>
              <h4>Recherche</h4>
              <ul><li>VLA (CHORUS)</li><li>RL sans plan</li><li>EUPHORIA</li></ul>
            </div>
          </div>"""
    return _wrap("", inner, 3, "Horizon de déploiement par maturité terrain")


def funnel(preset: str, *, animate: bool = True) -> str:
    pal = get_palette(preset)
    p, s, su, s2, m = pal["primary"], pal["secondary"], pal["surface"], pal["surface2"], pal["muted"]
    l1 = ' class="fig-layer fig-layer-1"' if animate else ""
    l2 = ' class="fig-layer fig-layer-2"' if animate else ""
    l3 = ' class="fig-layer fig-layer-3"' if animate else ""
    svg = f"""          <svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Entonnoir méthodologie PRISMA" class="fig-svg">
            <defs>
              <linearGradient id="fig4-grad-1" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="{su}"/><stop offset="100%" stop-color="{s2}"/></linearGradient>
              <marker id="fig4-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 Z" fill="{m}"/></marker>
              <filter id="fig4-shadow" x="-5%" y="-5%" width="110%" height="110%"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="{p}" flood-opacity="0.15"/></filter>
            </defs>
            <polygon{l1} points="240,16 400,52 400,70 240,70 80,70 80,52" fill="url(#fig4-grad-1)" stroke="{s}" stroke-width="1.5" filter="url(#fig4-shadow)"/>
            <text x="240" y="46" text-anchor="middle" font-size="13" font-weight="700" fill="{p}">179 découvertes</text>
            <line x1="400" y1="46" x2="428" y2="46" stroke="{m}" stroke-width="1" marker-end="url(#fig4-arrow)"/>
            <text x="436" y="49" font-size="10" fill="{m}">14 exclues</text>
            <polygon{l2} points="240,78 360,108 360,126 240,126 120,126 120,108" fill="{s2}" stroke="{s}" stroke-width="1.5"/>
            <text x="240" y="111" text-anchor="middle" font-size="12" font-weight="600" fill="{p}">165 retenues → 20 lues</text>
            <polygon{l3} points="240,138 300,168 300,186 240,186 180,186 180,168" fill="{p}" stroke="{p}" stroke-width="1.5"/>
            <text x="240" y="168" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Synthèse</text>
          </svg>"""
    return _wrap("", svg, 4, "Méthodologie : entonnoir PRISMA", animate=animate)


def insights_merged() -> str:
    cards = []
    for n, title, body, src in INSIGHTS:
        cards.append(
            f'            <div class="insight-card"><span class="num">{n}</span><strong>{title}</strong> — {body}<span class="src">{src}</span></div>'
        )
        if n == "4":
            cards.append(
                '            <div class="insights-split">Contexte marché &amp; réglementaire</div>'
            )
    inner = "          <div class=\"insights-grid insights-grid-8\">\n" + "\n".join(cards) + "\n          </div>"
    return _wrap("", inner, 5, "Huit messages clés — technique et marché")


def maturity(preset: str, *, animate: bool = True) -> str:
    pal = get_palette(preset)
    rows = []
    for label, cls, pct, tag, tone in MATURITY:
        bg = _fill(tone if tone != "primary" else "primary", pal)
        if tone == "success":
            bg = pal["success"]
        elif tone == "secondary":
            bg = pal["secondary"]
        elif tone == "muted":
            bg = pal["muted"]
        elif tone == "warning":
            bg = pal["warning"]
        else:
            bg = pal["primary"]
        bar_cls = "maturity-fill fig-bar-fill" if animate else "maturity-fill"
        style = f' style="--target:{pct}; background:{bg};"' if animate else f' style="width:{pct}; background:{bg};"'
        rows.append(
            f'            <div class="maturity-row {cls}"><span class="label">{label}</span>'
            f'<div class="maturity-bar"><div class="{bar_cls}"{style}>{pct}</div></div>'
            f'<span class="maturity-tag">{tag}</span></div>'
        )
    inner = "          <div class=\"maturity-grid\">\n" + "\n".join(rows) + "\n          </div>"
    return _wrap("", inner, 6, "Maturité terrain estimée par approche", animate=animate)


def taxonomy_wheel(preset: str) -> str:
    pal = get_palette(preset)
    p, s, ok, warn, m, su = pal["primary"], pal["secondary"], pal["success"], pal["warning"], pal["muted"], pal["surface"]
    svg = f"""          <svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Roue taxonomique A-F" class="fig-svg">
            <defs><marker id="fig7-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{m}"/></marker></defs>
            <circle cx="320" cy="150" r="48" fill="{p}"/>
            <text x="320" y="147" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">ASSEMBLAGE</text>
            <text x="320" y="162" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STRUCTUREL</text>
            <g><circle cx="320" cy="42" r="34" fill="{ok}"/><text x="320" y="44" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">A</text><text x="320" y="56" text-anchor="middle" font-size="10" fill="{su}">Dédié</text></g>
            <g><circle cx="460" cy="82" r="34" fill="{m}"/><text x="460" y="84" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">B</text><text x="460" y="96" text-anchor="middle" font-size="10" fill="#fff">Mobile</text></g>
            <g><circle cx="460" cy="218" r="34" fill="{p}"/><text x="460" y="220" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">C</text><text x="460" y="232" text-anchor="middle" font-size="10" fill="{su}">Grue</text></g>
            <g><circle cx="320" cy="258" r="34" fill="{s}"/><text x="320" y="260" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">D</text><text x="320" y="272" text-anchor="middle" font-size="10" fill="#fff">HRC</text></g>
            <g><circle cx="180" cy="218" r="34" fill="{warn}"/><text x="180" y="220" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">E</text><text x="180" y="232" text-anchor="middle" font-size="10" fill="#fff">Multi</text></g>
            <g><circle cx="180" cy="82" r="34" fill="{ok}"/><text x="180" y="84" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">F</text><text x="180" y="96" text-anchor="middle" font-size="10" fill="{su}">Préfab</text></g>
            <line x1="320" y1="76" x2="320" y2="102" stroke="{ok}" stroke-width="1.5" marker-end="url(#fig7-arrow)"/>
            <line x1="368" y1="112" x2="428" y2="98" stroke="{m}" stroke-width="1.5" marker-end="url(#fig7-arrow)"/>
            <line x1="368" y1="188" x2="428" y2="202" stroke="{p}" stroke-width="1.5" marker-end="url(#fig7-arrow)"/>
            <line x1="320" y1="198" x2="320" y2="224" stroke="{s}" stroke-width="1.5" marker-end="url(#fig7-arrow)"/>
            <line x1="272" y1="188" x2="212" y2="202" stroke="{warn}" stroke-width="1.5" marker-end="url(#fig7-arrow)"/>
            <line x1="272" y1="112" x2="212" y2="98" stroke="{ok}" stroke-width="1.5" marker-end="url(#fig7-arrow)"/>
          </svg>"""
    return _wrap("", svg, 7, "Les six familles autour de l'assemblage structurel")


def stack_layers(preset: str) -> str:
    pal = get_palette(preset)
    p, s, su, m = pal["primary"], pal["secondary"], pal["surface"], pal["muted"]
    svg = f"""          <svg viewBox="0 0 560 185" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Stack technique trois couches" class="fig-svg">
            <polygon points="280,8 520,38 40,38" fill="{su}" stroke="{p}" stroke-width="1.5"/>
            <text x="280" y="28" text-anchor="middle" font-size="10" font-weight="700" fill="{p}">ÉCART PLAN ↔ RÉALITÉ</text>
            <rect x="95" y="48" width="370" height="32" rx="6" fill="{s}"/>
            <text x="280" y="68" text-anchor="middle" font-size="11" font-weight="600" fill="#fff">COUCHE 3 — BIM / Jumeau / Séquence</text>
            <rect x="70" y="88" width="420" height="32" rx="6" fill="{p}"/>
            <text x="280" y="108" text-anchor="middle" font-size="11" font-weight="600" fill="#fff">COUCHE 2 — Perception (vision, laser, SLAM)</text>
            <rect x="45" y="128" width="470" height="38" rx="6" fill="{p}" opacity="0.85"/>
            <text x="280" y="152" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">COUCHE 1 — Robot (bras, grue, AGV)</text>
            <text x="530" y="145" font-size="14" fill="{p}">✗</text>
            <text x="538" y="100" font-size="9" fill="{m}">sans 2–3 = échec</text>
          </svg>"""
    return _wrap("", svg, 8, "Stack transverse : BIM → Perception → Robot")


def workflow_hrc(preset: str) -> str:
    pal = get_palette(preset)
    p, s, warn, ok, m = pal["primary"], pal["secondary"], pal["warning"], pal["success"], pal["muted"]
    svg = f"""          <svg viewBox="0 0 560 120" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Workflow co-robotique" class="fig-svg">
            <defs><marker id="fig9-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{p}"/></marker></defs>
            <text x="280" y="22" text-anchor="middle" font-size="10" font-weight="600" fill="{m}">Workflow HRC — Gao &amp; Adel 2026</text>
            <rect x="20" y="40" width="100" height="50" rx="8" fill="{p}"/>
            <text x="70" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">ROBOT</text>
            <text x="70" y="76" text-anchor="middle" font-size="8" fill="{pal['surface']}">Pose brique</text>
            <line x1="120" y1="65" x2="155" y2="65" stroke="{p}" stroke-width="1.5" marker-end="url(#fig9-arrow)"/>
            <rect x="155" y="40" width="100" height="50" rx="8" fill="{s}"/>
            <text x="205" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">HUMAIN</text>
            <text x="205" y="76" text-anchor="middle" font-size="8" fill="#fff">Adhésif</text>
            <line x1="255" y1="65" x2="290" y2="65" stroke="{p}" stroke-width="1.5" marker-end="url(#fig9-arrow)"/>
            <rect x="290" y="40" width="110" height="50" rx="8" fill="{warn}"/>
            <text x="345" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">LASER</text>
            <text x="345" y="76" text-anchor="middle" font-size="8" fill="#fff">Correction</text>
            <line x1="400" y1="65" x2="435" y2="65" stroke="{p}" stroke-width="1.5" marker-end="url(#fig9-arrow)"/>
            <rect x="435" y="40" width="105" height="50" rx="8" fill="{ok}"/>
            <text x="487" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">NIVEAU OK</text>
            <text x="487" y="76" text-anchor="middle" font-size="8" fill="{pal['surface']}">Boucle fermée</text>
          </svg>"""
    return _wrap("", svg, 9, "Co-robotique : robot pose, humain finit, laser corrige")


def decision_tree(preset: str) -> str:
    pal = get_palette(preset)
    p, s, ok, warn, m, su = pal["primary"], pal["secondary"], pal["success"], pal["warning"], pal["muted"], pal["surface"]
    svg = f"""          <svg viewBox="0 0 600 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Arbre de décision chantier" class="fig-svg">
            <defs><marker id="fig10-arrow" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{p}"/></marker></defs>
            <rect x="200" y="8" width="200" height="32" rx="16" fill="{p}"/>
            <text x="300" y="29" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">Éléments standardisés ?</text>
            <line x1="300" y1="40" x2="300" y2="52" stroke="{p}" stroke-width="1.5" marker-end="url(#fig10-arrow)"/>
            <polygon points="300,52 390,88 300,124 210,88" fill="{su}" stroke="{p}" stroke-width="1.5"/>
            <text x="300" y="92" text-anchor="middle" font-size="10" font-weight="600">Répétitif ?</text>
            <line x1="230" y1="88" x2="90" y2="145" stroke="{ok}" stroke-width="1.5" marker-end="url(#fig10-arrow)"/>
            <rect x="30" y="145" width="120" height="44" rx="8" fill="{ok}"/>
            <text x="90" y="165" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">OUI → A ou F</text>
            <line x1="370" y1="88" x2="515" y2="145" stroke="{s}" stroke-width="1.5" marker-end="url(#fig10-arrow)"/>
            <rect x="450" y="145" width="130" height="44" rx="8" fill="{s}"/>
            <text x="515" y="165" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">NON → D</text>
            <polygon points="300,210 390,248 300,286 210,248" fill="{pal['bg']}" stroke="{warn}" stroke-width="1.5"/>
            <text x="300" y="252" text-anchor="middle" font-size="10" font-weight="600">Masse élevée ?</text>
            <rect x="30" y="310" width="110" height="40" rx="8" fill="{p}"/>
            <text x="85" y="335" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">C Grue/AGV</text>
            <rect x="245" y="310" width="110" height="40" rx="8" fill="{m}"/>
            <text x="300" y="335" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">B Mobile</text>
            <rect x="430" y="405" width="80" height="32" rx="6" fill="{warn}"/>
            <text x="470" y="426" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">E LASER</text>
          </svg>"""
    return _wrap("", svg, 10, "Arbre de décision par contexte chantier")


EXTRA_CSS = """
.insights-grid-8 { grid-template-columns: 1fr 1fr; }
.insights-split { grid-column: 1 / -1; font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); padding: .35rem 0 .15rem; border-top: 1px solid var(--border); margin-top: .25rem; }
@media (max-width: 800px) { .insights-grid-8 { grid-template-columns: 1fr; } }
"""