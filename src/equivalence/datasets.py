"""対象データセットの定義: 計測用ソース (data/) と、lm-cc 側の問題・テストデータの対応付け。

dataset 名は ``out/`` や summary CSV の ``dataset`` 列と同じ名前を使う。

| dataset | 計測用ソース | 課題 | テスト・正解 (lm-cc) |
|---|---|---|---|
| humaneval | data/humaneval/<ID>.py | 実行結果の推論 (IER) | dataset/humaneval/<ID>{,__0,__1}/input.txt, output.txt, asserts.txt |
| xcodeeval_apr | data/xcodeeval/apr/<uid>.py | プログラム修正 | dataset/xcodeeval/apr/*.jsonl の hidden_unit_tests |
| xcodeeval_code_translation | data/xcodeeval/code_translation/<uid>.py | Python→C 翻訳 | 同 code_translation/*.jsonl の hidden_unit_tests |
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import paths

TASK_IER = "humaneval_ier"
TASK_APR = "xcodeeval_apr"
TASK_CT = "xcodeeval_code_translation"


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    data_subdir: str                 # data/ からの相対パス
    task: str
    lm_cc_dir: str                   # lm-cc リポジトリからの相対パス
    jsonl: Optional[str] = None      # xcodeeval の問題ファイル名 (lm_cc_dir 内)
    uid_field: Optional[str] = None
    code_field: Optional[str] = None


DATASETS: Dict[str, DatasetSpec] = {
    spec.name: spec
    for spec in [
        DatasetSpec("humaneval", "humaneval", TASK_IER, "dataset/humaneval"),
        DatasetSpec("humaneval_simplified-top60", "humaneval_simplified-top60", TASK_IER,
                    "dataset/humaneval_simplified-top60"),
        DatasetSpec("xcodeeval_apr", "xcodeeval/apr", TASK_APR, "dataset/xcodeeval/apr",
                    "xcodeeval_apr_test_filtered.jsonl", "bug_code_uid", "bug_source_code"),
        DatasetSpec("xcodeeval_simplified-top50_apr", "xcodeeval_simplified-top50/apr", TASK_APR,
                    "dataset/xcodeeval/apr", "xcodeeval_apr_test_filtered-simplified-top50.jsonl",
                    "bug_code_uid", "bug_source_code"),
        DatasetSpec("xcodeeval_code_translation", "xcodeeval/code_translation", TASK_CT,
                    "dataset/xcodeeval/code_translation", "xcodeeval_codetranslation_test_filtered.jsonl",
                    "code_uid", "source_code"),
        DatasetSpec("xcodeeval_simplified-top50_code_translation", "xcodeeval_simplified-top50/code_translation",
                    TASK_CT, "dataset/xcodeeval/code_translation",
                    "xcodeeval_codetranslation_test_filtered_simplified-top50.jsonl", "code_uid", "source_code"),
    ]
}


def get_dataset(name: str) -> DatasetSpec:
    if name not in DATASETS:
        raise ValueError(f"未対応の dataset: {name!r} (対応: {', '.join(DATASETS)})")
    return DATASETS[name]


def data_dir(spec: DatasetSpec) -> Path:
    return paths.DATA_DIR / spec.data_subdir


def list_ids(spec: DatasetSpec) -> List[str]:
    return sorted(p.stem for p in data_dir(spec).glob("*.py"))


def source_path(spec: DatasetSpec, uid: str) -> Path:
    return data_dir(spec) / f"{uid}.py"


def lm_cc_dir(spec: DatasetSpec) -> Path:
    return paths.LM_CC_ROOT / spec.lm_cc_dir


@lru_cache(maxsize=None)
def _jsonl_index(path_str: str, uid_field: str) -> Dict[str, dict]:
    index: Dict[str, dict] = {}
    with open(path_str, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                index[str(record.get(uid_field))] = record
    return index


def xcodeeval_record(spec: DatasetSpec, uid: str) -> Optional[dict]:
    """xcodeeval の問題レコード (jsonl の1行)。見つからなければ None。"""
    path = lm_cc_dir(spec) / spec.jsonl
    if not path.exists():
        return None
    return _jsonl_index(str(path), spec.uid_field).get(uid)


def humaneval_case_dirs(spec: DatasetSpec, uid: str) -> List[Path]:
    """``<ID>``, ``<ID>__0``, ``<ID>__1`` のうち存在するディレクトリ (接尾辞なしが先頭)。"""
    root = lm_cc_dir(spec)
    dirs = [root / uid] + sorted(root.glob(f"{uid}__*"))
    return [d for d in dirs if (d / "main.py").exists()]


def task_code(spec: DatasetSpec, uid: str) -> Optional[str]:
    """lm-cc がプロンプトに入れる元コード (計測用ソースと同じ内容か確認するため)。

    - IER: ``main.py`` を ``strip("\\n")`` したもの (lm-cc ``tasks/ier/ier.py``)
    - APR / CT: jsonl のコード欄
    """
    if spec.task == TASK_IER:
        dirs = humaneval_case_dirs(spec, uid)
        if not dirs:
            return None
        return dirs[0].joinpath("main.py").read_text(encoding="utf-8").strip("\n")
    record = xcodeeval_record(spec, uid)
    if record is None:
        return None
    return record.get(spec.code_field)


def cases_with_same_code(spec: DatasetSpec, uid: str, source: str) -> Optional[List[str]]:
    """IER: ``main.py`` が計測用ソースと同じ内容のケースディレクトリ名 (前後の改行は無視)。

    lm-cc の HumanEval は ``<ID>`` と ``<ID>__0`` / ``<ID>__1`` で ``main.py`` の書き方が違うことがあり、
    data/humaneval/ はどちらかをコピーしたものなので、先行研究の pass@1 (接尾辞なしのケース) の
    プロンプトに入ったコードと計測用ソースが一致しているとは限らない。
    """
    if spec.task != TASK_IER:
        return None
    target = source.strip("\n")
    return [d.name for d in humaneval_case_dirs(spec, uid)
            if d.joinpath("main.py").read_text(encoding="utf-8").strip("\n") == target]
