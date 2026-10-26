"""先行研究のスコアファイルにある uid が summary CSV に揃っているか (推論漏れが無いか) を確認する。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # src/ を import ルートにする

import pandas as pd
import json
import logging

import paths
from analysis.scores import SCORE_FILES

logging.basicConfig(level=logging.INFO, format="%(message)s")

# ==========================================
# ⚙️ 設定エリア
# ==========================================
SUMMARY_CSV_PATH = paths.summary_csv()

# スコアファイルの定義は analysis/scores.py の SCORE_FILES (簡略化版を含む全データセットを確認する)


def load_expected_uids(dataset_name: str, config: dict) -> set:
    """JSONから期待されるすべてのUID（タスクID）を抽出し、Set(集合)として返す"""
    path = Path(config["path"])
    if not path.exists():
        logging.warning(f"⚠️ {dataset_name} のスコアファイルが見つかりません: {path}")
        return set()

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    expected_uids = set()
    if config["format"] == "simple":
        for k in data.keys():
            uid = k.split("__")[0]  # "HumanEval_80__0" -> "HumanEval_80"
            expected_uids.add(uid)
    elif config["format"] == "nested":
        for k in data.keys():
            expected_uids.add(k)

    return expected_uids


def main():
    if not Path(SUMMARY_CSV_PATH).exists():
        logging.error(f"❌ サマリーCSVが見つかりません: {SUMMARY_CSV_PATH}")
        return

    # 自分のCSVから、存在するすべての (dataset, uid) を取得
    df_summary = pd.read_csv(SUMMARY_CSV_PATH)

    total_missing = 0

    print("🔍 データ欠落チェックを開始します...\n")

    for dataset, config in SCORE_FILES.items():
        print(f"{'=' * 50}\n📂 データセット: {dataset}\n{'-' * 50}")

        # 1. 先行研究のJSONから期待されるUIDのリストを取得
        expected_uids = load_expected_uids(dataset, config)
        if not expected_uids:
            continue

        # 2. 自分のCSVから、このデータセットに属するUIDのリストを取得
        my_uids = set(df_summary[df_summary['dataset'] == dataset]['uid'].tolist())

        # 3. 差分（JSONにはあるが、自分のCSVにはないUID）を計算
        missing_uids = expected_uids - my_uids

        # 逆の差分（自分のCSVにはあるが、JSONにないUID。参考情報）
        extra_uids = my_uids - expected_uids

        # 結果の出力
        print(f"  期待される総件数 (JSON)   : {len(expected_uids)} 件")
        print(f"  推論完了した件数 (CSV)   : {len(my_uids)} 件")

        if missing_uids:
            print(f"  ❌ 欠落データ (Missing)  : {len(missing_uids)} 件")
            # リストが長すぎる場合は最初の20件だけ表示する
            missing_list = sorted(list(missing_uids))
            display_limit = 20
            print("     [欠落しているUIDのリスト]")
            for uid in missing_list[:display_limit]:
                print(f"       - {uid}")
            if len(missing_list) > display_limit:
                print(f"       ... 他 {len(missing_list) - display_limit} 件")

            total_missing += len(missing_uids)
        else:
            print("  ✅ 欠落なし！期待されるデータはすべて揃っています。")

        if extra_uids:
            print(f"  ⚠️ 参考: JSONに存在しない余分なデータがCSVに {len(extra_uids)} 件あります。")

        print("\n")

    print("=" * 50)
    print(f"🏁 チェック完了！ 全データセットでの欠落データ合計: {total_missing} 件")
    print("=" * 50)


if __name__ == "__main__":
    main()