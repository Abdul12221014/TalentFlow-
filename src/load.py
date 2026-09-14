"""Raw JSON in data/raw/ -> typed pandas DataFrames, with linked-record resolution.

The schema endpoint returned 403 (token lacks schema scope), so SCHEMA below is inferred from
the cached records of the 2026-09-14 snapshot. It is enforced, not advisory:
  - a field in the raw data that SCHEMA does not declare raises SchemaDriftError;
  - a value of the wrong JSON type (e.g. a string in a number field) raises;
  - a single-link field holding more than one record ID raises.

Every declared field becomes a column even where records omit it, so fill rates are always
computed against the table's record count (len(df)), never against keys present.

Link fields keep Airtable record IDs (display fields such as Application ID and Full Name are
not unique). A single link becomes a scalar ID column; a multi link stays a list of IDs. Use
`index_by_id` / `resolve` to join. Reads the cache only; never touches the network.
"""
from __future__ import annotations

import json
from typing import NamedTuple

import pandas as pd

import config

DATE, INT, FLOAT, STR = "date", "int", "float", "str"


class Link(NamedTuple):
    target: str
    many: bool


ONE = lambda target: Link(target, many=False)  # noqa: E731
MANY = lambda target: Link(target, many=True)  # noqa: E731

SCHEMA: dict[str, dict[str, object]] = {
    "Departments": {
        "Name": STR,
        "Code": STR,
        "Location": STR,
        "Headcount Budget": INT,
        "People": MANY("People"),
        "Job Openings": MANY("Job Openings"),
    },
    "People": {
        "Full Name": STR,
        "Work Email": STR,
        "Role": STR,
        "Joined On": DATE,
        "Department": ONE("Departments"),
        "Reqs as Recruiter": MANY("Job Openings"),
        "Reqs as Hiring Manager": MANY("Job Openings"),
        "Applications as Recruiter": MANY("Applications"),
        "Referrals Made": MANY("Applications"),
        "Interviews": MANY("Interviews"),
    },
    "Job Openings": {
        "Req ID": STR,
        "Title": STR,
        "Level": STR,
        "Employment Type": STR,
        "Location": STR,
        "Status": STR,
        "Headcount": INT,
        "Salary Band Min": INT,
        "Salary Band Max": INT,
        "Opened On": DATE,
        "Target Close": DATE,
        "Department": ONE("Departments"),
        "Hiring Manager": ONE("People"),
        "Recruiter": ONE("People"),
        "Applications": MANY("Applications"),
    },
    "Candidates": {
        "Candidate ID": STR,
        "Full Name": STR,
        "Email": STR,
        "Phone": STR,
        "City": STR,
        "Current Company": STR,
        "Source": STR,
        "Notes": STR,
        "Created On": DATE,
        "Current CTC": INT,
        "Expected CTC": INT,
        "Notice Period Days": INT,
        "Years Experience": FLOAT,
        "Applications": MANY("Applications"),
    },
    "Applications": {
        "Application ID": STR,
        "Stage": STR,
        "Status": STR,
        "Rejection Reason": STR,
        "Applied On": DATE,
        "Screened On": DATE,
        "First Interview On": DATE,
        "Final Interview On": DATE,
        "Offered On": DATE,
        "Closed On": DATE,
        "Candidate": ONE("Candidates"),
        "Opening": ONE("Job Openings"),
        "Recruiter": ONE("People"),
        "Referred By": ONE("People"),
        "Interviews": MANY("Interviews"),
        "Offers": ONE("Offers"),
    },
    "Interviews": {
        "Interview ID": STR,
        "Round": STR,
        "Outcome": STR,
        "Recommendation": STR,
        "Feedback": STR,
        "Score": FLOAT,
        "Scheduled On": DATE,
        "Completed On": DATE,
        "Application": ONE("Applications"),
        "Interviewer": ONE("People"),
    },
    "Offers": {
        "Offer ID": STR,
        "Status": STR,
        "Decline Reason": STR,
        "Base CTC": INT,
        "Joining Bonus": INT,
        "Offered On": DATE,
        "Decision On": DATE,
        "Proposed Start Date": DATE,
        "Application": ONE("Applications"),
    },
    # 0 records in the snapshot and no schema scope: field names are unknown.
    "Findings": {},
}

# Human-readable field per table for `resolve`. Not unique in every table; join on IDs.
DISPLAY_FIELD = {
    "Departments": "Name",
    "People": "Full Name",
    "Job Openings": "Req ID",
    "Candidates": "Candidate ID",
    "Applications": "Application ID",
    "Interviews": "Interview ID",
    "Offers": "Offer ID",
    "Findings": "id",
}


