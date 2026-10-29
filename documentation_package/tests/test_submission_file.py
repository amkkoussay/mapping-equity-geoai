"""Runnable checks on the packaged copy of the submitted s0.8 file.

PATH ADAPTATION (package repair, 2026-10-29): all inputs are resolved
package-relatively, so this suite runs from any working directory —
including an isolated copy of documentation_package/ alone. The checks are
unchanged; the only difference from the original-environment version is
that the POI-probe anchor is now read from the byte-identical packaged
copy evidence/05_poi_component_probe.csv (SHA-256 f5acaa10...) instead of
upload28b/staged/05_poi_component_probe.csv in the project tree.

Run from anywhere:
    python documentation_package/tests/test_submission_file.py
Checks the evidence copy of the submission (byte-identical to the original,
sha256-verified in 06_validation_report.md) against the format the campaign
used throughout and against the anchor file's tract set and row order.
Exit 0 = all checks pass. Observed results: ALL PASS in the original
environment and in an isolated package copy (06_validation_report.md).
"""
import pandas as pd, numpy as np, hashlib, sys, os
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

f = os.path.join(PKG, 'evidence', 'submission_s0.8_HeXaMraA.csv')
h = hashlib.sha256(open(f, 'rb').read()).hexdigest()
df = pd.read_csv(f, dtype={'GEOID': str})
probe = pd.read_csv(os.path.join(PKG, 'evidence', '05_poi_component_probe.csv'),
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
