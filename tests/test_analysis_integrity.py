import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from src.analysis.score_io import load_scores, validate_summary_ids, new_output_dir, audit_humaneval_code
from src.analysis.semantic_unit_threshold_analysis import build_frequency_table
from src.analysis.semantic_unit_model_comparison import compare_models, compute_aic_bic
from src.analysis.util.correlation import group_by_metric, grouped_partial_corr


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'scores.json'

    def load(self, data, format='simple'):
        self.path.write_text(json.dumps(data))
        return load_scores('fixture', {'path': self.path, 'format': format})

    def test_variants_keep_full_id_and_exact_base_score(self):
        scores = self.load({'HumanEval_0': 0.6, 'HumanEval_0__0': 0.0, 'HumanEval_0__1': 1.0})
        self.assertEqual(scores['HumanEval_0'], 0.6)
        self.assertEqual(len(scores), 3)

    def test_missing_id_check_keeps_distinct_question_ids(self):
        from src.analysis.check_missing_data import load_expected_uids
        self.path.write_text(json.dumps({'HumanEval_0': 0.6, 'HumanEval_0__0': 1.0}))
        ids = load_expected_uids('fixture', {'path': self.path, 'format': 'simple'})
        self.assertEqual(ids, {'HumanEval_0', 'HumanEval_0__0'})

    def test_missing_score_is_excluded_not_zero(self):
        self.assertEqual(self.load({'missing': {}, 'incorrect': {'pass@1': 0.0}}, 'nested'), {'incorrect': 0.0})

    def test_duplicate_json_ids_are_rejected(self):
        self.path.write_text('{"id": 0, "id": 1}')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            load_scores('fixture', {'path': self.path, 'format': 'simple'})

    def test_invalid_score_is_rejected(self):
        for value in [float('nan'), -0.1, 1.1, '0.6']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.load({'id': value})

    def test_nested_id_mismatch_is_rejected(self):
        with self.assertRaises(ValueError):
            self.load({'id': {'task_id': 'other', 'pass@1': 0.6}}, 'nested')

    def test_duplicate_summary_id_is_rejected_within_dataset(self):
        with self.assertRaises(ValueError):
            validate_summary_ids(pd.DataFrame({'dataset': ['a', 'a'], 'uid': ['1', '1']}))
        validate_summary_ids(pd.DataFrame({'dataset': ['a', 'b'], 'uid': ['1', '1']}))

    def test_existing_output_directory_is_rejected(self):
        with self.assertRaises(FileExistsError):
            new_output_dir(self.path.parent, self.path.parent)

    def test_code_identity_ignores_spacing_but_detects_program_changes(self):
        measured = self.path.parent / 'measured'; measured.mkdir()
        scored = self.path.parent / 'scored'; scored.mkdir()
        for uid, code in [('same', 'x=1\n'), ('changed', 'x=2\n')]:
            (measured / f'{uid}.py').write_text('x = 1\n')
            (scored / uid).mkdir()
            (scored / uid / 'main.py').write_text(code)
        rows = audit_humaneval_code(pd.DataFrame({'uid': ['same', 'changed']}), measured, scored)
        self.assertEqual([r['code_status'] for r in rows], ['ast_equal', 'ast_mismatch'])


