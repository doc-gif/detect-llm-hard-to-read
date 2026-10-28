#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE=/Users/hyoishitobi/experiments/llm-readability-20261026/detect-llm-hard-to-read
CONFIG=configs/equivalence/if_else_swap_humaneval_m2.toml
NAME=if_else_swap_humaneval_m2_20261026
fetch_results() {
    mkdir -p "$ROOT/results/equivalence/$NAME" "$ROOT/results/m2_preflight"
    rsync -a "m2:$REMOTE/results/equivalence/$NAME/" "$ROOT/results/equivalence/$NAME/"
    mkdir -p "$ROOT/results/equivalence/if_else_swap_humaneval_m2_preflight_20261026"
    rsync -a "m2:$REMOTE/results/equivalence/if_else_swap_humaneval_m2_preflight_20261026/" "$ROOT/results/equivalence/if_else_swap_humaneval_m2_preflight_20261026/"
    rsync -a "m2:$REMOTE/results/m2_preflight/" "$ROOT/results/m2_preflight/"
}
run_stage() {
    ssh -o BatchMode=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 m2 "cd $REMOTE && HF_HUB_OFFLINE=1 MPLBACKEND=Agg .venv/bin/python scripts/equivalence_experiment.py $1 --config $CONFIG"
}
case "${1:-status}" in
    prepare)
        run_stage transform
        run_stage behavior
        fetch_results
        ;;
    measure)
        trap fetch_results EXIT
        run_stage measure
        run_stage compare
        ;;
    status) run_stage status ;;
    fetch) fetch_results ;;
    *) echo "Usage: bash scripts/m2_experiment.sh {prepare|measure|status|fetch}" >&2; exit 2 ;;
esac
