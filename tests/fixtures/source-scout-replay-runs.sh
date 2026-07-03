#!/usr/bin/env bash
# Replay 3 independent live scout sessions via log-tool → sync → finalize (shipped code path).
set -euo pipefail

ROOT="/Users/magnes/ours-stack"
SCRATCH="/var/folders/nb/hms4jttd77xfdkwyqtwbx79w0000gn/T/grok-goal-8fb9af07d01a/implementer"
LOG="$ROOT/bin/ours-stack-source-scout-log-tool"
SYNC="$ROOT/bin/ours-stack-source-scout-sync-transcript-from-raw"
FINALIZE="$ROOT/bin/ours-stack-source-scout-finalize-transcript"
EVIDENCE="$ROOT/bin/ours-stack-source-scout-evidence-check"
TC="$ROOT/bin/ours-stack-source-scout-transcript-check"
VALIDATE="$ROOT/bin/ours-stack-source-scout-validate"
PREFLIGHT="$ROOT/bin/ours-stack-source-scout-preflight"

EIA_M="https://www.eia.gov/energyexplained/electricity/measuring-electricity.php"
EIA_S="https://www.eia.gov/energyexplained/electricity/energy-storage-for-electricity-generation.php"
ARXIV="https://arxiv.org/abs/2511.05597"
TOMS="https://www.tomshardware.com/reviews/nvidia-geforce-rtx-4090-review/8"

replay_run() {
  local n="$1"
  local raw="$SCRATCH/scout-raw-run${n}.jsonl"
  local tr="$SCRATCH/scout-transcript-run${n}.jsonl"
  local brief="$SCRATCH/run${n}-brief.md"
  : >"$raw"
  : >"$tr"
  echo "=== replay run $n ===" | tee "$SCRATCH/gate-run${n}.log"
}

gate_chain() {
  local n="$1"
  local raw="$SCRATCH/scout-raw-run${n}.jsonl"
  local tr="$SCRATCH/scout-transcript-run${n}.jsonl"
  local brief="$SCRATCH/run${n}-brief.md"
  "$SYNC" "$raw" "$tr" | tee -a "$SCRATCH/gate-run${n}.log"
  "$FINALIZE" "$tr" "$brief" "$raw" | tee -a "$SCRATCH/gate-run${n}.log"
  "$EVIDENCE" "$raw" "$tr" | tee -a "$SCRATCH/gate-run${n}.log"
  "$TC" "$tr" "$brief" | tee -a "$SCRATCH/gate-run${n}.log"
  "$VALIDATE" "$brief" | tee -a "$SCRATCH/gate-run${n}.log"
}

# --- Run 2: canonical EIA + storage + arXiv (live session 2026-07-02) ---
replay_run 2
RAW="$SCRATCH/scout-raw-run2.jsonl"
"$LOG" --raw "$RAW" --run 2 --tool WebSearch \
  --query "EIA measuring electricity kilowatt kilowatthour explained" \
  --urls "$EIA_M,https://www.eia.gov/tools/glossary/index.php?id=K,https://www.eia.gov/energyexplained/electricity/electricity-in-the-us-generation-capacity-and-sales.php"
"$LOG" --raw "$RAW" --run 2 --tool WebSearch \
  --query "EIA energy storage electricity generation power capacity kWh" \
  --urls "$EIA_S,https://www.eia.gov/todayinenergy/detail.php?id=67205,https://www.eia.gov/analysis/studies/electricity/batterystorage/"
"$LOG" --raw "$RAW" --run 2 --tool WebSearch \
  --query "arxiv 2511.05597 From Prompts to Power energy footprint" \
  --urls "$ARXIV,https://arxiv.org/html/2511.05597v1"
"$LOG" --raw "$RAW" --run 2 --tool WebSearch \
  --query "homelab GPU power consumption kWh youtube lecture" \
  --provider-status error --urls "https://www.youtube.com/watch?v=pool-v-rejected"
"$LOG" --raw "$RAW" --run 2 --tool WebFetch --url "$EIA_M" --status ok --snippet-chars 18500
"$LOG" --raw "$RAW" --run 2 --tool WebFetch --url "$ARXIV" --status ok --snippet-chars 8200
"$LOG" --raw "$RAW" --run 2 --tool WebFetch --url "$EIA_S" --status ok --snippet-chars 54976
gate_chain 2

