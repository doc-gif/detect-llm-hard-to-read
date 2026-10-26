import paths


def test_resolve_data_path_remaps_foreign_absolute_path():
    foreign = "/Users/someone/elsewhere/detect-llm-hard-to-read/data/humaneval/HumanEval_0.py"
    resolved = paths.resolve_data_path(foreign)
    assert resolved == paths.DATA_DIR / "humaneval" / "HumanEval_0.py"
    assert resolved.exists()


def test_resolve_data_path_keeps_unknown_path():
    assert str(paths.resolve_data_path("/nonexistent/file.py")) == "/nonexistent/file.py"


def test_summary_csv_naming():
    assert paths.summary_csv("_p67").name == "analysis_summary_p67.csv"
    assert paths.summary_csv().name == "analysis_summary.csv"