class SchemaDriftError(ValueError):
    pass


def load_raw(table: str) -> list[dict]:
    return json.loads(config.raw_path(table).read_text(encoding="utf-8"))


def _require_types(table: str, field: str, col: pd.Series, types: tuple, label: str) -> None:
    present = col.dropna()
    bad = present[~present.map(lambda v: isinstance(v, types) and not isinstance(v, bool))]
    if len(bad):
        raise SchemaDriftError(
            f"{table}.{field}: {len(bad)} of {len(present)} non-empty values are not {label} "
            f"(first offending record index {bad.index[0]})"
        )


def _coerce(table: str, field: str, kind: object, col: pd.Series) -> pd.Series:
    if kind == STR:
        _require_types(table, field, col, (str,), "strings")
        return col.astype("string")
    if kind == DATE:
        _require_types(table, field, col, (str,), "date strings")
        return pd.to_datetime(col, format="%Y-%m-%d")
    if kind == INT:
        _require_types(table, field, col, (int, float), "numbers")
        return pd.to_numeric(col).astype("Int64")  # raises on non-integral values
    if kind == FLOAT:
        _require_types(table, field, col, (int, float), "numbers")
        return pd.to_numeric(col).astype("Float64")
    if isinstance(kind, Link):
        _require_types(table, field, col, (list,), "record-ID lists")
        if kind.many:
            return col
        too_many = col.dropna().map(len).gt(1)
        if too_many.any():
            raise SchemaDriftError(f"{table}.{field}: {int(too_many.sum())} records link more than one {kind.target}")
        return col.map(lambda v: v[0] if isinstance(v, list) else pd.NA).astype("string")
    raise ValueError(f"unknown kind {kind!r} for {table}.{field}")


def to_frame(table: str, records: list[dict]) -> pd.DataFrame:
    spec = SCHEMA[table]
    undeclared = sorted({k for r in records for k in r["fields"]} - set(spec))
    if undeclared:
        raise SchemaDriftError(f"{table}: fields in raw data but not in SCHEMA: {undeclared}")
    rows = [{"id": r["id"], "createdTime": r["createdTime"], **r["fields"]} for r in records]
    df = pd.DataFrame(rows, columns=["id", "createdTime", *spec])
    df["id"] = df["id"].astype("string")
    df["createdTime"] = pd.to_datetime(df["createdTime"], utc=True)
    for field, kind in spec.items():
        df[field] = _coerce(table, field, kind, df[field])
    return df


def load_all() -> dict[str, pd.DataFrame]:
    return {table: to_frame(table, load_raw(table)) for table in config.TABLES}


def index_by_id(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """table -> DataFrame indexed by record id. Build once, before any join."""
    return {table: df.set_index("id", drop=False) for table, df in frames.items()}


def resolve(
    frames: dict[str, pd.DataFrame],
    table: str,
    field: str,
    column: str | None = None,
) -> pd.Series:
    """Map a link field's IDs to `column` of the linked table (default: its display field).

    Single links return a scalar Series; multi links return a Series of lists. IDs that are
    not found in the target table resolve to NA (single) or are kept as None (multi).
    """
    kind = SCHEMA[table][field]
    if not isinstance(kind, Link):
        raise ValueError(f"{table}.{field} is not a link field")
    target = frames[kind.target].set_index("id")[column or DISPLAY_FIELD[kind.target]]
    lookup = target.to_dict()
    col = frames[table][field]
    if kind.many:
        return col.map(lambda ids: [lookup.get(i) for i in ids] if isinstance(ids, list) else pd.NA)
    return col.map(lambda i: lookup.get(i, pd.NA) if isinstance(i, str) else pd.NA)


def main() -> int:
    """Smoke test: load every table and confirm link IDs resolve. No analysis."""
    frames = load_all()
    known_ids = {table: set(df["id"]) for table, df in frames.items()}
    for table, df in frames.items():
        links = unresolved = 0
        for field, kind in SCHEMA[table].items():
            if not isinstance(kind, Link):
                continue
            ids = df[field].dropna()
            flat = [i for v in ids for i in (v if kind.many else [v])]
            links += len(flat)
            unresolved += sum(1 for i in flat if i not in known_ids[kind.target])
        print(f"{table:14} {len(df):4} rows x {df.shape[1]:2} cols   link ids {links:4}, unresolved {unresolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
