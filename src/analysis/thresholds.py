"""Thresholds that reproduce the checked-in analysis_summary_pXX CSV files.

The pXX names are historical labels. In particular, the saved p80 file used
1.3238 nats; 1.2515 is the 80th percentile of the currently pooled original
three datasets, but does not reproduce that saved file. See docs for the audit.
"""

SAVED_SUMMARY_THRESHOLDS = {
    "p05": 0.0037,
    "p10": 0.0114,
    "p15": 0.0214,
    "p20": 0.0335,
    "p25": 0.0483,
    "p30": 0.0675,
    "p35": 0.0921,
    "p40": 0.1244,
    "p45": 0.1691,
    "p50": 0.2327,
    "p55": 0.3254,
    "p60": 0.4536,
    "p65": 0.6154,
    "p67": 0.6813,
    "p70": 0.7781,
    "p75": 0.9829,
    "p80": 1.3238,
    "p85": 1.5920,
    "p90": 2.1097,
    "p95": 3.2355,
}
