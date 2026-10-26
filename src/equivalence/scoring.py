"""lm-cc の採点処理の移植 (正解との比較方法を先行研究と揃えるため)。

- IER (HumanEval): ``scripts/tasks/ier/parse_result.py`` の ``parse_chatgpt`` と ``get_result``
- xcodeeval (APR / CT): ``scripts/tasks/evaluate_apr.py`` の ``_run_code_in_subprocess``
  (stdout を strip して1要素のリストにし、テストの ``output`` と比較)

挙動を変えるときは lm-cc 側の実装と比較してから。
"""
from __future__ import annotations

from typing import List


def extract_ier_prediction(response: str) -> str:
    """回答から予測値を取り出す (lm-cc ``parse_chatgpt``)。

    deepseek-v3 / gpt 系はこの処理 (``<<<Output>>>`` 以降、``[END-OF-RESPONSE]`` まで)。
    """
    return response.split("<<<Output>>>")[-1].split("[END-OF-RESPONSE]")[0]


def normalize_ier_answer(text: str) -> str:
    """予測値・正解の正規化 (lm-cc ``get_result``)。"""
    text = text.replace("\n", "").replace(" ", "").replace('"', "'")
    if text.startswith("'") or text.startswith("`"):
        text = text[1:]
    if text.endswith("'") or text.endswith("`"):
        text = text[:-1]
    return text


def ier_is_correct(prediction: str, ground_truth: str) -> bool:
    """lm-cc ``get_result`` と同じ判定。"""
    predict = normalize_ier_answer(prediction).replace("[END-OF-RESPONSE]", "")
    return predict == normalize_ier_answer(ground_truth)


def xcodeeval_output_matches(stdout: str, expected: List[str]) -> bool:
    """lm-cc ``evaluate_apr._run_code_in_subprocess`` と同じ比較。"""
    actual = stdout.strip()
    actual_list = [actual] if actual else []
    return actual_list == expected


def pass_at_1(n_correct: int, n_trials: int) -> float:
    """pass@1 (lm-cc の ``1 - C(n-c, 1) / C(n, 1)`` は c / n と同じ)。"""
    return n_correct / n_trials if n_trials else 0.0
