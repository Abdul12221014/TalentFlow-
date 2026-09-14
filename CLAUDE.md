# CLAUDE.md: talentflow-q3

Standing rules for this repo. These are hard constraints, not preferences.

## Context

TalentFlow is a recruiting-operations product. Acme Corp (largest design partner) gave read access
to its production Airtable base. This repo tests two claims from Acme's VP People to inform how
6 engineer-weeks are allocated next quarter. The PM makes the calls; the agent produces and
verifies the numbers.

## Airtable access

- Base `appYePRAI75PMbQNQ`. Tables: Departments, People, Job Openings, Candidates, Applications,
  Interviews, Offers, Findings. URL-encode names with spaces.
- Token: `AIRTABLE_TOKEN` in `.env`, read from the environment only. Never print or echo it, never
  write it to any file other than `.env`, never put it in code, and never let it reach a log.
  `.env` is git-ignored; check `git status --porcelain` before every commit.
- The token is read-only. Never write to Airtable. A write returning 403 is expected; do not debug
  or retry it.
- Rate limit is 5 req/s per base; a 429 locks the base for 30s. Requests run sequentially with a
  250ms sleep. Never parallelise. On a 429: sleep 35s, retry once, then fail loudly.
- List endpoints return at most 100 records. Paginate on `offset` until it is absent.
- No `filterByFormula`. Pull whole tables.

## Cache-first

- `src/pull.py --refresh` (`make refresh`) is the only code path that calls the API.
- All analysis reads `data/raw/`. Never re-hit the API for analysis.
- `data/raw/` is committed so a re-run reproduces the same numbers. `_manifest.json` records the
  pull timestamps, per-table counts, total API requests and each file's sha256; `make pull`
  verifies the cache against it.

## API facts (known; don't rediscover)

- Empty fields are omitted from `fields`, not returned as null. Fill rate = non-empty / total
  records in the table, never / keys present.
- Linked-record fields are arrays of record IDs. Build id→record lookups before any join.
- Every record carries a top-level `createdTime`; keep it as the fallback if date fields are
  unreliable.
- Schema: `GET /v0/meta/bases/{base}/tables`. In the committed snapshot it returned 403 (no
  schema scope), so `SCHEMA` in `src/load.py` is inferred from records and enforced on load.

## Stack

Python 3 (3.8 locally), requests + pandas + python-dotenv. Nothing heavier.

## Layout

- `src/config.py` env, base id, table list, paths · `src/pull.py` pull / cache verify ·
  `src/load.py` typed frames + links · `src/audit.py`, `src/metrics.py`, `src/report.py`
- `outputs/tables/`, `outputs/logs/` generated artefacts
- `deliverables/` is the PM's writing. `notes/decisions.md` logs judgement calls and why;
  `notes/open_questions.md` holds questions for the hiring manager.

## Working agreement

- Do not flatter. Do not call an approach great. If the PM is wrong, say so and why.
- Every number comes with its denominator. No bare percentages.
- If a number rests on fewer than ~30 records, say so unprompted.
- When asked to check something, compute it and show the code path. Never report a result that
  was inferred rather than calculated.
- If two ways of counting the same thing disagree, give both and stop.
- Write to `deliverables/` only when explicitly asked.
