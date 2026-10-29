# 08 — Award Requirements & Compliance Checklist

Sources: official Zindi competition rules page for the *Bias Bounty
Mapping Equity Challenge*, fetched as page text on **2026-10-29** from
`https://zindi.world/competitions/bias-bounty-mapping-equity-challenge`
(the URL given in `repo/README.md`); Humane Intelligence's Bias Bounty
programme page (search result, 2026-10-29). Items that could not be
confirmed from an official source are marked **Unverified** — no form URL
or requirement has been invented.

## 1. Competition rules compliance (leaderboard solution)

| # | Requirement (official source) | Evidence in this package | Status |
|---|---|---|---|
| R1 | "You may use only the datasets provided for this challenge, however you may use additional public datasets for the Best Bias Discovery prize only (documented and reproducible)." (rules page) | `03`/`04`: every input of the documented chain is a challenge-package file; code read in full. The separate Bias Discovery track used external data under this explicit exception and does not feed the documented submission | **Satisfied** (for the documented submission) |
| R2 | Removed reference layers (TIGER / Microsoft footprints / USGS / CBP) must not be used for the leaderboard — implied by R1 and by the organisers' removal of the layers from the package | `repo/features.py` and `repo/pipeline_v2.py` headers + full code inspection: no such input is read. Internal records (`TRACKING.md`, 2026-10-28) document that a request to download the reference layers and reconstruct the target was **refused and not executed** | **Satisfied** |
| R3 | "The solution must use publicly-available, open-source packages only"; open-source languages/tools only | `requirements.txt`: Python, numpy, pandas, pyarrow, DuckDB — all open-source | **Satisfied** |
| R4 | "Automated machine learning tools such as automl are not permitted" | The method is a hand-built heuristic + algebra (`03` §0); no AutoML anywhere in the chain | **Satisfied** |
| R5 | Data licence: challenge data under CC-BY-SA 4.0; sharing conditions | Package contains no challenge datasets — only the participant's own submission CSV and derived documentation. `repo/` licence notes (MIT code; CC-BY-SA data derivatives) in `repo/WRITEUP.md` §2.1 | **Satisfied** |
| R6 | Submission limits: rules page states max 10/day and 300 overall | Campaign total: 20 scored submissions (+1 unscored error) over 2026-10-26…29 — within the stated limits. (The platform's *effective* cap was observed as 5/day with an account counter of 200 — a documented discrepancy, `01` C024; the campaign stayed within the stricter observed limits as well) | **Satisfied** |
| R7 | Pre-select 2 submissions for private judging before close; fallback = 2 best public submissions (rules page) | The participant's final-2 handling is his own platform action on 2026-10-31; campaign records note the anchor candidate is the documented submission (s0.8). Not an artifact this package can evidence | **Unverified** (platform action, outside package scope) |
| R8 | Top-10 code review: code requested by e-mail at close; 48 hours to submit; code must reproduce the score; non-running code is dropped from the top 10 (rules page) | This package + `05`/`06`: the final transformation reproduces the file exactly from retained inputs; **gap**: L1 (features from raw extracts) not re-executable in this tree (F1) and Stage D script missing (F2) — if a code review is requested, the reproducible chain has documented breaks upstream of $P$ | **Partially satisfied** — see blockers in `10` |
| R9 | "General-purpose development assistants … may be used for code drafting, debugging, testing or documentation, provided they are not required to execute or reproduce the submitted solution" (rules page) | This documentation package was prepared with an AI assistant (Muse) under the participant's direction; the solution pipeline itself is plain Python requiring no assistant to run | **Satisfied** (disclosed) |
| R10 | Single account / no code sharing outside a team | Solo participant, one account (koussayy) per all records | **Satisfied** (as recorded) |

**Open compliance question (flagged by the author himself):** the v2
building component uses the strata column `usfs_BuildingCount_sum` as its
reference denominator. It ships inside the provided challenge package, so
it falls under R1's "datasets provided"; `repo/WRITEUP.md` §2 nonetheless
flags the theoretical concern that organisers could view it as close to a
reference layer, and ships a fallback (`BUILDING_REF=none`). The documented
submission does not consume the building component directly (`04` §1), but
its probe ancestry includes v2-derived submissions. Status: **documented
risk, participant's call whether to raise it with the organisers**.

## 2. Best Documentation award mechanics

| # | Item | Finding | Status |
|---|---|---|---|
| A1 | Prize exists: **Best Documentation, $500**, within a $10,000 pool (1st $4,500 / 2nd $2,500 / 3rd $1,500 / Best Bias Discovery $1,000 / Best Documentation $500) | Campaign record of the competition page (`TRACKING.md` line 10, claim C017); the fetched rules-page text did not include the prize table | **Strongly supported** — re-confirm on the live page |
| A2 | A dedicated submission route exists, distinct from leaderboard submission | Campaign records state the entry is a **Google Form the participant submits himself on Oct 31** (C018) | **Unverified** — the form was **not** found on the fetched rules page; **no URL is cited anywhere in this package** |
| A3 | Required identifiers for the form (username / team name / submission IDs) | Zindi username **koussayy**; documented submission ID **HeXaMraA**; whether the form asks for these is unknown | **Unverified** — check the form itself |
| A4 | Required files / accepted formats for the documentation entry | Unknown from official sources retrieved. This package provides Markdown documents + CSV evidence + a zip archive; `repo/WRITEUP.pdf` exists as a pre-rendered PDF of the earlier writeup | **Unverified** |
| A5 | Deadline | Challenge closes **31 October 2026** (Humane Intelligence programme page). The campaign's working deadline is **2026-10-31 23:29 UTC**; the Zindi page displays the close as "01 Nov" without an hour (C023) | **Strongly supported** — confirm the exact instant on the live page; submit early |
| A6 | Restrictions on public code/data for award entries | Rules require any shared code to be available to all participants via the platform; the participant's repo is private during the challenge and, per campaign records, goes public only after the close, at his decision | **Unverified** — align the repo's visibility with the form's instructions when submitting |

## 3. Exact remaining actions before award submission

1. Open the official competition page, locate the Best Documentation form
   link (A2), and record the exact required fields/files (A3, A4) and the
   exact deadline with timezone (A5).
2. On the participant's Zindi submissions page, confirm HeXaMraA ↔
   0.081231862 and, if possible, capture a screenshot/receipt to upgrade
   the provenance in `02` from Strongly supported to Verified.
3. Complete the platform's private-leaderboard submission selection (R7)
   before the close.
4. Decide the `usfs_BuildingCount_sum` question (§1, open question):
   disclose as-is (this package already does) or ask the organisers.
5. Attach this package (zip) and/or `repo/WRITEUP.pdf` per the form's
   format requirements; if the form requires the methodology writeup
   specifically, note that `repo/WRITEUP.md` covers the v2 method only —
   this package is the document that covers the best submission's full
   chain.
