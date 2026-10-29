# Reviewer Quick Start

**What this package documents.** The best official submission of
participant **koussayy** (Koussay Mehdouani) in the Zindi *Bias Bounty
Mapping Equity Challenge*: submission **HeXaMraA**, official public score
**0.081231862** (public-split RMSE), submitted 2026-10-29. The
file → ID → score association is **Verified — platform record
captured** (`evidence/zindi_submissions_proof.pdf`).

**The method in one paragraph.** A deterministic heuristic pipeline (no
trained model). Per-tract Overture features feed a three-component
heuristic composite (building / transport / POI coverage-gap components,
`repo/pipeline_v2.py`). Fifteen scored submissions from that family serve
as anchors; exact quadratic span algebra over them yields a balanced
combination (span5), and a quarter-amplitude step along the POI-component
direction yields the probe vector $P$. The documented submission applies
a **density calibration** to $P$:
$\hat y = \mathrm{clip01}\bigl([s_0 + \alpha\tanh(z/\tau)]\cdot P +
\text{mean-preserving shift}\bigr)$ with $s_0 = 0.8$, $\alpha = -0.4$,
$\tau = 0.5$, where $z$ is standardised $\log(1 + \text{housing
units}/\text{area})$. Full detail: `03_methodology.md`.

## Key files

| File | Purpose |
|---|---|
| `README.md` | Package overview, navigation, executed checks |
| `02_submission_provenance.md` | Which submission this is, the evidence chain, candidate comparison |
| `03_methodology.md` | The implemented method in execution order, with formulas |
| `04_data_lineage_and_edge_cases.md` | Input→output lineage; edge cases as actually coded |
| `05_reproduction_guide.md` | Reproduction at three levels (features / file / official score) |
| `06_validation_report.md` | Every test actually run, with commands and observed results |
| `07_results_and_limitations.md` | Official results vs local diagnostics; negative results |
| `08_award_requirements_checklist.md` | Rules compliance + Best Documentation requirements (form link: row A2) |
| `09_claims_and_uncertainties.md` | All important claims grouped by confidence |
| `10_audit_summary.md` | Final verdicts and remaining blockers |
| `01_evidence_register.csv` | 33 claims with evidence pointers and statuses |
| `evidence/submission_s0.8_HeXaMraA.csv` | The documented submission file (SHA-256 `e5430d51…`) |
| `evidence/zindi_submissions_proof.pdf` | Capture of the official submissions page verifying HeXaMraA ↔ 0.081231862 (SHA-256 `46c507f4…`) |

## Run it (from this package alone)

All inputs resolve inside the package; no project files are read.

```bash
python documentation_package/tests/test_submission_file.py
# verified result: 10/10 PASS, exit 0

python documentation_package/scripts/rebuild_s08.py
# verified result: rows=9794 max_abs_diff=0.0 mean_abs_diff=0.0 exact_rows=9794, exit 0
```

Both were executed in an isolated copy of this package with no access to
the project tree (`06` R3) and re-run in place after the
official-evidence update (`06` R5).

## Open items (declared, not hidden)

- **Probe construction gap** — the script that built $P$ was searched
  for across the full workspace and all archives and **not found**; the
  step is documented and numerically consistent, not re-executable
  (`02` §3.1, `06` R4).
- **L1 raw-feature stage not re-executed** — the challenge-data layout
  (`repo/data/`) is absent from this tree, so `features.py` /
  `pipeline_v2.py` could not be re-run; the stage is evidenced by its
  surviving output artifact and code (`05` §2, `06` F1).
- **`usfs_BuildingCount_sum` — compliance item OPEN** (the v2 building
  denominator; reaches this file only through the anchor span). A Zindi
  staff post allows "permitted columns in the strata tables" without
  naming this field; five direct participant questions about it are
  unanswered; a clarification e-mail has been drafted, not sent
  (`08` R11 and §1.1).
- **Award form — submitted** — the Best Documentation entry was
  submitted by the participant on 2026-10-29 via the official form, category Best Documentation, uploading the consolidated PDF `Koussay-Mehdouani_Best-Documentation_HeXaMraA.pdf` (57 pages, 502,105 bytes, SHA-256 `17d7527ef9cf148fdb607c98c34024dd424af301572dac9aca83fb9d22260aee`) and entering Submission ID **HeXaMraA**
  (register C033; `08` A5, §3). The form's sections beyond the Best
  Documentation section remain unexamined.

## Distribution caveat

The GitHub copy of this package contains the **text files only**; the
complete package — including the binary proof PDF
(`evidence/zindi_submissions_proof.pdf`) — is the zip archive
(`zindi_best_documentation_package.zip`). The repository itself is
publicly readable (observed 2026-10-29 evening — `08` A7, register
C032). Every packaged file, the PDF
included, is hash-listed in `MANIFEST.sha256`.
