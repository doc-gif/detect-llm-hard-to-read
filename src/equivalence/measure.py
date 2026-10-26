"""エントロピーの計測: 既存の Phase 1 (``collect_metrics.collect``) をそのまま使う。

元コードと変換後コードを、同じモデル・同じトークン化 (BOS 付き、特殊トークンなし)・
同じ isolated 戦略で計測し、``out/`` と同じ形式の Parquet を保存する。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import collect_metrics
from model import ModelAdapter, create_model_adapter
from writer import create_writer


def load_model(measure_cfg: Dict[str, Any]) -> ModelAdapter:
    """設定 (``[measure]``) からモデルを読み込む。"""
    model = create_model_adapter(
        measure_cfg.get("model_kind", "hf_causal_lm"),
        model_name=measure_cfg["model"],
        revision=measure_cfg.get("revision") or None,
        device=measure_cfg.get("device") or None,
        dtype=measure_cfg.get("dtype") or None,
    )
    model.load()
    return model


def measure_file(model: ModelAdapter, source_path: Path, output_path: Path, measure_cfg: Dict[str, Any],
                 project: str) -> int:
    """1ファイルを計測して Parquet に保存し、トークン数を返す。"""
    result = collect_metrics.collect(
        source_path=source_path,
        model=model,
        context_strategy_name=measure_cfg.get("context_strategy", "function_scope"),
        project=project,
    )
    tmp = output_path.with_suffix(".tmp.parquet")
    create_writer("parquet").write(result, tmp)
    tmp.replace(output_path)  # 途中で止まっても壊れたファイルを残さない
    return result.metadata.total_tokens
