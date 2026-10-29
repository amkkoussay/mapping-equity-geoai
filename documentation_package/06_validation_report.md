# 06 — Validation Report (tests actually executed)

All tests were executed on 2026-10-29 in the project environment
(`~/workspace/geoai-zindi/.venv`, Python 3.12.3; versions in
`requirements.txt`). Tests are non-destructive: nothing under test was
modified; rebuilds were computed in memory. The audit driver is preserved
in the session record; the two packaged, re-runnable equivalents are
`scripts/rebuild_s08.py` and `tests/test_submission_file.py` (both re-run
after packaging: exit code 0).

| # | Check | Command / method | Observed result |
|---|---|---|---|
| T1 | Submission file identity | `sha256sum stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv` | `e5430d51d509955e4ce5def4eaf0c8f3c00e23a805b38642062eb7529311ede4`; 315,349 bytes. The packaged copy in `evidence/` is byte-identical (same hash) |
| T2 | Schema and row count | pandas read with `dtype={'GEOID': str}` | Columns exactly `[GEOID, coverage_gap_score]`; **9,794 data rows** (9,795 lines incl. header) |
| T3 | Identifier validity and ordering | comparisons vs `upload28b/staged/05_poi_component_probe.csv` and `exp-v7/candidates/h1_winner.csv` | 9,794 unique GEOIDs; all 11-character text; tract **set** equal to the anchors'; **row order identical** to both anchor files |
| T4 | Numeric sanity | min/max/mean, NaN and finiteness scan | No NaN; all finite; min 0.011793, max 0.248202, mean 0.059308 — all inside [0, 1] |
| T5 | **Regeneration of the documented file** | `scripts/rebuild_s08.py` (formula of `03` §5 from $P$ + `v2_tracts.parquet`) | **max abs diff 0.0, mean abs diff 0.0, exact on 9,794/9,794 rows**; campaign content-hash (md5 of values rounded to 8 dp) matches: `6909cb9bc9326598d591963b3a9e8a06` both sides |
| T6 | Determinism | second independent execution of the same build | Byte-for-value identical (`np.array_equal` → True) |
| T7 | Sibling-file control | same code path, H1 parameters (0.8, −0.2, 1.0) vs `exp-v7/candidates/h1_winner.csv` | max abs diff **0.0**, exact on 9,794/9,794 rows — the family code path reproduces a second, independently scored submission |
| T8 | Probe-construction consistency (exploratory) | correlations of $(P - \mathrm{span5})$ with centred v2 components from `v2_tracts.parquet` | corr with centred `poi_gap` = **0.940**; corr with centred `building_gap` = **−0.010**; max $\lvert P-\mathrm{span5}\rvert$ = 0.0214. Consistent with the documented "POI direction at quarter amplitude"; **inference, not proof** (script not retained) |
| T9 | Local screen recomputation | `screening-v2/unified_screen.py::screen_v2` on the submitted vector | approx **0.0711**, maxcoef **6.10**, proj 0.0682, resid 0.0201 — identical to `calibrated-screen/registry.csv` and to `exp-v7/attempts.csv` line 78 |
| T10 | Packaged test suite | `tests/test_submission_file.py` | **10/10 PASS**, exit code 0 |
| T11 | Packaged rebuild script | `scripts/rebuild_s08.py` | `rows=9794 max_abs_diff=0.0 mean_abs_diff=0.0 exact_rows=9794`, exit code 0 |
| T12 | Secrets / prohibited-content scan of this package | manual review + file inventory of `documentation_package/` | No credentials, tokens or vault material anywhere in the package; no challenge datasets or reference layers included — only the participant's own submission CSV, code copies, logs and this documentation |

## Failures and non-results (reported, not patched)

- **F1 — L1 reproduction not executable.** `repo/data/` (raw challenge
  extracts in the `repo/` layout) is absent, so `features.py` /
  `pipeline_v2.py` could not be re-run. No substitute data tree was used.
  This is a gap in the reproduction chain, recorded in `05` §2.
