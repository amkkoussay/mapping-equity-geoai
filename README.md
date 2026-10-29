# Audit-Ready Documentation Package — Best Zindi Submission

**Competition:** Zindi *Bias Bounty Mapping Equity Challenge* (Humane
Intelligence / Radiant Earth / Reliabl).
**Participant:** Koussay Mehdouani — Zindi username **koussayy**.
**Package prepared:** 2026-10-29 (forensic documentation audit; original
solution files untouched).

## What the solution does

The documented submission estimates, for each of 9,794 US Census tracts in
five regions, a coverage-gap score in [0, 1] — how much of the built
environment is missing from Overture Maps relative to reference layers the
organisers removed from the challenge package. The method is a
**deterministic heuristic pipeline** (no trained model): per-tract Overture
features → a three-component heuristic composite (building / transport /
POI) → a chain of scored anchor submissions combined with exact quadratic
algebra → a component probe → a final **density calibration** that
multiplicatively re-weights the probe signal by standardised log housing
density, $\hat y = \mathrm{clip01}\bigl([s_0 + \alpha\tanh(z/\tau)]\cdot P
+ (\bar P - \overline{[s_0+\alpha\tanh(z/\tau)]\cdot P})\bigr)$ with
$s_0 = 0.8$, $\alpha = -0.4$, $\tau = 0.5$. Full detail: `03_methodology.md`.

## Which official submission this documents

| | |
|---|---|
| Zindi submission ID | **HeXaMraA** |
| Official public score | **0.081231862** (public-split RMSE; best of the participant's 20 scored submissions) |
| Submitted | 2026-10-29 14:40 (Africa/Tunis), account koussayy |
| File | `stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv` — SHA-256 `e5430d51d509955e4ce5def4eaf0c8f3c00e23a805b38642062eb7529311ede4`; byte-identical copy in `evidence/submission_s0.8_HeXaMraA.csv` |
| Association status | **Verified — platform record captured** (a capture of the official submissions page is retained as `evidence/zindi_submissions_proof.pdf`, corroborated by three independent internal records — see `02_submission_provenance.md`) |
| Code→file status | **Verified by re-execution** — the file is reproduced exactly (max abs diff 0.0, 9,794/9,794 rows) from its documented formula and inputs |

## How to navigate this package

| File | Contents |
|---|---|
| `00_reviewer_quick_start.md` | **Start here** — one page: what this documents, exact run commands with verified results, and the open items |
| `00_project_inventory.md` | Project/repo inventory, artifact table with hashes, inconsistencies found |
| `01_evidence_register.csv` | 33 claims with evidence pointers, status and follow-ups |
| `02_submission_provenance.md` | The submission, its evidence chain, candidate comparison, discrepancies |
| `03_methodology.md` | The implemented method in execution order, with formulas and per-feature definitions |
| `04_data_lineage_and_edge_cases.md` | Input→output lineage table; edge cases as actually coded |
| `05_reproduction_guide.md` | Reproduction at three separate levels (features / file / official score) with exact commands |
| `06_validation_report.md` | Every test actually run, with commands and observed results; failures and gaps reported |
| `07_results_and_limitations.md` | Official results vs local diagnostics vs unverified hypotheses; negative results |
| `08_award_requirements_checklist.md` | Official-rules compliance + Best Documentation award mechanics and remaining actions |
| `09_claims_and_uncertainties.md` | All important claims grouped by confidence |
| `10_audit_summary.md` | Final verdicts and blockers |
| `requirements.txt` | Audit environment (derived from the project's actual .venv) |
| `scripts/rebuild_s08.py` | Audit helper that rebuilds the submission file and compares it (not part of the original solution) |
| `tests/test_submission_file.py` | Runnable format/identity checks on the packaged submission copy |
| `evidence/` | Byte-identical copies of the key small artifacts (submission CSV, **probe vector $P$**, anchor registry `evaluator.py`, registry, grid log, pipeline code, probe design note, screening standard) plus `v2_tracts_columns.csv` — the verified `hu`/`area_km2` extract of the v2 tract table (`06` R2) — and `zindi_submissions_proof.pdf`, the capture of the official submissions page that verifies the HeXaMraA association (`02` §2). Together these make the L2 rebuild and the test suite **runnable from this package alone** |
| `MANIFEST.sha256` | SHA-256 of every packaged file except the manifest itself |

## How to reproduce the documented steps

```bash
# from any working directory — all inputs resolve inside this package:
python documentation_package/tests/test_submission_file.py   # 10/10 PASS
python documentation_package/scripts/rebuild_s08.py          # max_abs_diff=0.0, exit 0
```
Self-containment is verified, not asserted: both commands were executed
successfully in an isolated copy of this package with no access to the
project tree (`06` R3).
Feature-level reproduction (`features.py` → `pipeline_v2.py`) requires the
challenge package in `repo/data/<region>/`, which is absent from this
working tree — see `05_reproduction_guide.md` §2 (status: **Not
verified**). The official score can only be confirmed on Zindi (submission
HeXaMraA).

## Checks actually executed

File identity and schema; GEOID uniqueness/format/order; numeric bounds;
**exact regeneration** of the documented file and of the sibling H1 file;
determinism (double execution); local-screen recomputation; probe-
consistency correlations; secrets/prohibited-content scan of this package;
**isolated self-containment run** of the packaged tests and rebuild from
the package alone; verification of the packaged `hu`/`area_km2` column
extract against its source parquet. Details and observed outputs:
`06_validation_report.md`. **No executed check failed.**

## What remains unverified

- The probe step's construction script — **searched for across the full
  workspace and all zip archives on 2026-10-29 and not found** (scope and
  negative result: `02` §3.1); the construction is documented and
  numerically consistent, but its exact arithmetic is unverified.
- span5's exact combination coefficients.
- Feature-pipeline re-execution (raw data layout absent).
- The Best Documentation form's sections **beyond** the Best
  Documentation section (that section's upload requirement — a single
  PDF or text document, max 10 MB — and its required
  "Submission ID" field were verified from the form itself on
  2026-10-29, and the form was **submitted by the participant on 2026-10-29 via the official form, category Best Documentation, uploading the consolidated PDF `Koussay-Mehdouani_Best-Documentation_HeXaMraA.pdf` (57 pages, 502,105 bytes, SHA-256 `17d7527ef9cf148fdb607c98c34024dd424af301572dac9aca83fb9d22260aee`) and entering Submission ID **HeXaMraA**** — `08` A5, register C033).
- The compliance status of the provided strata column
  `usfs_BuildingCount_sum` — an **open item**, with the evidence on both
  sides and the full dependency chain (`03` §7, `08` R11/§1.1).
- All private-split (70%) results.

## Award compliance

See `08_award_requirements_checklist.md` for the requirement-by-requirement
checklist against the official rules (fetched 2026-10-29), the prize
mechanics as far as official sources establish them, and the award
submission record: the form was **submitted by the participant on 2026-10-29 via the official form, category Best Documentation, uploading the consolidated PDF `Koussay-Mehdouani_Best-Documentation_HeXaMraA.pdf` (57 pages, 502,105 bytes, SHA-256 `17d7527ef9cf148fdb607c98c34024dd424af301572dac9aca83fb9d22260aee`) and entering Submission ID **HeXaMraA**** (register C033); `08` §3
also lists the actions that remain after submission.
