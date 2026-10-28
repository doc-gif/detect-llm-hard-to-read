import json
import numpy as np
import pandas as pd
from pathlib import Path
import logging

# --- ログの設定 ---
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

# ==========================================
# ⚙️ 設定エリア (環境に合わせてパスを変更してください)
# ==========================================
BASELINE_JSON_PATH = "/Users/hyoishitobi/PycharmProjects/lm-cc/results/humaneval-ier/entropy/entropies-CodeLlama-7b-hf-1.0.json"
MY_OUT_DIR = "../out/humaneval"

# 許容する最大誤差（float16 や MPS/CUDA の演算誤差を考慮して 1e-3 とする）
ERROR_TOLERANCE = 1e-3


def normalize_token(token_str: str) -> str:
    """自分のトークン表現を先行研究の表現に合わせる正規化処理"""
    if pd.isna(token_str):
        return ""
    # LlamaのSentencePieceトークナイザーの空白「 」を先行研究の「 」(U+2581)に変換
    return str(token_str).replace(" ", "\u2581")


def run_verification():
    json_path = Path(BASELINE_JSON_PATH).resolve()
    out_dir = Path(MY_OUT_DIR).resolve()

    if not json_path.exists():
        logging.error(f"❌ 先行研究のJSONが見つかりません: {json_path}")
        return

    # 1. 先行研究のJSONを読み込み、task_id をキーにした辞書（O(1)アクセス用）を作成
    logging.info(f"📂 先行研究のデータをロード中: {json_path.name}")
    with open(json_path, "r", encoding="utf-8") as f:
        baseline_list = json.load(f)

    baseline_dict = {item["task_id"]: item for item in baseline_list}
    logging.info(f"  -> {len(baseline_dict)} 件のベースラインデータを読み込みました。\n")

    # 2. 自分のParquetファイルを再帰的に検索
    parquet_files = list(out_dir.rglob("*.parquet"))
    logging.info(f"🔍 自分の出力ディレクトリから {len(parquet_files)} 件のParquetファイルを検出しました。\n")

    # 結果の集計用
    stats = {
        "perfect_match": 0,
        "token_mismatch": 0,
        "length_mismatch": 0,
        "high_error": 0,
        "not_in_baseline": 0,
        "read_error": 0
    }

    print("-" * 50)

    # 3. 1件ずつ検証
    for p_file in parquet_files:
        # "result_HumanEval_0.parquet" -> "HumanEval_0"
        task_id = p_file.stem.replace("result_", "")

        if task_id not in baseline_dict:
            stats["not_in_baseline"] += 1
            continue

        try:
            # 自分のデータを読み込み、エントロピーが計算されている有効なトークンのみ抽出
            my_df = pd.read_parquet(p_file)
            my_clean = my_df[my_df['metric_entropy'].notnull()].copy()

            my_tokens = my_clean['token_str'].apply(normalize_token).tolist()
            my_entropies = my_clean['metric_entropy'].tolist()

            base_data = baseline_dict[task_id]
            base_tokens = base_data["tokens"]
            base_entropies = base_data["entropies"]

            # --- 検証 A: 配列の長さ ---
            if len(my_tokens) != len(base_tokens):
                logging.warning(f"[Length Mismatch] {task_id}: 自分={len(my_tokens)} vs 先行={len(base_tokens)}")
                stats["length_mismatch"] += 1
                continue

            # --- 検証 B: トークンの完全一致 ---
            tokens_match = True
            for i, (my_tok, base_tok) in enumerate(zip(my_tokens, base_tokens)):
                if my_tok != base_tok:
                    logging.warning(f"[Token Mismatch] {task_id} (Idx {i}): 自分='{my_tok}' vs 先行='{base_tok}'")
                    tokens_match = False
                    break

            if not tokens_match:
                stats["token_mismatch"] += 1
                continue

            # --- 検証 C: エントロピー値の誤差 ---
            my_ent_arr = np.array(my_entropies)
            base_ent_arr = np.array(base_entropies)

            max_error = np.max(np.abs(my_ent_arr - base_ent_arr))

            if max_error > ERROR_TOLERANCE:
                logging.warning(f"[High Error] {task_id}: 最大誤差={max_error:.6f} (許容値超過)")
                stats["high_error"] += 1
            else:
                stats["perfect_match"] += 1

        except Exception as e:
            logging.error(f"[Read Error] {task_id}: {e}")
            stats["read_error"] += 1

    # 4. サマリーの出力
    print("-" * 50)
    print("📊 検証サマリー")
    print("-" * 50)
    print(f"✅ 完全一致 (トークン一致 & 誤差 {ERROR_TOLERANCE} 以下) : {stats['perfect_match']} 件")
    print(f"⚠️ 誤差過大 (トークン一致するが値がズレている)     : {stats['high_error']} 件")
    print(f"❌ トークン不一致 (文字列レベルで異なる)           : {stats['token_mismatch']} 件")
    print(f"❌ 長さ不一致 (抽出されたトークン数が異なる)       : {stats['length_mismatch']} 件")
    print(f"⏭️ ベースラインに存在しないためスキップ           : {stats['not_in_baseline']} 件")
    print(f"⚠️ ファイル読み込みエラー                         : {stats['read_error']} 件")
    print("-" * 50)

    if stats["perfect_match"] > 0 and (stats["token_mismatch"] + stats["length_mismatch"] + stats["high_error"]) == 0:
        print("\n🎉 大成功！検証したすべてのデータが先行研究と完全に一致しました。")
    else:
        print(
            "\n💡 ヒント: 不一致がある場合、トークンのデコード仕様（改行文字 <0x0A> の扱いなど）や、BOSトークンの除去条件が原因である可能性が高いです。")


if __name__ == "__main__":
    run_verification()