- **F2 — Probe construction script missing.** Stage D cannot be re-executed;
  only its documented description and the T8 consistency check support it.
  (Second pass, 2026-10-29: the script was searched for across the full
  workspace and all archives and **not found** — see R4 below and
  `02` §3.1. The *staging* script, `upload28b/check_order.py`, is retained;
  it re-keys already-built probe files and does not construct them.)
- **F3 — No platform-side artifact.** No test can upgrade the
  file→HeXaMraA→0.081231862 association beyond Strongly supported from
  local evidence alone (`02` §2).

No test that was run failed. Items F1–F3 are evidence gaps, not test
failures; they are carried into `09` and `10` as open items.

## Addendum — package self-containment repair (2026-10-29, second pass)

The first-pass package was **not self-contained**: `scripts/rebuild_s08.py`
read `max-gamble-pack/scored/v2_tracts.parquet`,
`upload28b/staged/05_poi_component_probe.csv` and `work29/evaluator.py`
from the project tree, and `tests/test_submission_file.py` also read the
probe from the project tree — a reviewer holding only this package could
not re-run them. This was found by the participant's own audit. The repair
below was executed and verified; the originals outside the package were
not touched, and no computation logic changed (path adaptation only, noted
in each file's header).

| # | Check | Command / method | Observed result |
|---|---|---|---|
| R1 | Byte-identity of the new evidence copies | `sha256sum` on copies vs originals | `evidence/05_poi_component_probe.csv` = `f5acaa101fc6fb5d094653ca09dd0a914c1b28f29dcad53cedd34b5d2298461d` — identical to `upload28b/staged/05_poi_component_probe.csv`. `evidence/evaluator.py` = `c65fc16d4791bc2d03779bb3be884fecdaea8ce9263b67c2171a59d44c996e38` — identical to `work29/evaluator.py` |
| R2 | Column-extract verification | Extract `GEOID, hu, area_km2` from `max-gamble-pack/scored/v2_tracts.parquet` (SHA-256 `f216c703ab9bfaf1b369eff466b038352f08b2df35766aaa3826d68f5b933c19`) into `evidence/v2_tracts_columns.csv`; re-read and compare | Rows 9,794 = 9,794; GEOID sequence identical; `hu` max abs diff **0.0**; `area_km2` max abs diff **0.0**; neither column contains NaNs. The runnable path uses this verified extract; the parquet remains the archival artifact (hash-recorded in `00`) and is **not** packaged, because it is binary |
| R3 | **Isolated self-containment run** | `cp -r documentation_package /tmp/pkgtest/`, then from `/tmp` (outside the project tree): `/home/hatch/workspace/geoai-zindi/.venv/bin/python /tmp/pkgtest/documentation_package/tests/test_submission_file.py` and `.../scripts/rebuild_s08.py` | Tests: **10/10 PASS**, exit 0. Rebuild: `rows=9794 max_abs_diff=0.0 mean_abs_diff=0.0 exact_rows=9794`, exit 0. All inputs resolved under the isolated copy's `evidence/`; the interpreter is the project's `.venv` (an environment, not project data); **no project files were read** |
| R4 | Probe-construction search + reconstruction attempt | Full-workspace and archive search (scope in `02` §3.1); four candidate direction forms fitted to $(P - \mathrm{span5})$: regionally centred/std-normalised `poi_gap` (the `dirn()` convention of `max-gamble-pack/code/make_batch28.py`), global z-score, globally centred raw `poi_gap`, and the building analogue against probe 04 — each at least-squares amplitude (≈0.0073) and at the round value 0.0075 | Construction script **not found** anywhere searched. No candidate form reproduces $P$: best max abs diff **5.0e-3** (vs 0.0 required). The exact Stage-D arithmetic therefore remains **Unverified**; T8's correlation consistency stands as the strongest available support |

After the repair, the packaged tests were re-run in place as well:
10/10 PASS and rebuild exit 0 (same outputs as R3).