class AggregationTests(unittest.TestCase):
    def test_equal_width_boundaries_mean_and_sample_std(self):
        df = pd.DataFrame({'num_semantic_units': [0, 4, 5, 9, 10],
                           'pass_at_1': [0.0, 0.6, 0.2, 1.0, 0.8], 'lm_cc': [1, 2, 3, 4, 5]})
        result = build_frequency_table(df, 5)
        np.testing.assert_allclose(result.loc[:2, 'pass_at_1_mean'], [0.3, 0.6, 0.8])
        np.testing.assert_array_equal(result.loc[:2, 'n'], [2, 2, 1])
        self.assertAlmostEqual(result.loc[0, 'pass_at_1_std'], np.std([0, 0.6], ddof=1))
        self.assertTrue(np.isnan(result.loc[2, 'pass_at_1_std']))
        self.assertEqual(result['n'].sum(), len(df))

    def test_frequency_table_without_optional_lmcc(self):
        result = build_frequency_table(pd.DataFrame({'num_semantic_units': [1], 'pass_at_1': [0.6]}), 1)
        self.assertNotIn('lm_cc_mean', result)

    def test_plot_representatives_drop_the_same_tail_as_correlation(self):
        score, metric = [1, 1, 0, 0, 1], [1, 2, 3, 4, 100]
        means, _, medians, counts = group_by_metric(score, metric, None, 2, include_incomplete=False)
        self.assertEqual(means, [1, 0])
        self.assertEqual(medians, [1.5, 3.5])
        self.assertEqual(counts, [2, 2])
        self.assertEqual(grouped_partial_corr(score, metric, min_cnt=2)['valid_groups'], len(means))

    def test_missing_step_fit_does_not_crash_model_comparison(self):
        df = pd.DataFrame({'num_semantic_units': [1, 2, 3], 'pass_at_1': [0.2, 0.6, 1.0]})
        with patch('src.analysis.semantic_unit_model_comparison.fit_step', return_value=None), \
             patch('src.analysis.semantic_unit_model_comparison.fit_logistic', return_value=None), \
             patch('src.analysis.semantic_unit_model_comparison.plot_model_comparison'):
            result = compare_models(df, 'fixture')
        self.assertEqual(set(result['model']), {'linear', 'hinge'})

    def test_partial_corr_supports_current_pingouin_column(self):
        frame = pd.DataFrame({'x': [1, 5, 3, 9, 2, 6], 'y': [4, 3, 1, 2, 5, 6],
                              'z': [9, 2, 1, 4, 7, 8]})
        with patch('src.analysis.util.correlation.pg.partial_corr',
                   return_value=pd.DataFrame({'r': [0.25], 'p_val': [0.75]})):
            result = grouped_partial_corr(frame.y, frame.x, frame.z, min_cnt=1)
        self.assertEqual(result['partial_correlation'], {'spearman-r': 0.25, 'spearman-pval': 0.75})

    def test_partial_fallback_uses_one_covariate_degree_of_freedom(self):
        frame = pd.DataFrame({'x': [1, 5, 3, 9, 2, 6], 'y': [4, 3, 1, 2, 5, 6],
                              'z': [9, 2, 1, 4, 7, 8]})
        import pingouin as pg
        expected = pg.partial_corr(frame, x='x', y='y', covar='z', method='spearman')
        with patch('src.analysis.util.correlation.pg.partial_corr', side_effect=RuntimeError):
            result = grouped_partial_corr(frame.y, frame.x, frame.z, min_cnt=1)['partial_correlation']
        self.assertAlmostEqual(result['spearman-r'], expected.r.iloc[0])
        self.assertAlmostEqual(result['spearman-pval'], expected['p_val'].iloc[0])

    def test_partial_corr_rejects_zero_rank_residual_variance(self):
        x, y = [1, 2, 3, 4, 5, 6], [4, 3, 1, 2, 5, 6]
        for z in [x, [1] * 6]:
            with self.subTest(z=z), patch('src.analysis.util.correlation.pg.partial_corr') as pg_call:
                result = grouped_partial_corr(y, x, z, min_cnt=1)['partial_correlation']
                self.assertIsNone(result['spearman-r'])
                self.assertIsNone(result['spearman-pval'])
                pg_call.assert_not_called()

    def test_gaussian_aic_counts_noise_variance(self):
        aic, bic = compute_aic_bic(10, 20, 2)
        self.assertAlmostEqual(aic, 20 * np.log(0.5) + 2 * 3)
        self.assertAlmostEqual(bic, 20 * np.log(0.5) + 3 * np.log(20))


if __name__ == '__main__':
    unittest.main()
