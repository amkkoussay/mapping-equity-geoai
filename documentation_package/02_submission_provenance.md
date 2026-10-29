# 02 — Submission Provenance

## 1. The selected submission

| Field | Value | Status |
|---|---|---|
| Participant | Koussay Mehdouani — Zindi username **koussayy** | Documented (`repo/WRITEUP.md` §1) |
| Zindi submission ID | **HeXaMraA** | Strongly supported (§2) |
| Official public score | **0.081231862** (public leaderboard RMSE; public split ≈30% of test tracts) | Strongly supported (§2) |
| Submitted | 2026-10-29, 14:40 (Africa/Tunis), via the Zindi web interface | Documented (`TRACKING.md`) |
| Local file | `stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv` | Verified as an artifact (hash below) |
| File SHA-256 | `e5430d51d509955e4ce5def4eaf0c8f3c00e23a805b38642062eb7529311ede4` | Verified (computed 2026-10-29) |
| File format | CSV, 9,794 data rows, columns `GEOID,coverage_gap_score`; GEOIDs as 11-character text | Verified (`06`) |
| Score range in file | [0.01179, 0.24820], mean 0.05931 | Verified (`06`) |
| Local screen (frozen v2 standard) | approx **0.0711**, maxcoef **6.10** — a local approximation, **not** the official score | Verified (`06`) |
| Campaign rank context | Best of the participant's 20 scored submissions; at last live check (2026-10-29) the account stood at 20/200 submissions used | Documented (`TRACKING.md`) |

## 2. Evidence for the file → ID → score association

Three mutually independent internal records agree on the triple
(file, HeXaMraA, 0.081231862):

1. **`TRACKING.md`**, entry "2026-10-29 ~14:29–14:42 — LOWEST-3 SUBMITTED TO
   THE BOARD", item 2: *"v7_probe_s0.8_a-0.4_tau0.5 (HeXaMraA, 14:40): public
   0.081231862 (screen 0.0711 @ 6.10) — NEW PUBLIC BEST"*.
2. **`calibrated-screen/registry.csv`**, row `HeXaMraA`: name `s0.8`, file
   `stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv`, screen 0.0711, official
   0.081231862, maxcoef 6.1, L1 38.596613, family `density_calibration`
   (copy in `evidence/registry.csv`).
3. **Code tables** in `calibrated-screen/calibrate.py` and
   `screen-study/apply_law_all.py` (`GENUINE` dict) record the same
   file→ID→score mapping, and `screen-study/LAW_APPLIED_ALL.md` reproduces
   the same screen value (0.0711) for the file.

**Residual uncertainty (stated plainly):** no official platform receipt,
confirmation e-mail, or screenshot of the submission exists in the project
tree (searched 2026-10-29; see `00` §4.3). The association is therefore
labelled **Strongly supported**, not Verified. It can be upgraded to Verified
only against the participant's own Zindi submissions page.

## 3. Generation chain (how the file was produced)

```
(1) repo/features.py            challenge package → per-tract Overture features
(2) repo/pipeline_v2.py         features + strata → v2 components & composite
                                → max-gamble-pack/scored/v2_tracts.parquet
(3) scored submissions          v2 variants scored on the board (15 anchors,
                                official scores in work29/evaluator.py SCORED)
(4) span algebra (work29)       affine-span fits over anchors → span5
                                (01_span5_balanced.csv, official 0.084844078)
(5) component probe (upload28b) span5 + quarter-amplitude POI-component
                                direction → P = 05_poi_component_probe.csv
                                (official 0.08483727)
(6) exp-v7 grid                 456 recorded configurations of a density
                                calibration applied to P; the documented
                                configuration is attempts.csv line 78
(7) regeneration (2026-10-29)   the three lowest-screen configurations were
                                regenerated into stage2/lowest3/ and checked
                                to reproduce their recorded screen values
(8) submission                  file (7) uploaded 2026-10-29 14:40 → HeXaMraA
```

Step-by-step status:

| Step | Status | Basis |
|---|---|---|
| (1)–(2) code exists and reads only challenge-package files | Verified (code inspection) | `repo/features.py`, `repo/pipeline_v2.py` read in full |
| (1)–(2) executed output `v2_tracts.parquet` | Strongly supported | Artifact present (SHA-256 `f216c703…`); the run itself was **not** re-executed (raw data absent in `repo/` layout) |
| (3) anchor scores | Strongly supported | `work29/evaluator.py` SCORED + `repo/docs/experiments.csv` + `TRACKING.md` agree |
| (4) span5 construction | Strongly supported | `upload28/…/README.md` + `experiments.csv`; exact fit coefficients not separately recorded |
| (5) probe construction | Strongly supported (documented) / exact arithmetic **Unverified** | `upload28b/HYPOTHESIS.md`; construction script **searched for across the full workspace and archives (2026-10-29) and not found** (§3.1); staging script `check_order.py` retained (it re-keys, does not construct); numeric consistency check in `06` (corr 0.940 with the centred POI component) and reconstruction attempt `06` R4 |
| (6) grid record of the configuration | Verified | `exp-v7/attempts.csv` line 78 |
| (6)+(7) code → file | **Verified by re-execution** | Audit rebuild (`scripts/rebuild_s08.py`) reproduces the file with max abs diff **0.0** on all 9,794 rows; the sibling H1 file also reproduces exactly (`06`) |
| (8) file → HeXaMraA → 0.081231862 | Strongly supported | §2 above |

