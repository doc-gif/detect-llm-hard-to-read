from analysis.scores import parse_scores


def test_simple_format_uses_unsuffixed_key_like_prior_study():
    # HumanEval は 1 問 3 キー。先行研究 (lm-cc) は接尾辞なしのキーを使う
    data = {"HumanEval_1": 1.0, "HumanEval_1__0": 0.0, "HumanEval_1__1": 0.0, "HumanEval_2__0": 0.4, "HumanEval_2": 0.6}
    assert parse_scores(data, "simple") == {"HumanEval_1": 1.0, "HumanEval_2": 0.6}


def test_nested_format_reads_pass_at_1():
    data = {"abc": {"task_id": "abc", "pass@1": 0.2, "pass@3": 0.5}, "def": {}}
    assert parse_scores(data, "nested") == {"abc": 0.2, "def": 0.0}