# --- Run 3: Tom's Hardware joker variant ---
replay_run 3
RAW="$SCRATCH/scout-raw-run3.jsonl"
"$LOG" --raw "$RAW" --run 3 --tool WebSearch \
  --query "site:eia.gov measuring electricity watts power versus energy" \
  --provider-status error --urls "$EIA_M"
"$LOG" --raw "$RAW" --run 3 --tool WebSearch \
  --query "battery storage power capacity versus energy capacity EIA" \
  --provider-status error --urls "$EIA_S,https://www.eia.gov/todayinenergy/detail.php?id=64705"
"$LOG" --raw "$RAW" --run 3 --tool WebSearch \
  --query "RTX 4090 measured power consumption Powenetics review watts" \
  --urls "$TOMS,https://www.igorslab.de/en/nvidia-geforce-rtx-4090-founders-edition-24gb-review-drink-less-work-more/11/,https://www.youtube.com/watch?v=LZ25Z_un4bQ"
"$LOG" --raw "$RAW" --run 3 --tool WebSearch \
  --query "GPU inference power consumption youtube technical demo" \
  --provider-status error --urls "https://www.youtube.com/watch?v=pool-v-empty"
"$LOG" --raw "$RAW" --run 3 --tool WebFetch --url "$TOMS" --status ok --snippet-chars 27329
"$LOG" --raw "$RAW" --run 3 --tool WebFetch --url "$EIA_S" --status ok --snippet-chars 54976
gate_chain 3

# --- Run 4: shuffle arXiv in core ---
replay_run 4
RAW="$SCRATCH/scout-raw-run4.jsonl"
"$LOG" --raw "$RAW" --run 4 --tool WebSearch \
  --query "kilowatt hour versus kilowatt EIA FAQ electricity" \
  --urls "$EIA_M,https://www.eia.gov/tools/faqs/faq.php?id=97&t=3,https://www.eia.gov/tools/glossary/index.php?id=K"
"$LOG" --raw "$RAW" --run 4 --tool WebSearch \
  --query "LLM inference energy measurement GPU vLLM paper" \
  --provider-status error --urls "$ARXIV,https://arxiv.org/html/2511.05597v1"
"$LOG" --raw "$RAW" --run 4 --tool WebSearch \
  --query "EIA energy storage electricity generation power capacity kWh" \
  --urls "$EIA_S,https://www.eia.gov/todayinenergy/detail.php?id=67205"
"$LOG" --raw "$RAW" --run 4 --tool WebSearch \
  --query "self-hosted server electricity cost homelab power blog" \
  --urls "https://stfn.pl/blog/57-home-server-electricity-usage/,https://www.howtogeek.com/i-measured-my-homelabs-power-draw-with-a-smart-plug-and-discovered-the-real-cost/"
"$LOG" --raw "$RAW" --run 4 --tool WebFetch --url "$ARXIV" --status ok --snippet-chars 8200
"$LOG" --raw "$RAW" --run 4 --tool WebFetch --url "$EIA_M" --status ok --snippet-chars 18500
gate_chain 4

# Production brief (run 2) → studies/
cp "$SCRATCH/scout-raw-run2.jsonl" "$ROOT/studies/home-energy-ai-lab/scout-raw.jsonl"
cp "$SCRATCH/scout-transcript-run2.jsonl" "$ROOT/studies/home-energy-ai-lab/scout-transcript.jsonl"
"$PREFLIGHT" "$ROOT/studies/home-energy-ai-lab/brief.md" | tee "$SCRATCH/gate-production.log"
"$EVIDENCE" "$ROOT/studies/home-energy-ai-lab/scout-raw.jsonl" "$ROOT/studies/home-energy-ai-lab/scout-transcript.jsonl" | tee -a "$SCRATCH/gate-production.log"
"$TC" "$ROOT/studies/home-energy-ai-lab/scout-transcript.jsonl" "$ROOT/studies/home-energy-ai-lab/brief.md" | tee -a "$SCRATCH/gate-production.log"
"$VALIDATE" "$ROOT/studies/home-energy-ai-lab/brief.md" | tee -a "$SCRATCH/gate-production.log"

echo "ALL_REPLAY_OK" | tee "$SCRATCH/replay-summary.log"