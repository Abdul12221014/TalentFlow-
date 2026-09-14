"""Pull every Airtable table into data/raw/, or verify the cached snapshot.

    python src/pull.py            # default: verify data/raw/ against _manifest.json, no network
    python src/pull.py --refresh  # the only code path that calls the Airtable API

Requests are strictly sequential with a 250ms sleep before each one. A 429 sleeps 35s and
retries once, then aborts. The token lives in the session's Authorization header only; it is
never logged, and the log formatter scrubs it from every line as a second line of defence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from urllib.parse import quote

import requests

import config

log = logging.getLogger("pull")


class PullError(RuntimeError):
    pass


class RedactingFormatter(logging.Formatter):
    """Replaces the token in every formatted line, tracebacks included."""

    converter = time.gmtime

    def __init__(self, fmt: str, secret: str | None) -> None:
        super().__init__(fmt, datefmt="%Y-%m-%dT%H:%M:%SZ")
        self._secret = secret

    def format(self, record: logging.LogRecord) -> str:
        text = super().format(record)
        return text.replace(self._secret, "[REDACTED]") if self._secret else text


def setup_logging() -> None:
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    formatter = RedactingFormatter(
        "%(asctime)s %(levelname)-7s %(message)s",
        os.environ.get("AIRTABLE_TOKEN") or None,
    )
    log.setLevel(logging.INFO)
    log.propagate = False
    for handler in (
        logging.FileHandler(config.PULL_LOG, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ):
        handler.setFormatter(formatter)
        log.addHandler(handler)


class AirtableClient:
    """Sequential GETs only. Counts every request sent, retries included."""

    def __init__(self, token: str) -> None:
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {token}"})
        self.requests_made = 0
        self.rate_limit_hits = 0

    def get(self, url: str, params: dict | None = None) -> requests.Response:
        for attempt in (1, 2):
            time.sleep(config.REQUEST_SLEEP_S)
            self.requests_made += 1
            resp = self._session.get(url, params=params, timeout=config.REQUEST_TIMEOUT_S)
            log.info("GET %s params=%s -> %d", url, params or {}, resp.status_code)
            if resp.status_code != 429:
                return resp
            self.rate_limit_hits += 1
            if attempt == 1:
                log.warning("429 rate limited; sleeping %ds, then retrying once", config.RATE_LIMIT_SLEEP_S)
                time.sleep(config.RATE_LIMIT_SLEEP_S)
        raise PullError(f"429 again after retry on {url}; aborting")


def pull_schema(client: AirtableClient) -> tuple[int, dict | None]:
    url = f"{config.API_ROOT}/meta/bases/{config.BASE_ID}/tables"
    resp = client.get(url)
    if resp.status_code == 200:
        log.info("schema endpoint OK: %d tables", len(resp.json().get("tables", [])))
        return 200, resp.json()
    if resp.status_code == 403:
        log.warning("schema endpoint 403 (token lacks schema scope); fields must be inferred from records")
        return 403, None
    raise PullError(f"schema endpoint: unexpected HTTP {resp.status_code}: {resp.text[:300]}")


def pull_table(client: AirtableClient, table: str) -> tuple[list[dict], int]:
    url = f"{config.API_ROOT}/{config.BASE_ID}/{quote(table, safe='')}"
    records: list[dict] = []
    seen: set[str] = set()
    offset = None
    pages = 0
    while True:
        params = {"pageSize": config.PAGE_SIZE}
        if offset:
            params["offset"] = offset
        resp = client.get(url, params)
        if resp.status_code != 200:
            raise PullError(f"{table}: HTTP {resp.status_code} on page {pages + 1}: {resp.text[:300]}")
        body = resp.json()
        pages += 1
        for rec in body.get("records", []):
            if rec["id"] in seen:
                raise PullError(f"{table}: record {rec['id']} returned twice across pages")
            seen.add(rec["id"])
            records.append(rec)
        offset = body.get("offset")
        if not offset:
            break
    log.info("%s: %d records in %d page(s)", table, len(records), pages)
    return records, pages


def _dump(obj: object) -> bytes:
    return (json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_atomic(path, data: bytes) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def refresh() -> int:
    client = AirtableClient(config.get_token())
    started = _utc_now()
    log.info("refresh start: base=%s, %d tables", config.BASE_ID, len(config.TABLES))

    schema_status, schema = pull_schema(client)

    # Everything is held in memory until every table has pulled, so a failed refresh
    # leaves the previous snapshot intact.
    payloads: dict[str, bytes] = {}
    tables_meta: dict[str, dict] = {}
    for table in config.TABLES:
        records, pages = pull_table(client, table)
        name = config.raw_filename(table)
        payloads[name] = _dump(records)
        tables_meta[table] = {
            "file": name,
            "record_count": len(records),
            "pages": pages,
            "sha256": _sha256(payloads[name]),
        }

    schema_meta: dict = {"endpoint_status": schema_status, "file": None, "sha256": None}
    if schema is not None:
        payloads[config.SCHEMA_FILE] = _dump(schema)
        schema_meta.update(file=config.SCHEMA_FILE, sha256=_sha256(payloads[config.SCHEMA_FILE]))

    manifest = {
        "base_id": config.BASE_ID,
        "pull_started_utc": started,
        "pull_finished_utc": _utc_now(),
        "total_api_requests": client.requests_made,
        "rate_limit_429s": client.rate_limit_hits,
        "schema": schema_meta,
        "tables": tables_meta,
    }

    config.RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in payloads.items():
        _write_atomic(config.RAW_DIR / name, data)
    _write_atomic(config.MANIFEST_PATH, _dump(manifest))
    write_data_readme(manifest)

    log.info(
        "refresh done: %d records across %d tables, %d API requests, %d x 429",
        sum(m["record_count"] for m in tables_meta.values()),
        len(tables_meta),
        client.requests_made,
        client.rate_limit_hits,
    )
    return 0


def verify_cache() -> int:
    if not config.MANIFEST_PATH.exists():
        log.error("no cached snapshot at %s; run `make refresh` (needs AIRTABLE_TOKEN)", config.RAW_DIR)
        return 1
    manifest = json.loads(config.MANIFEST_PATH.read_text(encoding="utf-8"))
    problems: list[str] = []

    for table in config.TABLES:
        meta = manifest["tables"].get(table)
        if meta is None:
            problems.append(f"{table}: not in manifest")
            continue
        path = config.RAW_DIR / meta["file"]
        if not path.exists():
            problems.append(f"{table}: {path.name} missing")
            continue
        data = path.read_bytes()
        count = len(json.loads(data))
        if _sha256(data) != meta["sha256"]:
            problems.append(f"{table}: sha256 mismatch in {path.name}")
        if count != meta["record_count"]:
            problems.append(f"{table}: {count} records on disk, manifest says {meta['record_count']}")
        log.info("cache %-14s %5d records", table, count)

    schema_file = manifest["schema"]["file"]
    if schema_file:
        path = config.RAW_DIR / schema_file
        if not path.exists() or _sha256(path.read_bytes()) != manifest["schema"]["sha256"]:
            problems.append(f"schema: {schema_file} missing or sha256 mismatch")

    if problems:
        for problem in problems:
            log.error("cache check failed: %s", problem)
        return 1
    log.info(
        "cache OK: snapshot %s, all sha256 match, no network used",
        manifest["pull_finished_utc"],
    )
    return 0


def write_data_readme(manifest: dict) -> None:
    schema = manifest["schema"]
    schema_line = (
        f"HTTP {schema['endpoint_status']}, cached as `raw/{schema['file']}`"
        if schema["file"]
        else f"HTTP {schema['endpoint_status']}, not available; field types inferred from records"
    )
    lines = [
        "# data/",
        "",
        "Generated by `src/pull.py --refresh`. Do not hand-edit; `make refresh` regenerates it.",
        "",
        "## Snapshot",
        "",
        f"- Pull started (UTC): {manifest['pull_started_utc']}",
        f"- Pull finished (UTC): {manifest['pull_finished_utc']}",
        f"- Base: `{manifest['base_id']}`",
        f"- API requests: {manifest['total_api_requests']} (429 responses: {manifest['rate_limit_429s']})",
        f"- Schema endpoint: {schema_line}",
        "",
        "## Row counts",
        "",
        "| Table | File | Records | Pages | sha256 |",
        "|---|---|---:|---:|---|",
    ]
    for table, meta in manifest["tables"].items():
        lines.append(
            f"| {table} | `raw/{meta['file']}` | {meta['record_count']} | {meta['pages']} | `{meta['sha256'][:12]}…` |"
        )
    lines += [
        "",
        "## Provenance",
        "",
        "- Source: Acme Corp's production Airtable base, read with a read-only personal access token "
        "under design-partner access.",
        "- Method: `GET /v0/{base}/{table}?pageSize=100`, paginated on `offset` until absent. No view, "
        "no `filterByFormula`, default cell format. Sequential requests, 250ms apart.",
        "- `raw/<table>.json` is the full record list as returned (`id`, `createdTime`, `fields`), "
        "serialised with sorted keys. `raw/_schema.json` is the meta-endpoint response. "
        "`raw/_manifest.json` holds timestamps, counts, the request total and each file's sha256; "
        "`make pull` verifies the files against it.",
        "- Raw semantics: empty fields are absent from `fields` rather than null; linked-record fields "
        "are arrays of record IDs.",
        "- Contains candidate and employee personal data. Keep this repository private.",
        "",
    ]
    config.DATA_README.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true", help="re-pull every table from the Airtable API")
    args = parser.parse_args()
    setup_logging()
    try:
        return refresh() if args.refresh else verify_cache()
    except PullError as exc:
        log.error("PULL FAILED: %s", exc)
        return 1
    except requests.RequestException as exc:
        log.error("PULL FAILED (network): %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
