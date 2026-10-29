# 03 — Technical Methodology (as implemented)

## 0. What kind of method this is

The documented solution is a **deterministic heuristic pipeline with two
algebraic calibration steps — not a trained machine-learning model**. There
is no training set, no fitted regressor and no randomness anywhere in the
chain. The only quantities "fit" anywhere are (a) affine combination
coefficients derived from the *public scores of earlier submissions* and the
second moments of their prediction vectors, and (b) three scalar parameters
$(s_0, \alpha, \tau)$ selected from a logged grid by a local screening
statistic. Every step is stated below in execution order, with the
implementation file and function named. Where a detail could not be
established from code or artifacts, it is marked **Unverified** rather than
reconstructed from memory.

**Problem.** For each of 9,794 scored Census tracts (five regions:
eastern-ok 1,192; eastern-wa 415; maricopa-az 1,593; northern-ca 591;
south-central-tx 6,003), estimate a coverage-gap score in $[0,1]$: how much
of the real-world built environment is missing from Overture Maps, relative
to reference layers (TIGER roads, Microsoft building footprints, USGS
facilities, CBP establishments) that the organisers removed from the
challenge package and that the rules forbid using. The official metric
behaves as RMSE (see `07` §2 and `metric-audit/REPORT.txt`); the public
leaderboard reflects ≈30% of the scored tracts.

## 1. Stage A — per-tract feature extraction (`repo/features.py`)

Engine: DuckDB with the `spatial` extension; all geometry work in
EPSG:5070 (NAD83 / Conus Albers, equal-area) after transforming from
EPSG:4326. Inputs per region, all from the challenge package:
`<region>-census-tracts.parquet`, `-overture-buildings.parquet`,
`-overture-roads.parquet`, `-overture-pois.parquet`,
`-overture-infrastructure.parquet`, `-census-acs-housing.parquet`.
Output: `feat/<region>.parquet`, one row per tract. Features:

| Feature | Definition (as coded) | Source columns | Missing behaviour |
|---|---|---|---|
| `area_km2` | $\mathrm{ST\_Area}(\text{tract polygon in EPSG:5070}) / 10^6$ | census-tracts `geometry` | — |
| `n_bldg` | Count of buildings whose **bounding-box centroid** falls inside the tract (`ST_Intersects` of tract polygon with the bbox-centre point) | overture-buildings `bbox`, `sources` | Tracts with no joined buildings get 0 (`coalesce`) |
| `n_bldg_osm` | Subset of `n_bldg` with `sources[1].dataset = 'OpenStreetMap'` | overture-buildings `sources` | 0 if none |
| `km_road` | Sum over road segments intersecting the tract of the **tract-clipped** length in km (EPSG:5070) | overture-roads `class`, `geometry` | 0 if none |
| `km_hwy` | Same, restricted to classes {motorway, trunk, primary, secondary} | overture-roads `class` | 0 if none |
| `n_poi` | Count of places whose point geometry intersects the tract | overture-pois `geometry` | 0 if none |
| `n_fire` / `n_ems` / `n_school` | Subsets of `n_poi` by `categories.primary`: fire = `fire_department`; EMS = `ambulance_and_ems_services`; school ∈ {elementary_school, middle_school, high_school, school, private_school, public_school} | overture-pois `categories.primary` | 0 if none |
| `n_infra` | Count of infrastructure features intersecting the tract | overture-infrastructure | 0 if none (extracted; **not used** by pipeline v2) |
| `hu` | ACS housing units | census-acs-housing `housing_units` | Left-joined; may be NaN if a tract is absent from ACS |

