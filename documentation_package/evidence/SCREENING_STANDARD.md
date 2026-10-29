# SCREENING STANDARD v2 — FROZEN 2026-10-28 (قصي's methodological decision)

## Implementation (the only valid screen from now on)
- Code: screening-v2/unified_screen.py (screen_v2). Projection = truncated-SVD
  pseudo-inverse of the augmented affine system, relative cutoff 1e-10.
  Rationale (numerical, outcome-independent): the 15 anchors have effective
  affine rank 11 (SVD cliff: sigma_11 = 1.4e-2, sigma_12 = 6.7e-15; x0.8/x1.2
  are EXACT multiples of v2_a0; span5 a near-exact combination). Coefficients
  are non-unique along 4 null directions; v2 reports the UNIQUE minimum-norm
  representative. maxcoef_v2 = max|c| of that representative. Raw LU solve is
  NOT a valid implementation (it returns an arbitrary representative).
- Verified: perturbation 1e-9 changes no reported digit; v2 reproduces the
  campaign's lstsq-family numbers exactly (lstsq's default truncation was
  already computing this representative; GBM's recorded approx 0.0816 was the
  one solve-contaminated value — corrected to 0.0825).

## Acceptance gates (registered; changes require a new dated amendment BEFORE
## any new results are seen)
1. Full-sample v2: approx < incumbent board best AND maxcoef_v2 <= 2.5.
2. Random split pairs: selection pair (7,123) for fitting only; judgment pairs
   are SPENT for the H1 family (val-A 999/31337, val-B 555/2024, county pair).
   A future candidate family must register NEW judgment splits in advance or
   use the board itself (one slot, user-approved) as the judgment.
3. Geographic gate (LORO): parameters re-selected without the judged region;
   PASS = median delta <= +0.001, >=4/5 regions delta <= +0.002, worst <= +0.010.
   Per-region performance vs the incumbent must be REPORTED in full (n, median,
   dispersion, worst) — a gate pass does not imply per-region superiority.
4. Orthogonal-energy share and proj/resid decomposition reported for every
   candidate (screening-v2 SCREENING_DECOMPOSITION format).

## Standing verdicts under v2 (screening-v2/reverdicts.csv)
span5 / poi probe: incumbents (0.0848). rubric s0.6: PASS 0.0804/2.33.
gbm_lr04: PASS 0.0825/2.34 (approx corrected). gbm_eng_lr04: PASS 0.0817/2.47.
H1: PASS 0.0787/2.45 + GEO GATE PASS (method generalization); per-region
advantage concentrated in eastern-ok, negative in WA/CA subset screens.
H5 (all doses) and f1: FAIL — robust under every implementation.
