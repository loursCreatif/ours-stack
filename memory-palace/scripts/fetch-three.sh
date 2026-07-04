#!/usr/bin/env bash
# Fetch pinned Three.js IIFE build for memory-palace HTML inlining.
set -euo pipefail

# 0.160.0 is the last release shipping build/three.min.js (IIFE) on npm CDNs.
VERSION="${THREE_VERSION:-0.160.0}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENDOR_DIR="$SCRIPT_DIR/../references/vendor"
OUT="$VENDOR_DIR/three.min.js"
URL="https://cdn.jsdelivr.net/npm/three@${VERSION}/build/three.min.js"

mkdir -p "$VENDOR_DIR"

if [ -f "$OUT" ]; then
  echo "three.min.js already present ($OUT)"
  exit 0
fi

echo "Fetching Three.js ${VERSION}..."
curl -fsSL "$URL" -o "$OUT"
echo "Saved to $OUT ($(wc -c < "$OUT" | tr -d ' ') bytes)"