# 04 — Data Lineage and Edge Cases

## 1. Lineage table

All inputs are files of the challenge package (Source Cooperative bucket for
the Bias Bounty Mapping Equity Challenge; data licence CC-BY-SA 4.0 per the
official rules). No removed reference layer (TIGER, Microsoft footprints,
USGS facilities, CBP) is read by any step of this chain — verified by reading
`repo/features.py` and `repo/pipeline_v2.py` in full: their only inputs are
the per-region challenge files listed below.

| Input dataset (per region) | Input fields used | Transformation | Output feature / artifact | Evidence | Limitations |
|---|---|---|---|---|---|
| `<r>-census-tracts.parquet` | `GEOID`, `geometry` | Transform to EPSG:5070; polygon area / 10⁶ | `area_km2` (feat parquet; also in `v2_tracts.parquet`) | `repo/features.py` `run()` | Polygon area (Stage A) and strata `ALAND` (land area) are different quantities; both are used, for different purposes |
| `<r>-overture-buildings.parquet` | `bbox`, `sources` | Bbox-centroid point-in-tract count; OSM-source subset | `n_bldg`, `n_bldg_osm` | `repo/features.py` | Centroid assignment is an approximation (code comment): a building whose bbox centre falls outside the tract is missed, and vice versa |
| `<r>-overture-roads.parquet` | `class`, `geometry` | Intersect with tract; clip; length in EPSG:5070 / 1000 | `km_road`, `km_hwy` (classes motorway/trunk/primary/secondary) | `repo/features.py` | Segments are prefiltered by `ST_Intersects` then clipped; length is of the clipped part |
| `<r>-overture-pois.parquet` | `geometry`, `categories.primary` | Point-in-tract counts, total and by category set | `n_poi`, `n_fire`, `n_ems`, `n_school` | `repo/features.py` | Category sets are hard-coded lists in `features.py` |
| `<r>-overture-infrastructure.parquet` | `geometry` | Point-in-tract count | `n_infra` | `repo/features.py` | Extracted but **unused** downstream |
| `<r>-census-acs-housing.parquet` | `housing_units` | Left join on GEOID | `hu` | `repo/features.py` | May be NaN where a tract is absent from ACS |
| `<r>-strata-tract-table.parquet` | `ALAND`, `pop_total`, `ur_class`, `svi_overall`, `cvi_overall`, `tribal_any`, `usfs_BuildingCount_sum` | Left join on GEOID | flags, building reference $R$ | `repo/pipeline_v2.py` `STRATA`, `load()` | `usfs_BuildingCount_sum` is a provided strata column (USFS structure count), not a downloaded reference layer — see the compliance discussion in `08` |
| `<r>-sample-submission.csv` | `GEOID` | Authoritative tract list; GEOID read as text | Row set of every downstream artifact (9,794 tracts) | `repo/pipeline_v2.py` `load()` | Concatenation order of regions follows the `REGIONS` list in the code |
| `feat/<r>.parquet` + strata | all above | Components → composite → shrinkage (Stage B, `03` §2) | `v2_tracts.parquet` (29 cols), `submission_v2.csv` | `repo/pipeline_v2.py`; artifact hash in `00` | `repo/feat/` not present locally; the saved `v2_tracts.parquet` is the surviving output |
| 15 scored submission CSVs | `coverage_gap_score` + official scores | Gram matrix + quadratic identity (Stage C) | anchor span; span5 | `work29/evaluator.py`; `upload28/` README | Span coefficients for span5 not separately recorded |
| span5 + v2 POI component | — | + quarter-amplitude POI direction, clip (Stage D) | $P$ = `05_poi_component_probe.csv` | `upload28b/HYPOTHESIS.md` | Generating script not retained (see `02` §3) |
| $P$ + `v2_tracts.parquet` (`hu`, `area_km2`) | — | Density calibration (Stage E) | **submission file** `2_v7_probe_s0.8_a-0.4_tau0.5.csv` | `exp-v7/code/h1_density_calibration.py`; verified by re-execution (`06`) | Exact (verified) given its two inputs |

## 2. Edge cases — as actually implemented

Verified against the code; only cases the selected pipeline actually handles
are listed.

