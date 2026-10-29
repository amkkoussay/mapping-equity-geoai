"""Audit helper (NOT part of the original solution): rebuild the s0.8 submission
vector from its documented formula and compare it with the submitted file.

Formula (exp-v7/code/h1_density_calibration.py, function build()):
    z   = standardised log1p(hu / area_km2), area clipped below at 0.05 km^2
    s   = s0 + alpha * tanh(z / tau)          with s0=0.8, alpha=-0.4, tau=0.5
    y   = clip01( s * P + (mean(P) - mean(s * P)) )
where P is the board-scored POI component probe vector (official public
RMSE 0.08483727) and hu / area_km2 are per-tract values from the v2 tract
table.

PATH ADAPTATION (package repair, 2026-10-29): this packaged copy resolves
ALL inputs package-relatively under evidence/, so it runs from any working
directory — including an isolated copy of documentation_package/ alone.
The computation is unchanged; only the input locations differ from the
original-environment version:
  * P and the tract order: the original read them via work29/evaluator.py's
    anchor frame F, whose probe column is loaded from
    upload28b/staged/05_poi_component_probe.csv. This copy reads the
    byte-identical packaged file evidence/05_poi_component_probe.csv
    directly (SHA-256 f5acaa10...; evaluator.py itself is packaged at
    evidence/evaluator.py for reference — importing it standalone would
    try to load all 15 anchor files relative to the project root).
  * hu / area_km2: the original read max-gamble-pack/scored/
    v2_tracts.parquet. This copy reads evidence/v2_tracts_columns.csv, an
    extract of exactly the consumed columns (GEOID, hu, area_km2),
    verified against the parquet (9,794 rows; per-column max abs diff 0.0;
    parquet SHA-256 f216c703... — see 06_validation_report.md, R2).
  * Comparison target: the original compared against
    stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv; this copy compares
    against the byte-identical packaged evidence/submission_s0.8_HeXaMraA.csv
    (SHA-256 e5430d51...).

Run from anywhere:
    python documentation_package/scripts/rebuild_s08.py
Writes only to stdout. Exit code 0 iff the rebuild matches the submitted
file exactly (max abs diff 0.0) — as observed in the 2026-10-29 audit runs
(original environment and isolated package copy; see 06_validation_report.md).
"""
import pandas as pd, numpy as np, sys, os
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(PKG, 'evidence')

probe = pd.read_csv(os.path.join(EV, '05_poi_component_probe.csv'),
                    dtype={'GEOID': str}).set_index('GEOID')
IDX = probe.index
P = probe.coverage_gap_score
t = pd.read_csv(os.path.join(EV, 'v2_tracts_columns.csv'),
                dtype={'GEOID': str}).set_index('GEOID').loc[IDX]

def zstd(x):
    x = pd.Series(np.asarray(x, float)); return ((x - x.mean()) / x.std()).values

area = t['area_km2'].clip(lower=0.05)
z = zstd(np.log1p(t['hu'] / area))
s = 0.8 + (-0.4) * np.tanh(z / 0.5)
y = s * P.values
y = np.clip(y + (P.values.mean() - y.mean()), 0, 1)

sub = pd.read_csv(os.path.join(EV, 'submission_s0.8_HeXaMraA.csv'),
                  dtype={'GEOID': str}).set_index('GEOID').coverage_gap_score.reindex(IDX).values
d = np.abs(y - sub)
print(f'rows={len(y)}  max_abs_diff={d.max()}  mean_abs_diff={d.mean()}  exact_rows={(d == 0).sum()}')
sys.exit(0 if d.max() == 0.0 else 1)
