"""Regression tests for the saved-token block-tree exporter (no model needed)."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "src" / "analysis")]
import generate_block_tree as exporter
from macro.lm_cc_helper.code_block_processor import CodeBlockProcessor
from thresholds import SAVED_SUMMARY_THRESHOLDS


class BlockTreeExportTests(unittest.TestCase):
    def setUp(self):
        self.frame = pd.DataFrame({
            "token_str": ["x", "=", "1", "<0x0A>", "y", "=", "2", "<0x0A>"],
            "metric_entropy": [0.0, 0.8, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0],
        })

    def test_exports_real_helper_result_without_doubling_newlines(self):
        with patch.object(pd, "read_parquet", return_value=self.frame):
            result, task_id = exporter.process_parquet_to_blocktree(
                Path("result_example.parquet"), CodeBlockProcessor()
            )
        self.assertEqual(task_id, "example")
        self.assertEqual(result["code"], "x=1\ny=2\n")
        self.assertEqual(result["num_semantic_units"], 3)
        self.assertEqual(result["entropy_threshold"], 0.67)
        self.assertEqual(result["block_tree"]["block_code"], "x=1\ny=2")

    def test_preserves_explicit_entropy_threshold(self):
        with patch.object(pd, "read_parquet", return_value=self.frame):
            result, _ = exporter.process_parquet_to_blocktree(
                Path("result_example.parquet"), CodeBlockProcessor(), threshold=1.0
            )
        self.assertEqual(result["num_semantic_units"], 1)
        self.assertEqual(result["entropy_threshold"], 1.0)
        self.assertEqual(result["block_tree"]["children"], [])

    def test_saved_p80_threshold_reproduces_stored_semantic_units(self):
        # This file distinguishes the saved p80 threshold from the old 1.2515 label.
        source = ROOT / "out" / "humaneval" / "result_HumanEval_106.parquet"
        summary = pd.read_csv(ROOT / "results" / "summaries" / "analysis_summary_p80.csv")
        expected = summary.loc[
            (summary["dataset"] == "humaneval") & (summary["uid"] == "HumanEval_106"),
            "num_semantic_units",
        ].item()
        result, _ = exporter.process_parquet_to_blocktree(
            source, CodeBlockProcessor(), threshold=SAVED_SUMMARY_THRESHOLDS["p80"]
        )
        self.assertEqual(result["num_semantic_units"], expected)

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input"
            source.mkdir()
            (source / "result_example.parquet").touch()
            target = root / "output" / "example"
            target.mkdir(parents=True)
            existing = target / "block_tree_example.json"
            existing.write_text("original")
            with patch.object(exporter, "DATA_DIRECTORIES", {"example": source}), \
                 patch.object(exporter, "OUTPUT_BASE_DIR", root / "output"), \
                 patch.object(pd, "read_parquet", return_value=self.frame), \
                 patch("builtins.print"):
                exporter.main()
            self.assertEqual(existing.read_text(), "original")


if __name__ == "__main__":
    unittest.main()
