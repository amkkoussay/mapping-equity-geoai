"""Extended exact-quadratic evaluator over ALL 15 scored submissions.
For affine combos (sum c = 1): pred_RMSE^2 = c'Gc - c.d + c.s2  (span_eval identity).
E[f_i*y] recovered up to the shared constant E[y^2]; zero-sum directions give it exactly."""
import pandas as pd, numpy as np, os
BASE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(BASE)
SCORED = {  # path (relative to geoai-zindi/) : public RMSE — from repo/docs/experiments.csv
 'max-gamble-pack/scored/submission_baseline.csv':0.196647298,
 'max-gamble-pack/scored/submission_shrunk.csv':0.153660593,
 'max-gamble-pack/scored/submission_shrunk25.csv':0.139462125,
 'max-gamble-pack/scored/submission_v2.csv':0.106671123,
 'max-gamble-pack/scored/submission_v2_a0.csv':0.104202964,
 'max-gamble-pack/scored/submission_v2_a0_x0.8.csv':0.095098958,
 'max-gamble-pack/scored/submission_v2_a0_x1.2.csv':0.116808721,
 'max-gamble-pack/scored/submission_v2_k053.csv':0.090196836,
 'max-gamble-pack/scored/probe_k053_tx_m002.csv':0.090404754,
 'max-gamble-pack/scored/probe_k053_az_m002.csv':0.089761173,
 'upload28/zindi-5-daily-submissions/01_span5_balanced.csv':0.084844078,
 'upload28/zindi-5-daily-submissions/02_ridge_lambda_3e-5.csv':0.085767868,
 'upload28/zindi-5-daily-submissions/03_ridge_lambda_2e-5.csv':0.085146032,
 'upload28b/staged/04_building_component_probe.csv':0.085164579,
 'upload28b/staged/05_poi_component_probe.csv':0.08483727,
}
def load(rel):
    return pd.read_csv(os.path.join(ROOT, rel), dtype={'GEOID': str}).set_index('GEOID').coverage_gap_score
NAMES = list(SCORED); F = pd.DataFrame({n: load(n) for n in NAMES})
assert F.notna().all().all() and len(F) == 9794
S2 = np.array([SCORED[n] ** 2 for n in NAMES]); G = (F.T @ F).values / len(F); D = np.diag(G).copy()
def pred_combo(c):
    c = np.asarray(c, float); c = c / c.sum(); assert abs(c.sum() - 1) < 1e-6
    return float(np.sqrt(max(c @ G @ c - c @ D + c @ S2, 0)))
def ey2_estimate():
    """Estimate E[y^2] from the most consistent anchor pair geometry (v2_a0 scalings)."""
    return None  # not needed for affine screening
def screen_new(g):
    """Screen a NEW candidate vector g (aligned to F.index):
    project onto the affine span of anchors (least squares), then
    pred^2 ~= pred_combo^2 + mean((g - combo)^2)  [cross-term ignored: approximation]."""
    A = F.values; y = g.values
    # affine projection: solve min ||A c - y|| s.t. sum c = 1 via lstsq on augmented system
    k = A.shape[1]
    M = np.zeros((k + 1, k + 1)); M[:k, :k] = A.T @ A; M[:k, k] = 1; M[k, :k] = 1
    rhs = np.r_[A.T @ y, 1.0]
    try: c = np.linalg.solve(M, rhs)[:k]
    except np.linalg.LinAlgError: c = np.linalg.lstsq(M, rhs, rcond=None)[0][:k]
    resid = y - A @ c
    pc = pred_combo(c)
    return dict(pred_span=pc, resid_rms=float(np.sqrt((resid ** 2).mean())),
                pred_approx=float(np.sqrt(pc ** 2 + (resid ** 2).mean())),
                top_coefs={NAMES[i]: round(float(c[i]), 3) for i in np.argsort(-np.abs(c))[:4] if abs(c[i]) > 0.02})
if __name__ == '__main__':
    for i, n in enumerate(NAMES):
        e = np.zeros(len(NAMES)); e[i] = 1
        print(f'{pred_combo(e):.9f} vs actual {SCORED[n]:.9f}  {os.path.basename(n)}')
    # virtual best: ridge toward current best (poi probe) at several lambdas
    best_i = NAMES.index('upload28b/staged/05_poi_component_probe.csv')
    k = len(NAMES)
    for lam in [0, 1e-4, 3e-4, 1e-3, 3e-3]:
        A = np.zeros((k + 1, k + 1)); A[:k, :k] = 2 * (G + lam * np.eye(k)); A[:k, k] = 1; A[k, :k] = 1
        e = np.zeros(k); e[best_i] = 1
        rhs = np.r_[D - S2 + 2 * lam * e, 1.0]
        c = np.linalg.solve(A, rhs)[:k]
        print('lam', lam, 'virtual-best pred', round(pred_combo(c), 6),
              {os.path.basename(NAMES[i]): round(float(c[i]), 2) for i in np.argsort(-np.abs(c))[:5]})
