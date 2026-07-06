#!/usr/bin/env python3
"""Validate mind-map.json schema and limits."""
import json
import re
import sys
from pathlib import Path

MAX_NODES = 80
MAX_DEPTH = 5
MAX_LABEL = 80
MAX_SUMMARY = 200
MAX_NOTE = 600
MIN_IMPORTANCE = 1
MAX_IMPORTANCE = 5
VALID_TYPES = {"concept", "detail", "example", "source"}
VALID_LAYOUTS = {"auto", "tree", "centered"}
# Mirror of compose-html.py — custom preset token contract
TOKEN_NAMES = {"bg", "surface", "text", "muted", "border", "accent",
               "accent-light", "secondary", "success", "warning", "radius"}
SAFE_TOKEN_VALUE = re.compile(r"^[#a-zA-Z0-9 .,%()-]+$")


def count_nodes(node, depth=0):
    if depth > MAX_DEPTH:
        raise ValueError(f"depth exceeds {MAX_DEPTH} at id={node.get('id')}")
    n = 1
    for c in node.get("children") or []:
        n += count_nodes(c, depth + 1)
    return n


def validate(path: Path) -> int:
    data = json.loads(path.read_text())
    if "meta" not in data or "root" not in data:
        raise ValueError("missing meta or root")
    if "layout" in data and data["layout"] not in VALID_LAYOUTS:
        raise ValueError("layout must be auto, tree, or centered")
    if data["meta"].get("preset") == "custom":
        tokens = data["meta"].get("customTokens")
        if not isinstance(tokens, dict) or not tokens:
            raise ValueError("preset custom requires meta.customTokens (non-empty object)")
        for key, value in tokens.items():
            if key not in TOKEN_NAMES:
                raise ValueError(f"unknown custom token: {key} (allowed: {sorted(TOKEN_NAMES)})")
            if not isinstance(value, str) or not SAFE_TOKEN_VALUE.match(value.strip()):
                raise ValueError(f"unsafe custom token value for {key}")
    root = data["root"]
    if root.get("type") != "concept":
        raise ValueError("root.type must be concept")
    seen = set()

    def walk(node, depth=0):
        if depth > MAX_DEPTH:
            raise ValueError(f"depth > {MAX_DEPTH}: {node.get('id')}")
        nid = node.get("id")
        if not nid:
            raise ValueError("node missing id")
        if nid in seen:
            raise ValueError(f"duplicate id: {nid}")
        seen.add(nid)
        if not node.get("label"):
            raise ValueError(f"empty label: {nid}")
        if len(node["label"]) > MAX_LABEL:
            raise ValueError(f"label exceeds {MAX_LABEL} chars on {nid}")
        t = node.get("type")
        if t not in VALID_TYPES:
            raise ValueError(f"invalid type {t} on {nid}")
        if t == "source" and node.get("href") and not str(node["href"]).startswith("http"):
            raise ValueError(f"invalid href on {nid}")
        if "summary" in node:
            s = node["summary"]
            if not isinstance(s, str) or not s.strip():
                raise ValueError(f"summary must be non-empty string on {nid}")
            if len(s) > MAX_SUMMARY:
                raise ValueError(f"summary exceeds {MAX_SUMMARY} chars on {nid}")
        if "note" in node:
            note = node["note"]
            if not isinstance(note, str) or not note.strip():
                raise ValueError(f"note must be non-empty string on {nid}")
            if len(note) > MAX_NOTE:
                raise ValueError(f"note exceeds {MAX_NOTE} chars on {nid}")
        if "importance" in node:
            importance = node["importance"]
            if isinstance(importance, bool) or not isinstance(importance, int):
                raise ValueError(f"importance must be integer 1-5 on {nid}")
            if importance < MIN_IMPORTANCE or importance > MAX_IMPORTANCE:
                raise ValueError(f"importance must be integer 1-5 on {nid}")
        for c in node.get("children") or []:
            walk(c, depth + 1)

    walk(root)
    total = count_nodes(root)
    if total > MAX_NODES:
        raise ValueError(f"node count {total} exceeds {MAX_NODES}")
    declared = data["meta"].get("nodeCount")
    if declared is not None and declared != total:
        print(f"warn: meta.nodeCount={declared} but actual={total}", file=sys.stderr)
    print(f"ok: {total} nodes, depth ok, ids unique")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: validate-map.py <mind-map.json>", file=sys.stderr)
        sys.exit(2)
    try:
        sys.exit(validate(Path(sys.argv[1])))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
