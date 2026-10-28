"""Checks of analysis units, ties, separation, and robust uncertainty."""
import importlib.util
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
from scipy import special
import statsmodels.api as sm
from statsmodels.stats.sandwich_covariance import cov_cluster

SCRIPT = Path(__file__).resolve().parents[1]/'scripts/run_su_fractional_analysis.py'
if not SCRIPT.exists():
    SCRIPT = Path(__file__).with_name('run_su_fractional_analysis.py')
spec=importlib.util.spec_from_file_location('su_fractional',SCRIPT)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class FractionalAnalysisTests(unittest.TestCase):
    def test_counts_require_integer_successes_and_observed_trials(self):
        self.assertEqual(module.recover_count(.6,5),3)
        with self.assertRaises(ValueError):module.recover_count(.61,5)
        with self.assertRaises(ValueError):module.recover_count(.6,0)

    def test_ties_are_not_split_and_duplicate_boundaries_collapse(self):
        x=np.array([1]*8+[2]*2+[3]*2)
        cuts=module.tercile_cuts(x);bins=module.assign_intervals(x,cuts)
        for value in np.unique(x):self.assertEqual(len(set(bins[x==value])),1)
        self.assertLessEqual(len(set(bins)),3)
        self.assertEqual(module.tercile_cuts([4,4,4]),[])

    def test_fractional_interior_prevents_spurious_separation(self):
        X=np.column_stack([np.ones(6),np.arange(6)])
        self.assertEqual(module.separation_check(X,np.array([0,0,.2,.6,1,1])),'none')
        self.assertEqual(module.separation_check(X,np.array([0,0,0,1,1,1])),'complete_separation')

    def test_all_correct_cell_is_quasi_separated(self):
        X=np.array([[1,0,0],[1,1,0],[0,0,1],[0,0,1]],float)
        self.assertEqual(module.separation_check(X,np.array([.2,.8,1,1])),'quasi_separation')

    def test_singleton_cluster_covariance_equals_hc1(self):
        X=np.column_stack([np.ones(8),np.linspace(-1,1,8)])
        y=np.array([0,.4,.2,.8,.2,.8,1,.6])
        fit=sm.GLM(y,X,family=sm.families.Binomial()).fit()
        cov,factor,G,bread=module.sandwich(X,y,fit.fittedvalues,np.arange(8))
        score=X*(y-fit.fittedvalues)[:,None];inv=np.linalg.inv(bread)
        np.testing.assert_allclose(cov,8/6*inv@score.T@score@inv)
        self.assertAlmostEqual(factor,8/6)

    def test_cluster_sandwich_matches_library_and_is_not_trial_expansion(self):
        X=np.column_stack([np.ones(12),np.linspace(-1,1,12)])
        y=np.array([0,.2,.4,.2,.8,.6,.4,.8,.6,1,.8,1])
        groups=np.repeat(np.arange(6),2)
        fit=sm.GLM(y,X,family=sm.families.Binomial()).fit()
        cov,factor,G,_=module.sandwich(X,y,fit.fittedvalues,groups)
        np.testing.assert_allclose(cov,cov_cluster(fit,groups,use_correction=True))
        self.assertEqual(G,6);self.assertAlmostEqual(factor,6/5*11/10)

    def test_marginal_gradient_matches_finite_difference(self):
        X=np.array([[1,2,.4],[1,2,.8],[1,2,1.2]])
        beta=np.array([-.5,.2,.3]);cov=np.eye(3)*.01
        mean,se,lo,hi,grad=module.prediction(beta,cov,X,99)
        delta=1e-6
        numeric=np.array([(special.expit(X@(beta+np.eye(3)[i]*delta)).mean()-special.expit(X@(beta-np.eye(3)[i]*delta)).mean())/(2*delta) for i in range(3)])
        np.testing.assert_allclose(grad,numeric,rtol=1e-7)
        self.assertTrue(0<=lo<mean<hi<=1)

    def test_support_flags_outside_pairs(self):
        ref=pd.DataFrame({'su':[1,1,2,2],'logloc':[0,1,0,1]})
        self.assertEqual(module.outside_fraction(ref,1.5),0)
        self.assertEqual(module.outside_fraction(ref,3),1)

    def test_interval_design_has_distinct_slopes_and_common_loc(self):
        ref=pd.DataFrame({'su':[2,4,6,8],'logloc':[1,2,3,4],'interval':[0,0,1,1]})
        X=module.design(ref,'interval_B',{'0':3,'1':7})
        self.assertEqual(list(X),['intercept_0','su10_0','intercept_1','su10_1','logloc'])
        np.testing.assert_allclose(X.su10_0,[-.1,.1,0,0])
        np.testing.assert_allclose(X.su10_1,[0,0,-.1,.1])

    def test_endpoint_responses_do_not_by_themselves_mean_insufficient_information(self):
        ref=pd.DataFrame({'su':np.arange(40),'y':[0,1]*20,'k':[0,5]*20,
                          'n':5,'cluster_id':np.arange(40)})
        cfg={'diagnostic_rules':{'min_interval_codes':20,'min_interval_clusters':20,
              'min_unique_su':3,'min_codes_with_errors_for_stable_inference':5,
              'min_codes_with_success_for_stable_inference':5}}
        self.assertEqual(module.diagnostic_reasons(ref,cfg),[])


if __name__=='__main__':unittest.main()
