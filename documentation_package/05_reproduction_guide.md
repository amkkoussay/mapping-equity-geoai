# 05 — Reproduction Guide

Reproduction has **three distinct levels**. They are kept separate
throughout this package; success at one level implies nothing about the
others.

| Level | What it means | Status in this audit |
|---|---|---|
| L1 | Re-running the feature pipeline from the raw challenge package (`features.py` → `pipeline_v2.py` → `v2_tracts.parquet` and the v2 submissions) | **Not verified** — raw data absent in the `repo/` layout (see §2) |
| L2 | Rebuilding the documented submission file from its immediate inputs ($P$ and the v2 tract table's `hu`/`area_km2` columns) | **Verified exactly, and self-contained** — max abs diff 0.0 on all 9,794 rows; since the 2026-10-29 package repair, runnable **from this package alone** (isolated-directory run, `06` R3; see §3) |
| L3 | Reproducing the official leaderboard score 0.081231862 | **Not reproducible locally by construction** — only the Zindi evaluation system (or an official record) can produce/confirm it (see §4) |

## 1. Environment (as used for the audit runs)

- OS: Linux (project VM). Hardware: not recorded for the original runs; the
  audit runs are lightweight (seconds) except Stage A.
- Python 3.12.3 with the versions in `requirements.txt` (derived from the
  project's actual `.venv` and the imports of the relevant code paths). The
  original run-time package versions on 2026-10-28/29 were not separately
  recorded; L2 was reproduced exactly under the listed versions.
- No environment variables or credentials are required by any step. No
  secrets exist in the pipeline.

Setup:
```bash
cd geoai-zindi
python3.12 -m venv .venv && .venv/bin/pip install -r documentation_package/requirements.txt
# (the project already ships a .venv with these versions)
```

## 2. Level L1 — feature pipeline (NOT verified in this audit)

Expected layout (from `repo/features.py` / `repo/pipeline_v2.py`, which use
relative paths — run from `repo/`):
```
repo/data/<region>/<region>-{census-tracts,overture-buildings,overture-roads,
     overture-pois,overture-infrastructure,census-acs-housing,
     strata-tract-table,sample-submission}.parquet/csv
```
Commands (from `repo/README.md`):
```bash
pip install duckdb pandas pyarrow numpy   # duckdb spatial extension: LOAD spatial (auto in features.py)
python features.py          # writes feat/<region>.parquet
python pipeline_v2.py       # writes submission_v2.csv, v2_tracts.parquet, v2_summary.json
```
Status: **not executed**. `repo/data/` and `repo/feat/` do not exist in this
working tree, so the commands cannot run here as-is. A separate 2.9 GB
extract tree exists under `families-vexpfull/data/`, but it belongs to a
different feature pipeline and was **not** substituted. The pre-existing
writeup (`repo/WRITEUP.md` §1) states a runtime of "about 25 minutes for
features.py on 2 CPU / 5 GB RAM; under 10 seconds for pipeline_v2.py" — this
is a **documented claim from the original author, not a measurement of this
audit**, and is labelled accordingly.

Expected L1 outputs if the data is restored: `feat/*.parquet`,
`submission_v2.csv` (9,794 rows), `v2_tracts.parquet` (9,794 × 29). Their
agreement with the surviving artifacts (hashes in `00`) would then be
checkable byte-for-byte.

## 3. Level L2 — rebuilding the documented submission file (Verified, self-contained)

Since the 2026-10-29 package repair, **all L2 inputs are inside this
package** under `evidence/` (byte-identical copies / a verified extract;
hashes in `00` and `06` R1–R2):

- `evidence/05_poi_component_probe.csv` (the vector $P$; byte-identical to
  `upload28b/staged/05_poi_component_probe.csv`)
- `evidence/v2_tracts_columns.csv` — the `GEOID, hu, area_km2` columns of
  `max-gamble-pack/scored/v2_tracts.parquet`, verified against the parquet
  (9,794 rows; per-column max abs diff 0.0). The parquet itself remains the
  archival artifact in the project tree (SHA-256 in `00`); it is not
  packaged because it is binary.
- `evidence/submission_s0.8_HeXaMraA.csv` (comparison target; byte-identical
  to the submitted file)
- `evidence/evaluator.py` (byte-identical copy of `work29/evaluator.py`,
  packaged for reference: the original helper obtained $P$ and the tract
  order through its anchor frame; the packaged helper reads the probe CSV
  directly — same vector, same order — because importing `evaluator.py`
  standalone would try to load all 15 anchor files from the project tree)

Commands (runnable from **any** working directory; they write only to
stdout). The only external requirement is a Python environment with the
packages in `requirements.txt`:
```bash
python documentation_package/scripts/rebuild_s08.py
# observed output (2026-10-29): rows=9794  max_abs_diff=0.0  mean_abs_diff=0.0  exact_rows=9794
# exit code 0
python documentation_package/tests/test_submission_file.py
# observed: 10/10 PASS, exit code 0
```
Self-containment was **proven by execution**: the package directory alone
was copied to an isolated location (`/tmp/pkgtest/`) and both commands
were run there with no access to the project tree — 10/10 PASS and rebuild
exact, exit 0 (`06` R3). The same outputs were observed in the original
project environment (`06` T5/T10/T11).

The same computation with $(s_0,\alpha,\tau) = (0.8, -0.2, 1.0)$ reproduces
the sibling file `exp-v7/candidates/h1_winner.csv` exactly as well
(`06` T7; that control runs against project-tree files and is not part of
the self-contained level).

What L2 does **not** cover: the construction of $P$ itself (Stage D, script
not retained — `02` §3) and everything upstream of it (Stages A–C). L2
verifies the final, documented transformation exactly, given its inputs.

## 4. Level L3 — the official score (Not reproducible locally)

The official public score (0.081231862) is produced by Zindi's scorer
against the organisers' held-out reference data on the public split
(≈30% of tracts). Neither the reference data nor the scorer is available
locally, and the rules prohibit obtaining the reference data. The local
screen (approx 0.0711) is an anchor-projection approximation of that score,
not a reproduction of it (`03` §5, `07` §3). Verification of L3 is possible
only through the participant's Zindi submission record (ID HeXaMraA).

## 5. Troubleshooting (from the campaign record)

- **Platform "Missing entries for IDs …" error**: GEOID column parsed as
  integer, dropping leading zeros. Always read/write GEOID as text
  (`dtype={'GEOID': str}`). Documented incident: `repo/docs/experiments.csv`
  row Z81nvmtR (a different file; corrected before resubmission).
- **DuckDB spatial join slowness on south-central-tx** (11.46M buildings):
  encountered by a later, unrelated extraction; not part of this chain.
- **Screen disagreements between solver implementations**: use only the
  frozen `screening-v2/unified_screen.py` (minimum-norm projection); raw LU
  solves return arbitrary coefficient representatives
  (`screening-v2/SCREENING_STANDARD.md`).
