# 07 — Results and Limitations

Results are reported in three strictly separated categories. **Local
diagnostic numbers are not official scores** and are never presented as
such.

## 1. Official competition results (as recorded)

Public-leaderboard RMSE values, from `repo/docs/experiments.csv`,
`work29/evaluator.py` (`SCORED`) and `calibrated-screen/registry.csv`
(copy in `evidence/`). All are **public-split** scores (≈30% of tracts);
private-split (70%) scores are unknown until the challenge closes.

| # | Submission ID | File / name | Official public RMSE |
|---|---|---|---|
| 1 | NqUc8kRn | submission_baseline.csv (v1 proxy) | 0.196647298 |
| 2 | h4RYWmn2 | submission_shrunk.csv | 0.153660593 |
| 3 | v7Kk8Vox | submission_shrunk25.csv | 0.139462125 |
| 4 | oqcqYSdK | submission_v2.csv | 0.106671123 |
| 5 | LaAz2SoB | submission_v2_a0.csv | 0.104202964 |
| 6 | LcZaou8v | submission_v2_a0_x0.8.csv | 0.095098958 |
| 7 | GwJRxqt3 | submission_v2_a0_x1.2.csv | 0.116808721 |
| 8 | d2rnaHtv | submission_v2_k053.csv | 0.090196836 |
| 9 | 3F8vK2QT | probe_k053_tx_m002.csv | 0.090404754 |
| 10 | Jccs9z7s | probe_k053_az_m002.csv | 0.089761173 |
| 11 | Pih3vnoM | 01_span5_balanced.csv | 0.084844078 |
| 12 | X6P4h1CX | 02_ridge_lambda_3e-5.csv | 0.085767868 |
| 13 | PzxiTJCz | 03_ridge_lambda_2e-5.csv | 0.085146032 |
| 14 | 9kHGjoHz | 04_building_component_probe.csv | 0.085164579 |
| 15 | cjw1BmR3 | 05_poi_component_probe.csv (= $P$) | 0.08483727 |
| 16 | 6QMBo4iq | H1 (density calibration, α=−0.2, τ=1.0) | 0.082777005 |
| 17 | Cvdyznfk | s1.1 (α=−0.4, τ=0.5, s0=1.1) | 0.082179413 |
| 18 | **HeXaMraA** | **s0.8 — the documented submission** | **0.081231862** |
| 19 | 7WvX14fp | H4 piecewise | 0.082783512 |
| 20 | SobRVFX8 | H6 β=−0.6 interaction | 0.082509789 |

Status of this table: **Strongly supported** (internal records agree).
The documented submission's own row (HeXaMraA ↔ 0.081231862) is separately
**Verified — platform record captured** (`evidence/zindi_submissions_proof.pdf`;
`02` §2). One additional attempt
(Z81nvmtR, an early staging of the building probe) errored unscored due to
the GEOID-formatting incident (`04` §2) and consumed no scoring slot.
The participant's final leaderboard rank is **not** recorded locally and is
not claimed here. Competition context from campaign records: ≈494 active
entrants on 2026-10-29; the sub-0.05 tier (22 entries) consists of exact
target reconstructions by other participants, a method this campaign
declined on rules grounds (`08`).

## 2. The metric

The organisers do not publish the metric's definition in the fetched rules
text (the leaderboard column is labelled RMSE). An independent local audit
(`metric-audit/REPORT.txt`) tested the behaviour of the returned scores:
quadratic (RMSE-form) fits on a scaling triple reproduce held-out scores to
≤5.6×10⁻⁵; RMSE-form triangle inequalities hold on all 120 anchor pairs
(MAE-form fails once). Conclusion recorded by the campaign: **the board
behaves as RMSE**. One published external data point (a competitor's
all-zeros probe scored 0.0598) is inconsistent with both pure metrics and
is treated as an anomaly in that audit; it does not affect any number in
this package.

## 3. Local diagnostic results (NOT official scores)

Procedure: the frozen anchor-projection screen (`03` §5;
`screening-v2/SCREENING_STANDARD.md`). Its known properties, all documented
in the campaign records:

- For the 15 anchors themselves the screen reproduces their official scores
  to within 3.4×10⁻⁴ (identity check; also the screen's noise floor —
  differences below ≈0.0003 are not decisions).
