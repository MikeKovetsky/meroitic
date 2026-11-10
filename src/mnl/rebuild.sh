#!/bin/bash
# Rebuild the local Newsletter files from the readers' raw typing (readings/raw/<pack>/out/).
# usage: bash rebuild.sh <repo root> [out dir]      out dir defaults to <repo root>/data/sources/mnl
set -euo pipefail
ROOT="$1"; M="$ROOT/data/sources/mnl"; OUT="${2:-$M}"; T="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
python3 -I "$T/mnl_build.py" "$ROOT" "$M/readings/raw" "$OUT/mnl_texts.jsonl" | head -1
python3 -I "$T/mnl_dedupe.py" "$ROOT" "$OUT/mnl_texts.jsonl" --show > "$OUT/dedupe_report.txt"
head -3 "$OUT/dedupe_report.txt"
python3 -I "$T/mnl_corpus.py" "$ROOT" "$OUT/mnl_texts.jsonl" "$OUT/corpus_v4.jsonl"
