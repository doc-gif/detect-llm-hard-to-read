"""エントロピーの計測: 既存の Phase 1 (``collect_metrics.collect``) をそのまま使う。

元コードと変換後コードを、同じモデル・同じトークン化 (BOS 付き、特殊トークンなし)・
同じ isolated 戦略で計測し、``out/`` と同じ形式の Parquet を保存する。

同じ条件 (モデル・dtype など) で同じコードを計測した結果はキャッシュから再利用できる
(``MeasureCache``)。元コードは変換の種類が違っても同じなので、2つ目以降の実験では計測しない。
"""
from __future__ import annotations

import hashlib
import json
import shutil
from importlib import metadata
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pyarrow as pa
import pyarrow.parquet as pq

import collect_metrics
from model import ModelAdapter, create_model_adapter
from schema import COLLECTOR_VERSION
from schema.records import ParquetSchema
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


# ----------------------------------------------------------------------
# 計測結果のキャッシュ
# ----------------------------------------------------------------------
#: キャッシュキーに含める計測条件 ([measure] のキー)
CACHE_CONFIG_KEYS = ["model", "model_kind", "revision", "device", "dtype", "context_strategy"]
_CACHE_PACKAGES = ["torch", "transformers"]


def cache_key(source_bytes: bytes, measure_cfg: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """コードの中身と計測条件からキャッシュキーを作る。``(キー, キーの元になった値)`` を返す。

    同じモデル・同じ dtype などで同じバイト列を計測した結果だけを再利用する。
    collector や torch / transformers の版が変わったら別キーになる。
    """
    versions = {}
    for name in _CACHE_PACKAGES:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = None
    parts = {
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "measure": {k: measure_cfg.get(k) for k in CACHE_CONFIG_KEYS},
        "collector_version": COLLECTOR_VERSION,
        "packages": versions,
    }
    key = hashlib.sha256(json.dumps(parts, sort_keys=True).encode("utf-8")).hexdigest()
    return key, parts


class MeasureCache:
    """``<cache_dir>/<key[:2]>/<key>.parquet`` と、条件を書いた ``<key>.json`` を置く。"""

    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir

    def path(self, key: str) -> Path:
        return self.cache_dir / key[:2] / f"{key}.parquet"

    def get(self, key: str, output_path: Path, source_path: Path, project: str) -> Optional[int]:
        """キャッシュがあれば ``output_path`` に書き出してトークン数を返す。無ければ None。

        ``meta_project`` / ``meta_file`` だけはこの実験の値に書き換える。
        """
        cached = self.path(key)
        if not cached.exists():
            return None
        table = pq.read_table(cached)
        for col, value in ((ParquetSchema.META_PROJECT, project), (ParquetSchema.META_FILE, str(source_path))):
            if col in table.column_names:
                i = table.column_names.index(col)
                table = table.set_column(i, col, pa.array([value] * table.num_rows, type=table.schema.field(i).type))
        tmp = output_path.with_suffix(".tmp.parquet")
        pq.write_table(table, tmp)
        tmp.replace(output_path)
        return int(json.loads(cached.with_suffix(".json").read_text(encoding="utf-8"))["tokens"])

    def put(self, key: str, parts: Dict[str, Any], measured_path: Path, tokens: int) -> None:
        cached = self.path(key)
        cached.parent.mkdir(parents=True, exist_ok=True)
        tmp = cached.with_suffix(".tmp.parquet")
        shutil.copyfile(measured_path, tmp)
        cached.with_suffix(".json").write_text(
            json.dumps({**parts, "tokens": tokens, "created_from": str(measured_path)}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        tmp.replace(cached)  # parquet を最後に置く (json だけ残っても get では使われない)
