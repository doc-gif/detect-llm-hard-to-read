"""Exploratory fractional-logit analysis of audited, saved SU/score records.

Prepare freezes outcome-blind SU cutpoints and diagnostics before fit runs.
No inference API, entropy model, historic output write, or regularized fit is used.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import platform
from pathlib import Path
import re
import subprocess
import sys
import warnings

import numpy as np
import pandas as pd
import scipy
from scipy import optimize, special, stats
from scipy.spatial import Delaunay, QhullError
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.sandwich_covariance import cov_cluster

DATASETS = {'humaneval': 158, 'xcodeeval_apr': 271,
            'xcodeeval_code_translation': 535}
LABELS = {'humaneval': 'HumanEval', 'xcodeeval_apr': 'APR',
          'xcodeeval_code_translation': 'Translation'}
THRESHOLDS = {'p67': 0.6813, 'p80': 1.3238}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object)


def write_json(path, data):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def recover_count(score, n):
    if not isinstance(n, int) or n <= 0 or not np.isfinite(score) or not 0 <= score <= 1:
        raise ValueError('Invalid score or observed trial count')
    k = round(score * n)
    if not np.isclose(k / n, score, atol=1e-10, rtol=0):
        raise ValueError('Score does not correspond to an integer success count')
    return int(k)


def tercile_cuts(su):
    values = np.asarray(su, float)
    q = np.quantile(values, [1/3, 2/3], method='linear')
    # A tie is never split. Extreme/duplicate boundaries cannot create empty bins.
    cuts = sorted({float(x) for x in q if values.min() <= x < values.max()})
    return cuts


def assign_intervals(su, cuts):
    return np.searchsorted(np.asarray(cuts), np.asarray(su), side='left').astype(int)


def normalize_newlines(s):
    return s.replace('\r\n', '\n').replace('\r', '\n')


def code_identity(measured, scored):
    if normalize_newlines(measured) == normalize_newlines(scored):
        return 'exact_normalized_newlines'
    try:
        if ast.dump(ast.parse(measured), include_attributes=False) == ast.dump(
                ast.parse(scored), include_attributes=False):
            return 'ast_equal'
    except SyntaxError:
        return 'syntax_error_and_text_mismatch'
    return 'ast_mismatch'


def decode_tokens(tokens):
    source = ''.join(tokens).replace('▁', ' ')
    chunks = re.split(r'(<0x[0-9A-Fa-f]{2}>)', source)
    raw = b''.join(bytes([int(x[3:5], 16)]) if re.fullmatch(r'<0x[0-9A-Fa-f]{2}>', x)
                   else x.encode('utf-8') for x in chunks)
    return raw.decode('utf-8')


def describe(frame, keys):
    rows = []
    for key, sub in frame.groupby(keys, observed=True):
        key = key if isinstance(key, tuple) else (key,)
        row = dict(zip(keys, key))
        row.update(n_codes=len(sub), n_clusters=sub.cluster_id.nunique(),
                   error_codes=int((sub.k < sub.n).sum()),
                   all_correct_codes=int((sub.k == sub.n).sum()),
                   all_incorrect_codes=int((sub.k == 0).sum()),
                   mixed_codes=int(((sub.k > 0) & (sub.k < sub.n)).sum()),
                   su_unique=sub.su.nunique(), accuracy_unique=sub.y.nunique(),
                   spearman_su_loc=float(stats.spearmanr(sub.su, sub['loc']).statistic))
        for name in ['su', 'loc', 'k', 'n', 'y']:
            a = sub[name]
            row.update({f'{name}_{q}': float(v) for q,v in zip(
                ['min','q25','median','q75','max'], a.quantile([0,.25,.5,.75,1]))})
            row[f'{name}_mean'] = float(a.mean())
            row[f'{name}_sd'] = float(a.std(ddof=1))
        rows.append(row)
    return pd.DataFrame(rows)


def prepare(detect, lmcc, output):
    output.mkdir(parents=True, exist_ok=False)
    inputs = {}
    def track(p):
        p = Path(p).resolve()
        inputs[str(p)] = sha(p)
        return p
    audit = detect/'results/audit/2026-10-19-analysis-final'
    source_frames = {}
    for label in THRESHOLDS:
        df = pd.read_csv(track(audit/f'corrected_join_{label}.csv'))
        assert df.groupby('dataset').size().to_dict() == DATASETS
        assert not df.duplicated(['dataset','uid']).any()
        assert not df[['dataset','uid','num_semantic_units','loc','pass_at_1']].isna().any().any()
        assert (df[['num_semantic_units','loc']] > 0).all().all()
        assert np.isfinite(df[['num_semantic_units','loc','pass_at_1']]).all().all()
        summary = pd.read_csv(track(detect/f'results/summaries/analysis_summary_{label}.csv'))
        both = df.merge(summary, on=['dataset','uid'], validate='one_to_one', suffixes=['','_summary'])
        assert len(both) == 964
        for col in ['num_semantic_units','loc']:
            np.testing.assert_array_equal(both[col], both[col+'_summary'])
        source_frames[label] = df
    base = source_frames['p67'].sort_values(['dataset','uid']).reset_index(drop=True)
    other = source_frames['p80'].sort_values(['dataset','uid']).reset_index(drop=True)
    for col in ['dataset','uid','pass_at_1','loc']:
        pd.testing.assert_series_equal(base[col], other[col])

    trial_maps = []
    for trial in range(1,6):
        path = track(lmcc/f'results/humaneval-ier/initial-output/result-humaneval-{trial}.json')
        data = read_json(path)
        correct, incorrect = data['id_correct'], data['id_incorrect']
        assert len(correct) == len(set(correct)) and len(incorrect) == len(set(incorrect))
        assert not set(correct) & set(incorrect)
        trial_maps.append(dict([(x,1) for x in correct]+[(x,0) for x in incorrect]))
    assert all(set(x) == set(trial_maps[0]) for x in trial_maps)
    he_scores = read_json(track(lmcc/'results/humaneval-ier/results_score.json'))

    answers = {}
    descriptions = {}
    score_maps = {'humaneval': he_scores}
    for task, score_name in [('apr','python_test_filtered_results.json'),
                             ('code_translation','python2c_test_filtered_results.json')]:
        ds = 'xcodeeval_'+task
        score_maps[ds] = read_json(track(lmcc/'results/xcodeeval'/task/score_name))
        for path in sorted((lmcc/'results/xcodeeval'/task/'initial-output').glob('*.json')):
            record = read_json(track(path))
            source = record['source_data']
            uid = source['bug_code_uid' if task == 'apr' else 'code_uid']
            assert (ds,uid) not in answers
            choices = record['oai_response']['response']['choices']
            assert len(choices) == 5
            indices = [x.get('index') for x in choices]
            if all(x is not None for x in indices):
                assert len(set(indices)) == len(indices)
            answers[ds,uid] = (source, len(choices), path)
            desc = source['prob_desc_description']
            descriptions.setdefault((ds,source['src_uid']),set()).add(desc)
    assert all(len(x) == 1 for x in descriptions.values())
    for ds in ['xcodeeval_apr','xcodeeval_code_translation']:
        ds_descriptions = [next(iter(v)) for (d,k),v in descriptions.items() if d == ds]
        assert len(ds_descriptions) == len(set(ds_descriptions))

    helper = track(detect/'src/analysis/macro/lm_cc_helper/calculate_code_with_boudaries.py')
    spec = importlib.util.spec_from_file_location('saved_su_boundaries', helper)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    identities, counts = [], []
    for row in base.itertuples():
        ds, uid = row.dataset, row.uid
        if ds == 'humaneval':
            n = len(trial_maps)
            assert all(uid in x for x in trial_maps)
            k = sum(x[uid] for x in trial_maps)
            assert '__' not in uid
            codepath = track(lmcc/'dataset/humaneval'/uid/'main.py')
            scored = codepath.read_text()
            score = he_scores[uid]
            cluster = uid
            provenance = 'five_saved_binary_verdicts'
            data_path = detect/'data/humaneval'/f'{uid}.py'
        else:
            source,n,codepath = answers[ds,uid]
            scored = source['bug_source_code' if ds == 'xcodeeval_apr' else 'source_code']
            record = score_maps[ds][uid]
            assert record['task_id'] == uid
            score = record['pass@1']; k = recover_count(score,n)
            cluster = source['src_uid']
            provenance = 'integer_count_recovered_from_pass_at_1_with_five_saved_choices'
            task = ds.removeprefix('xcodeeval_')
            data_path = detect/'data/xcodeeval'/task/f'{uid}.py'
        assert n == 5 and np.isclose(k/n, row.pass_at_1, atol=1e-10, rtol=0)
        assert np.isclose(score,row.pass_at_1,atol=1e-10,rtol=0)
        measured = track(data_path).read_text()
        identity = code_identity(measured,scored)
        if identity not in ['exact_normalized_newlines','ast_equal']:
            raise ValueError(f'Code identity not verified: {ds}/{uid}: {identity}')
        parquet = track(detect/'out'/ds/f'result_{uid}.parquet')
        tokens = pd.read_parquet(parquet)
        clean = tokens.loc[tokens.metric_surprisal.notna()]
        assert len(clean) == len(tokens) and clean.metric_entropy.notna().all()
        decoded = decode_tokens(clean.token_str.tolist())
        assert measured in (decoded, decoded[1:] if decoded.startswith(' ') else decoded)
        assert int(clean.line.max()) == row.loc
        su_values = {}
        for label, threshold in THRESHOLDS.items():
            su = module.get_code_with_boundaries(clean.token_str.tolist(),clean.metric_entropy.tolist(),threshold)[3]
            expected = source_frames[label].loc[(source_frames[label].dataset==ds)&(source_frames[label].uid==uid),'num_semantic_units'].item()
            assert su == expected
            su_values[label] = su
        identities.append(dict(dataset=ds,uid=uid,code_status=identity,
             measured_sha256=sha(data_path),scored_code_sha256=hashlib.sha256(scored.encode()).hexdigest(),
             scored_source=str(codepath),parquet=str(parquet),su_p67=su_values['p67'],su_p80=su_values['p80'],
             loc_recomputed=int(clean.line.max()),unhandled_byte_tokens=bool(clean.token_str.str.contains(r'<0x(?!0A)[0-9A-Fa-f]{2}>',regex=True).any())))
        counts.append(dict(dataset=ds,uid=uid,k=k,n=n,y=k/n,cluster_id=cluster,count_provenance=provenance))
    count_frame = pd.DataFrame(counts)
    rows = []
    boundaries = {}
    for label,df in source_frames.items():
        df = df.merge(count_frame,on=['dataset','uid'],validate='one_to_one')
        df['threshold_label'] = label; df['entropy_threshold'] = THRESHOLDS[label]
        df['su'] = df.num_semantic_units
        df['logloc'] = np.log1p(df['loc'])
        for ds,sub in df.groupby('dataset'):
            cuts = tercile_cuts(sub.su)
            assigned = assign_intervals(sub.su,cuts)
            df.loc[sub.index,'interval'] = assigned
            boundaries[f'{label}/{ds}'] = dict(cuts=cuts,quantile_method='linear',
                assignment='right closed: SU <= cut1; cut1 < SU <= cut2; SU > cut2',
                interval_count=len(set(assigned)),su_min=int(sub.su.min()),su_max=int(sub.su.max()),
                centers={str(j):float(sub.loc[assigned==j,'su'].median()) for j in sorted(set(assigned))})
        df['interval'] = df.interval.astype(int);rows.append(df)
    final = pd.concat(rows,ignore_index=True).sort_values(['threshold_label','dataset','uid'])
    final.to_csv(output/'analysis_input.csv',index=False)
    pd.DataFrame(identities).to_csv(output/'code_identity.csv',index=False)
    exclusions = []
    for uid in ['HumanEval_1','HumanEval_105','HumanEval_124','HumanEval_150']:
        measured = track(detect/'data/humaneval'/f'{uid}.py').read_text()
        scored = track(lmcc/'dataset/humaneval'/uid/'main.py').read_text()
        assert code_identity(measured,scored) == 'ast_mismatch'
        exclusions.append(dict(dataset='humaneval',uid=uid,reason='measured_source_AST_differs_from_base_question',stage='prior_audit'))
    for uid in sorted(set(he_scores)-set(base.loc[base.dataset=='humaneval','uid'])-set(x['uid'] for x in exclusions)):
        exclusions.append(dict(dataset='humaneval',uid=uid,reason='derived_question_has_no_full_ID_metric',stage='prior_audit'))
    for ds in ['xcodeeval_apr','xcodeeval_code_translation']:
        for uid in sorted(set(score_maps[ds])-set(base.loc[base.dataset==ds,'uid'])):
            exclusions.append(dict(dataset=ds,uid=uid,reason='no_saved_metric_row',stage='prior_audit'))
    pd.DataFrame(exclusions).to_csv(output/'exclusions.csv',index=False)
    describe(final,['threshold_label','dataset']).to_csv(output/'descriptive.csv',index=False)
    describe(final,['threshold_label','dataset','interval']).to_csv(output/'interval_descriptive.csv',index=False)
    final.groupby(['threshold_label','dataset','k','n']).size().rename('n_codes').reset_index().to_csv(output/'count_distribution.csv',index=False)
    final.groupby(['threshold_label','dataset','cluster_id']).size().rename('n_codes').reset_index().to_csv(output/'cluster_sizes.csv',index=False)
    env = dict(python=platform.python_version(),platform=platform.platform(),numpy=np.__version__,
               pandas=pd.__version__,scipy=scipy.__version__,statsmodels=statsmodels.__version__)
    git = {name:dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
           status=subprocess.check_output(['git','-c','core.safecrlf=false','status','--porcelain','-uall'],cwd=repo,text=True))
           for name,repo in [('detect',detect),('lm-cc',lmcc)]}
    config = dict(created_at_utc=datetime.now(timezone.utc).isoformat(),analysis_status='exploratory_reanalysis_not_preregistered_or_independent_confirmation',
        prepared_before_regression=True,thresholds=THRESHOLDS,
        threshold_provenance={'p67':'0.6813; previous audit original 3 tasks 329534 token 67th percentile 0.6812911409',
            'p80':'1.3238 reproduces saved summaries; quantile source population unknown; sensitivity analysis'},
        primary_threshold='p67',primary_datasets=['xcodeeval_apr','xcodeeval_code_translation'],
        response='one code one row, k/n, Bernoulli quasi log likelihood; no frequency/variance n weights',
        models={'A':'intercept + SU/10','B':'intercept + SU/10 + log(1+LOC)',
                'interval_A':'interval-specific intercept and centered SU/10 slope',
                'interval_B':'interval-specific intercept and centered SU/10 slope + common log(1+LOC)'},
        loc_choice='log(1+LOC) is a choice for this reanalysis; LOC remains maximum token line after missing surprisal removal',
        su_definition='existing entropy-triggered line boundaries plus 1; unchanged helper',
        covariance='CR1 sandwich on sums of code scores by src_uid for APR/translation, base uid for HumanEval; correction G/(G-1)*(N-1)/(N-p); singleton clusters reduce to HC1 N/(N-p)',
        inference='two-sided t with G-1 df for scalar contrasts; joint Wald F(q,G-1); 95% pointwise delta-method confidence intervals, not simultaneous',
        multiplicity='one Holm family includes all global SU slopes, interval SU slopes, and joint equality-of-slopes tests across both thresholds, both A/B, all three tasks; nonestimable hypotheses retained at p=1 for family size; no p tests for probability contrasts or nuisance coefficients',
        boundaries=boundaries,
        diagnostic_rules=dict(min_interval_codes=20,min_interval_clusters=20,min_unique_su=3,
              min_codes_with_errors_for_stable_inference=5,min_codes_with_success_for_stable_inference=5,
              max_scaled_design_condition=1e6,
              max_hessian_condition=1e10,max_abs_eta=30,max_covariance_se=10,
              max_outside_hull_fraction=0.10),
        failure_policy='Fit the full specified interaction model. Separation/rank failure/nonconvergence is reported; no regularization or outcome-driven refit with omitted bins. Sparse/constant intervals are judgment difficult even if numeric fit exists.',
        prediction='A: marginal prediction; B: standardize to same observed LOC distribution in each task (global) or interval (local). Contrast SU q75 minus q25 within each interval; coefficient uncertainty only, empirical covariates fixed.',
        support='fraction of standardized SU-logLOC pairs outside convex hull of observed pairs in the matching task/interval; >10% at either endpoint marks the contrast judgment difficult; hull membership is necessary support screening, not proof of dense support',
        irls=dict(maxiter=200,tol=1e-10),input_files=inputs,
        analysis_input_sha256=sha(output/'analysis_input.csv'),script_sha256=sha(__file__),environment=env,git=git)
    write_json(output/'config.json',config)
    write_json(output/'input_checks.json',dict(codes_per_threshold=DATASETS,
        rechecked_metric_rows=1928,rechecked_code_rows=964,
        human_eval_all_correct=int(((count_frame.dataset=='humaneval')&(count_frame.k==5)).sum()),
        all_observed_n_five=bool((count_frame.n==5).all()),new_exclusions=0,
        counts_origin=count_frame.groupby('count_provenance').size().to_dict(),
        clusters=count_frame.groupby('dataset').cluster_id.nunique().to_dict(),
        description_cluster_consistency=True,missing_values=0,duplicate_keys=0))
    print(json.dumps(read_json(output/'input_checks.json'),ensure_ascii=False))
    print('Frozen cutpoints:',json.dumps(boundaries))


def separation_check(X, y):
    """LP recession-direction check; fractional interior rows require Xd=0."""
    X = np.asarray(X,float);y=np.asarray(y,float)
    scale = np.maximum(np.max(np.abs(X),axis=0),1)
    Z = X/scale
    endpoint = (y == 0) | (y == 1)
    A = (2*y[endpoint]-1)[:,None]*Z[endpoint]
    interior = Z[~endpoint]
    if not len(A):return 'none'
    res = optimize.linprog(-A.sum(axis=0), A_ub=-A,b_ub=np.zeros(len(A)),
        A_eq=interior if len(interior) else None,b_eq=np.zeros(len(interior)) if len(interior) else None,
        bounds=[(-1,1)]*X.shape[1],method='highs')
    if not res.success: return 'diagnostic_failed'
    if -res.fun < 1e-7:return 'none'
    if len(interior):return 'quasi_separation'
    complete = optimize.linprog(np.r_[np.zeros(X.shape[1]),-1],
        A_ub=np.column_stack([-A,np.ones(len(A))]),b_ub=np.zeros(len(A)),
        bounds=[(-1,1)]*X.shape[1]+[(0,1)],method='highs')
    return 'complete_separation' if complete.success and complete.x[-1]>1e-7 else 'quasi_separation'


def sandwich(X, y, mu, clusters):
    X=np.asarray(X,float);y=np.asarray(y,float);mu=np.asarray(mu,float)
    codes, levels = pd.factorize(clusters,sort=True)
    G=len(levels);N,p=X.shape
    if G<2 or N<=p:raise ValueError('Insufficient independent clusters or residual degrees of freedom')
    bread=X.T@((mu*(1-mu))[:,None]*X)
    inverse=np.linalg.inv(bread)
    scores=X*(y-mu)[:,None]
    sums=np.zeros((G,p));np.add.at(sums,codes,scores)
    correction=G/(G-1)*(N-1)/(N-p)
    covariance=correction*inverse@(sums.T@sums)@inverse
    return covariance,correction,G,bread


def design(sub, model, centers):
    interval_model=model.startswith('interval')
    adjusted=model.endswith('B')
    columns={}
    if interval_model:
        for j in sorted(sub.interval.unique()):
            indicator=(sub.interval.to_numpy()==j).astype(float)
            columns[f'intercept_{j}']=indicator
            columns[f'su10_{j}']=indicator*(sub.su.to_numpy()-centers[str(j)])/10
    else:
        columns={'intercept':np.ones(len(sub)),'su10':sub.su.to_numpy()/10}
    if adjusted:columns['logloc']=sub.logloc.to_numpy()
    return pd.DataFrame(columns,index=sub.index)


def scalar_contrast(beta, cov, contrast, dof):
    est=float(contrast@beta)
    se=float(np.sqrt(max(0,contrast@cov@contrast)))
    critical=stats.t.ppf(.975,dof)
    p=float(2*stats.t.sf(abs(est/se),dof)) if se>0 else np.nan
    return dict(estimate=est,se=se,ci_low=est-critical*se,ci_high=est+critical*se,p_raw=p)


def prediction(beta,cov,X,dof):
    prob=special.expit(np.asarray(X)@beta)
    mean=float(prob.mean());grad=np.mean(prob[:,None]*(1-prob[:,None])*X,axis=0)
    se=float(np.sqrt(max(0,grad@cov@grad)))
    critical=stats.t.ppf(.975,dof)
    # Logit-transform the marginal mean for a bounded, pointwise delta interval.
    den=max(mean*(1-mean),1e-15)
    lo,hi=special.expit(special.logit(np.clip(mean,1e-15,1-1e-15))+np.array([-1,1])*critical*se/den)
    return mean,se,float(lo),float(hi),grad


def outside_fraction(reference, su):
    points=reference[['su','logloc']].to_numpy(float)
    scale=points.std(axis=0)
    if np.any(scale<1e-12):
        if reference.su.nunique()==1:return float(su != reference.su.iloc[0])
        return 0.0 if reference.su.min()<=su<=reference.su.max() else 1.0
    origin=points.mean(axis=0)
    try:
        hull=Delaunay((points-origin)/scale)
        targets=np.column_stack([np.repeat(su,len(reference)),reference.logloc])
        return float((hull.find_simplex((targets-origin)/scale,tol=1e-9)<0).mean())
    except QhullError:
        return 1.0


def diagnostic_reasons(sub,config):
    rules=config['diagnostic_rules'];reasons=[]
    if len(sub)<rules['min_interval_codes']:reasons.append('fewer_than_20_codes')
    if sub.cluster_id.nunique()<rules['min_interval_clusters']:reasons.append('fewer_than_20_clusters')
    if sub.su.nunique()<rules['min_unique_su']:reasons.append('fewer_than_3_distinct_SU')
    if sub.y.nunique()<2:reasons.append('constant_accuracy')
    if (sub.k<sub.n).sum()<rules['min_codes_with_errors_for_stable_inference']:reasons.append('fewer_than_5_error_codes')
    if (sub.k>0).sum()<rules['min_codes_with_success_for_stable_inference']:reasons.append('fewer_than_5_success_codes')
    return reasons


def fit_one(sub, model, config, label, ds, output):
    model_id=f'{label}__{ds}__{model}'
    centers=config['boundaries'][f'{label}/{ds}']['centers']
    Xdf=design(sub,model,centers);X=Xdf.to_numpy();y=sub.y.to_numpy()
    cols=list(Xdf.columns);G=sub.cluster_id.nunique()
    diag=dict(model_id=model_id,threshold_label=label,dataset=ds,model=model,n_codes=len(sub),
              n_clusters=G,n_parameters=X.shape[1],columns=cols,converged=False,status='not_fit',reasons=[])
    diag['rank']=int(np.linalg.matrix_rank(X))
    diag['separation']=separation_check(X,y)
    scale=np.sqrt((X*X).mean(axis=0));diag['scaled_design_condition']=float(np.linalg.cond(X/scale))
    if diag['rank']<X.shape[1]:diag['reasons'].append('rank_deficient')
    if diag['separation']!='none':diag['reasons'].append(diag['separation'])
    if diag['reasons']:
        diag['status']='not_estimable';return diag,None
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        try:
            result=sm.GLM(y,X,family=sm.families.Binomial()).fit(maxiter=config['irls']['maxiter'],tol=config['irls']['tol'])
            beta=np.asarray(result.params);mu=np.asarray(result.fittedvalues)
            cov,factor,G,bread=sandwich(X,y,mu,sub.cluster_id.to_numpy())
            library_cov=cov_cluster(result,sub.cluster_id.to_numpy(),use_correction=True)
            np.testing.assert_allclose(cov,library_cov,rtol=1e-7,atol=1e-9)
            diag.update(converged=bool(result.converged),iterations=int(result.fit_history['iteration']),
                covariance_correction=float(factor),df_inference=int(G-1),
                sandwich_check_max_abs=float(np.max(np.abs(cov-library_cov))),
                hessian_condition=float(np.linalg.cond(bread)),max_abs_eta=float(np.max(np.abs(X@beta))),
                max_se=float(np.max(np.sqrt(np.diag(cov)))),score_max_abs=float(np.max(np.abs(X.T@(y-mu)))),
                response_mean=float(y.mean()),fitted_mean=float(mu.mean()),
                quasi_loglik=float(np.sum(y*(X@beta)-np.logaddexp(0,X@beta))),
                quasi_dispersion=float(np.sum((y-mu)**2/np.maximum(mu*(1-mu),1e-15))/(len(y)-X.shape[1])))
            # Independent Newton score root confirms coefficients; not an alternative estimator.
            root=optimize.root(lambda b:X.T@(y-special.expit(X@b)),beta,
                jac=lambda b:-(X.T@((special.expit(X@b)*(1-special.expit(X@b)))[:,None]*X)),method='hybr')
            diag['independent_score_root_max_abs']=float(np.max(np.abs(root.x-beta)))
            rules=config['diagnostic_rules']
            if not result.converged:diag['reasons'].append('nonconvergence')
            if diag['max_abs_eta']>rules['max_abs_eta']:diag['reasons'].append('extreme_linear_predictor')
            if diag['max_se']>rules['max_covariance_se']:diag['reasons'].append('large_standard_error')
            if diag['hessian_condition']>rules['max_hessian_condition']:diag['reasons'].append('ill_conditioned_hessian')
            if diag['scaled_design_condition']>rules['max_scaled_design_condition']:diag['reasons'].append('ill_conditioned_design')
            if diag['score_max_abs']>1e-6:diag['reasons'].append('nonzero_score')
            diag['warnings']=[str(x.message) for x in ws]
            diag['status']='unstable' if diag['reasons'] else 'estimated'
            artifact=dict(**diag,beta=beta.tolist(),covariance=cov.tolist(),centers=centers,
                          code_keys=sub[['dataset','uid']].to_dict('records'),
                          analysis_input_sha256=config['analysis_input_sha256'],config_sha256=sha(output.parent/'config.json'))
            write_json(output/'models'/f'{model_id}.json',artifact)
            pd.DataFrame(dict(uid=sub.uid,dataset=ds,threshold_label=label,model=model,y=y,fitted=mu,
                             interval=sub.interval,cluster_id=sub.cluster_id)).to_csv(output/'fitted'/f'{model_id}.csv',index=False)
            return diag,(beta,cov,cols,G-1,centers)
        except Exception as exc:
            diag['status']='not_estimable';diag['reasons'].append(type(exc).__name__+': '+str(exc))
            diag['warnings']=[str(x.message) for x in ws]
            return diag,None


def fit(run):
    config=read_json(run/'config.json')
    assert sha(run/'analysis_input.csv')==config['analysis_input_sha256']
    for path,digest in config['input_files'].items():
        assert sha(path)==digest, f'Input changed after prepare: {path}'
    output=run/'fit';output.mkdir(exist_ok=False)
    for dirname in ['models','fitted','figures']:(output/dirname).mkdir()
    frame=pd.read_csv(run/'analysis_input.csv')
    diagnostics=[];coefficients=[];slopes=[];interactions=[];contrasts=[];curves=[]
    for (label,ds),sub in frame.groupby(['threshold_label','dataset']):
        for model in ['A','B','interval_A','interval_B']:
            diag,result=fit_one(sub,model,config,label,ds,output)
            diagnostics.append(diag)
            base=dict(model_id=diag['model_id'],threshold_label=label,dataset=ds,model=model,n_codes=len(sub),n_clusters=diag['n_clusters'])
            local=model.startswith('interval'); adjusted=model.endswith('B')
            levels=sorted(sub.interval.unique()) if local else [-1]
            if result:
                beta,cov,cols,dof,centers=result
                for i,col in enumerate(cols):
                    c=np.eye(len(cols))[i];estimate=scalar_contrast(beta,cov,c,dof)
                    coefficients.append(dict(**base,term=col,**{k:v for k,v in estimate.items() if k!='p_raw'},df=dof,status=diag['status']))
            for j in levels:
                ref=sub.loc[sub.interval==j].copy() if local else sub.copy()
                reasons=diagnostic_reasons(ref,config)+diag['reasons']
                row=dict(**base,interval=int(j),interval_n=len(ref),su_min=int(ref.su.min()),su_max=int(ref.su.max()),
                         su_unique=ref.su.nunique(),error_codes=int((ref.k<ref.n).sum()),
                         status='judgment_difficult' if reasons else 'estimated',reasons=';'.join(reasons))
                if result:
                    term=f'su10_{j}' if local else 'su10';c=np.zeros(len(cols));c[cols.index(term)]=1
                    row.update(scalar_contrast(beta,cov,c,dof))
                else:row.update(estimate=np.nan,se=np.nan,ci_low=np.nan,ci_high=np.nan,p_raw=np.nan)
                slopes.append(row)
                if not result:continue
                q25,q75=np.quantile(ref.su,[.25,.75],method='linear')
                def at(su):
                    new=ref.copy();new['su']=su
                    return design(new,model,centers).reindex(columns=cols,fill_value=0).to_numpy()
                if local:
                    pred_low=prediction(beta,cov,at(q25),dof);pred_high=prediction(beta,cov,at(q75),dof)
                    grad=pred_high[4]-pred_low[4];se=float(np.sqrt(max(0,grad@cov@grad)))
                    delta=pred_high[0]-pred_low[0];crit=stats.t.ppf(.975,dof)
                    low_out=outside_fraction(ref,q25) if adjusted else 0.0
                    high_out=outside_fraction(ref,q75) if adjusted else 0.0
                    contrast_reasons=list(reasons)
                    if q25==q75:contrast_reasons.append('identical_SU_quartiles')
                    if max(low_out,high_out)>config['diagnostic_rules']['max_outside_hull_fraction']:
                        contrast_reasons.append('more_than_10pct_standardized_pairs_outside_convex_hull')
                    contrasts.append(dict(**base,interval=int(j),su_q25=q25,su_q75=q75,
                        mean_q25=pred_low[0],mean_q75=pred_high[0],delta_pp=100*delta,
                        ci_low_pp=100*(delta-crit*se),ci_high_pp=100*(delta+crit*se),
                        se_pp=100*se,outside_q25=low_out,outside_q75=high_out,
                        status='judgment_difficult' if contrast_reasons else 'estimated',reasons=';'.join(contrast_reasons)))
                grid=np.unique(np.r_[np.linspace(ref.su.min(),ref.su.max(),101),q25,q75])
                for su in grid:
                    mean,se,lo,hi,_=prediction(beta,cov,at(su),dof)
                    outside=outside_fraction(ref,su) if adjusted else 0.0
                    curves.append(dict(**base,interval=int(j),su=float(su),predicted_mean=mean,se=se,
                        ci_low=lo,ci_high=hi,outside_hull_fraction=outside,
                        supported=outside<=config['diagnostic_rules']['max_outside_hull_fraction'],
                        status=row['status'],standardization_n=len(ref)))
            if local:
                row=dict(**base,n_intervals=len(levels),p_raw=np.nan,F=np.nan,df_num=len(levels)-1,
                         df_den=diag['n_clusters']-1,status=diag['status'])
                if result and len(levels)>1:
                    R=np.zeros((len(levels)-1,len(cols)))
                    for i,j in enumerate(levels[1:]):
                        R[i,cols.index(f'su10_{j}')]=1;R[i,cols.index(f'su10_{levels[0]}')]=-1
                    Rcov=R@cov@R.T
                    if np.linalg.matrix_rank(Rcov)==len(R):
                        diff=R@beta;F=float(diff@np.linalg.solve(Rcov,diff)/len(R))
                        row.update(F=F,p_raw=float(stats.f.sf(F,len(R),dof)))
                    else:row['status']='singular_contrast_covariance'
                interactions.append(row)
    slopes=pd.DataFrame(slopes);interactions=pd.DataFrame(interactions)
    all_p=np.r_[slopes.p_raw.fillna(1).to_numpy(),interactions.p_raw.fillna(1).to_numpy()]
    adjusted=multipletests(all_p,method='holm')[1]
    slopes['p_holm']=adjusted[:len(slopes)];interactions['p_holm']=adjusted[len(slopes):]
    slopes.loc[slopes.p_raw.isna(),'p_holm']=np.nan
    interactions.loc[interactions.p_raw.isna(),'p_holm']=np.nan
    slopes['holm_family_size']=len(all_p);interactions['holm_family_size']=len(all_p)
    slopes.to_csv(output/'slopes.csv',index=False);interactions.to_csv(output/'interactions.csv',index=False)
    pd.DataFrame(coefficients).to_csv(output/'coefficients.csv',index=False)
    pd.DataFrame(contrasts).to_csv(output/'probability_contrasts.csv',index=False)
    pd.DataFrame(curves).to_csv(output/'prediction_curves.csv',index=False)
    write_json(output/'diagnostics.json',diagnostics)
    write_json(output/'execution.json',dict(started_after_config=True,finished_at_utc=datetime.now(timezone.utc).isoformat(),
               config_sha256=sha(run/'config.json'),script_sha256=sha(__file__),holm_family_size=len(all_p),
               fits=len(diagnostics),estimated=sum(x['status']=='estimated' for x in diagnostics),
               commands=sys.argv))
    plots(run,frame,pd.DataFrame(curves),slopes)
    verify_outputs(run)
    print('Fit completed:',output)
    print(slopes.loc[(slopes.threshold_label=='p67')&(slopes.model=='B'),['dataset','estimate','ci_low','ci_high','p_raw','p_holm','status']].to_string(index=False))


def plots(run,frame,curves,slopes):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    dest=run/'fit/figures'
    fig_records=[]
    colors={'A':'#2b6cb0','B':'#bc4b36'}
    for (label,ds),sub in frame.groupby(['threshold_label','dataset']):
        fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
        axes[0,0].scatter(sub.su,sub.y,s=18,alpha=.45,color='#2e5770')
        axes[0,0].set(xlabel='SU count',ylabel='Correct answers / 5',ylim=(-.03,1.03))
        cuts=read_json(run/'config.json')['boundaries'][f'{label}/{ds}']['cuts']
        for c in cuts:axes[0,0].axvline(c,color='grey',ls=':',lw=1)
        axes[0,1].hist(sub.su,bins=25,color='#2e5770');axes[0,1].set(xlabel='SU count',ylabel='Codes')
        axes[1,0].hist(sub['loc'],bins=25,color='#658a50');axes[1,0].set(xlabel='LOC (maximum token line)',ylabel='Codes')
        counts=sub.k.value_counts().reindex(range(6),fill_value=0)
        axes[1,1].bar(counts.index,counts.values,color='#9a6b37');axes[1,1].set(xlabel='Correct answers k (n=5)',ylabel='Codes',xticks=range(6))
        rho=stats.spearmanr(sub.su,sub['loc']).statistic
        fig.suptitle(f'{LABELS[ds]} | {label} ({THRESHOLDS[label]} nats) | n={len(sub)}, clusters={sub.cluster_id.nunique()}\nSU-LOC Spearman r={rho:.3f}; {int((sub.k<5).sum())} codes with errors')
        path=dest/f'descriptive__{label}__{ds}.png';fig.savefig(path,dpi=160);plt.close(fig)
        fig_records.append(dict(file=path.name,kind='descriptive',threshold_label=label,dataset=ds,n_codes=len(sub),source='analysis_input.csv'))

        fig,axes=plt.subplots(1,2,figsize=(12,4.7),sharey=True,layout='constrained')
        for ax,local in zip(axes,[False,True]):
            ax.scatter(sub.su,sub.y,s=14,alpha=.23,color='#6a737b',label='Observed code')
            for model in (['interval_A','interval_B'] if local else ['A','B']):
                cr=curves.loc[(curves.threshold_label==label)&(curves.dataset==ds)&(curves.model==model)]
                color=colors[model[-1]]
                for j,pts in cr.groupby('interval'):
                    pts=pts.sort_values('su');x=pts.su.to_numpy();mean=pts.predicted_mean.to_numpy()
                    ax.fill_between(x,pts.ci_low,pts.ci_high,color=color,alpha=.12)
                    ax.plot(x,mean,ls='--',color=color,alpha=.45,lw=1.3)
                    okay=pts.supported.to_numpy(bool)
                    ax.plot(x,np.where(okay,mean,np.nan),color=color,lw=2,
                            label=('B: LOC adjusted' if model[-1]=='B' else 'A: unadjusted') if j==cr.interval.min() else None)
            for c in cuts:ax.axvline(c,color='grey',ls=':',lw=1)
            ax.set(xlabel='SU count',ylim=(-.03,1.03),title='Interval intercepts and slopes' if local else 'Single SU slope')
        axes[0].set_ylabel('Predicted / observed mean accuracy');axes[0].legend(fontsize=8)
        fig.suptitle(f'{LABELS[ds]} | {label} | code-level fractional logit\nBands: pointwise 95% CI; dashed: >10% standardized pairs outside observed hull')
        path=dest/f'models__{label}__{ds}.png';fig.savefig(path,dpi=170);plt.close(fig)
        fig_records.append(dict(file=path.name,kind='models',threshold_label=label,dataset=ds,n_codes=len(sub),source='fit/prediction_curves.csv'))
    for label in THRESHOLDS:
        fig,ax=plt.subplots(figsize=(10,7),layout='constrained')
        subset=slopes.loc[(slopes.threshold_label==label)&(slopes.model=='interval_B')].sort_values(['dataset','interval'])
        labels=[]
        for pos,row in enumerate(subset.itertuples()):
            labels.append(f'{LABELS[row.dataset]}  SU {row.su_min}-{row.su_max} (n={row.interval_n})')
            if np.isfinite(row.estimate):
                color='#bc4b36' if row.status=='estimated' else '#777777'
                ax.errorbar(row.estimate,pos,xerr=[[row.estimate-row.ci_low],[row.ci_high-row.estimate]],fmt='o',color=color,capsize=4)
            else:ax.text(0,pos,'Not estimable',va='center')
        ax.axvline(0,color='black',ls=':',lw=1);ax.set(yticks=range(len(labels)),yticklabels=labels,xlabel='Logit-mean slope per +10 SU (LOC adjusted)')
        ax.invert_yaxis();ax.set_title(f'{label}: within-interval slopes, pointwise 95% CI\nGrey: sparse/unstable; intervals are not simultaneous')
        path=dest/f'slopes__{label}.png';fig.savefig(path,dpi=170);plt.close(fig)
        fig_records.append(dict(file=path.name,kind='slopes',threshold_label=label,dataset='all',source='fit/slopes.csv'))
    for row in fig_records:row['sha256']=sha(dest/row['file'])
    write_json(run/'fit/figure_manifest.json',fig_records)


def verify_outputs(run):
    data=pd.read_csv(run/'analysis_input.csv')
    curves=pd.read_csv(run/'fit/prediction_curves.csv')
    slopes=pd.read_csv(run/'fit/slopes.csv')
    contrasts=pd.read_csv(run/'fit/probability_contrasts.csv')
    checks=[]
    for path in (run/'fit/models').glob('*.json'):
        m=read_json(path);beta=np.array(m['beta']);cov=np.array(m['covariance'])
        sub=data.loc[(data.threshold_label==m['threshold_label'])&(data.dataset==m['dataset'])]
        X=design(sub,m['model'],m['centers']).reindex(columns=m['columns']).to_numpy()
        fitted=pd.read_csv(run/'fit/fitted'/f"{m['model_id']}.csv")
        np.testing.assert_array_equal(fitted.uid,sub.uid)
        np.testing.assert_allclose(fitted.fitted,special.expit(X@beta),atol=1e-12)
        for row in curves.loc[curves.model_id==m['model_id']].itertuples():
            ref=sub.loc[sub.interval==row.interval].copy() if row.interval>=0 else sub.copy()
            ref['su']=row.su
            xx=design(ref,m['model'],m['centers']).reindex(columns=m['columns'],fill_value=0).to_numpy()
            p=prediction(beta,cov,xx,m['df_inference'])
            np.testing.assert_allclose([row.predicted_mean,row.ci_low,row.ci_high],[p[0],p[2],p[3]],atol=1e-12)
        for row in slopes.loc[slopes.model_id==m['model_id']].itertuples():
            term='su10' if row.interval<0 else f'su10_{row.interval}'
            assert abs(row.estimate-beta[m['columns'].index(term)])<1e-12
        for row in contrasts.loc[contrasts.model_id==m['model_id']].itertuples():
            c=curves.loc[(curves.model_id==row.model_id)&(curves.interval==row.interval)]
            lo=c.loc[np.isclose(c.su,row.su_q25),'predicted_mean'].iloc[0]
            hi=c.loc[np.isclose(c.su,row.su_q75),'predicted_mean'].iloc[0]
            assert abs(row.delta_pp-100*(hi-lo))<1e-10
        checks.append(dict(model_id=m['model_id'],fitted_rows=len(sub),curve_rows=int((curves.model_id==m['model_id']).sum()),matched=True))
    write_json(run/'fit/numerical_verification.json',dict(models=checks,
        maximum_tolerance=1e-10,all_matches=True,plots_use_saved_curve_and_slope_tables=True,
        input_sha256=sha(run/'analysis_input.csv'),config_sha256=sha(run/'config.json')))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    prep=commands.add_parser('prepare')
    prep.add_argument('--detect-root',type=Path,default=Path(__file__).resolve().parents[1])
    prep.add_argument('--lmcc-root',type=Path)
    prep.add_argument('--output-dir',type=Path,required=True)
    model=commands.add_parser('fit');model.add_argument('--run-dir',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='prepare':
        prepare(args.detect_root.resolve(),(args.lmcc_root or args.detect_root.parent/'lm-cc').resolve(),args.output_dir.resolve())
    else:fit(args.run_dir.resolve())


if __name__=='__main__':
    main()
