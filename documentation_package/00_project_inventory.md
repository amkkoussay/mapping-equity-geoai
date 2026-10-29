# 00 — Project Inventory

Project root: `~/workspace/geoai-zindi` (working tree of participant **koussayy**,
Koussay Mehdouani, for the Zindi *Bias Bounty Mapping Equity Challenge*).
Inventory taken 2026-10-29 during the documentation audit. The working tree
contains the full experiment campaign (≈60 experiment directories); this
inventory covers the complete structure at the top level and, in detail, every
artifact on the provenance chain of the documented submission (see
`02_submission_provenance.md`).

## 1. Top-level structure

| Entry | Role |
|---|---|
| `TRACKING.md` (93,334 bytes, 502 lines) | Timestamped campaign log; primary internal record of submissions, scores, decisions and rules quotations |
| `SPLITS.md` | Registered train/judgement split definitions |
| `repo/` | Clean solution repository (features + v2 pipeline + writeup + submission ledger) |
| `max-gamble-pack/scored/` | First scored submission files + `v2_tracts.parquet` (the v2 pipeline's full per-tract output table) |
| `upload28/`, `upload28b/` | 2026-10-28 submission batches: span/ridge candidates, component probes, staging + validation scripts |
| `work29/` | `evaluator.py` — exact-quadratic evaluator over the 15 scored anchor submissions; batch builders and sweeps |
| `exp-v3` … `exp-v15-audit/` | Sequential experiment families (GBM models, rubric recalibration, density calibration, piecewise, interaction, audits) |
| `screening-v2/` | Frozen local screening standard (`unified_screen.py`, `SCREENING_STANDARD.md`) |
| `screen-study/`, `calibrated-screen/` | Screen→board calibration study; `calibrated-screen/registry.csv` is the 20-submission registry |
| `stage2/` | 2026-10-29 second-stage families; `stage2/lowest3/` holds the three regenerated lowest-screen files that were submitted on 2026-10-29 |
| `metric-audit/` | Independent audit establishing that the leaderboard metric behaves as RMSE |
| `feature-audit/`, `audit-final/`, `forensic-error-analysis/` | Prior forensic audits of the campaign |
| `bias-build/`, `families-*`, `h1-next/`, `new-hypotheses/`, others | Bias-discovery track and later hypothesis families (not on this submission's chain) |
| `competitor-ref/` | Public competitor material kept for reference (not used by the documented pipeline) |
| `.venv/` | Python 3.12.3 environment (see `requirements.txt`) |

No `.git` directory exists in the project root or in `repo/`; there is **no git
history available locally**. Version provenance therefore rests on file hashes,
timestamps and logs, not commits.

## 2. Artifacts on the documented submission's chain (detailed)

All sizes/timestamps as observed 2026-10-29; hashes SHA-256.

| Artifact | Size | Modified | SHA-256 | Role |
|---|---|---|---|---|
| `repo/features.py` | 3,364 B | 2026-10-26 | `ab11895c127d9a6c0c61247ae53c6d7900b5f8e05d76bf302da0c11d90f28013` | Per-tract Overture feature extraction (DuckDB spatial) |
| `repo/pipeline_v2.py` | 5,616 B | 2026-10-26 | `08882bb1db6bf5a4034e4494c7a92ed58453e791635aa6bde79f0198f580ac10` | Heuristic component composite ("v2") |
| `max-gamble-pack/scored/v2_tracts.parquet` | 1,134,425 B | 2026-10-27 | `f216c703ab9bfaf1b369eff466b038352f08b2df35766aaa3826d68f5b933c19` | v2 output table: 9,794 tracts × 29 columns (features, components, flags) |
| `upload28/zindi-5-daily-submissions/01_span5_balanced.csv` | — | 2026-10-28 | `016d353013bab0bdc3576e45c4e616f0a16279be61c4158acbebee93e5f06cda` | Anchor submission "span5" (official 0.084844078) |
| `upload28b/staged/05_poi_component_probe.csv` | 239,776 B | 2026-10-28 | `f5acaa101fc6fb5d094653ca09dd0a914c1b28f29dcad53cedd34b5d2298461d` | Anchor submission "POI probe" (official 0.08483727); the vector **P** consumed by the documented solution |
| `upload28b/HYPOTHESIS.md` | 1,394 B | 2026-10-28 | (copy in `evidence/`) | Design note for the component probes |
| `work29/evaluator.py` | 3,826 B | 2026-10-28 | `c65fc16d4791bc2d03779bb3be884fecdaea8ce9263b67c2171a59d44c996e38` (copy in `evidence/`) | Anchor registry (`SCORED`: 15 files → official public scores) + quadratic evaluator |
| `exp-v7/code/h1_density_calibration.py` | 4,411 B | 2026-10-28 | `8854a88fd568647c0613e39407474f117ca9bf17f7eef7d8ee3101d55e0054fc` | The density-calibration family code (grid + winner export) |
| `exp-v7/attempts.csv` | 56,674 B | 2026-10-28 | (copy in `evidence/`) | 456-row grid log; the documented configuration is recorded at line 78 (see `02`) |
| `exp-v7/candidates/h1_winner.csv` | 314,951 B | 2026-10-28 | `02ffcc0eea928af85bf552311f09a6e8dba0e7be7d0f5b0be4ef4b26b45a5811` | Sibling submission H1 (official 0.082777005); same code path, different parameters |
| `exp-v7/log.txt` | 1,632 B | 2026-10-28 | — | Run log of the exp-v7 grid |
| `screening-v2/unified_screen.py` | 2,908 B | 2026-10-29 | — | Frozen local screen implementation (`screen_v2`) |
| `screening-v2/SCREENING_STANDARD.md` | 2,385 B | 2026-10-29 | (copy in `evidence/`) | Frozen screening standard and acceptance gates |
| `stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv` | 315,349 B | 2026-10-29 13:18 | `e5430d51d509955e4ce5def4eaf0c8f3c00e23a805b38642062eb7529311ede4` | **THE documented submission file** (copy in `evidence/submission_s0.8_HeXaMraA.csv`) |
| `calibrated-screen/registry.csv` | 3,611 B | 2026-10-29 | (copy in `evidence/`) | Registry of all 20 scored submissions (IDs, files, official scores, screen values) |
| `metric-audit/REPORT.txt` | 4,865 B | 2026-10-29 | — | Metric audit: leaderboard behaves as RMSE |
| `repo/docs/experiments.csv` | — | through 2026-10-29 (H1) | — | Repo submission ledger — **stops at H1; the 2026-10-29 afternoon submissions (s1.1, s0.8, H4, H6) are absent** (see §4) |
| `repo/WRITEUP.md`, `repo/README.md` | — | 2026-10-26/27 | — | Pre-existing documentation-prize texts for the v2 method (see §4) |

**Package-repair additions (2026-10-29, second pass).** To make this
package self-contained at reproduction level L2, `evidence/` additionally
holds: a byte-identical copy of `upload28b/staged/05_poi_component_probe.csv`
(SHA-256 `f5acaa10…`, see table above), a byte-identical copy of
`work29/evaluator.py` (hash in table above), and
`evidence/v2_tracts_columns.csv` — the `GEOID, hu, area_km2` extract of
`v2_tracts.parquet`, verified against the parquet (9,794 rows; per-column
max abs diff 0.0; `06` R2). The parquet itself (1,134,425 B, binary) is
not packaged; it remains the hash-recorded archival artifact in the
project tree.

## 3. Code entry points and execution flow (documented chain)

```
challenge package (per region: Overture extracts, ACS housing, strata, sample submission)
  └─ repo/features.py            → feat/<region>.parquet          [NOT re-run in this audit: repo/data absent locally]
      └─ repo/pipeline_v2.py     → submission_v2*.csv, v2_tracts.parquet
          └─ scored anchor submissions (15 files, official scores in work29/evaluator.py SCORED)
              └─ affine-span / ridge algebra (work29) → span5 (01_span5_balanced.csv)
                  └─ component probe step (upload28b)  → P = 05_poi_component_probe.csv
                      └─ exp-v7 density calibration (s0=0.8, alpha=-0.4, tau=0.5, z=housing density)
                          └─ stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv  → submitted as HeXaMraA
```

## 4. Inconsistencies and missing artifacts found during inventory

1. **`repo/README.md` is stale**: it states "Best public RMSE: 0.104203". The
   best official public score in the records is 0.081231862 (this package).
   `repo/WRITEUP.md` documents only the v2 method and lists 0.104203 as its
   best; neither file mentions the span/probe/calibration chain.
2. **`repo/docs/experiments.csv` is incomplete**: it ends at H1
   (2026-10-29, 6QMBo4iq — recorded twice, a duplicate row) and omits the four
   scored submissions of 2026-10-29 afternoon (Cvdyznfk, HeXaMraA, 7WvX14fp,
   SobRVFX8), which appear only in `TRACKING.md`, `calibrated-screen/` and
   `screen-study/` records.
3. **No official submission receipt, confirmation e-mail or platform
   screenshot** for any submission exists anywhere in the tree (searched:
   receipt/screenshot/image artifacts — only competitor figures found). The
   file→submission-ID→score association initially rested on internal
   records (see `02`). **Update (2026-10-29 evening):** a capture of the
   official submissions page was obtained and is retained in this package
   as `evidence/zindi_submissions_proof.pdf` (SHA-256 `46c507f4…`),
   upgrading the documented submission's association to **Verified —
   platform record captured** (`02` §2). The other submissions'
   associations still rest on internal records.
4. **The exact construction script of the staged POI-probe file was not
   retained**; its construction is documented in `upload28b/HYPOTHESIS.md`
   and `repo/docs/experiments.csv`. A dedicated second-pass search of the
   full workspace and all zip archives (2026-10-29) did **not** find it —
   scope and negative result in `02` §3.1. (The staging script
   `upload28b/check_order.py` IS retained; it re-keys, but does not
   construct, the probe files.)
5. **`repo/data/` and `repo/feat/` are absent**: the raw challenge extracts in
   the `repo/` layout are not in this working tree (a separate 2.9 GB extract
   tree exists under `families-vexpfull/data/`, built for a different feature
   pipeline). The feature-extraction level is therefore not re-runnable in
   place (see `05`).
6. **No git history** (see §1).
