# talentflow-q3

Tests two claims from Acme Corp's VP People against Acme's production Airtable data, to inform
how TalentFlow allocates 6 engineer-weeks next quarter:

1. "Job boards are our biggest channel by a wide margin and bring in 26.9% of our hires."
2. "Our offer acceptance rate is around 72% and I need that number moving."

## Reproduce

The snapshot in `data/raw/` is committed, so no Airtable token is needed to reproduce the numbers.

```sh
make venv      # optional: .venv with pinned requirements (Python 3.8+)
make all       # verify cache -> audit -> metrics
```

| Target | Does | Network |
|---|---|---|
| `make pull` | Verifies `data/raw/` against `_manifest.json` (sha256, record counts) | No |
| `make refresh` | Re-pulls every table; needs `AIRTABLE_TOKEN` in `.env` (see `.env.example`) | Yes |
| `make audit` | Data-quality audit (stub) | No |
| `make metrics` | Claim metrics (stub) | No |
| `make all` | `pull`, `audit`, `metrics` | No |

A refresh overwrites the snapshot, so numbers can change. Snapshot time, row counts and
provenance are in [data/README.md](data/README.md).

## Layout

```
src/config.py     env loading, base id, table list, paths
src/pull.py       rate-limited paginated pull -> data/raw/, or cache verification
src/load.py       raw JSON -> typed DataFrames, link resolution
src/audit.py      data-quality audit
src/metrics.py    claim metrics
src/report.py     report rendering
data/raw/         <table>.json + _manifest.json
outputs/          tables/, logs/pull.log
deliverables/     SUBMISSION.md, findings.csv
notes/            decisions.md, open_questions.md
```

`data/raw/` holds candidate and employee personal data. Keep this repository private.
