# 10 — Audit Summary

Documentation audit of the best official submission of participant
**koussayy** in the Zindi Bias Bounty Mapping Equity Challenge, performed
2026-10-29. (Per the task specification, no numeric quality score is
assigned.)

## Verdicts

**Provenance confidence — high for the code→file link, moderate for the
file→platform link.** The documented file
(`stage2/lowest3/2_v7_probe_s0.8_a-0.4_tau0.5.csv`, SHA-256 `e5430d51…`) is
reproduced *exactly* from its documented formula and retained inputs. Its
association with Zindi submission **HeXaMraA** and official public score
**0.081231862** is attested by three independent internal records but by
no platform-side artifact — **Strongly supported**, upgradeable by the
participant from his own submissions page.

**Reproducibility — exact at the final level, broken at two upstream
points.** L2 (submission file from its inputs) is verified bit-for-value
and deterministic — and, after the 2026-10-29 package repair,
**self-contained**: the packaged tests and rebuild were executed
successfully in an isolated copy of this package alone (`06` R1–R3), so a
reviewer holding only the package can re-run them. L1 (features from raw
extracts) cannot be re-run in this tree (data layout absent), and Stage
D's construction script was searched for across the full workspace and
archives and not found (`02` §3.1). L3 (the official score) is not
locally reproducible by construction.

**Technical documentation completeness — complete for the implemented
chain.** Every step from challenge files to the submitted CSV is described
from code, with formulas, constants, missing-value behaviour and
implementation locations (`03`, `04`). Three details are honestly marked
Unverified rather than reconstructed: span5's coefficients, the probe
direction's exact arithmetic, and the original run-time package versions.

**Validation coverage — all runnable checks executed and passing.**
10 packaged checks + the audit suite (`06`): file identity/schema/order,
numeric bounds, exact regeneration of two independently scored files,
determinism, screen recomputation, package hygiene scan, and — after the
repair — an isolated package-only execution of the packaged tests and
rebuild (`06` R3). No executed test failed. The untestable areas (raw-geometry handling in Stage A; platform
association) are named as gaps, not silently skipped.

**Compliance status — clean for the documented submission, one OPEN
question.** Only challenge-provided data enters the chain; removed
reference layers were never used for the leaderboard (a documented request
to do so was refused); open-source tools only; no AutoML; submission
counts within limits. The open question is the v2 building denominator
(`usfs_BuildingCount_sum`, a column of the provided strata table): its
full dependency chain into the documented file is mapped in `03` §7 — it
arrives only through the anchor span, and the final calibration's direct
inputs are free of it — but the official rules text does not address the
field, and a documented second-hand attribution derives the underlying
product from a removed layer. The item is recorded as **Unverified —
OPEN** (`08` R11/§1.1), resolved in neither direction. Award mechanics
(form URL, required fields/formats) remain **Unverified** from official
sources.

**Candour items a reviewer should know.** (i) The documented
configuration breached the campaign's own frozen stability gate
(maxcoef 6.10 > 2.5) and was submitted by explicit participant decision;
its local screen (0.0711) is not its official score (0.081231862), and the
gap is documented, not smoothed. (ii) The repository's own README/writeup
are stale relative to this submission (`00` §4). (iii) All results are
public-split; private-split behaviour — especially for a high-leverage
file — is unknown.

## Remaining blockers before award submission

1. Retrieve the official Best Documentation form (link, required fields,
   formats, exact deadline) from the competition page — `08` §3.1.
2. Confirm HeXaMraA ↔ 0.081231862 on the participant's Zindi submissions
   page; capture proof if possible — `08` §3.2.
3. Complete the private-leaderboard 2-submission selection before the
   close — `08` R7.
4. If a top-10 code review is later requested, be ready to explain the two
   upstream reproduction breaks (L1 data layout, Stage D script) — the
   retained inputs and this package are the mitigation.
