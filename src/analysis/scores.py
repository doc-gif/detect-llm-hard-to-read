"""LLM の正答率 (pass@1) スコアの読み込み。

pass@1 は先行研究リポジトリ lm-cc の ``results/`` 配下にあるので、
:data:`paths.LM_CC_RESULTS_DIR` を基点に参照する。

以前は各分析スクリプトが ``SCORE_FILES`` と ``load_scores`` を個別に
コピーして持っていたが、ここに集約した。
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Optional

from paths import LM_CC_RESULTS_DIR

logger = logging.getLogger(__name__)

#: データセット名 (summary CSV の ``dataset`` 列) -> スコアファイルの設定
#:   - ``simple``: ``{"HumanEval_0": 1.0, "HumanEval_0__0": 1.0, ...}``
#:   - ``nested``: ``{"<uid>": {"pass@1": 0.5, ...}, ...}``
SCORE_FILES: Dict[str, dict] = {
    "humaneval": {
        "path": LM_CC_RESULTS_DIR / "humaneval-ier" / "results_score.json",
        "format": "simple",
    },
    "humaneval_simplified-top60": {
        "path": LM_CC_RESULTS_DIR / "humaneval-ier-simplified" / "results_score_simplified.json",
        "format": "simple",
    },
    "xcodeeval_apr": {
        "path": LM_CC_RESULTS_DIR / "xcodeeval" / "apr" / "python_test_filtered_results.json",
        "format": "nested",
    },
    "xcodeeval_simplified-top50_apr": {
        "path": LM_CC_RESULTS_DIR / "xcodeeval" / "apr-simplified" / "python_test_filtered_results.json",
        "format": "nested",
    },
    "xcodeeval_code_translation": {
        "path": LM_CC_RESULTS_DIR / "xcodeeval" / "code_translation" / "python2c_test_filtered_results.json",
        "format": "nested",
    },
    "xcodeeval_simplified-top50_code_translation": {
        "path": LM_CC_RESULTS_DIR / "xcodeeval" / "code_translation-simplified" / "python2c_test_filtered_results.json",
        "format": "nested",
    },
}

#: 論文の主要3データセット (多くの分析スクリプトはこれだけを対象にする)
MAIN_DATASETS = ("humaneval", "xcodeeval_apr", "xcodeeval_code_translation")


def parse_scores(data: dict, fmt: str) -> Dict[str, float]:
    """スコア JSON の中身を ``{uid: pass@1}`` に変換する。

    ``simple`` 形式 (HumanEval) には ``HumanEval_80`` / ``HumanEval_80__0`` /
    ``HumanEval_80__1`` のように 1 問につき 3 つのキーがある。``__N`` 付きは
    同じコードに対する別の入出力ケースで、先行研究 (lm-cc の
    ``scripts/utils/lm_cc_correlation.py``) は接尾辞なしのキーのスコアを使う。
    ここでもそれに合わせて接尾辞なしのキーだけを採用する。

    (以前の実装は ``k.split("__")[0]`` で上書きしていたため、JSON 内で最後に
    現れた入出力ケースのスコアが使われていた。HumanEval では 162 問中 17 問で
    先行研究と異なるスコアになっていた。)
    """
    scores: Dict[str, float] = {}
    if fmt == "simple":
        for k, v in data.items():
            if "__" not in k:
                scores[k] = v
    elif fmt == "nested":
        for k, v in data.items():
            scores[k] = v.get("pass@1", 0.0)
    else:
        raise ValueError(f"Unknown score format: {fmt!r}")
    return scores


def load_scores(dataset_name: str, config: Optional[dict] = None) -> Dict[str, float]:
    """データセットの pass@1 を ``{uid: score}`` で返す。ファイルが無ければ空 dict。"""
    if config is None:
        if dataset_name not in SCORE_FILES:
            logger.warning("dataset '%s' のスコアファイルは未登録です (analysis/scores.py)", dataset_name)
            return {}
        config = SCORE_FILES[dataset_name]
    path = Path(config["path"])
    if not path.exists():
        logger.warning("スコアファイルが見つかりません (dataset=%s): %s", dataset_name, path)
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return parse_scores(data, config["format"])