Documented approximation (in the code's own comment): buildings are assigned
by bounding-box centre, not by polygon intersection.

## 2. Stage B — heuristic component composite "v2" (`repo/pipeline_v2.py`)

`load()` takes the tract list from the per-region **sample-submission files**
(authoritative; GEOID read as text) and left-joins Stage-A features and the
strata table columns `ALAND, pop_total, ur_class, svi_overall, cvi_overall,
tribal_any, usfs_BuildingCount_sum`. All constants live in one dict `P`:
`ROAD_CONST=0.05`, `WATER_FRAC=0.5`, `ALPHA=0.25`, `BUILDING_REF="usfs"`,
component weights all 1.0.

**Flags** (`flags()`):
- $\mathrm{water\_frac} = \mathrm{clip01}\bigl(1 - \mathrm{ALAND} / (\mathrm{area\_km2}\cdot10^6)\bigr)$; `is_water` iff water_frac > 0.5.
- `is_zero_pop` iff `pop_total` = 0 (NaN→0) or `hu` = 0 (NaN→0).
- `no_overture` iff `n_bldg` = 0 and `n_poi` = 0 and `km_road` = 0.

**Components** (each a per-tract gap in $[0,1]$, possibly undefined = NaN):

*Building* (`building()`), reference = strata `usfs_BuildingCount_sum` $R$:
$$ g^{bld}_i = \mathrm{clip01}\bigl(1 - n^{bld}_i / R_i\bigr) \quad \text{if } R_i > 0, \text{ else undefined.} $$
Fallback mode `BUILDING_REF="none"` (not the submitted configuration):
$g = \mathrm{clip01}\bigl(1 - (n^{bld}/\max(hu,1))\,/\,\text{regional median of that ratio}\bigr)$.

*Transport* (`transport()`): $g^{tr}_i = 0.05$ if `km_hwy` > 0, else
undefined. (Presence-only: without a named-highway reference layer the code
assigns a small constant where a highway-class road exists in Overture.)

*POI* (`poi()`): two halves, combined by `nanmean`:
- facilities half: expected counts $\hat n^{school} = hu/1500$,
  $\hat n^{fire} = hu/4000$; sub-gap $\mathrm{clip01}(1 - n/\hat n)$ defined
  only when $\hat n \ge 0.5$; half = `nanmean` of the two sub-gaps
  ($hu$ clipped below at 1).
- establishments half: $\mathrm{clip01}\bigl(1 - (n^{poi}/hu) / \text{regional median}(n^{poi}/hu)\bigr)$,
  undefined for zero-population tracts.

**Composite** (`composite()`): weighted mean over the components that are
**defined** for the tract (weights 1.0):
$$ \mathrm{raw}_i = \frac{\sum_k w_k\, g^k_i \,\mathbb 1[g^k_i \text{ defined}]}{\sum_k w_k\, \mathbb 1[g^k_i \text{ defined}]} $$
Edge rules, in order: if every component is undefined, `raw` = the tract's
regional mean of `raw`; if `no_overture` and not water and not zero-pop,
`raw` := 1.0. Final score applies regional shrinkage with `ALPHA = 0.25`:
$$ \hat y^{v2}_i = \mathrm{clip01}\bigl(0.25\cdot \mathrm{raw}_i + 0.75\cdot \overline{\mathrm{raw}}_{\text{region}(i)}\bigr). $$
Outputs: `submission_v2.csv`, `v2_tracts.parquet` (all intermediates),
`v2_summary.json`. In the saved `v2_tracts.parquet` (9,794 × 29, SHA-256 in
`00`): undefined shares are transport 1.4%, POI 0.8%, building 0.0%; flags:
`is_water` 43 tracts, `is_zero_pop` 82, `no_overture` 2.

## 3. Stage C — scored anchors and affine-span algebra (`work29/evaluator.py`)

Fifteen submission files were scored on the public leaderboard (the
"anchors"; official scores in `evaluator.py`'s `SCORED` dict and in
`repo/docs/experiments.csv`): the v1/v2 family, global level scalings of the
v2 regional means (×0.8, ×1.2, ×0.53 from a quadratic level fit), regional
shift probes, span/ridge combinations, and the two component probes.

For any affine combination $\hat y = \sum_k c_k f_k$ of anchor vectors $f_k$
with $\sum_k c_k = 1$, the evaluator uses the exact quadratic identity
$$ \widehat{\mathrm{RMSE}}^2(\hat y) \;=\; c^{\top} G\, c \;-\; c^{\top} \mathrm{diag}(G) \;+\; c^{\top} s^{2}, $$
where $G = F^{\top}F/n$ is the Gram matrix of the anchor vectors over all
9,794 tracts and $s$ is the vector of their official public scores. This is
exact algebra for combinations of scored submissions given the anchors'
second moments; using full-tract second moments in place of the (unknown)
public-subset moments is the working approximation, and the campaign treated
the outputs as estimates (documented caveat in
`upload28/zindi-5-daily-submissions/README.md`).

**span5** (`01_span5_balanced.csv`, official 0.084844078): a five-direction
affine candidate produced with this algebra (`upload28` README, candidate 1).
The exact five directions and coefficient vector are **not separately
recorded** in the retained artifacts — **Unverified detail**; the file and
its score are artifacts of record.

## 4. Stage D — POI component probe (`upload28b/`)

Per `upload28b/HYPOTHESIS.md` and `repo/docs/experiments.csv` (row
`cjw1BmR3`): the probe starts from span5 and adds **one component direction
— the POI component — at quarter amplitude**:
$$ P \;=\; \mathrm{span5} \;+\; \tfrac{1}{4}\cdot(\text{POI-component direction}), \qquad P \text{ clipped to } [0,1]. $$
The result, `upload28b/staged/05_poi_component_probe.csv` (SHA-256
`f5acaa10…`), scored **0.08483727** officially. The staging script that
produced the file was not retained; the exact form of the direction
(centering convention) is **Unverified**. Audit consistency check
(`06` T8): $\mathrm{corr}(P - \mathrm{span5},\; \text{centred } g^{poi}) =
0.940$, $\mathrm{corr}(P - \mathrm{span5},\; \text{centred } g^{bld}) =
-0.010$, $\max|P - \mathrm{span5}| = 0.0214$ — consistent with the documented
construction, not a proof of it.

## 5. Stage E — density calibration (exp-v7) — the documented step

Implementation: `exp-v7/code/h1_density_calibration.py`, functions `build()`
and `zstd()`. Inputs: the probe vector $P$ (Stage D) and, from
`v2_tracts.parquet`, each tract's housing units $hu_i$ and polygon area
$a_i$ (`area_km2`, clipped below at 0.05 km²).

$$ z_i = \frac{\log\bigl(1 + hu_i / \max(a_i, 0.05)\bigr) - \mu}{\sigma}
\qquad\text{(standardised log housing density)} $$
$$ s_i = s_0 + \alpha \tanh\!\bigl(z_i / \tau\bigr), \qquad
\tilde y_i = s_i \cdot P_i, \qquad
\hat y_i = \mathrm{clip01}\Bigl(\tilde y_i + \underbrace{\bar P - \bar{\tilde y}}_{\text{mean-preserving shift } a}\Bigr). $$

**Documented configuration ("s0.8"):** $s_0 = 0.8$, $\alpha = -0.4$,
$\tau = 0.5$, $z$ = housing density. Because $\alpha < 0$, the multiplier
ranges from ≈1.2 in the least dense tracts to ≈0.4 in the densest: the probe
signal is amplified where housing is sparse and damped where it is dense,
then re-centred so the overall mean equals the probe's mean, and clipped to
$[0,1]$.

**How the configuration was found.** The exp-v7 run evaluated a logged grid
of 456 configurations (`evidence/exp-v7_attempts.csv`): two base vectors
(probe; raw `poi_gap`), three density variables (building, housing, their
mean), $s_0 \in \{0.8, 0.9, 1.0, 1.1\}$, $\alpha \in \{-0.4,-0.2,-0.1,0.1,
0.2,0.4\}$ plus $\alpha=0$ references, $\tau \in \{0.5, 1.0, 2.0\}$, each
scored by the local screen of the time. The grid's selected winner
($\alpha=-0.2$, $\tau=1.0$) became submission H1 (official 0.082777005).
The documented configuration is grid line 78 of `attempts.csv`
(approx 0.0711, maxcoef 6.1, recorded `ok=False` because maxcoef exceeded
the 2.5 gate). On 2026-10-29 the three lowest-screen grid configurations
were regenerated into `stage2/lowest3/` and submitted by the participant's
decision; s0.8 returned the best official score of the three.

**The local screen (selection diagnostic only — not part of the file's
computation).** Frozen standard: `screening-v2/SCREENING_STANDARD.md`,
implementation `screen_v2` in `screening-v2/unified_screen.py`. A candidate
vector is projected onto the affine span of the 15 anchors by the unique
minimum-norm coefficient vector (truncated-SVD pseudo-inverse, relative
cutoff $10^{-10}$; the anchors' effective affine rank is 11 of 15).
$\mathrm{approx}^2 = \mathrm{proj}^2 + \mathrm{resid}^2$, where `proj` is the
quadratic-form value of Stage C at the projection coefficients and `resid`
is the RMS of the component orthogonal to the anchor span.
$\mathrm{maxcoef} = \max_k |c_k|$ measures extrapolation leverage. Frozen
gates: approx below the incumbent's board score **and** maxcoef ≤ 2.5. For
the documented file: approx 0.0711, maxcoef 6.10, proj 0.0682, resid 0.0201
(recomputed in `06`). **approx is a local approximation of the public score
built from the anchors — it is not the official metric and not an official
score** (official: 0.081231862; the screen-to-board gap for this family is
documented in `07`).

## 6. Output

CSV with header `GEOID,coverage_gap_score`, one row per scored tract
(9,794), GEOID as 11-character zero-padded text, scores in $[0,1]$, row
order identical to the anchor files' order (verified in `06`). This matches
the sample-submission schema used throughout the campaign.