| Case | Where | Actual behaviour |
|---|---|---|
| Tract missing from Overture features | `pipeline_v2.load()` | Assertion fails the run (`assert d.region.notna().all()`) rather than silently dropping the tract |
| Building reference $R_i \le 0$ or missing | `pipeline_v2.building()` | Building component undefined (NaN); composite averages over the remaining defined components |
| No highway-class road in tract | `pipeline_v2.transport()` | Transport component undefined (NaN), **not** zero — absence of a highway is not treated as a full gap |
| Tract with no buildings/POIs/roads at all (`no_overture`) | `pipeline_v2.composite()` | If also not water-dominated and not zero-population: raw score forced to 1.0 ("people live there, nothing mapped") — 2 tracts carry the `no_overture` flag in `v2_tracts.parquet` |
| Water-dominated tracts (`is_water`, water share > 0.5 of polygon area) | `flags()`, `composite()` | Exempt from the forced-1.0 rule above — 43 tracts flagged |
| Zero-population tracts (`pop_total`=0 or `hu`=0) | `flags()`, `poi()` | POI establishments half undefined; exempt from the forced-1.0 rule — 82 tracts flagged |
| All three components undefined | `composite()` | Raw score filled with the tract's **regional mean** of raw — this is the pipeline's own documented rule |
| Division by zero | `poi()`, `building()` | Denominators guarded: `hu` clipped below at 1; building reference via `ref.where(ref > 0)`; expected-count sub-gaps defined only when expectation ≥ 0.5 |
| The two all-undefined ("water") tracts in the calibration stage | Stage E | The calibration consumes $P$, $hu$, $area$ only; every tract has a defined $P$ (the probe file is complete: 9,794/9,794 values), and $z$ is defined wherever $hu$ and $area$ exist. No special-casing occurs at this stage. (Separately, the campaign's local *screen* is sensitive to how these tracts are filled in some diagnostic variants — a property of the diagnostic, not of the submitted file; see `07` §3.) |
| Duplicate GEOIDs | `pipeline_v2.main()` + audit `06` | Pipeline asserts uniqueness of the output; the submitted file verified: 9,794 unique GEOIDs |
| GEOID leading zeros | staging history | A real incident is on record (`repo/docs/experiments.csv`, Z81nvmtR): an early staging of a *different* file parsed GEOIDs as integers and dropped leading zeros (2,183 IDs), causing a platform "missing entries" error; it was corrected and byte-verified before resubmission. The documented file was checked in `06`: all GEOIDs are 11-character text |
| Row ordering | Stage E + audit | Output order follows the anchor/probe file order; verified identical to the POI-probe and H1 files' order (`06` T3). The platform joins on GEOID; order is nevertheless kept identical to the sample/anchor convention |
| Invalid/missing geometries in raw extracts | Stage A | Not explicitly handled in `features.py` beyond DuckDB spatial semantics; **not tested** in this audit (raw data absent in `repo/` layout) — recorded as an untested area, not an assumed behaviour |
| Determinism / seeds | all stages | No randomness anywhere in the chain (no sampling, no fitting with random init); the calibration rebuild was executed twice in the audit with identical output (`06` T6). No seeds exist to set |

## 3. Worked miniature of the documented step (Stage E)

For this file's parameters the multiplier $s_i$ ranges over $[0.400, 1.200]$
across tracts and the mean-preserving shift is $a = \bar P - \bar{\tilde y}
= +0.011793$ (computed from the actual vectors during the audit; note the
file's mean, 0.059308, equals $\bar P$ exactly, as the construction
guarantees before clipping). For a tract with $P_i = 0.10$ in a sparse area
($z_i = -1.0$): $s_i = 0.8 - 0.4\tanh(-2) = 1.186$; $\tilde y_i = 0.1186$;
$\hat y_i = \mathrm{clip01}(0.1186 + 0.0118) \approx 0.130$. For a dense
tract ($z_i = +1.0$): $s_i = 0.414$, $\tilde y_i = 0.0414$, $\hat y_i
\approx 0.053$ — the same probe value is damped to about 40% of its sparse
counterpart. (Illustrative arithmetic from the formula in `03` §5; the
audit's exact reproduction of all 9,794 values is in `06`.)