## 3.1 Search for the probe construction script (2026-10-29, second pass)

The first pass of this audit reported the Stage-D generating script as
"not retained". At the participant's direction, a dedicated search was
executed before that wording was allowed to stand. **Result: not found.**
Scope and method, so the negative result is itself auditable:

- **Trees searched (content grep over `*.py`, `*.ipynb`, `*.sh`, `*.R`,
  plus filename search):** the entire `~/workspace/geoai-zindi` tree
  (excluding `.venv`) — including `repo/`, `upload28/`, `upload28b/`,
  `max-gamble-pack/`, `work29/`, `batch28/`, `batch29/`, `batch-final/`,
  `pkg/`, `pkg2/`, `review-bundle/`, `rebuild-lab/`, `audit-final/` and
  all `exp-*` directories — and the rest of `~/workspace/` outside
  `geoai-zindi/` (filename search for `*probe*`, content grep for the
  probe filename).
- **Keys:** `poi_component_probe`, `component_probe`, `05_poi`,
  `span5`, `quarter`, `amplitude`, `staged`, and code writing
  `04_building_component_probe.csv` / `05_poi_component_probe.csv`.
- **Archives searched (member listings + name grep):** every zip in
  `~/workspace/your_files/` (9 archives, incl. `zindi-ALL-work-2026-10-28.zip`,
  `zindi-max-gamble-pack.zip`, `zindi-experiments-package-2026-10-28.zip`,
  `zindi-forensic-audit-2026-10-28.zip`, `H1-complete-2026-10-28.zip`) and
  the zip of this package.
- **Ruled out by inspection:** `repo/probe.py` (read in full — a v1-era
  hypothesis script: regional mean + β·standardised feature probes; a
  different construction); `upload28b/check_order.py` and
  `upload28b/validate_b.py` (retained — they validate and re-key the
  already-built raw probe CSVs into `staged/`; they do not construct
  them); `max-gamble-pack/code/make_batch28.py` (retained — builds the
  *batch28* candidates from a different base at 0.03 amplitude; not the
  component probes).
- **Archive snapshot evidence:** `zindi-ALL-work-2026-10-28.zip` captures
  the whole project tree at 2026-10-28 00:24 — after the raw probe files
  were written (2026-10-27 23:18) — and its `upload28b/` contains only
  `HYPOTHESIS.md`, `validate_b.py`, `check_order.py`, the raw CSVs and
  `staged/`. No construction script exists even in that contemporaneous
  snapshot.
- **Reconstruction attempt (`06` R4):** four candidate direction forms
  (including the exact `dirn()` centring convention of the retained
  batch28 builder) were fitted to $(P - \mathrm{span5})$; none reproduces
  $P$ (best max abs diff 5.0e-3, not 0.0).

Conclusion: the raw probe files were most plausibly produced in an
interactive session whose code was never saved to disk. The construction
remains **documented** (`HYPOTHESIS.md`, experiments ledger) and
**numerically consistent** (T8), but it is not re-executable and its exact
arithmetic is **Unverified**. This replaces any bare "script lost" wording
elsewhere in this package.

## 4. Candidate comparison (why this file, not another)

| Candidate | Official score | File | Association status |
|---|---|---|---|
| **s0.8 (documented)** | **0.081231862** | `stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv` | Strongly supported; code→file Verified |
| s1.1 | 0.082179413 | `stage2/lowest3/1_v7_probe_s1.1_a-0.4_tau0.5.csv` | Same record set; worse official score |
| H4 piecewise | 0.082783512 | `stage2/lowest3/3_H4_piecewise_a.75_b-.2_c-.2_d.2.csv` | Same record set; worse official score |
| H1 | 0.082777005 | `exp-v7/candidates/h1_winner.csv` | Ledger + records; code→file Verified in this audit; worse official score |
| H6 β=−0.6 | 0.082509789 | `screen-study/h6_beta-0.6_candidate.csv` | Pre-registration + hash-stamped test in `TRACKING.md`; worse official score |

Selection rule applied: the documented submission is the one with the best
**official** score in the records — not the best local screen (the best local
screen of the campaign, 0.0679 for a blend candidate, belongs to a file that
was never submitted).

## 5. Discrepancies noted

- `repo/docs/experiments.csv` does not contain HeXaMraA (ledger stops at H1,
  with H1 duplicated). The afternoon submissions of 2026-10-29 exist only in
  `TRACKING.md` and the screen-study/calibrated-screen records.
- The exp-v7 grid log marks the documented configuration `ok=False`: under
  the campaign's frozen gates its maxcoef (6.10) exceeded the 2.5 cap. It was
  regenerated and submitted on 2026-10-29 by the participant's explicit
  decision, as one of the three lowest-screen candidates — **not** as a
  gate-passing candidate. This is disclosed, not hidden (`07` §4).
- The file in `stage2/lowest3/` is a **regeneration** (2026-10-29 13:18) of
  the configuration first computed in the exp-v7 grid (2026-10-28). Because
  the regeneration reproduces the grid-era values exactly and the audit
  rebuild reproduces the file exactly, the regeneration and the original
  computation are value-identical; no earlier byte-copy of the s0.8 vector
  survives (the exp-v7 script only exported its winner, H1).
