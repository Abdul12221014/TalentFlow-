# TalentFlow Q3: what Acme's data supports

A product exercise: test two claims from Acme Corp's VP People against a read-only snapshot of Acme's Airtable base, and decide how TalentFlow spends 6 engineer-weeks next quarter.
Every number in the submission is recomputed from the committed snapshot by the code in this repository.

## Deliverables

| The brief asks for | Where it is |
|---|---|
| 1. The memo, the roadmap and the metrics spec | [`deliverables/SUBMISSION.md`](deliverables/SUBMISSION.md): D1 verdicts, D2 roadmap, D3 metrics spec, D4 data trust, D5 memo |
| 2. A findings table: claim, metric, value, method, confidence | [`deliverables/findings.csv`](deliverables/findings.csv), 57 rows |
| 3. Code that re-runs and gives the numbers back | [`verify.py`](verify.py), [`src/`](src/), [`Makefile`](Makefile), with the snapshot in [`data/raw/`](data/raw/) |
| 4. The Claude Code session transcript | Supplied separately, not in this repository: it contains the Airtable access token, and this repository is public |

## Re-run

**Zero-dependency check.** Standard library only, nothing to install:

```sh
python3 verify.py
```

It recomputes 7/26, 26/36, 26/31 and 25/35 from `data/raw/`, prints each with its definition, and exits 0 when all four match. Tested on Python 3.8.10, 3.9.6, 3.10.13, 3.11.15, 3.12.10 and 3.13.1.

**Full pipeline.** Reads the committed snapshot; no network and no token needed:

```sh
make venv   # creates .venv from requirements.txt
make all    # verify the cache against its manifest, run the audit and metrics, write the figure and citation tables
```

| Target | Does |
|---|---|
| `make all` | Checks `data/raw/` against the manifest's sha256 values, then writes `outputs/tables/` (citation tables, `audit/`, `exploration/`) and `outputs/figures/` |
| `make findings` | Regenerates `deliverables/findings.csv` (overwrites it, so it is not part of `all`) |
| `make refresh` | Re-pulls from Airtable. Needs `AIRTABLE_TOKEN` in `.env` (see `.env.example`) and replaces the snapshot, so numbers can change |

Tested on Python 3.8.10 with requests 2.32.4, pandas 2.0.3, python-dotenv 1.0.1 and numpy 1.24.4. `requirements.txt` allows newer releases below the next major version; only these versions were tested. On the tested stack, `make all` reproduces all 54 output files byte for byte, and `make findings` reproduces `deliverables/findings.csv` byte for byte.

## Snapshot

| | |
|---|---|
| Base | `appYePRAI75PMbQNQ` |
| Pulled (UTC) | 2026-09-14T18:07:20Z to 2026-09-14T18:07:35Z |
| Records | 892 across 8 tables |
| API requests | 15, with 0 rate-limit responses |

Source: [`data/raw/_manifest.json`](data/raw/_manifest.json). The pull's log is frozen at [`outputs/logs/pull_snapshot.log`](outputs/logs/pull_snapshot.log); provenance is in [`data/README.md`](data/README.md). Every candidate and employee email in the snapshot is on the reserved example.com domain.

## Headline numbers

| Number | What it is | Confidence | Table |
|---|---|---|---|
| 195/298 = 65.44% (95% CI 59.87–70.61) | Job-board share of applications, Source as recorded | high | `outputs/tables/claim1_job_board_share_of_applications.csv` |
| 7/195 = 3.59% (95% CI 1.75–7.22) | Job-board conversion from application to hire; carries the claim 1 verdict | medium | `outputs/tables/claim1_conversion_by_channel.csv` |
| 25/35 = 71.43% (95% CI 54.95–83.67) | Offer acceptance, defended definition | low | `outputs/tables/claim2_offer_acceptance.csv` |
| 1,210 offers per period | Offers needed in each of two periods to detect 71.43% → 76.43% (two-sided alpha 0.05, 80% power); carries the claim 2 verdict | high | `outputs/tables/claim2_offers_needed_for_5pt_move.csv` |

Wilson bounds are computed at full precision (z = 1.959964) and rounded once, to two decimal places of a percentage, on the stored binary value (Python `round` and `format`, ties to even); CSV string columns drop trailing zeros, so 14.6 there is 14.60.

## Layout

```
verify.py         zero-dependency check of four headline fractions
src/              config, pull (cache verification or --refresh), load, audit, metrics, report
data/raw/         committed snapshot: one JSON file per table, plus _manifest.json
outputs/          tables/ (citation CSVs, audit/, exploration/), figures/, logs/pull_snapshot.log
deliverables/     SUBMISSION.md, findings.csv, D3_draft_metrics_spec.md
notes/            decisions.md, open_questions.md, evidence/ (the evidence pack behind SUBMISSION.md)
```
