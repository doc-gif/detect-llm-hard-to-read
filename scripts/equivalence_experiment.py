"""等価変換の前後で SU・エントロピー (・回答精度) を比較する実験の CLI。

使い方 (詳細は docs/equivalence_experiment.md):
    python scripts/equivalence_experiment.py transform --config configs/equivalence/if_else_swap_humaneval_sample.toml
    python scripts/equivalence_experiment.py behavior  --config ...
    python scripts/equivalence_experiment.py measure   --config ...   # 要モデル (Mac で実行)
    python scripts/equivalence_experiment.py compare   --config ...
    python scripts/equivalence_experiment.py all       --config ...   # transform → behavior → measure → compare
    python scripts/equivalence_experiment.py status    --config ...

    python scripts/equivalence_experiment.py accuracy-prepare --config ...
    python scripts/equivalence_experiment.py accuracy-run     --config ...  # HumanEval のみ。API を呼ぶ
    python scripts/equivalence_experiment.py accuracy-score   --config ... [--details lm-cc の details.jsonl]

    # 候補の一覧だけを見る (ファイルを書かない dry-run)。--config は省略できる
    python scripts/equivalence_experiment.py scan --dataset all --transform if_else_swap [--out 候補.csv]

    # 1つの設定 (または既定値) をデータセット × 変換ごとに回す。実験名は "{transform}_{dataset}"
    python scripts/equivalence_experiment.py all --config configs/equivalence/template.toml --dataset all

同じコマンドを再実行すると、成功済みの対象は飛ばして未実行・失敗分だけを処理する。
計測結果は (モデル・dtype・コードの中身などが同じなら) キャッシュから再利用する。
"""
import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))  # src/ を import ルートにする

import pandas as pd  # noqa: E402

from equivalence import scan  # noqa: E402
from equivalence.experiment import Experiment, build_configs, target_ids  # noqa: E402

STAGES = ["scan", "transform", "behavior", "measure", "compare", "all", "status",
          "accuracy-prepare", "accuracy-run", "accuracy-score"]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="等価変換前後の SU・エントロピー比較実験")
    parser.add_argument("stage", choices=STAGES)
    parser.add_argument("--config", type=Path, help="TOML 設定ファイル (省略時は既定値。dataset は --dataset で指定)")
    parser.add_argument("--dataset", nargs="+", help='データセットを上書き (複数可、"all" で全部)。ids / targets は全件に戻る')
    parser.add_argument("--transform", nargs="+", help='変換を上書き (複数可、"all" で登録済みの全部)')
    parser.add_argument("--name", help="実験名を上書き。{transform} / {dataset} を置き換える")
    parser.add_argument("--out", type=Path, help="scan: 候補ごとの一覧を書き出す CSV")
    parser.add_argument("--ids", nargs="+", help="対象 ID を上書き (設定の experiment.ids の代わり)")
    parser.add_argument("--targets", nargs="+", help='対象を "uid" または "uid:variant_id" で指定')
    parser.add_argument("--limit", type=int, help="対象 ID を先頭から N 件に絞る")
    parser.add_argument("--only-failed", action="store_true", help="失敗した対象だけを再実行する")
    parser.add_argument("--max-calls", type=int, help="accuracy-run: API 呼び出し回数の上限")
    parser.add_argument("--details", type=Path, help="accuracy-score (xcodeeval): lm-cc の *_details.jsonl")
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args(argv)


def run_scan(configs, out=None) -> int:
    """候補の一覧と、適用できない理由の内訳を表示する (実験ディレクトリは作らない)。"""
    tables = []
    for config in configs:
        name = config["transform"]["name"]
        dataset = config["experiment"]["dataset"]
        logging.info(f"🔍 {dataset} × {name}")
        tables.append(scan.scan_dataset(dataset, name, config["transform"]["options"], target_ids(config)))
    table = pd.concat(tables, ignore_index=True)
    with pd.option_context("display.width", 200, "display.max_columns", None, "display.max_colwidth", 60):
        print("\n## データセット × 変換ごとの候補数\n")
        print(scan.summarize(table).to_string(index=False))
        reasons = scan.reason_counts(table)
        if not reasons.empty:
            print("\n## 適用できない・失敗した理由\n")
            print(reasons.drop(columns=["example_reason"]).to_string(index=False))
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(out, index=False, encoding="utf-8")
        logging.info(f"💾 候補一覧: {out}")
    return 0


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO),
                        format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    for name in ["httpx", "httpcore", "transformers", "huggingface_hub", "collect_metrics", "model", "writer"]:
        logging.getLogger(name).setLevel(logging.WARNING)

    overrides = {"experiment": {}}
    if args.ids:
        overrides["experiment"]["ids"] = args.ids
    if args.targets:
        overrides["experiment"]["targets"] = args.targets
    if args.limit:
        overrides["experiment"]["limit"] = args.limit
    configs = build_configs(args.config, args.dataset, args.transform, args.name, overrides)

    if args.stage == "scan":
        return run_scan(configs, args.out)

    for config in configs:
        exp = Experiment(config)
        logging.info(f"📁 実験ディレクトリ: {exp.run_dir}")
        stages = ["transform", "behavior", "measure", "compare"] if args.stage == "all" else [args.stage]
        for stage in stages:
            if stage == "transform":
                exp.run_transform(args.only_failed)
            elif stage == "behavior":
                exp.run_behavior(args.only_failed)
            elif stage == "measure":
                exp.run_measure(args.only_failed)
            elif stage == "compare":
                exp.run_compare(args.only_failed)
            elif stage == "accuracy-prepare":
                table = exp.run_accuracy_prepare()
                logging.info(f"✅ 評価対象 {int(table['usable'].sum())} / {len(table)} 件 → {exp.accuracy_dir()}")
            elif stage == "accuracy-run":
                exp.run_accuracy(args.only_failed, args.max_calls)
            elif stage == "accuracy-score":
                exp.run_accuracy_score(args.details)
        print(json.dumps({"experiment": exp.config["experiment"]["name"], **exp.status_counts()},
                         ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
