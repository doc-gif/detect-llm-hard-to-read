"""loc_variation_9pairs 専用の入口。段階は暗黙には進まない。

    check     入力の検証と一覧 (出力ディレクトリは作らない。モデル不要)
    behavior  tests.json の args / expected で動作を検証する (モデル不要)
    measure   計測する。モデルを読み込むので --run-model が必要
    compare   計測済みの結果から比較表を作る (モデル不要)
    summary   LOC・トークン数・SU 数の前後と差の一覧を作る (モデル不要)
    status    段階ごとの進み具合

対象と反復:
    --cases first3 (既定) | all | first:N | id1,id2
    --repetition K   反復 ID K だけ (既定 1)
    --repeat N       反復 ID 1..N
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import paths
from equivalence.loc_variation import LocVariationRun, rep_label, select_cases


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="loc_variation_9pairs の 9 組を計測・比較する")
    parser.add_argument("stage", choices=["check", "behavior", "measure", "compare", "summary", "status"])
    parser.add_argument("--config", type=Path, default=paths.PROJECT_ROOT / "configs/equivalence/loc_variation_9pairs.toml")
    parser.add_argument("--package", type=Path, default=None, help="zip または展開済みディレクトリ (設定を上書き)")
    parser.add_argument("--output", type=Path, default=None, help="出力ルート (設定を上書き。新しいディレクトリにする)")
    parser.add_argument("--cases", default="first3", help="first3 | all | first:N | id1,id2 (既定: first3)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--repetition", type=int, default=None, help="反復 ID (既定: 1)")
    group.add_argument("--repeat", type=int, default=None, help="反復 ID 1..N を対象にする")
    parser.add_argument("--run-model", action="store_true", help="measure でモデルを読み込むことを許可する")
    return parser.parse_args(argv)


def repetitions(args) -> list:
    if args.repeat is not None:
        if args.repeat < 1:
            raise ValueError("--repeat は 1 以上")
        return list(range(1, args.repeat + 1))
    return [args.repetition if args.repetition is not None else 1]


def main(argv=None) -> int:
    args = parse_args(argv)
    run = LocVariationRun(args.config.resolve(), package_path=args.package, output_root=args.output)
    cases = select_cases(run.package, args.cases)
    reps = repetitions(args)
    for repetition in reps:
        rep_label(repetition)

    if args.stage == "check":
        print(json.dumps({"condition_key": run.key, "condition": run.condition, "output": str(run.dir),
                          "package": {"path": str(run.package.path), "kind": run.package.kind,
                                      "manifest_sha256": run.package.manifest_sha256}}, ensure_ascii=False, indent=1))
        for case in run.package.cases:
            selected = "*" if case in cases else " "
            print(f"{selected} {case.case_id:18s} {case.category:16s} LOC {case.source_loc['original']:>3d} -> "
                  f"{case.source_loc['transformed']:>3d} (manifest {case.declared_loc['original']} -> "
                  f"{case.declared_loc['transformed']}) tests={len(case.tests)}")
        return 0
    if args.stage == "status":
        print(json.dumps(run.status(cases, reps), ensure_ascii=False, indent=1))
        return 0
    with run.locked():
        if args.stage == "behavior":
            run.behavior(cases)
        elif args.stage == "measure":
            report = run.measure(cases, reps, allow_model=args.run_model)
            print(json.dumps({k: len(v) for k, v in report.items()}, indent=1))
        elif args.stage == "compare":
            report = run.compare(cases, reps)
            print(json.dumps({k: len(v) for k, v in report.items()}, indent=1))
        elif args.stage == "summary":
            rows = run.summarize()
            print((run.dir / "summary_all.md").read_text(encoding="utf-8") if rows else "比較済みの結果がない")
        print(json.dumps(run.status(cases, reps), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
