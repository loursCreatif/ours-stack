#!/usr/bin/env python3
"""Validate layout-html output files against skill constraints."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS))

from figure_templates import FORBIDDEN_NON_ACADEMIC, MAX_ANIMATED  # noqa: E402

FIG_CAPTION = re.compile(r"Fig\.\s*(\d+)")
BAD_IDS = re.compile(r'\bid="(g[0-9]|arr)"')
SCRIPT_TAG = re.compile(r"<script\b", re.I)
ONCLICK = re.compile(r"\bonclick\s*=", re.I)
CDN = re.compile(r"https?://", re.I)
REDUCED = re.compile(r"prefers-reduced-motion")
ANIM_BEAT = re.compile(r'class="visual-beat fig-animate"')


def validate(path: Path, preset: str | None = None) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    low = text.lower()

    if SCRIPT_TAG.search(text):
        errors.append("contains <script>")
    if ONCLICK.search(text):
        errors.append("contains onclick (no JS rule)")
    if CDN.search(text) and "xmlns=" not in text:
        errors.append("contains external URL")
    if not REDUCED.search(text):
        errors.append("missing prefers-reduced-motion block")

    figs = [int(m.group(1)) for m in FIG_CAPTION.finditer(text)]
    if figs and max(figs) > 10:
        errors.append(f"figure count exceeds 10 (max Fig. {max(figs)})")
    if figs and min(figs) < 1:
        errors.append("figure numbering must start at Fig. 1")

    anim_count = len(ANIM_BEAT.findall(text))
    if anim_count > MAX_ANIMATED:
        errors.append(f"too many animated visual-beats: {anim_count} > {MAX_ANIMATED}")

    if BAD_IDS.search(text):
        errors.append("generic SVG ids (g1/g2/arr) detected")

    check_preset = preset
    if not check_preset:
        if "preset-editorial" in low or "#8b2942" in text:
            check_preset = "editorial"
        elif "preset-warm" in low:
            check_preset = "warm"
        elif "ff4757" in text:
            check_preset = "creative-pop"

    if check_preset and check_preset != "academic":
        for hx in FORBIDDEN_NON_ACADEMIC:
            if hx in text:
                errors.append(f"academic palette leak: {hx}")
                break

    return errors


def main():
    ap = argparse.ArgumentParser(description="Validate layout-html output")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--preset", default=None)
    args = ap.parse_args()

    failed = 0
    for p in args.paths:
        errs = validate(p, args.preset)
        if errs:
            failed += 1
            print(f"FAIL {p}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"PASS {p}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()