- For genuinely new vectors the screen is **optimistic**: screen-to-board
  gaps were +0.0041 (H1), +0.0115 (s1.1), +0.0101 (s0.8), +0.0112 (H4),
  +0.0099 (H6). The gap grows with projection leverage ($\|c\|_1$): a
  fitted leverage law `predicted = sqrt(screen² + κ(‖c‖₁−1))`,
  κ ≈ 4.22×10⁻⁵, described the first four genuine points with leave-one-out
  convergence 0.96–1.00, then **failed out-of-family** on H6 (convergence
  0.763) — recorded as a preliminary ranking tool, not a predictor
  (`screen-study/STUDY.md`; `calibrated-screen/APPLIED.md`).
- Screen ordering did **not** preserve board ordering among the three
  2026-10-29 submissions (screen: s1.1 < s0.8 < H4; board: s0.8 < s1.1 < H4).
- The screen is sensitive to the treatment of the two all-undefined tracts
  in some diagnostic variants (absolute approx shifts of ≈0.021 across
  fillings), although candidate *orderings* were filling-robust in the
  tested cases (`new-hypotheses/round2/WATER_SENSITIVITY.md`). This affects
  diagnostics only; the submitted file's values do not depend on any
  filling choice.

Diagnostics for the documented file: approx 0.0711, maxcoef 6.10,
proj 0.0682, resid 0.0201 (`06` T9).

## 4. Negative results and disclosed weaknesses

1. **Gate breach by decision.** The documented configuration's maxcoef
   (6.10) exceeds the campaign's own frozen acceptance gate (≤ 2.5). Its
   local screen was therefore known, in advance, to be an extrapolation
   with an unreliable board translation. It was submitted by the
   participant's explicit decision as one of the three lowest-screen
   candidates (an independent-judgment path), and it happened to return
   the best official score. The outcome does not retroactively validate
   the screen value.
2. **Private-split behaviour unknown.** All evidence above is public-split
   (≈30%). The documented file's high leverage makes its private-split
   (70%) behaviour genuinely uncertain; no claim is made about it.
3. **The v2 heuristic's tract-level signal is weak.** The campaign's own
   records show the v2 regional means alone (α=0) scored 0.104202964 vs
   0.106671123 for the full tract-level composite: most of the measurable
   gain is regional level, not tract detail. The documented chain builds
   on a probe vector that descends from those submissions.
4. **Upstream weak links.** span5's exact coefficients are not recorded;
   the probe's construction script was searched for across the full
   workspace and archives and not found (documented construction +
   correlation 0.940 only; `02` §3.1). If either vector contained an
   error, L2 reproduction would still succeed — it verifies the final
   step, not the ancestry.
5. **Building-denominator sensitivity.** The v2 building component divides
   by a provided strata column (`usfs_BuildingCount_sum`). The method's
   author flags this himself in `repo/WRITEUP.md` §2 and ships a fallback
   mode. The documented submission's own inputs are $P$, $hu$ and $area$,
   none of which involves the column — but the column reaches the file
   through the anchor span ($P$ descends from span5, fitted over
   v2-derived anchors), so the dependence is real and indirect, not
   absent. Full chain: `03` §7. Compliance status: open (`08` R11).
6. **Assumption load of the calibration form.** The tanh density
   modulation is a chosen functional form from a 456-point grid, selected
   by a local screen — a selection procedure with documented optimism
   (§3). The grid's own winner (H1) scored worse on the board than s0.8
   despite a better-behaved maxcoef, which cuts both ways: the family's
   board behaviour is not well predicted by any local statistic the
   campaign produced.

## 5. Unverified hypotheses (labelled, not results)

- *Why* the density calibration helped on the public split (e.g., a real
  density-dependence of the organisers' POI gap vs a public-split
  artefact) cannot be determined from local evidence; the campaign's
  geographic analysis found H1's advantage regionally concentrated
  (eastern-ok), and the same caveat plausibly applies to s0.8 — not tested
  separately for s0.8.
- The screen→board leverage law's family-dependence (per-family κ in
  `calibrated-screen/`) is an n=5 observation, not an established model.

## 6. What cannot be concluded from the available evidence

- The private-leaderboard standing of any submission.
- That the documented method would generalise to other regions, other
  Overture snapshots, or the organisers' full test set.
- That the density calibration reflects a property of the true target
  rather than of the public split.
- Any claim about the bias-discovery questions (who is under-mapped and
  why); those are addressed by the separate Bias Discovery entry
  (`repo/docs/BIAS_ANALYSIS.md`), which itself declines to claim a
  discovery.
