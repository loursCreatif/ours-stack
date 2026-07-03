#!/usr/bin/env python3
"""Source-scout engine: cassette → dynamic pools → rubric score → pick → brief."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

MIN_SCORE = 9
MAX_AUTHORITY_CAP = 6  # hard cap when author/channel not identifiable

GENERIC_AUTHORS = frozenset({
    "youtube", "unknown", "anonymous", "n/a", "none", "channel", "creator", "user",
})
INSTITUTION_MARKERS = (
    ".edu", ".gov", "university", "laboratory", "laboratories", "institute", "ieee",
    "acm", "conference", "prof.", "professor", "dr.", "phd", "stanford", "mit",
    "pnnl", "sandia", "energy.gov", "arxiv", "tom's hardware", "anandtech",
    "techpowerup", "department", "college", "school of",
)

REJECT_HOSTS = (
    "howtogeek.com", "buzzfeed.com", "medium.com/@", "linkedin.com", "facebook.com",
    "threads.com", "tesla.com/learn", "nvidia.com", "investopedia.com", "phemex.com",
    "coingeek.com", "reddit.com", "wikipedia.org", "nakamotoinstitute.org",
)
REJECT_PATH = re.compile(
    r"top[-_]?\d+|introduction[-_]to|what[-_]is|best[-_]resources|/specs?/|/learn/", re.I
)

# Role signals from URL path + search query (generic patterns, not study-specific).
UNITS_RE = re.compile(
    r"kilowatt|kilowatthour|kwh|kw[\s_./-]|watthour|watt[\s_./-]hour|measuring|"
    r"electric[-_/].*meter|electricity.?basics|power.?vs.?energy|utility.?bill|"
    r"faq.*kilowatt|energysaver|appliance.*energy",
    re.I,
)
STORAGE_RE = re.compile(
    r"storage|batter|capacity|autonom|grid.?scale|power.?capacity|energy.?capacity|"
    r"grid.?energy|gridpiq",
    re.I,
)
INFERENCE_RE = re.compile(
    r"inference|llm|vllm|language.?model|prompt.?to.?power|energy.?footprint|"
    r"workload",
    re.I,
)
HW_MEASURE_RE = re.compile(
    r"rtx|geforce|powenetics|power.?draw|tdp|graphics.?card|measured.?power|"
    r"techpowerup|anandtech|tomshardware",
    re.I,
)

TIER1_HOST_MARKERS = (
    ".gov", "arxiv.org", "doi.org", "ieee.org", "pnnl.gov", "nrel.gov", "sandia.gov",
    "energy.gov", "eia.gov", "ledgerjournal.org",
)
TIER2_HOST_MARKERS = (
    "tomshardware.com", "anandtech.com", "techpowerup.com", "igorslab.de",
    "fidelitydigitalassets.com",
)

ROLE_UNITS = "units"
ROLE_STORAGE = "storage"
ROLE_INFERENCE = "inference"
ROLE_HW_MEASURE = "hw_measure"
ROLE_VIDEO = "video"
ROLE_HOMELAB = "homelab"


@dataclass
class WedgeSignals:
    wedge: str
    criteria: str
    open_questions: str
    beliefs: str
    text: str
    wants_units: bool = False
    wants_storage: bool = False
    wants_hardware: bool = False
    wants_inference: bool = False
    consumed: set[str] = field(default_factory=set)

    @classmethod
    def from_brief(
        cls,
        wedge: str,
        criteria: str,
        open_questions: str,
        beliefs: str,
        consumed: set[str] | None = None,
    ) -> WedgeSignals:
        blob = "\n".join((wedge, criteria, open_questions, beliefs)).lower()
        return cls(
            wedge=wedge.strip(),
            criteria=criteria.strip(),
            open_questions=open_questions.strip(),
            beliefs=beliefs.strip(),
            text=blob,
            wants_units=any(
                k in blob
                for k in ("kw", "kwh", "watt", "puissance", "énergie", "unité", "kilowatt")
            ),
            wants_storage=any(
                k in blob for k in ("autonomie", "stockée", "stockage", "batterie", "storage")
            ),
            wants_hardware=any(
                k in blob
                for k in (
                    "hardware", "serveur", "labo", "tdp", "rtx", "carte graphique",
                    "graphics", "accelerator",
                )
            ),
            wants_inference=any(
                k in blob for k in ("ia", "inférence", "inference", "llm", "vllm", "workload")
            ),
            consumed=consumed or set(),
        )

    def primary_anchor_role(self) -> str:
        if self.wants_units:
            return ROLE_UNITS
        if self.wants_storage:
            return ROLE_STORAGE
        if self.wants_inference:
            return ROLE_INFERENCE
        if self.wants_hardware:
            return ROLE_HW_MEASURE
        return ROLE_UNITS


@dataclass
class Candidate:
    url: str
    key: str
    author: str
    title: str
    fmt: str
    tier: int
    minutes: int
    access: str
    roles: set[str] = field(default_factory=set)
    fetched: bool = False
    snippet_chars: int = 0
    from_queries: set[str] = field(default_factory=set)
    score: int = 0
    score_note: str = ""
    why: str = ""
    targets: str = ""
    slot: str = ""

    @property
    def is_youtube(self) -> bool:
        return ROLE_VIDEO in self.roles


def norm_key(url: str) -> str:
    raw = url if url.startswith("http") else f"https://{url}"
    p = urlparse(raw)
    host = p.netloc.lower().removeprefix("www.")
    path = p.path.rstrip("/")
    if "youtube.com" in host and path == "/watch":
        from urllib.parse import parse_qs
        vid = parse_qs(p.query).get("v", [""])[0]
        if vid:
            return f"youtube.com/watch/{vid.lower()}"
    if host == "youtu.be" and path:
        return f"youtu.be/{path.lstrip('/').lower()}"
    u = f"{host}{path}".lower()
    return u.split("#")[0].split("?")[0]


def load_cassette(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def parse_consumed_urls(text: str) -> set[str]:
    keys: set[str] = set()
    for m in re.finditer(r"- \[x\].*?— (https?://\S+)", text):
        keys.add(norm_key(m.group(1).rstrip(">")))
    return keys


def _extract_section(text: str, heading: str) -> str:
    m = re.search(rf"{re.escape(heading)}\s*\n+(.*?)(?=\n## |\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def parse_brief(path: Path) -> WedgeSignals:
    text = path.read_text()
    return WedgeSignals.from_brief(
        _extract_section(text, "## Narrow wedge"),
        _extract_section(text, "## Success criteria"),
        _extract_section(text, "## Open questions"),
        _extract_section(text, "## Current beliefs"),
        parse_consumed_urls(text),
    )


def _query_blob(queries: set[str]) -> str:
    return " ".join(queries).lower()


def _domain_tier(host: str) -> int:
    if any(m in host for m in TIER1_HOST_MARKERS):
        return 1
    if any(m in host for m in TIER2_HOST_MARKERS):
        return 2
    if host.endswith(".edu"):
        return 2
    return 3


def _infer_roles(signal_blob: str, signals: WedgeSignals) -> set[str]:
    roles: set[str] = set()
    if UNITS_RE.search(signal_blob):
        roles.add(ROLE_UNITS)
    if STORAGE_RE.search(signal_blob):
        roles.add(ROLE_STORAGE)
    if INFERENCE_RE.search(signal_blob):
        roles.add(ROLE_INFERENCE)
    if HW_MEASURE_RE.search(signal_blob):
        roles.add(ROLE_HW_MEASURE)
    if "homelab" in signal_blob and signals.wants_hardware:
        roles.add(ROLE_HOMELAB)
    return roles


def _author_label(host: str, tier: int) -> str:
    if "eia.gov" in host:
        return "U.S. EIA"
    if "energy.gov" in host:
        return "U.S. DOE / Energy Saver"
    if "pnnl.gov" in host:
        return "Pacific Northwest National Laboratory"
    if "sandia.gov" in host:
        return "Sandia National Laboratories"
    if "arxiv.org" in host or "ar5iv" in host:
        return "arXiv preprint"
    if "ledgerjournal.org" in host:
        return "Ledger"
    if "tomshardware.com" in host:
        return "Tom's Hardware"
    if "anandtech.com" in host:
        return "AnandTech"
    if "techpowerup.com" in host:
        return "TechPowerUp"
    if tier <= 2:
        return host.replace("www.", "")
    return host.replace("www.", "")


def classify_url(url: str, queries: set[str], signals: WedgeSignals) -> Candidate | None:
    if not url.startswith("http"):
        url = f"https://{url}"
    key = norm_key(url)
    if key in signals.consumed:
        return None
    host = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    qblob = _query_blob(queries)

    for rh in REJECT_HOSTS:
        if rh in host:
            return None
    if REJECT_PATH.search(path):
        return None
    if "youtube.com/shorts" in key:
        return None

    if "youtube.com" in host or "youtu.be" in host:
        slug = path.rstrip("/").split("/")[-1].replace("-", " ").title()
        return Candidate(
            url=url, key=key, author="", title=slug or "Video",
            fmt="video", tier=3, minutes=15, access="open access",
            roles={ROLE_VIDEO}, from_queries=queries,
        )

    tier = _domain_tier(host)
    path_roles = _infer_roles(path, signals)
    query_roles = _infer_roles(qblob, signals)

    if "arxiv.org" in host or "ar5iv" in host:
        roles = set(path_roles)
        roles |= query_roles & {ROLE_INFERENCE, ROLE_HW_MEASURE}
        if not roles and signals.wants_inference:
            roles.add(ROLE_INFERENCE)
    elif tier <= 2:
        roles = path_roles | query_roles
    else:
        roles = path_roles | (query_roles & path_roles)

    if tier == 1 and not roles and signals.wants_units and re.search(r"electric|energy|meter", path, re.I):
        roles.add(ROLE_UNITS)

    if not roles:
        return None
    if not _on_wedge(roles, signals):
        return None

    slug = path.rstrip("/").split("/")[-1].replace("-", " ").replace("_", " ").title() or host
    if "arxiv" in host:
        pid = re.search(r"(\d{4}\.\d{4,5})", path)
        slug = f"arXiv {pid.group(1)}" if pid else "arXiv paper"
    minutes = 45 if ROLE_INFERENCE in roles and tier == 1 else 15
    fmt = "article"

    return Candidate(
        url=url, key=key, author=_author_label(host, tier), title=slug,
        fmt=fmt, tier=tier, minutes=minutes, access="open access",
        roles=roles, from_queries=queries,
    )


def _on_wedge(roles: set[str], signals: WedgeSignals) -> bool:
    if ROLE_UNITS in roles and signals.wants_units:
        return True
    if ROLE_STORAGE in roles and signals.wants_storage:
        return True
    if ROLE_INFERENCE in roles and (signals.wants_inference or signals.wants_hardware):
        return True
    if ROLE_HW_MEASURE in roles and signals.wants_hardware:
        return True
    if ROLE_VIDEO in roles and (
        signals.wants_hardware or signals.wants_inference or signals.wants_units
    ):
        return True
    if ROLE_HOMELAB in roles and signals.wants_hardware:
        return True
    return False


def build_candidates(
    cassette: list[dict[str, Any]], signals: WedgeSignals
) -> tuple[list[Candidate], dict[str, Any]]:
    url_queries: dict[str, set[str]] = {}
    fetches: dict[str, dict[str, Any]] = {}
    youtube_attempt = False
    primary_queries: list[str] = []

    for row in cassette:
        tool = row.get("tool")
        if tool == "WebSearch":
            q = row.get("query", "")
            if q:
                primary_queries.append(q)
            if re.search(r"youtube|video|demo", q, re.I):
                youtube_attempt = True
            for u in row.get("results") or []:
                url_queries.setdefault(u, set()).add(q)
        elif tool == "WebFetch":
            key = norm_key(row.get("url", ""))
            fetches[key] = {
                "snippet_chars": int(row.get("snippet_chars") or 0),
                "author": (row.get("author") or "").strip(),
            }

    by_key: dict[str, Candidate] = {}
    for url, queries in url_queries.items():
        c = classify_url(url, queries, signals)
        if not c:
            continue
        if c.key in by_key:
            by_key[c.key].from_queries |= queries
            by_key[c.key].roles |= c.roles
        else:
            by_key[c.key] = c

    for c in by_key.values():
        if c.key in fetches:
            c.fetched = True
            c.snippet_chars = fetches[c.key]["snippet_chars"]
            logged_author = fetches[c.key]["author"]
            if logged_author:
                c.author = logged_author

    ctx = {
        "youtube_attempt": youtube_attempt,
        "youtube_fetch_count": sum(1 for k in fetches if "youtube.com" in k or "youtu.be" in k),
        "primary_queries": primary_queries,
    }
    return list(by_key.values()), ctx


def _author_identifiable(c: Candidate) -> bool:
    raw = (c.author or "").strip()
    if not raw:
        return False
    low = raw.lower()
    if low in GENERIC_AUTHORS:
        return False
    if c.tier <= 2 and not c.is_youtube:
        return True
    if c.is_youtube:
        return len(raw) >= 4
    return len(raw) >= 3


def _authority_score(c: Candidate) -> float:
    """Authority / traceability — max 1.5 (15 %)."""
    if not _author_identifiable(c):
        return 0.0
    blob = f"{c.author} {c.key}".lower()
    if c.tier <= 2:
        return 1.5
    if any(m in blob for m in INSTITUTION_MARKERS):
        return 1.5
    if c.is_youtube and c.fetched:
        return 1.2
    if c.tier == 3:
        return 0.8
    return 0.5


def _role_slot_match(c: Candidate, role: str, signals: WedgeSignals) -> float:
    """Wedge alignment — max 3.5 (35 %)."""
    primary = signals.primary_anchor_role()
    if role == "anchor":
        if primary in c.roles:
            return 3.5 if c.fetched else 3.0
        return 1.5
    if role == "video":
        return 3.5 if c.fetched else 1.5
    slot_roles = {
        "storage": ROLE_STORAGE,
        "inference": ROLE_INFERENCE,
        "hw_measure": ROLE_HW_MEASURE,
        "fallback": None,
    }
    if role in slot_roles and role != "fallback":
        if slot_roles[role] in c.roles:
            return 3.5
        return 1.5
    if role == "fallback" and c.roles:
        return 3.0
    return 1.5


def _brief_overlap(c: Candidate, signals: WedgeSignals) -> float:
    """Open question / belief — max 1.5 (15 %)."""
    blob = f"{c.title} {c.author} {c.key} {_query_blob(c.from_queries)}".lower()
    hits = sum(1 for token in re.findall(r"[a-zàâçéèêëîïôùûü]{4,}", signals.text) if token in blob)
    base = 1.2 if c.tier <= 2 else 0.6
    if c.fetched:
        base = max(base, 1.2)
    if any(m in c.author.lower() for m in INSTITUTION_MARKERS):
        base = max(base, 1.5)
    if hits >= 3:
        return 1.5
    if hits >= 1:
        return max(base, 1.4)
    return base


def rubric_score(c: Candidate, role: str, signals: WedgeSignals, picked_roles: set[str]) -> int:
    """0–10 rubric: wedge 35 % · density 25 % · authority 15 % · question 15 % · access 5 % · redundant 5 %."""
    align = _role_slot_match(c, role, signals)
    density = {1: 2.5, 2: 2.0, 3: 1.0, 4: 0.5}.get(c.tier, 0.5)
    if c.fetched and c.snippet_chars >= 5000:
        density = min(2.5, density + 0.5)
    elif c.fetched and c.snippet_chars >= 3000:
        density = min(2.5, density + 0.3)

    authority = _authority_score(c)
    question = _brief_overlap(c, signals)
    accessible = 0.5 if c.tier <= 2 or "arxiv" in c.key or ".gov" in c.key else 0.25
    redundant = 0.5 if role != "anchor" or not (c.roles & picked_roles) else 0.0

    if c.is_youtube and not c.fetched:
        return 5

    total = align + density + authority + question + accessible + redundant
    if not _author_identifiable(c):
        total = min(total, float(MAX_AUTHORITY_CAP))
    return int(min(10, max(0, total + 0.499)))


def _brief_hook(signals: WedgeSignals) -> str:
    line = signals.wedge.split("\n")[0].strip()
    return (line[:100] + "…") if len(line) > 100 else (line or "le wedge")


def _targets_for_role(role: str, signals: WedgeSignals) -> str:
    if signals.criteria:
        items = [
            re.sub(r"^-\s*\[[ x]\]\s*", "", ln.strip())
            for ln in signals.criteria.splitlines()
            if ln.strip().startswith("-")
        ]
        if items:
            if role == "anchor":
                return items[0]
            return "; ".join(items[:2])
    if signals.open_questions:
        items = [
            re.sub(r"^-\s*", "", ln.strip())
            for ln in signals.open_questions.splitlines()
            if ln.strip().startswith("-")
        ]
        if items:
            return items[0]
    return "Open questions du brief"


def _role_label(role: str) -> str:
    return {
        "anchor": "anchor écrit",
        "video": "vidéo Pool V",
        "storage": "stockage/autonomie",
        "inference": "mesure inférence/workload",
        "hw_measure": "mesure tierce hardware",
        "fallback": "complément on-wedge",
    }.get(role, role)


def _apply_copy(
    c: Candidate, role: str, signals: WedgeSignals, video_fallback: bool = False
) -> None:
    hook = _brief_hook(signals)
    c.slot = "anchor" if role == "anchor" else "core"
    prefix = "**Slot vidéo fallback** — " if video_fallback else ""
    if role == "anchor":
        c.why = f"Référence écrite dense — alignée sur le wedge : {hook}"
    elif role == "video":
        c.why = f"Vidéo technique sur le wedge (cours, conférence, démo) — {hook}"
    elif role == "storage":
        c.why = f"{prefix}Couvre stockage/autonomie liée au wedge — {hook}"
    elif role == "inference":
        c.why = f"{prefix}Mesures workload/inférence locale — {hook}"
    elif role == "hw_measure":
        c.why = (
            f"{prefix}Mesure tierce puissance hardware — peak labo, pas spec vendeur ; "
            f"{hook}"
        )
    else:
        c.why = f"{prefix}Couverture complémentaire on-wedge — {hook}"
    c.targets = _targets_for_role(role, signals)
    if c.fetched and c.snippet_chars >= 3000:
        fetch_note = "WebFetch validé"
    elif c.fetched:
        fetch_note = "snippet partiel"
    else:
        fetch_note = "snippet seul"
    auth_note = "auteur identifié" if _author_identifiable(c) else "auteur non identifiable (cap ≤6)"
    c.score_note = f"Tier {c.tier}, {_role_label(role)}, {fetch_note}, {auth_note}."


def _rank(c: Candidate) -> tuple:
    return (-c.score, -int(c.fetched), -c.snippet_chars, -int(c.tier == 1), -c.tier, c.key)


def _anchor_rank(c: Candidate, signals: WedgeSignals) -> tuple:
    primary = signals.primary_anchor_role()
    focused = int(primary in c.roles and ROLE_STORAGE not in c.roles) if primary == ROLE_UNITS else int(
        primary in c.roles and len(c.roles) == 1
    )
    return (-c.score, -focused, -int(c.fetched), -c.snippet_chars, -int(c.tier == 1), c.key)


def _anchor_pool(candidates: list[Candidate], signals: WedgeSignals) -> list[Candidate]:
    primary = signals.primary_anchor_role()
    pool = [
        c for c in candidates
        if primary in c.roles and not c.is_youtube
    ]
    if signals.wants_units:
        pool = [c for c in pool if "arxiv" not in c.key]
    if not pool:
        pool = [
            c for c in candidates
            if not c.is_youtube and c.roles and "arxiv" not in c.key
        ]
    return pool


def _score_role(c: Candidate, signals: WedgeSignals, picked_roles: set[str]) -> str:
    if ROLE_INFERENCE in c.roles:
        return "inference"
    if ROLE_HW_MEASURE in c.roles:
        return "hw_measure"
    if ROLE_STORAGE in c.roles:
        return "storage"
    return "fallback"


def pick_three(
    candidates: list[Candidate], ctx: dict[str, Any], signals: WedgeSignals
) -> tuple[Candidate, Candidate, Candidate, list[str]]:
    skipped: list[str] = []
    picked_roles: set[str] = set()

    anchor_pool = _anchor_pool(candidates, signals)
    if not anchor_pool:
        raise SystemExit("engine: no anchor pool in cassette")

    for c in anchor_pool:
        c.score = rubric_score(c, "anchor", signals, picked_roles)
    anchor_pool.sort(key=lambda c: _anchor_rank(c, signals))
    anchor = anchor_pool[0]
    if anchor.score < MIN_SCORE:
        raise SystemExit(f"engine: best anchor scores {anchor.score}/10 < {MIN_SCORE}")
    _apply_copy(anchor, "anchor", signals)
    picked_roles |= anchor.roles

    youtube_strong = ctx["youtube_fetch_count"] > 0
    video_candidates = [c for c in candidates if c.is_youtube]
    core_a: Candidate | None = None

    if youtube_strong:
        for c in video_candidates:
            c.score = rubric_score(c, "video", signals, picked_roles)
        video_candidates.sort(key=_rank)
        if video_candidates and video_candidates[0].score >= MIN_SCORE:
            core_a = video_candidates[0]
            _apply_copy(core_a, "video", signals)
            picked_roles |= core_a.roles

    if core_a is None:
        video_fallback = ctx["youtube_attempt"] or True
        storage_pool = [c for c in candidates if ROLE_STORAGE in c.roles and c.key != anchor.key]
        inference_pool = [c for c in candidates if ROLE_INFERENCE in c.roles and c.key != anchor.key]
        hw_pool = [
            c for c in candidates
            if ROLE_HW_MEASURE in c.roles and c.fetched and c.key != anchor.key
        ]

        if signals.wants_storage and storage_pool and ctx["youtube_attempt"]:
            for c in storage_pool:
                c.score = rubric_score(c, "storage", signals, picked_roles)
            storage_pool.sort(key=_rank)
            if storage_pool[0].score >= MIN_SCORE:
                core_a = storage_pool[0]
                _apply_copy(core_a, "storage", signals, video_fallback=True)

        if core_a is None and inference_pool and not ctx["youtube_attempt"]:
            for c in inference_pool:
                c.score = rubric_score(c, "inference", signals, picked_roles)
            inference_pool.sort(key=_rank)
            if inference_pool[0].score >= MIN_SCORE:
                core_a = inference_pool[0]
                _apply_copy(core_a, "inference", signals, video_fallback=True)

        if core_a is None and storage_pool:
            for c in storage_pool:
                c.score = rubric_score(c, "storage", signals, picked_roles)
            storage_pool.sort(key=_rank)
            if storage_pool[0].score >= MIN_SCORE:
                core_a = storage_pool[0]
                _apply_copy(core_a, "storage", signals, video_fallback=True)

        if core_a is None and inference_pool:
            for c in inference_pool:
                c.score = rubric_score(c, "inference", signals, picked_roles)
            inference_pool.sort(key=_rank)
            if inference_pool[0].score >= MIN_SCORE:
                core_a = inference_pool[0]
                _apply_copy(core_a, "inference", signals, video_fallback=True)

        if core_a is None:
            raise SystemExit("engine: video fallback pool exhausted")

    picked_roles |= core_a.roles
    used = {anchor.key, core_a.key}

    remainder = [c for c in candidates if c.key not in used and not c.is_youtube]
    for c in remainder:
        slot_role = _score_role(c, signals, picked_roles)
        c.score = rubric_score(c, slot_role, signals, picked_roles)

    def _joker_rank(c: Candidate) -> tuple:
        boost = 0
        if signals.wants_hardware or signals.wants_inference:
            if ROLE_INFERENCE in c.roles:
                boost = 2
            elif ROLE_HW_MEASURE in c.roles:
                boost = 1
        return (-c.score, -boost, -int(c.fetched), -c.snippet_chars, c.key)

    remainder.sort(key=_joker_rank)
    core_b: Candidate | None = None
    for c in remainder:
        if c.score >= MIN_SCORE:
            core_b = c
            slot_role = _score_role(c, signals, picked_roles)
            _apply_copy(c, slot_role, signals)
            break

    if core_b is None:
        raise SystemExit("engine: no joker candidate >= 9/10 in remainder pool")

    if ctx["youtube_attempt"] and not youtube_strong:
        skipped.append("*YouTube pool* — timeboxé, aucun WebFetch retenu → fallback article.")
    for c in video_candidates:
        if c.key not in used and c.key != core_a.key:
            if not _author_identifiable(c) or c.score <= MAX_AUTHORITY_CAP:
                skipped.append(f"*{c.title}* — auteur/chaîne non identifiable (autorité ≤{MAX_AUTHORITY_CAP}/10).")
            else:
                skipped.append(f"*{c.title}* — rejet pool V (faible densité / hors barème).")
    for c in candidates:
        if ROLE_HOMELAB in c.roles and c.key not in used:
            skipped.append(f"*{c.title}* — Tier 3 homelab blog, swap vers Tier 1–2.")
        if c.tier >= 3 and c.key not in used and c.key not in {core_b.key}:
            if len(skipped) < 3:
                skipped.append(f"*{c.title}* — Tier 3, remplacé par source plus dense.")

    if not skipped:
        skipped.append("*Sources adjacentes* — hors wedge, rejetées en pool.")

    return anchor, core_a, core_b, skipped[:3]


def format_source(c: Candidate) -> str:
    return (
        f"- [ ] **{c.author}** — *{c.title}* — {c.url}\n"
        f"  - Format: {c.fmt}\n"
        f"  - Tier: {c.tier} · ~{c.minutes} min · {c.access}\n"
        f"  - Why: {c.why}\n"
        f"  - Targets: {c.targets}\n"
        f"  - Score: {c.score}/10 — {c.score_note}"
    )


def render_section(
    anchor: Candidate, core_a: Candidate, core_b: Candidate, skipped: list[str],
    signals: WedgeSignals | None = None,
) -> str:
    today = date.today().isoformat()
    roles = anchor.roles | core_a.roles | core_b.roles
    parts: list[str] = []
    if signals:
        if ROLE_UNITS in roles and signals.wants_units:
            parts.append("unités")
        if ROLE_STORAGE in roles and signals.wants_storage:
            parts.append("autonomie kW/kWh")
        if ROLE_INFERENCE in roles or ROLE_HW_MEASURE in roles:
            if signals.wants_inference or signals.wants_hardware:
                parts.append("conso hardware/inférence")
        if ROLE_VIDEO in roles:
            parts.append("angle vidéo")
    set_note = (
        f"Wedge couvert : {', '.join(parts) or '3 slots on-wedge'} ; "
        "fallback vidéo documenté si utilisé."
    )

    lines = [
        "## Source material", "",
        f"Scouted {today} via `/source-scout` :", "",
        "### Read first (anchor)", format_source(anchor), "",
        "### Core", format_source(core_a), format_source(core_b), "",
        "### Skipped (wedge boundary)",
    ]
    lines.extend(f"- {s}" for s in skipped)
    lines += ["", "### Scout scores", f"- Set: {MIN_SCORE}/10 — {set_note}", ""]
    return "\n".join(lines)


def merge_brief(brief_path: Path, section: str, out_path: Path) -> None:
    text = brief_path.read_text()
    if "## Source material" in text:
        text = re.sub(r"## Source material.*?(?=\n## |\Z)", section.rstrip() + "\n\n", text, count=1, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + section
    out_path.write_text(text)


def wedge_coverage(
    anchor: Candidate, core_a: Candidate, core_b: Candidate, signals: WedgeSignals
) -> dict[str, bool]:
    all_roles = anchor.roles | core_a.roles | core_b.roles
    return {
        "units": not signals.wants_units or ROLE_UNITS in all_roles,
        "storage_or_autonomy": not signals.wants_storage or ROLE_STORAGE in all_roles,
        "hardware_or_inference": (
            not (signals.wants_hardware or signals.wants_inference)
            or ROLE_INFERENCE in all_roles
            or ROLE_HW_MEASURE in all_roles
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="source-scout engine")
    ap.add_argument("--brief", required=True, type=Path)
    ap.add_argument("--cassette", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--json", type=Path, help="manifest with roles + coverage")
    args = ap.parse_args()

    signals = parse_brief(args.brief)
    cassette = load_cassette(args.cassette)
    candidates, ctx = build_candidates(cassette, signals)
    anchor, core_a, core_b, skipped = pick_three(candidates, ctx, signals)

    merge_brief(args.brief, render_section(anchor, core_a, core_b, skipped, signals), args.out)

    if args.json:
        cov = wedge_coverage(anchor, core_a, core_b, signals)
        manifest = {
            "anchor": anchor.url,
            "anchor_roles": sorted(anchor.roles),
            "core": [core_a.url, core_b.url],
            "core_roles": [sorted(core_a.roles), sorted(core_b.roles)],
            "scores": {anchor.url: anchor.score, core_a.url: core_a.score, core_b.url: core_b.score},
            "wedge_coverage": cov,
            "primary_queries": ctx["primary_queries"],
            "youtube_attempt": ctx["youtube_attempt"],
            "video_fallback": core_a.fmt != "video",
            "pool_size": len(candidates),
        }
        args.json.write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"engine: OK — pool={len(candidates)} anchor={anchor.key} core={core_a.key}+{core_b.key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())