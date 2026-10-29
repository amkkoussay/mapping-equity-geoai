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
- **This package is self-contained at reproduction level L2**: the test
  suite (10/10) and the rebuild (max abs diff 0.0) were executed in an
  isolated copy of the package alone, with no reads from the project tree
  (`06` R3). The packaged `hu`/`area_km2` extract is verified against its
  source parquet (9,794 rows, per-column max abs diff 0.0; `06` R2), and
  the packaged probe and evaluator copies are byte-identical to their
  originals (`06` R1).
- `repo/README.md`'s "best public RMSE 0.104203" is stale; the repo ledger
  omits the 2026-10-29 afternoon submissions; no git history and no
  platform receipt exist locally (`00` §4).
- Official rules text (fetched 2026-10-29): provided-data-only for the
  leaderboard with a Bias-Discovery exception; ≈30/70 public/private
  split; 2-submission private selection with best-public fallback; top-10
  code review within 48 hours; open-source tools only; no AutoML;
  CC-BY-SA 4.0 data licence (`08`).
- **HeXaMraA ↔ the documented file ↔ official public score
  0.081231862** — a capture of the official Zindi submissions page is
  retained in this package (`evidence/zindi_submissions_proof.pdf`,
  SHA-256 `46c507f4…`): one row shows the ID, submitter koussayy, the
  score, and the comment "v7_probe_s0.8_a-0.4_tau0.5" (C028; `02` §2).
- Zindi staff post "Challenge Update" (meganomaly, 2026-10-08,
  discussion 35250): *"Features derived from the currently provided
  datasets are allowed, including Overture attributes and permitted
  columns in the strata tables"*; removed reference layers may not be
  used to reconstruct, derive or approximate the targets (C029).
- The Best Documentation requirements and form link as stated on the
  official Info page (prize $500; content, category-indication and
  identification requirements; form URL) (C018, C031; `08` §2).

## Strongly supported

- All 20 official public scores in `07` §1 (internal record base; the
  documented submission's own score is Verified separately — see above).
- $P$'s identity and score (cjw1BmR3, 0.08483727); span5's identity and
  score (Pih3vnoM, 0.084844078).
- The probe construction "span5 + quarter-amplitude POI direction"
  (documented in two places; numeric consistency corr 0.940 — `06` T8;
  construction script searched for across the full workspace and all zip
  archives on 2026-10-29 and **not found** — `02` §3.1, `06` R4).
- The leaderboard metric behaves as RMSE (`metric-audit/REPORT.txt`).
- Prize pool $10,000 total (campaign record of the competition page; not
  in the fetched rules text). The Best Documentation $500 prize itself is
  confirmed on the official Info page (see Verified).
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
- The exact arithmetic of the probe's POI direction (Stage D; construction
  script searched for and not found — `02` §3.1; four candidate direction
  forms fail to reproduce $P$, best max abs diff 5.0e-3 — `06` R4).
- The Best Documentation **form's own fields** and its accepted upload
  format: the form sits behind a Google sign-in wall and was not
  inspected; the format (PDF, max 10 MB) rests on a participant report
  (discussion 35334 — participant, not organizer; `08` A5). The form URL
  itself is retrieved and cited (`08` A2). No special-prize-specific
  deadline is stated (`08` A6).
- **OPEN:** whether the organisers would treat `usfs_BuildingCount_sum`
  as an ordinary provided column or as reference-layer-adjacent. The
  column indisputably ships inside the provided strata table and reaches
  the documented file only through the anchor-span path (full chain:
  `03` §7); the official rules text retrieved 2026-10-29 does not address
  this field at all; the strongest organizer text (staff post, discussion
  35250) allows "permitted columns in the strata tables" without naming
  this field; five participant threads asking about it by name had no
  organizer answer as of 2026-10-29 (C030); and a second-hand documented
  attribution says the underlying USFS product derives from the removed
  Microsoft footprints (not independently verified here). A clarification
  e-mail to the organisers has been drafted by the participant and, as of
  this update, **not sent**. Evidence on both sides: `08` §1.1.
  Status: **Unverified — OPEN**, by the participant's own framing.
- The participant's final rank and all private-split scores (revealed at
  close).
- Whether the density calibration's public-split gain reflects the true
  target (`07` §5).
- Contents/history of the participant's remote GitHub repository
  (referenced in records as private during the challenge; not inspected).

## The evidence gaps that matter most

0. **Closed (2026-10-29 evening): platform-side proof.** The gap that
   headed this list — no platform-side proof linking the file to ID
   HeXaMraA / score 0.081231862 — is closed by the retained capture of
   the official submissions page (`evidence/zindi_submissions_proof.pdf`;
   `02` §2, C028).
1. **Stage D's construction script was searched for and not found**
   (full workspace + all archives, 2026-10-29 — `02` §3.1); the probe step
   is documented and numerically consistent but not re-executable.
2. **L1 is not re-runnable in this tree** (`repo/data/` absent), so the
   chain from raw extracts to `v2_tracts.parquet` is evidenced by the
   surviving artifact and code, not by re-execution.
3. **The `usfs_BuildingCount_sum` interpretation (R11)** remains open:
   the general staff statement does not name the field and the five
   direct questions are unanswered; the drafted clarification e-mail has
   not been sent (see Unverified above).
