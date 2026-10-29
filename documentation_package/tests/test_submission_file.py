"""Runnable checks on the packaged copy of the submitted s0.8 file.
Run from the geoai-zindi project root:
    .venv/bin/python documentation_package/tests/test_submission_file.py
Checks the evidence copy (byte-identical to the original, sha256-verified in
06_validation_report.md) against the format the campaign used throughout and
against the anchor files' tract set and row order. Exit 0 = all checks pass.
Observed result in the 2026-10-29 audit run: ALL PASS (see 06_validation_report.md).
"""
import pandas as pd, numpy as np, hashlib, sys, os
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(PKG)

f = os.path.join(PKG, 'evidence', 'submission_s0.8_HeXaMraA.csv')
h = hashlib.sha256(open(f, 'rb').read()).hexdigest()
df = pd.read_csv(f, dtype={'GEOID': str})
probe = pd.read_csv(os.path.join(ROOT, 'upload28b/staged/05_poi_component_probe.csv'),
                    dtype={'GEOID': str})
checks = {
    'sha256 matches audited original (e5430d51...)': h == 'e5430d51d509955e4ce5def4eaf0c8f3c00e23a805b38642062eb7529311ede4',
    'columns are [GEOID, coverage_gap_score]': list(df.columns) == ['GEOID', 'coverage_gap_score'],
    'row count is 9794': len(df) == 9794,
    'GEOIDs unique': df.GEOID.nunique() == 9794,
    'GEOIDs are 11-character text': bool((df.GEOID.str.len() == 11).all()),
    'no missing scores': int(df.coverage_gap_score.isna().sum()) == 0,
    'all scores finite': bool(np.isfinite(df.coverage_gap_score).all()),
    'all scores inside [0, 1]': bool(df.coverage_gap_score.min() >= 0 and df.coverage_gap_score.max() <= 1),
    'tract set equals the POI-probe anchor tract set': set(df.GEOID) == set(probe.GEOID),
    'row order equals the POI-probe anchor row order': bool((df.GEOID.values == probe.GEOID.values).all()),
}
for k, ok in checks.items():
    print(('PASS' if ok else 'FAIL'), '-', k)
sys.exit(0 if all(checks.values()) else 1)
