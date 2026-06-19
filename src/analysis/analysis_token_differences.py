import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import spearmanr, pearsonr

# ==========================================
# 1. パスとデータセットの設定 (環境非依存)
# ==========================================
# スクリプトの位置からプロジェクト群のルートディレクトリを動的に取得
# ※ スクリプトの保存場所（階層の深さ）に合わせて .parent の数を調整してください。
# 例: detect-llm-hard-to-read/scripts/eval/compare.py なら parent は 4つ
PROJECTS_DIR = Path(__file__).resolve().parent.parent.parent.parent

BASE_DIR_MINE = PROJECTS_DIR / "detect-llm-hard-to-read" / "out"
BASE_DIR_PRIOR = PROJECTS_DIR / "lm-cc" / "results"

DATASETS = [
    {
        "name": "HumanEval",
        "prior_json": BASE_DIR_PRIOR / "humaneval-ier-simplified" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
        "my_dir": BASE_DIR_MINE / "humaneval_simplified-top60",
        "parquet_format": "result_{task_id}.parquet"
    },
    {
        "name": "XcodeEval (APR)",
        "prior_json": BASE_DIR_PRIOR / "xcodeeval" / "apr-simplified" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
        "my_dir": BASE_DIR_MINE / "xcodeeval_simplified-top50_apr",
        "parquet_format": "result_{task_id}.parquet"
    },
    {
        "name": "XcodeEval (Code Translation)",
        "prior_json": BASE_DIR_PRIOR / "xcodeeval" / "code_translation-simplified" / "entropy" / "entropies-CodeLlama-7b-hf-1.0.json",
        "my_dir": BASE_DIR_MINE / "xcodeeval_simplified-top50_code_translation",
        "parquet_format": "result_{task_id}.parquet"
    }
]


# ==========================================
# 2. 分析ロジック
# ==========================================
def analyze_entropy_differences(task_id, prior_entropies, my_entropies, my_tokens=None):
    """先行研究と自分のエントロピー配列を比較する"""
    prior = np.array(prior_entropies, dtype=float)
    mine = np.array(my_entropies, dtype=float)

    print("\n" + "=" * 50)
    print(f"📊 エントロピー誤差分析レポート: {task_id}")
    print("=" * 50)

    # NaN（欠損値）のクリーニング
    if np.isnan(mine).any():
        print("  ⚠️ [Debug] 自身のデータに NaN (計算不能値) が含まれています。NaNを除外して比較を試みます。")
        valid_idx = ~np.isnan(mine)
        mine = mine[valid_idx]
        if my_tokens is not None:
            my_tokens = np.array(my_tokens)[valid_idx]

    if np.isnan(prior).any():
        print("  ⚠️ [Debug] 先行研究のデータに NaN が含まれています。")

    # 1. 配列長の確認
    print("\n[1] トークン数の確認")
    print(f"  - 先行研究のトークン数: {len(prior)}")
    print(f"  - 自分のトークン数 : {len(mine)}")

    min_len = min(len(prior), len(mine))
    if len(prior) != len(mine):
        print(f"  🚨 警告: トークン数が一致しません。先頭から {min_len} トークン分のみで比較します。")

    prior = prior[:min_len]
    mine = mine[:min_len]
    if my_tokens is not None:
        my_tokens = my_tokens[:min_len]

    if min_len < 2:
        print("  ❌ [Error] 比較可能なトークン数が少なすぎます。スキップします。")
        return

    # 2. 誤差の基本統計量
    diff = prior - mine
    abs_diff = np.abs(diff)

    print("\n[2] 誤差の基本統計")
    print(f"  - 平均絶対誤差 (MAE) : {np.mean(abs_diff):.6f}")
    print(f"  - 最大絶対誤差 (Max) : {np.max(abs_diff):.6f}")

    if np.max(abs_diff) == 0:
        print("  🌟 判定: 完全に一致しています！")
    elif np.max(abs_diff) < 1e-2:
        print("  ✅ 判定: 誤差は非常に小さく、FP16/BF16などの計算精度の違いによる許容範囲内です。")
    else:
        print("  ❌ 判定: 計算精度以上の大きな誤差が含まれています。ロジックの差異を疑ってください。")

    # 3. 相関関係
    spearman_corr, _ = spearmanr(prior, mine)
    pearson_corr, _ = pearsonr(prior, mine)
    print("\n[3] 相関分析")
    print(f"  - スピアマン順位相関 : {spearman_corr:.6f} (1.0に近いほど順位が一致)")
    print(f"  - ピアソン相関 (線形): {pearson_corr:.6f} (1.0に近いほど値が比例)")

    # 4. Off-by-one (1つズレ) 検知
    print("\n[4] Off-by-one (ズレ) 検知")
    if min_len > 2:
        corr_shift_minus1, _ = pearsonr(prior[:-1], mine[1:])
        corr_shift_plus1, _ = pearsonr(prior[1:], mine[:-1])

        print(f"  - ズレなしの相関     : {pearson_corr:.6f}")
        print(f"  - 自分を -1 ズラす   : {corr_shift_minus1:.6f}")
        print(f"  - 自分を +1 ズラす   : {corr_shift_plus1:.6f}")

        if max(corr_shift_minus1, corr_shift_plus1) > pearson_corr and max(corr_shift_minus1, corr_shift_plus1) > 0.9:
            print(
                "  🚨 警告: ズラした方が相関が高くなりました！「予測ターゲットのインデックス」が1つズレている可能性が高いです。")

    # 5. 誤差が大きいトークン Top 5
    print("\n[5] 誤差が大きい箇所 Top 5")
    df_diff = pd.DataFrame({
        'Index': np.arange(min_len),
        'Token': my_tokens if my_tokens is not None else ["-"] * min_len,
        'Prior': prior,
        'Mine': mine,
        'Diff': diff,
        'AbsDiff': abs_diff
    })
    top5_diff = df_diff.sort_values('AbsDiff', ascending=False).head(5)
    print(top5_diff.to_string(index=False))


