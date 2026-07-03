#!/usr/bin/env python3
"""Source-scout engine: cassette → wedge-token pools → rubric score → pick 3 → brief.

Domain-agnostic: wedge alignment comes from token overlap between the brief and
each candidate (title + URL path + originating queries + author), with a 5-char
stem match so French briefs align with English queries (énergie/energy,
décentralisation/decentralization). No study-specific keyword lists.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

MIN_SCORE = 9
MAX_AUTHORITY_CAP = 6  # hard cap when author/channel not identifiable
STEM_LEN = 5

GENERIC_AUTHORS = frozenset({
    "youtube", "unknown", "anonymous", "n/a", "none", "channel", "creator", "user",
})
INSTITUTION_MARKERS = (
    ".edu", ".gov", "university", "laboratory", "laboratories", "institute",
    "ieee", "acm", "conference", "prof.", "professor", "dr.", "phd", "arxiv",
    "department", "college", "school of",
)

# Quality rejects (see references/source-tiers.md): social/UGC aggregators,
# SEO farms, vendor spec pages, generalist finance/wiki primers.
REJECT_HOSTS = (
    "howtogeek.com", "buzzfeed.com", "medium.com/@", "linkedin.com",
    "facebook.com", "threads.com", "reddit.com", "wikipedia.org",
    "investopedia.com", "nvidia.com",
)
REJECT_PATH = re.compile(
    r"top[-_]?\d+|introduction[-_]to|what[-_]is|best[-_]resources|/specs?/|/learn/", re.I
)

TIER1_HOST_MARKERS = (".gov", "arxiv.org", "doi.org", "ieee.org")
TIER2_HOST_MARKERS = ("tomshardware.com", "anandtech.com", "techpowerup.com", "igorslab.de")

STOPWORDS = frozenset({
    # fr
    "les", "des", "une", "aux", "est", "sont", "que", "qui", "quoi", "pas",
    "plus", "pour", "dans", "avec", "sur", "par", "pas", "mais", "donc",
    "avant", "toute", "tout", "tous", "cette", "ces", "son", "ses", "leur",
    "peux", "peut", "sans", "entre", "comme", "quel", "quelle", "quels",
    "quelles", "mon", "moi", "vers", "chez", "ont", "fait", "faire", "être",
    "etre", "avoir", "aussi", "bien", "premier", "seul", "seule",
    # en
    "the", "and", "for", "with", "from", "that", "this", "these", "those",
    "are", "was", "were", "will", "what", "when", "which", "how", "why",
    "not", "but", "all", "any", "can", "into", "over", "under", "about",
    "than", "then", "them", "they", "their", "your", "you", "our", "out",
    "site", "http", "https", "www", "com", "org", "html", "pdf",
})

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})")


def _fold(text: str) -> str:
    """Lowercase + strip diacritics so French/English stems can match."""
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def _tokens(text: str) -> set[str]:
    out: set[str] = set()
    for t in re.findall(r"[a-z0-9]{3,}", _fold(text)):
        if t in STOPWORDS:
            continue
        if t.isdigit() and len(t) != 4:
            continue  # keep years, drop other bare numbers
        out.add(t)
    return out


def _stems(tokens: set[str]) -> set[str]:
    return {t[:STEM_LEN] for t in tokens}


@dataclass
class WedgeSignals:
    wedge: str
    criteria: str
    open_questions: str
    beliefs: str
    text: str
    stems: set[str] = field(default_factory=set)
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
        blob = "\n".join((wedge, criteria, open_questions, beliefs))
        return cls(
            wedge=wedge.strip(),
            criteria=criteria.strip(),
            open_questions=open_questions.strip(),
            beliefs=beliefs.strip(),
            text=blob,
            stems=_stems(_tokens(blob)),
            consumed=consumed or set(),
        )


@dataclass
class Candidate:
    url: str
    key: str
    author: str
    title: str
    fmt: str
    tier: int
    access: str
    fetched: bool = False
    snippet_chars: int = 0
    from_queries: set[str] = field(default_factory=set)
    co_query: bool = False  # found by a query whose other hit the agent fetched
    wedge_hits: int = 0
    score: int = 0
    score_note: str = ""
    why: str = ""
    targets: str = ""
    slot: str = ""

    @property
    def is_youtube(self) -> bool:
        return self.fmt == "video"

    @property
    def minutes(self) -> int:
        if self.is_youtube:
            return 15
        if self.tier <= 2 or self.snippet_chars >= 8000:
            return 45
        return 15


def norm_key(url: str) -> str:
    raw = url if url.startswith("http") else f"https://{url}"
    p = urlparse(raw)
    host = p.netloc.lower().removeprefix("www.")
    path = p.path.rstrip("/")
    if "youtube.com" in host and path == "/watch":
        vid = parse_qs(p.query).get("v", [""])[0]
        if vid:
            return f"youtube.com/watch/{vid.lower()}"
    if host == "youtu.be" and path:
        return f"youtu.be/{path.lstrip('/').lower()}"
    if "arxiv.org" in host or "ar5iv" in host:
        pid = ARXIV_ID_RE.search(path)
        if pid:
            return f"arxiv/{pid.group(1)}"
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


def _domain_tier(host: str) -> int:
    if any(m in host for m in TIER1_HOST_MARKERS):
        return 1
    if any(m in host for m in TIER2_HOST_MARKERS):
        return 2
    if host.endswith(".edu"):
        return 2
    return 3


def _search_hits(row: dict[str, Any]) -> list[tuple[str, str]]:
    """Accept both cassette shapes: results:[url] and hits:[{url,title}]."""
    out: list[tuple[str, str]] = []
    for u in row.get("results") or []:
        out.append((u, ""))
    for h in row.get("hits") or []:
        url = h.get("url", "")
        title = h.get("title", "")
        if title == url or title.startswith("http"):
            title = ""
        if url:
            out.append((url, title))
    return out


def classify_url(url: str, title: str, queries: set[str]) -> Candidate | None:
    if not url.startswith("http"):
        url = f"https://{url}"
    key = norm_key(url)
    host = urlparse(url).netloc.lower()
    path = unquote(urlparse(url).path)

    for rh in REJECT_HOSTS:
        if rh in host:
            return None
    if REJECT_PATH.search(path.lower()):
        return None
    if "youtube.com/shorts" in key:
        return None

    if "youtube.com" in host or "youtu.be" in host:
        vid = key.rsplit("/", 1)[-1]
        return Candidate(
            url=url, key=key, author="", title=title or f"YouTube {vid}",
            fmt="video", tier=3, access="open access", from_queries=queries,
        )

    tier = _domain_tier(host)
    slug = path.rstrip("/").split("/")[-1]
    slug = re.sub(r"\.(html?|pdf|php)$", "", slug, flags=re.I)
    slug = slug.replace("-", " ").replace("_", " ").strip().title() or host.removeprefix("www.")
    if key.startswith("arxiv/"):
        slug = f"arXiv {key.removeprefix('arxiv/')}"
    return Candidate(
        url=url, key=key, author=host.removeprefix("www."), title=title or slug,
        fmt="article", tier=tier, access="open access", from_queries=queries,
    )


def _candidate_blob(c: Candidate) -> str:
    return " ".join((c.title, unquote(urlparse(c.url).path), c.url, c.author, *c.from_queries))


def build_candidates(
    cassette: list[dict[str, Any]], signals: WedgeSignals
) -> tuple[list[Candidate], dict[str, Any]]:
    url_queries: dict[str, set[str]] = {}
    url_titles: dict[str, str] = {}
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
            if (row.get("provider_status") or "ok") != "ok":
                continue
            for u, title in _search_hits(row):
                url_queries.setdefault(u, set()).add(q)
                if title:
                    url_titles.setdefault(u, title)
        elif tool == "WebFetch":
            if (row.get("status") or "ok") != "ok":
                continue
            url = row.get("url", "")
            fetches[norm_key(url)] = {
                "url": url,
                "snippet_chars": int(row.get("snippet_chars") or 0),
                "author": (row.get("author") or "").strip(),
            }

    by_key: dict[str, Candidate] = {}
    for url, queries in url_queries.items():
        c = classify_url(url, url_titles.get(url, ""), queries)
        if not c or c.key in signals.consumed:
            continue
        if c.key in by_key:
            by_key[c.key].from_queries |= queries
        else:
            by_key[c.key] = c

    # A fetched URL is a candidate even if no logged search returned it.
    for key, info in fetches.items():
        if key in by_key or key in signals.consumed:
            continue
        c = classify_url(info["url"], "", set())
        if c:
            by_key[c.key] = c

    for c in by_key.values():
        if c.key in fetches:
            c.fetched = True
            c.snippet_chars = fetches[c.key]["snippet_chars"]
            if fetches[c.key]["author"]:
                c.author = fetches[c.key]["author"]

    queries_with_fetch = {
        q for c in by_key.values() if c.fetched for q in c.from_queries
    }
    for c in by_key.values():
        c.wedge_hits = len(_stems(_tokens(_candidate_blob(c))) & signals.stems)
        c.co_query = bool(c.from_queries & queries_with_fetch)

    # On-wedge filter: fetched (agent screened it), token overlap with the
    # brief, or sibling of a query the agent judged good enough to fetch from.
    pool = [c for c in by_key.values() if c.fetched or c.wedge_hits >= 1 or c.co_query]

    ctx = {
        "youtube_attempt": youtube_attempt,
        "youtube_fetch_count": sum(
            1 for k in fetches if "youtube.com" in k or "youtu.be" in k
        ),
        "primary_queries": primary_queries,
    }
    return pool, ctx


def _author_identifiable(c: Candidate) -> bool:
    raw = (c.author or "").strip()
    if not raw:
        return False
    if raw.lower() in GENERIC_AUTHORS:
        return False
    if c.is_youtube:
        return len(raw) >= 4
    return len(raw) >= 3


def _is_institutional(c: Candidate) -> bool:
    blob = f"{c.author} {c.key}".lower()
    return any(m in blob for m in INSTITUTION_MARKERS)


def _authority_score(c: Candidate) -> float:
    """Authority / traceability — max 1.5 (15 %)."""
    if not _author_identifiable(c):
        return 0.0
    if not c.is_youtube and c.tier <= 2:
        return 1.5
    if _is_institutional(c):
        return 1.5
    if c.is_youtube and c.fetched:
        return 1.3
    if c.fetched:
        return 1.0
    return 0.8


def _alignment_score(c: Candidate) -> float:
    """Wedge alignment — max 3.5 (35 %)."""
    if c.fetched:
        return 3.5
    if c.wedge_hits >= 2 or c.co_query:
        return 3.2
    if c.wedge_hits >= 1:
        return 3.0
    return 1.5


def _density_score(c: Candidate) -> float:
    """Density — max 2.5 (25 %). A fetched video is a screened demo/talk."""
    if c.is_youtube:
        return 1.5 if c.fetched else 1.0
    base = {1: 2.5, 2: 2.0}.get(c.tier, 1.0)
    if c.fetched:
        if c.snippet_chars >= 10000:
            base += 1.0
        elif c.snippet_chars >= 5000:
            base += 0.5
        elif c.snippet_chars >= 3000:
            base += 0.3
    return min(2.5, base)


def _question_score(c: Candidate) -> float:
    """Open question / belief — max 1.5 (15 %)."""
    if c.wedge_hits >= 3:
        return 1.5
    if c.wedge_hits >= 1:
        return 1.4
    if c.fetched or c.tier <= 2:
        return 1.2
    return 0.8


def rubric_score(c: Candidate, picked_hosts: set[str]) -> int:
    """0–10 rubric: wedge 35 % · density 25 % · authority 15 % · question 15 % · access 5 % · redundant 5 %."""
    if c.is_youtube and not c.fetched:
        return 5  # never eligible: SKILL requires WebFetch on every Pool V survivor

    host = urlparse(c.url).netloc.lower().removeprefix("www.")
    accessible = 0.5 if c.tier <= 2 else 0.4
    redundant = 0.0 if host in picked_hosts else 0.5

    total = (
        _alignment_score(c)
        + _density_score(c)
        + _authority_score(c)
        + _question_score(c)
        + accessible
        + redundant
    )
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
        "fallback": "fallback slot vidéo",
        "joker": "joker on-wedge",
    }.get(role, role)


def _apply_copy(c: Candidate, role: str, signals: WedgeSignals) -> None:
    hook = _brief_hook(signals)
    c.slot = "anchor" if role == "anchor" else "core"
    if role == "anchor":
        c.why = f"Référence écrite dense — alignée sur le wedge : {hook}"
    elif role == "video":
        c.why = f"Vidéo technique sur le wedge (cours, conférence, démo) — {hook}"
    elif role == "fallback":
        c.why = f"**Slot vidéo fallback** — meilleure source écrite disponible sur le wedge — {hook}"
    else:
        c.why = f"Couverture complémentaire on-wedge — {hook}"
    c.targets = _targets_for_role(role, signals)
    if c.fetched and c.snippet_chars >= 3000:
        fetch_note = "WebFetch validé"
    elif c.fetched:
        fetch_note = "WebFetch (snippet court)"
    else:
        fetch_note = "snippet seul"
    auth_note = "auteur identifié" if _author_identifiable(c) else f"auteur non identifiable (cap ≤{MAX_AUTHORITY_CAP})"
    c.score_note = f"Tier {c.tier}, {_role_label(role)}, {fetch_note}, {auth_note}."


def _rank(c: Candidate) -> tuple:
    return (
        -c.score, -int(c.fetched), -c.snippet_chars, -c.wedge_hits,
        -int(c.tier == 1), -c.tier, c.key,
    )


def _picked_hosts(picks: list[Candidate]) -> set[str]:
    return {urlparse(c.url).netloc.lower().removeprefix("www.") for c in picks}


def pick_three(
    candidates: list[Candidate], ctx: dict[str, Any], signals: WedgeSignals
) -> tuple[Candidate, Candidate, Candidate, list[str]]:
    written = [c for c in candidates if not c.is_youtube]
    videos = [c for c in candidates if c.is_youtube]

    # Anchor: best fetched written source (SKILL: anchor is WebFetch-validated).
    anchor_pool = [c for c in written if c.fetched]
    if not anchor_pool:
        raise SystemExit(
            "engine: no fetched written candidate — WebFetch the anchor before running"
        )
    for c in anchor_pool:
        c.score = rubric_score(c, set())
    anchor_pool.sort(key=_rank)
    anchor = anchor_pool[0]
    if anchor.score < MIN_SCORE:
        raise SystemExit(f"engine: best anchor scores {anchor.score}/10 < {MIN_SCORE}")
    _apply_copy(anchor, "anchor", signals)
    picks = [anchor]

    # Slot 2: best fetched video >= MIN_SCORE, else best written fallback.
    core_a: Candidate | None = None
    for c in videos:
        c.score = rubric_score(c, _picked_hosts(picks))
    fetched_videos = sorted((c for c in videos if c.fetched), key=_rank)
    if fetched_videos and fetched_videos[0].score >= MIN_SCORE:
        core_a = fetched_videos[0]
        _apply_copy(core_a, "video", signals)
    if core_a is None:
        fallback_pool = [c for c in written if c.key != anchor.key]
        for c in fallback_pool:
            c.score = rubric_score(c, _picked_hosts(picks))
        fallback_pool.sort(key=_rank)
        if not fallback_pool or fallback_pool[0].score < MIN_SCORE:
            raise SystemExit("engine: video fallback pool exhausted (no written source >= 9/10)")
        core_a = fallback_pool[0]
        _apply_copy(core_a, "fallback", signals)
    picks.append(core_a)

    # Joker: best remaining written source or second fetched video.
    used = {c.key for c in picks}
    remainder = [
        c for c in candidates
        if c.key not in used and (not c.is_youtube or c.fetched)
    ]
    for c in remainder:
        c.score = rubric_score(c, _picked_hosts(picks))
    remainder.sort(key=_rank)
    core_b = next((c for c in remainder if c.score >= MIN_SCORE), None)
    if core_b is None:
        raise SystemExit(f"engine: no joker candidate >= {MIN_SCORE}/10 in remainder pool")
    _apply_copy(core_b, "joker", signals)
    picks.append(core_b)

    skipped = _skipped_lines(candidates, picks, ctx)
    return anchor, core_a, core_b, skipped


def _skipped_lines(
    candidates: list[Candidate], picks: list[Candidate], ctx: dict[str, Any]
) -> list[str]:
    used = {c.key for c in picks}
    skipped: list[str] = []

    unfetched_videos = [c for c in candidates if c.is_youtube and not c.fetched and c.key not in used]
    if unfetched_videos:
        names = ", ".join(c.title for c in unfetched_videos[:2])
        more = f" (+{len(unfetched_videos) - 2})" if len(unfetched_videos) > 2 else ""
        skipped.append(f"*{names}{more}* — Pool V non fetchées (timebox) — non éligibles.")

    for c in (c for c in candidates if c.is_youtube and c.fetched and c.key not in used):
        if not _author_identifiable(c):
            skipped.append(
                f"*{c.title}* — chaîne/auteur non identifiable (autorité ≤{MAX_AUTHORITY_CAP}/10)."
            )
        else:
            skipped.append(f"*{c.title}* — vidéo fetchée {c.score}/10 < {MIN_SCORE} → slot vidéo en fallback.")

    if ctx["youtube_attempt"] and not any(c.is_youtube for c in candidates):
        skipped.append("*Pool V* — recherche vidéo tentée, aucun candidat exploitable → fallback article.")

    for c in sorted(
        (c for c in candidates if not c.is_youtube and c.key not in used), key=_rank
    ):
        if len(skipped) >= 3:
            break
        reason = (
            f"score {c.score}/10 < {MIN_SCORE}, hors set final"
            if 0 < c.score < MIN_SCORE
            else "battu au rang par une source plus dense"
        )
        skipped.append(f"*{c.title}* — {reason}.")

    if not skipped:
        skipped.append("*Sources adjacentes* — hors wedge, rejetées en pool.")
    return skipped[:3]


def format_source(c: Candidate) -> str:
    author = c.author or "?"
    return (
        f"- [ ] **{author}** — *{c.title}* — {c.url}\n"
        f"  - Format: {c.fmt}\n"
        f"  - Tier: {c.tier} · ~{c.minutes} min · {c.access}\n"
        f"  - Why: {c.why}\n"
        f"  - Targets: {c.targets}\n"
        f"  - Score: {c.score}/10 — {c.score_note}"
    )


def render_section(
    anchor: Candidate, core_a: Candidate, core_b: Candidate, skipped: list[str],
    video_fallback: bool,
) -> str:
    today = date.today().isoformat()
    formats = " + ".join(c.fmt for c in (anchor, core_a, core_b))
    fallback_note = (
        "slot vidéo en fallback article (aucune vidéo ≥9/10)"
        if video_fallback
        else "slot vidéo servi par une vidéo fetchée"
    )
    set_note = f"3 slots on-wedge ({formats}) ; {fallback_note}."

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


def main() -> int:
    ap = argparse.ArgumentParser(description="source-scout engine")
    ap.add_argument("--brief", required=True, type=Path)
    ap.add_argument("--cassette", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--json", type=Path, help="manifest with picks + coverage")
    args = ap.parse_args()

    signals = parse_brief(args.brief)
    cassette = load_cassette(args.cassette)
    candidates, ctx = build_candidates(cassette, signals)
    anchor, core_a, core_b, skipped = pick_three(candidates, ctx, signals)
    video_fallback = core_a.fmt != "video"

    merge_brief(
        args.brief,
        render_section(anchor, core_a, core_b, skipped, video_fallback),
        args.out,
    )

    if args.json:
        picks = [anchor, core_a, core_b]
        manifest = {
            "anchor": anchor.url,
            "core": [core_a.url, core_b.url],
            "formats": [c.fmt for c in picks],
            "scores": {c.url: c.score for c in picks},
            "wedge_coverage": {
                "on_wedge_picks": all(c.fetched or c.wedge_hits >= 1 for c in picks),
                "wedge_hits": {c.url: c.wedge_hits for c in picks},
            },
            "primary_queries": ctx["primary_queries"],
            "youtube_attempt": ctx["youtube_attempt"],
            "video_fallback": video_fallback,
            "pool_size": len(candidates),
        }
        args.json.write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"engine: OK — pool={len(candidates)} anchor={anchor.key} core={core_a.key}+{core_b.key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
