"""Environment loading, base id, table list and paths.

The Airtable token is read from the environment (populated from .env) and nowhere else.
Only `pull.py --refresh` asks for it; everything downstream works from data/raw/.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

BASE_ID = os.environ.get("AIRTABLE_BASE_ID") or "appYePRAI75PMbQNQ"
API_ROOT = "https://api.airtable.com/v0"

# Pull order. Names are the Airtable table names; spaces are URL-encoded at request time.
TABLES = [
    "Departments",
    "People",
    "Job Openings",
    "Candidates",
    "Applications",
    "Interviews",
    "Offers",
    "Findings",
]

# Rate limit is 5 req/s per base and a 429 locks the base for 30s.
REQUEST_SLEEP_S = 0.25
RATE_LIMIT_SLEEP_S = 35
PAGE_SIZE = 100
REQUEST_TIMEOUT_S = 30

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DATA_README = DATA_DIR / "README.md"
MANIFEST_PATH = RAW_DIR / "_manifest.json"
SCHEMA_FILE = "_schema.json"

OUTPUTS_DIR = ROOT / "outputs"
TABLES_OUT_DIR = OUTPUTS_DIR / "tables"          # citation tables only: one CSV per cited number
AUDIT_DIR = TABLES_OUT_DIR / "audit"              # audit per-check evidence and the ranked summary
EXPLORATION_DIR = TABLES_OUT_DIR / "exploration"  # definition grids and working tables, never cited directly
LOGS_DIR = OUTPUTS_DIR / "logs"
PULL_LOG = LOGS_DIR / "pull.log"


def raw_filename(table: str) -> str:
    """'Job Openings' -> 'job_openings.json' (no spaces in committed filenames)."""
    return table.lower().replace(" ", "_") + ".json"


def raw_path(table: str) -> Path:
    return RAW_DIR / raw_filename(table)


def get_token() -> str:
    token = os.environ.get("AIRTABLE_TOKEN", "").strip()
    if not token:
        raise SystemExit(
            "AIRTABLE_TOKEN is not set. Copy .env.example to .env and fill it in. "
            "Only `make refresh` needs it; every other target runs from data/raw/."
        )
    return token
