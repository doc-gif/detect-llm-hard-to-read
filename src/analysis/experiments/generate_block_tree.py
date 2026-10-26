"""out/ の Parquet から LM-CC のブロックツリー JSON (先行研究 lm-cc と同じ形式) を生成する。

出力: results/block_trees/<dataset>/block_tree_<task_id>.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # src/ を import ルートにする

import pandas as pd

import paths
from analysis.macro.lm_cc_helper.calculate_code_with_boundaries import get_code_with_boundaries
from analysis.macro.lm_cc_helper.code_block_processor import CodeBlockProcessor
from schema.records import ParquetSchema as PCol

# ---------------------------------------------------------
# ⚙️ 設定エリア
# ---------------------------------------------------------
BASE_OUT_DIR = paths.OUT_DIR

# 出力先のベースディレクトリ
OUTPUT_BASE_DIR = paths.BLOCK_TREES_DIR

# 境界判定のエントロピー閾値 [nats] (先行研究のコードと同じ 0.67)
THRESHOLD = 0.67

# 処理対象の Parquet ファイルが格納されているディレクトリのリスト
# 辞書のキーが「データセット名（出力時のフォルダ名）」になります
DATA_DIRECTORIES = {
    "humaneval": BASE_OUT_DIR / "humaneval",
    "humaneval_simplified": BASE_OUT_DIR / "humaneval_simplified",
    "humaneval_simplified-top60": BASE_OUT_DIR / "humaneval_simplified-top60",
    "xcodeeval_apr": BASE_OUT_DIR / "xcodeeval_apr",
    "xcodeeval_code_translation": BASE_OUT_DIR / "xcodeeval_code_translation",
    "xcodeeval_simplified-top50_apr": BASE_OUT_DIR / "xcodeeval_simplified-top50_apr",
    "xcodeeval_simplified-top50_code_translation": BASE_OUT_DIR / "xcodeeval_simplified-top50_code_translation",
    "xcodeeval_simplified_apr": BASE_OUT_DIR / "xcodeeval_simplified_apr",
    "xcodeeval_simplified_code_translation": BASE_OUT_DIR / "xcodeeval_simplified_code_translation"
}


def process_parquet_to_blocktree(parquet_file: Path, processor: CodeBlockProcessor) -> tuple[dict, str]:
    """1つのParquetファイルを読み込み、ブロックツリーの辞書を生成する"""
    df = pd.read_parquet(parquet_file)

    # 必須カラムの確認
    if PCol.TOKEN_STR not in df.columns or PCol.METRIC_ENTROPY not in df.columns:
        raise ValueError(f"Missing required columns in {parquet_file.name}")

    # トークンとエントロピーのリストを取得
    tokens = df[PCol.TOKEN_STR].tolist()
    entropies = df[PCol.METRIC_ENTROPY].tolist()

    # ファイル名から task_id を推測 (例: result_HumanEval_66.parquet -> HumanEval_66)
    task_id = parquet_file.stem.replace("result_", "")

    # 1. 境界情報の取得
    code_with_boundaries, clean_code_lines, start_end_tokens, _ = get_code_with_boundaries(
        tokens=tokens,
        entropies=entropies,
        threshold=THRESHOLD
    )

    # オリジナルのコード文字列を復元
    reconstructed_code = "\n".join(clean_code_lines)

    # 2. ブロックツリーの生成 (Tree-sitter AST解析)
    block_tree = processor.parse_code_blocks(
        code_with_boundaries=code_with_boundaries,
        tokens=tokens,
        start_end_tokens=start_end_tokens
    )

    # 3. 指定されたJSONフォーマットに整形
    result_dict = {
        "task_id": task_id,
        "tokens": tokens,
        "entropies": entropies,
        "code": reconstructed_code,
        "block_tree": block_tree
    }

    return result_dict, task_id


def main():
    print(f"🚀 ブロックツリーの一括生成を開始します...\n")

    # 共通のプロセッサーを初期化
    processor = CodeBlockProcessor()

    for dataset_name, data_dir in DATA_DIRECTORIES.items():
        if not data_dir.exists():
            print(f"⚠️ スキップ: ディレクトリが見つかりません -> {data_dir}")
            continue

        # このデータセット用の出力先ディレクトリを作成
        output_dir = OUTPUT_BASE_DIR / dataset_name
        output_dir.mkdir(parents=True, exist_ok=True)

        parquet_files = list(data_dir.glob("*.parquet"))
        if not parquet_files:
            print(f"⚠️ スキップ: {dataset_name} には Parquet ファイルがありません。")
            continue

        print(f"📂 データセット [{dataset_name}] の処理を開始します ({len(parquet_files)}件)")

        success_count = 0

        for idx, file_path in enumerate(parquet_files, 1):
            try:
                tree_data, task_id = process_parquet_to_blocktree(file_path, processor)

                # 1ファイルごとに JSON として保存
                output_file = output_dir / f"block_tree_{task_id}.json"

                with open(output_file, "w", encoding="utf-8") as f:
                    # JSONの配列形式ではなく、単体のオブジェクトとして保存（見本通り）
                    json.dump([tree_data], f, ensure_ascii=False, indent=2)

                success_count += 1

                # 進行状況の表示 (あまり長くなりすぎないように10件ごとに表示などでも可)
                # print(f"  [{idx}/{len(parquet_files)}] ✅ 生成成功: block_tree_{task_id}.json")

            except Exception as e:
                print(f"  [{idx}/{len(parquet_files)}] ❌ 失敗: {file_path.name} - Error: {e}")

        print(f"✅ {dataset_name}: {success_count} / {len(parquet_files)} 件完了 -> 出力先: {output_dir}\n")

    print(f"🎉 すべてのデータセットの処理が完了しました！")


if __name__ == "__main__":
    main()