# ==========================================
# 3. メイン処理（データのロードと結合）
# ==========================================
def run_analysis():
    for dataset in DATASETS:
        ds_name = dataset["name"]
        prior_json_path = dataset["prior_json"]
        my_dir = dataset["my_dir"]

        print(f"\n\n{'#' * 60}")
        print(f"🚀 データセット検証開始: {ds_name}")
        print(f"{'#' * 60}")

        # Pathオブジェクトによる存在確認
        if not prior_json_path.exists():
            print(f"  ❌ [Error] 先行研究のJSONが見つかりません:\n     {prior_json_path}")
            continue

        # JSONの読み込み
        try:
            with prior_json_path.open('r', encoding='utf-8') as f:
                prior_data = json.load(f)
            print(f"  ✅ 先行研究のデータをロードしました (計 {len(prior_data)} タスク)")
        except Exception as e:
            print(f"  ❌ [Error] JSONの読み込みに失敗しました: {e}")
            continue

        success_count = 0

        for item in prior_data:
            task_id = item.get("task_id")
            prior_entropies = item.get("entropies", [])

            # ディレクトリの区切り文字などが含まれる場合の安全なファイル名化
            safe_task_id = str(task_id).replace("/", "_")
            parquet_filename = dataset["parquet_format"].format(task_id=safe_task_id)

            # Pathオブジェクトの演算子 (/) で結合
            parquet_path = my_dir / parquet_filename

            if not parquet_path.exists():
                print(f"  ⚠️ [Debug] Parquetファイルが見つかりません。スキップします: {parquet_path}")
                continue

            # Parquetの読み込み
            try:
                df = pd.read_parquet(parquet_path)
            except Exception as e:
                print(f"  ❌ [Error] Parquetの読み込みに失敗しました ({parquet_path}): {e}")
                continue

            # 必須カラムの確認
            if "metric_entropy" not in df.columns:
                print(f"  ❌ [Error] 'metric_entropy' カラムが存在しません: {parquet_path}")
                continue

            my_entropies = df["metric_entropy"].values
            my_tokens = df["token_str"].values if "token_str" in df.columns else None

            # 比較実行
            analyze_entropy_differences(task_id, prior_entropies, my_entropies, my_tokens)
            success_count += 1

            # 1件検証したら次のデータセットへ移動（全体を回したい場合はこの break をコメントアウト）
            break

        if success_count == 0:
            print(f"  ❌ [Error] {ds_name} において、突合に成功したタスクが1件もありませんでした。")


if __name__ == "__main__":
    run_analysis()