"""Audit helper (NOT part of the original solution): rebuild the s0.8 submission
vector from its documented formula and compare it with the submitted file.

Formula (exp-v7/code/h1_density_calibration.py, function build()):
    z   = standardised log1p(hu / area_km2), area clipped below at 0.05 km^2
    s   = s0 + alpha * tanh(z / tau)          with s0=0.8, alpha=-0.4, tau=0.5
    y   = clip01( s * P + (mean(P) - mean(s * P)) )
where P is the board-scored POI component probe vector
(upload28b/staged/05_poi_component_probe.csv, official public RMSE 0.08483727)
and hu / area_km2 come from max-gamble-pack/scored/v2_tracts.parquet.

Run from the geoai-zindi project root:
    .venv/bin/python documentation_package/scripts/rebuild_s08.py
Writes only to stdout. Exit code 0 iff the rebuild matches the submitted file
exactly (max abs diff 0.0) — as observed in the 2026-10-29 audit run.
"""
import pandas as pd, numpy as np, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
sys.path.insert(0, 'work29')
import evaluator as ev

F = ev.F; IDX = F.index
t = pd.read_parquet('max-gamble-pack/scored/v2_tracts.parquet').set_index('GEOID').loc[IDX]
P = pd.Series(F['upload28b/staged/05_poi_component_probe.csv'].values, index=IDX)

def zstd(x):
    x = pd.Series(np.asarray(x, float)); return ((x - x.mean()) / x.std()).values

area = t['area_km2'].clip(lower=0.05)
z = zstd(np.log1p(t['hu'] / area))
s = 0.8 + (-0.4) * np.tanh(z / 0.5)
y = s * P.values
y = np.clip(y + (P.values.mean() - y.mean()), 0, 1)

sub = pd.read_csv('stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv',
                  dtype={'GEOID': str}).set_index('GEOID').coverage_gap_score.reindex(IDX).values
d = np.abs(y - sub)
print(f'rows={len(y)}  max_abs_diff={d.max()}  mean_abs_diff={d.mean()}  exact_rows={(d == 0).sum()}')
sys.exit(0 if d.max() == 0.0 else 1)
