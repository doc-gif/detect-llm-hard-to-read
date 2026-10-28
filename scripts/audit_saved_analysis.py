"""Recompute saved analysis without inference and write to a new directory only."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'src'), str(ROOT / 'src' / 'analysis')]

import numpy as np
import pandas as pd
import scipy
from src.analysis import semantic_unit_threshold_analysis as threshold
from src.analysis import semantic_unit_model_comparison as models
from src.analysis.score_io import audit_humaneval_code, load_scores, new_output_dir
from src.analysis.util.correlation import get_grouped_partial_corr, group_by_metric


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def legacy_join(summary):
    """Reproduce the pre-fix full-ID truncation solely for the audit comparison."""
    frames = []
    for ds, config in threshold.SCORE_FILES.items():
        raw = json.loads(Path(config['path']).read_text())
        scores = {uid.split('__')[0]: value for uid, value in raw.items()} if config['format'] == 'simple' else {
            uid: value.get('pass@1', 0.0) for uid, value in raw.items()}
        frame = summary.loc[summary.dataset == ds].copy()
        frame['pass_at_1'] = frame.uid.map(scores)
        frames.append(frame.dropna(subset=['num_semantic_units', 'pass_at_1']))
    return pd.concat(frames, ignore_index=True)


def fit_rows(frame):
    rows = []
    scopes = [('all', frame)] + list(frame.groupby('dataset'))
    for scope, subset in scopes:
        x, y = subset.num_semantic_units.to_numpy(float), subset.pass_at_1.to_numpy(float)
        fits = [fit(x, y) for fit in [models.fit_linear, models.fit_hinge, models.fit_step, models.fit_logistic]]
        for fit in fits:
            if fit is not None:
                aic, bic = models.compute_aic_bic(fit['rss'], len(subset), fit['k_params'])
                rows.append(dict(scope=scope, model=fit['name'], n=len(subset), rss=fit['rss'], aic=aic, bic=bic))
    scopes = [('all_dataset_controlled', frame),
              ('dataset_controlled_excl_humaneval', frame.loc[frame.dataset != 'humaneval'])]
    for scope, subset in scopes:
        x, y = subset.num_semantic_units.to_numpy(float), subset.pass_at_1.to_numpy(float)
        for fitting in [models.fit_linear_with_dataset, models.fit_hinge_with_dataset, models.fit_logistic_with_dataset]:
            fit = fitting(x, y, subset.dataset)
            if fit is not None:
                aic, bic = models.compute_aic_bic(fit['rss'], len(subset), fit['k_params'])
                rows.append(dict(scope=scope, model=fit['name'], n=len(subset), rss=fit['rss'], aic=aic, bic=bic))
    return pd.DataFrame(rows)


def compare_frames(calculated, stored, keys):
    joint = calculated.merge(stored, on=keys, suffixes=['_calculated', '_stored'], validate='one_to_one', how='outer', indicator=True)
    report = {'calculated_rows': len(calculated), 'stored_rows': len(stored), 'unmatched_keys': int((joint['_merge'] != 'both').sum())}
    for column in sorted(set(calculated.columns) & set(stored.columns) - set(keys)):
        if pd.api.types.is_numeric_dtype(calculated[column]) and pd.api.types.is_numeric_dtype(stored[column]):
            a, b = joint[column + '_calculated'], joint[column + '_stored']
            difference = ~np.isclose(a, b, rtol=1e-9, atol=1e-10, equal_nan=True)
            report[column] = {'different_rows': int(difference.sum()), 'max_absolute_difference': float((a-b).abs().max())}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True, help='New directory; existing paths are rejected.')
    args = parser.parse_args()
    out = new_output_dir(ROOT / 'results' / 'audit', args.output_dir)
    report = {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__,
              'scipy': scipy.__version__, 'score_id_policy': 'exact full ID; no averaging across question variants',
              'code_policy': 'exclude HumanEval AST mismatch; retain exact or AST-equal main.py',
              'historical_outputs': 'read only; no model inference, download or API calls'}
    sources = [Path(config['path']) for config in threshold.SCORE_FILES.values()]
    unused, changed = [], []
    for percentile in [67, 80]:
        path = ROOT / 'results' / 'summaries' / f'analysis_summary_p{percentile}.csv'
        sources.append(path)
        summary = pd.read_csv(path)
        old = legacy_join(summary)
        old.to_csv(out / f'legacy_join_p{percentile}.csv', index=False)
        new = threshold.load_and_merge_summary(path)
        new.to_csv(out / f'corrected_join_p{percentile}.csv', index=False)
        codes = pd.DataFrame(audit_humaneval_code(summary.loc[summary.dataset == 'humaneval']))
        codes.to_csv(out / f'code_identity_p{percentile}.csv', index=False)
        exact_frames = []
        for ds, config in threshold.SCORE_FILES.items():
            scores = load_scores(ds, config)
            exact = old.loc[old.dataset == ds, ['dataset', 'uid', 'pass_at_1']].rename(columns={'pass_at_1': 'legacy_score'})
            exact['exact_id_score'] = exact.uid.map(scores)
            exact['included_after_code_check'] = exact.uid.isin(new.loc[new.dataset == ds, 'uid'])
            exact['changed_score'] = ~np.isclose(exact.legacy_score, exact.exact_id_score)
            exact['percentile'] = percentile
            changed.extend(exact.to_dict('records'))
            present = set(summary.loc[summary.dataset == ds, 'uid'])
            for uid in sorted(set(scores) - present):
                unused.append({'percentile': percentile, 'dataset': ds, 'uid': uid,
                               'reason': 'no full-ID metric row', 'score': scores[uid]})
        tables = out / f'corrected_bins_p{percentile}'; tables.mkdir()
        for width in [1, 5, 10]:
            for label, subset in [('all', new)] + list(new.groupby('dataset')):
                threshold.build_frequency_table(subset, width).to_csv(tables / f'bin{width}_{label}.csv', index=False)
        report[f'p{percentile}'] = {'summary_rows': len(summary), 'legacy_join_rows': len(old),
                                  'corrected_join_rows': len(new), 'corrected_dataset_counts': new.dataset.value_counts().to_dict(),
                                  'excluded_datasets': summary.loc[~summary.dataset.isin(threshold.SCORE_FILES), 'dataset'].value_counts().to_dict()}
    pd.DataFrame(changed).to_csv(out / 'score_join_comparison.csv', index=False)
    pd.DataFrame(unused).to_csv(out / 'unmatched_score_ids.csv', index=False)
    saved_path = ROOT / 'results/semantic_unit_binning/analysis_summary_p80_with_score.csv'
    sources.append(saved_path)
    saved = pd.read_csv(saved_path)
    report['current_p80_vs_saved_merged'] = compare_frames(old, saved, ['dataset', 'uid'])
    report['saved_bin_tables'] = {}
    for width in [1, 5, 10]:
        for label, subset in [('all', saved)] + list(saved.groupby('dataset')):
            path = ROOT / 'results/semantic_unit_binning/tables' / f'bin{width}_{label}_freq_table.csv'
            sources.append(path)
            report['saved_bin_tables'][path.name] = compare_frames(threshold.build_frequency_table(subset, width), pd.read_csv(path), ['bin_start', 'bin_end'])
    model_path = ROOT / 'results/semantic_unit_model_comparison/tables/model_comparison_summary.csv'
    sources.append(model_path)
    fits = fit_rows(saved)
    fits.to_csv(out / 'recomputed_historical_models.csv', index=False)
    report['saved_models'] = compare_frames(fits, pd.read_csv(model_path), ['scope', 'model'])
    # Preserve the legacy grouping/search rule; only quantify the plotting tail bug.
    group_rows = []
    undefined_combinations = []
    for version, frame in [('legacy_score', old), ('corrected_score', new)]:
        for ds, subset in frame.groupby('dataset'):
            for metric in ['num_semantic_units', 'lm_cc']:
                y, x, z = subset.pass_at_1.to_numpy(), subset[metric].to_numpy(), subset['loc'].to_numpy()
                for control, covariate in [('none', None), ('loc', z)]:
                    with warnings.catch_warnings(record=True) as caught:
                        warnings.simplefilter("always")
                        result, size = get_grouped_partial_corr(y, x, covariate)
                    if size is None:
                        undefined_combinations.append(dict(
                            version=version, dataset=ds, metric=metric, control=control, n=len(subset),
                            status="no_valid_groups",
                            reason="No defined correlation among the 9-to-11-group candidates"))
                        continue
                    my, _, mx, counts = group_by_metric(y, x, None, size)
                    fy, _, fx, kept = group_by_metric(y, x, None, size, include_incomplete=False)
                    group_rows.append(dict(version=version, dataset=ds, metric=metric, control=control,
                        n=len(subset), min_count=size, valid_groups=result['valid_groups'],
                        covariance_warning_count=sum("rank-deficient" in str(w.message) for w in caught),
                        omitted_tail=len(subset)-sum(kept), spearman_r=result['partial_correlation']['spearman-r'],
                        nominal_p=result['partial_correlation']['spearman-pval'],
                        old_plot_slope=float(np.polyfit(mx, my, 1)[0]),
                        same_groups_plot_slope=float(np.polyfit(fx, fy, 1)[0])))
    pd.DataFrame(group_rows).to_csv(out / 'legacy_group_search_and_plot_tail.csv', index=False)
    (out / 'undefined_combinations.json').write_text(json.dumps(undefined_combinations, indent=2))
    report['undefined_combinations'] = undefined_combinations
    report['source_sha256'] = {str(path): sha256(path) for path in sources}
    report['png_provenance'] = 'Filenames and Git revisions identify likely producers; PNG pixels and original run commands are unverified.'
    (out / 'audit_report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({'output_dir': str(out), 'p67': report['p67'], 'p80': report['p80'], 'saved_models': report['saved_models']}, indent=2))


if __name__ == '__main__':
    main()
