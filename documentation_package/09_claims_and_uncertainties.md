# 09 — Claims and Uncertainties

Confidence labels: **Verified** (direct artifact or executed check) ·
**Strongly supported** (multiple agreeing records) · **Documented claim**
(single record, not independently checked) · **Unverified / Unknown**.

## Verified

- The documented file exists, is 9,794 rows of `GEOID,coverage_gap_score`,
  all GEOIDs unique 11-character text, all scores finite in
  [0.011793, 0.248202], SHA-256 `e5430d51…` (`06` T1–T4).
- The file is reproduced **exactly** (max abs diff 0.0) from
  $P$ = `05_poi_component_probe.csv` and `v2_tracts.parquet` by the formula
  of `03` §5 with $(s_0,\alpha,\tau) = (0.8, -0.4, 0.5)$; the build is
  deterministic; the sibling H1 file reproduces exactly too (`06` T5–T7).
- The frozen local screen of the file is approx 0.0711 / maxcoef 6.10,
  recomputed (`06` T9) — a local diagnostic, **not** an official score.
- The exp-v7 grid log records this configuration at `attempts.csv` line 78
  with `ok=False` under the era's guard.
- `repo/README.md`'s "best public RMSE 0.104203" is stale; the repo ledger
  omits the 2026-10-29 afternoon submissions; no git history and no
  platform receipt exist locally (`00` §4).
- Official rules text (fetched 2026-10-29): provided-data-only for the
  leaderboard with a Bias-Discovery exception; ≈30/70 public/private
  split; 2-submission private selection with best-public fallback; top-10
  code review within 48 hours; open-source tools only; no AutoML;
  CC-BY-SA 4.0 data licence (`08`).

## Strongly supported

- **HeXaMraA ↔ the documented file ↔ official public score 0.081231862**
  (three independent internal records; no platform artifact — `02` §2).
- All 20 official public scores in `07` §1 (same record base).
- $P$'s identity and score (cjw1BmR3, 0.08483727); span5's identity and
  score (Pih3vnoM, 0.084844078).
- The probe construction "span5 + quarter-amplitude POI direction"
  (documented in two places; numeric consistency corr 0.940 — `06` T8).
- The leaderboard metric behaves as RMSE (`metric-audit/REPORT.txt`).
- Prize pool $10,000 with Best Documentation $500 (campaign record of the
  competition page; not in the fetched rules text).
- Working deadline 2026-10-31 23:29 UTC (campaign's conservative reading;
  the page shows "01 Nov" without an hour; the organiser-side programme
  page says the challenge closes 31 October 2026).

## Documented claims (single-source, unchecked)

- Runtime figures in `repo/WRITEUP.md` (~25 min feature extraction on
  2 CPU / 5 GB; <10 s pipeline) — the author's statement, not re-measured.
- The platform's effective submission cap (5/day, counter of 200) vs the
  rules page's stated 10/day and 300 overall — observed behaviour recorded
  in `TRACKING.md`, unexplained.

## Unverified / Unknown

- The exact five directions and coefficients of span5 (Stage C).
- The exact arithmetic of the probe's POI direction (Stage D; script lost).
- The Best Documentation **form URL**, its required fields and accepted
  file formats (`08` A2–A4). **No URL is asserted anywhere in this
  package.**
- Whether the organisers would treat `usfs_BuildingCount_sum` as a
  provided column (our reading) or as reference-layer-adjacent (`08` §1).
- The participant's final rank and all private-split scores (revealed at
  close).
- Whether the density calibration's public-split gain reflects the true
  target (`07` §5).
- Contents/history of the participant's remote GitHub repository
  (referenced in records as private during the challenge; not inspected).

## The three evidence gaps that matter most

1. **No platform-side proof** links the file to ID HeXaMraA / score
   0.081231862 (fixable by the participant in minutes on his submissions
   page — `08` §3.2).
2. **Stage D's generating script is lost**; the probe step is documented
   and numerically consistent but not re-executable.
3. **L1 is not re-runnable in this tree** (`repo/data/` absent), so the
   chain from raw extracts to `v2_tracts.parquet` is evidenced by the
   surviving artifact and code, not by re-execution.
