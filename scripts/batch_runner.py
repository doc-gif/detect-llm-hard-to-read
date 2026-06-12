import subprocess
from pathlib import Path
import logging
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.language import supported_extensions

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# =========================================================
# ⚙️ 設定エリア (ここで測定対象や出力を直接指定します)
# =========================================================

# 1. 対象コードのディレクトリパス (複数指定可能)
INPUT_DIRS = [
    "../data/humaneval",
    "../data/humaneval_simplified",
    "../data/xcodeeval/apr",
    "../data/xcodeeval/code_translation",
    "../data/xcodeeval_simplified/apr",
    "../data/xcodeeval_simplified/code_translation"
]

# 2. 出力先の最上位ディレクトリパス
OUTPUT_DIR = "../out"

# 3. 測定に使うモデルと出力形式
MODEL_NAME = "codellama/CodeLlama-7b-hf"
OUTPUT_FORMAT = "parquet"  # "json" に変更可能


# =========================================================


def run_batch():
    # パスの解決 (scriptsディレクトリ基準)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    output_dir = Path(OUTPUT_DIR).resolve()
    # 大元の出力ディレクトリを作成
    output_dir.mkdir(parents=True, exist_ok=True)

    cli_script = project_root / "src" / "collect_metrics.py"

    if not cli_script.exists():
        logging.error(f"CLIスクリプトが見つかりません: {cli_script}")
        sys.exit(1)

    # ---------------------------------------------------------
    # 対象ファイルのリストアップ (入力元のベースディレクトリ情報を一緒に保持)
    # ---------------------------------------------------------
    target_files = []

    # システムがサポートしている拡張子（['.py', '.java', '.c'] など）を取得
    extensions = supported_extensions()

    for dir_str in INPUT_DIRS:
        in_dir = Path(dir_str).resolve()
        if not in_dir.exists():
            logging.warning(f"⚠️ 指定された入力ディレクトリが見つかりません (スキップします): {in_dir}")
            continue

        found_files = []
        for ext in extensions:
            found_files.extend(list(in_dir.rglob(f"*{ext}")))

        # ファイルパスだけでなく「どのベースディレクトリから見つけたか(in_dir)」もタプルで保持する
        target_files.extend([(f, in_dir) for f in found_files])
        logging.info(f"📁 読み込み: {in_dir} から {len(found_files)} 件のファイルを検出")

    if not target_files:
        logging.error("❌ 処理対象のファイルが1つも見つかりませんでした。")
        sys.exit(1)

    logging.info(f"🚀 合計 {len(target_files)} 件のファイルを処理します。")

    # ---------------------------------------------------------
    # バッチ処理の実行ループ
    # ---------------------------------------------------------
    success_count = 0
    error_count = 0

    total_files = len(target_files)

    data_root = (project_root / "data").resolve()

    for i, (filepath, base_dir) in enumerate(target_files, 1):
        project_name = filepath.stem

        # 1. 大元の data_root からの相対パスを取得する
        # 例: data/xcodeeval_simplified/code_translation/result_xxx.py
        # ➔ relative_to_data = Path("xcodeeval_simplified/code_translation/result_xxx.py")
        relative_to_data = filepath.relative_to(data_root)

        # 2. ファイル名を除く親フォルダの階層（parts）をアンダースコアで結合する
        # 例: ("xcodeeval_simplified", "code_translation") ➔ "xcodeeval_simplified_code_translation"
        flat_dir_name = "_".join(relative_to_data.parent.parts)

        # 3. out/ 直下にフラットなフォルダを作成する
        # 例: ../out/xcodeeval_simplified_code_translation/
        target_dir = output_dir / flat_dir_name
        target_dir.mkdir(parents=True, exist_ok=True)

        output_filename = f"result_{project_name}.{OUTPUT_FORMAT}"
        output_file = target_dir / output_filename

        # 💡 追記: ログの先頭につける進捗状況のプレフィックス (例: [1/50])
        progress_prefix = f"[{i}/{total_files}]"

        if output_file.exists():
            logging.info(f"{progress_prefix} ⏭️ スキップ: {project_name}")
            success_count += 1
            continue

        # 💡 変更: すべてのログに progress_prefix をつける
        logging.info(
            f"{progress_prefix} ▶️ 処理開始: {project_name} ({filepath.name}) -> {output_file.relative_to(project_root)}")

        cmd = [
            sys.executable,
            str(cli_script),
            "--model", MODEL_NAME,
            "--source", str(filepath),
            "--output", str(output_file),
            "--format", OUTPUT_FORMAT,
            "--project", project_name,
            "--device", "mps",
            "--dtype", "float16"
        ]

        try:
            subprocess.run(cmd, check=True)
            logging.info(f"{progress_prefix} ✅ 完了: {project_name}")
            success_count += 1
        except subprocess.CalledProcessError as e:
            logging.error(f"{progress_prefix} ❌ エラー発生 ({project_name}) - 終了コード: {e.returncode}")
            if e.stderr:
                stderr_tail = "\n".join(e.stderr.strip().split("\n")[-3:])
                logging.error(f"エラー内容:\n{stderr_tail}")
            error_count += 1
        except Exception as e:
            logging.error(f"{progress_prefix} ⚠️ 予期せぬエラー ({project_name}): {e}")
            error_count += 1

    # ---------------------------------------------------------
    # 結果のサマリー
    # ---------------------------------------------------------
    logging.info("=" * 40)
    logging.info("🎉 バッチ処理が終了しました。")
    logging.info(f"  成功 (スキップ含む): {success_count} 件")
    logging.info(f"  エラー: {error_count} 件")
    logging.info("=" * 40)


if __name__ == "__main__":
    run_batch()
