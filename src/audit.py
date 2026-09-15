"""Data-quality audit of the cached snapshot, run as a numbered checklist.

    python src/audit.py        # or: make audit

Reads data/raw/ through load.py (raw JSON directly where a check needs values before any
typing). Writes one CSV per check to outputs/tables/audit/audit_<n>_<name>.csv and a ranked
outputs/tables/audit/audit_summary.csv. Never touches the network. Rule ids are written with an "R" prefix
(R6.20) so no CSV reader can parse them as numbers: unprefixed, "6.20" and "6.2" both parse to 6.2.

Structure
---------
A check is a function registered with @check(number, name). It returns a CheckResult holding
Rules. A Rule is one defect: an id, a title, the table its percentage is taken against,
evidence rows (one per affected record) and a statement of how the defect could reach the
yardsticks. To add a rule, append a Rule inside the relevant check. To add a check, write another
@check function. Thresholds and declared vocabularies are constants below, so a reviewer can
disagree with a number without reading the logic.

Materiality
-----------
"Could this change a decision about channel mix or offer acceptance?" is computed, not asserted,
against three yardsticks taken from metrics.py:
    channel         Candidates.Source = Job Board / Applications at Stage = Hired     7/26
    accept_all      Offers.Status = Accepted / all Offers                             26/36
    accept_decided  Offers.Status = Accepted / (Accepted + Declined)                  26/31
The first two reproduce the VP's figures. The third is included because Pending treatment was
the largest definitional lever. They are measuring sticks, not endorsed definitions.

Each Rule either declares Scenarios (a corrected view of yardstick inputs: exclude records,
dedupe, reassign channel, change offer status) or states why no yardstick input can change.
Its materiality is the largest movement across its scenarios:
    SYSTEMIC  undermines every figure and cannot be scenario-tested (stated, not computed)
    HIGH      the top channel changes, or any yardstick moves >= TIER_HIGH_PP
    MEDIUM    any yardstick moves >= TIER_MEDIUM_PP
    SCOPE     PM decision: real, but outside the evidence the claim decisions rest on. The reason is
              recorded on the rule and no scenario is scored, so it never enters tie-breaking material
    LOW       a yardstick moves, by less than TIER_MEDIUM_PP
    NONE      no yardstick input changes
    PASS      the rule found nothing, on fields that could have carried the defect
    NOT TESTABLE  the rule found nothing, but it inspects placeholder identifiers, so it could not have
              fired; run() verifies this by injecting defects into those fields only (identifier_sensitive_rules)
The summary is ranked by tier, then movement, then top-channel change, then count. Never by count.
Its `mechanism` column is one computed sentence for the scenario that set the tier: which hires and
offers change, and what each change does to numerator and denominator.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable

import pandas as pd

import config
import load

# ============================================================== thresholds and vocabularies

SNAPSHOT_DAY = pd.Timestamp(json.loads(config.MANIFEST_PATH.read_text(encoding="utf-8"))["pull_finished_utc"][:10])
EPOCH_CUTOFF = pd.Timestamp("2000-01-01")
# Date fields that legitimately hold future values.
FORWARD_LOOKING_DATES = {("Job Openings", "Target Close"), ("Offers", "Proposed Start Date")}

TIER_HIGH_PP = 5.0
TIER_MEDIUM_PP = 1.0
TIER_ORDER = ["SYSTEMIC", "HIGH", "MEDIUM", "SCOPE", "LOW", "NONE", "PASS", "NOT TESTABLE"]
# Identifier fields that hold placeholders in this base (all 314 emails are on example.com; names and phones share the pattern).
PLACEHOLDER_IDENTIFIER_FIELDS = {
    ("Candidates", "Email"), ("Candidates", "Full Name"), ("Candidates", "Phone"),
    ("People", "Work Email"), ("People", "Full Name"),
}
# Keys the duplicate rules group on, and the fields each key is built from.
KEY_INSPECTS = {"email_norm": {("Candidates", "Email")}, "name_phone": {("Candidates", "Full Name"), ("Candidates", "Phone")}}
# PM decision, 2026-09-15 (Stage 1B item 2). Other tie-breaks are deliberately not implemented; the figures were computed once
# on snapshot 2026-09-14T18:07:35Z during the Stage 1 check (session transcript) and are recorded here, not recomputed.
RULE_NOTES = {
    "3.2": ("Tie-break sensitivity, computed once on snapshot 2026-09-14T18:07:35Z and not re-run: earliest Created On "
            "(implemented), latest Created On and earliest application each give Job Board 8/26; the hired record keeping "
            "its own Source gives 7/26; the range 7/26-8/26 changes no verdict (channel conversion order unchanged, first vs "
            "second not separable). The grouping key (name + phone) is identifier-dependent and the tie-break key "
            "Candidates.Created On contradicts the application dates of CAND-00002, CAND-00003 and CAND-00004, so no "
            "precision beyond the range is available."),
}
DECIDED_STATUSES = {"Accepted", "Declined"}
# Prefix for rule ids in every CSV this module writes. Without it, a file whose ids all look numeric
# (audit_6) is read as float64 by default parsers and "6.20" collapses into "6.2".
RULE_ID_PREFIX = "R"
MECHANISM_MAX_LABELS = 4

# Fields the yardsticks read. Missing values here can change a yardstick; elsewhere they cannot.
YARDSTICK_FIELDS = {
    ("Applications", "Stage"), ("Applications", "Candidate"), ("Candidates", "Source"),
    ("Offers", "Status"), ("Offers", "Application"),
}

# Enum-like = short strings with few distinct values relative to fill.
CATEGORICAL_MAX_DISTINCT = 25
CATEGORICAL_MAX_DISTINCT_RATIO = 0.5
CATEGORICAL_MAX_MEDIAN_LENGTH = 30
NEAR_DUPLICATE_MIN_RATIO = 0.85

# Lower-cased spelling -> canonical lower-cased spelling. Applied within one field only.
SYNONYMS = {
    "bangalore": "bengaluru", "bombay": "mumbai", "gurgaon": "gurugram", "new delhi": "delhi",
    "full time": "full-time", "fulltime": "full-time", "part time": "part-time", "contractor": "contract",
    "jobboard": "job board", "job boards": "job board", "job portal": "job board",
    "careers page": "career site", "career page": "career site", "company website": "career site",
    "linked in": "linkedin", "employee referral": "referral", "recruitment agency": "agency",
    "offer accepted": "accepted", "offer declined": "declined", "no-show": "no show", "noshow": "no show",
    "on-hold": "on hold", "canceled": "cancelled",
}
# Distinct labels whose meanings overlap for the channel question: (table, field, value, overlaps with).
TAXONOMY_OVERLAPS = [("Candidates", "Source", "LinkedIn", "Job Board")]

BUSINESS_KEY = {
    "Departments": "Code", "People": "id", "Job Openings": "Req ID", "Candidates": "Candidate ID",
    "Applications": "Application ID", "Interviews": "Interview ID", "Offers": "Offer ID", "Findings": "id",
}
# (child table, child link field, parent table, parent link field) that should mirror each other.
INVERSE_LINKS = [
    ("Applications", "Candidate", "Candidates", "Applications"),
    ("Applications", "Opening", "Job Openings", "Applications"),
    ("Applications", "Recruiter", "People", "Applications as Recruiter"),
    ("Applications", "Referred By", "People", "Referrals Made"),
    ("Offers", "Application", "Applications", "Offers"),
    ("Interviews", "Application", "Applications", "Interviews"),
    ("Interviews", "Interviewer", "People", "Interviews"),
    ("Job Openings", "Department", "Departments", "Job Openings"),
    ("Job Openings", "Recruiter", "People", "Reqs as Recruiter"),
    ("Job Openings", "Hiring Manager", "People", "Reqs as Hiring Manager"),
    ("People", "Department", "Departments", "People"),
]
EXPECTED_ROLES = {
    ("Applications", "Recruiter"): {"Recruiter"},
    ("Job Openings", "Recruiter"): {"Recruiter"},
    ("Job Openings", "Hiring Manager"): {"Hiring Manager"},
    ("Interviews", "Interviewer"): {"Interviewer", "Hiring Manager"},
}

TERMINAL_STAGES = {"Hired", "Rejected", "Withdrawn"}
OPEN_STAGES = {"Applied", "Screening", "Interview", "Offer"}
REJECTED_STAGES = {"Rejected", "Withdrawn"}
CLOSED_REQUISITION_STATUSES = {"Filled", "Cancelled"}
NOT_HIRING_REQUISITION_STATUSES = {"Cancelled", "On Hold"}
PIPELINE_ORDER = ["Applied On", "Screened On", "First Interview On", "Final Interview On", "Offered On", "Closed On"]

MONEY_FIELDS = [
    ("Offers", "Base CTC"), ("Candidates", "Current CTC"), ("Candidates", "Expected CTC"),
    ("Job Openings", "Salary Band Min"), ("Job Openings", "Salary Band Max"),
]
MAGNITUDE_FACTOR = 10
MAX_INTERVIEWS_PER_APPLICATION = 8
MAX_INTERVIEWS_PER_INTERVIEWER_DAY = 6
MAX_DURATION_DAYS = {"time to hire (Applied On -> Closed On)": 365, "offer decision (Offered On -> Decision On)": 45}
MAX_YEARS_EXPERIENCE = 50
MAX_NOTICE_PERIOD_DAYS = 180

TEST_TOKENS = re.compile(r"\b(test|dummy|sample|fake|asdf|qwerty|lorem|ipsum|placeholder|do not use|delete me|xxx+)\b", re.I)
PLACEHOLDER_EMAIL_DOMAINS = {"example.com", "example.org", "example.net", "test.com", "mailinator.com"}
BULK_CREATION_MAX_SECONDS = 300
TEMPLATED_TEXT_MIN_VALUES = 50
TEMPLATED_TEXT_MAX_DISTINCT = 20

RECOMMENDATION_POLARITY = {"Strong Hire": 1, "Hire": 1, "No Hire": -1, "Strong No Hire": -1}
# Declared reading of each Feedback template. Unlisted strings are reported, never guessed.
FEEDBACK_POLARITY = {
    "Clear communicator, solved the problem two ways and compared them.": 1,
    "Excellent depth on system design. Explained trade-offs without prompting.": 1,
    "Good practical experience. Some gaps in scale but coachable.": 1,
    "Reasonable answers throughout. No red flags.": 1,
    "Solid fundamentals. Needed a hint on the follow-up but recovered well.": 1,
    "Strongest candidate in this loop. Would hire on the spot.": 1,
    "Answers stayed surface level even after probing.": -1,
    "Could not complete the exercise. Defensive when given a hint.": -1,
    "Missed the main edge case and did not test the solution.": -1,
    "Not convinced. Did not meet the bar for this level.": -1,
    "Significant gaps against the level. Not close on the fundamentals.": -1,
    "Struggled with the core problem. Could not explain their own prior work.": -1,
}
POSITIVE_RECOMMENDATION_MIN_SCORE = 2   # a Hire/Strong Hire at or below this score contradicts
NEGATIVE_RECOMMENDATION_MAX_SCORE = 4   # a No Hire/Strong No Hire at or above this score contradicts

# ============================================================== rule model and registry


@dataclass
class Scenario:
    """A corrected view of the yardstick inputs. Every adjustment is optional."""

    label: str
    drop_apps: set = field(default_factory=set)       # application record ids removed
    drop_offers: set = field(default_factory=set)     # offer record ids removed
    app_source: dict = field(default_factory=dict)    # application record id -> channel
    source_remap: dict = field(default_factory=dict)  # Candidates.Source value -> replacement value
    stage_remap: dict = field(default_factory=dict)   # Applications.Stage value -> replacement value
    offer_status: dict = field(default_factory=dict)  # offer record id -> status
    status_remap: dict = field(default_factory=dict)  # Offers.Status value -> replacement value


@dataclass
class Rule:
    rule_id: str
    title: str
    table: str
    evidence: pd.DataFrame
    scenarios: list = field(default_factory=list)
    no_effect: str = ""        # why no yardstick input can change; used when scenarios is empty
    systemic: str = ""         # set when the defect undermines every figure and cannot be scenario-tested
    scope: str = ""            # PM decision to keep on record but out of scoring; holds the recorded reason
    inspects: set = field(default_factory=set)  # (table, field) text fields the rule reads; drives NOT TESTABLE
    note: str = ""             # one recorded line written to the summary and the check CSV
    table_level: bool = False  # the finding is about the table itself (e.g. it is empty)

    @property
    def count(self) -> int:
        return int(self.evidence["record_id"].nunique()) if len(self.evidence) else 0


@dataclass
class CheckResult:
    rules: list
    table: pd.DataFrame | None = None  # the check's CSV; defaults to the rules' evidence


CHECKS: list = []


def check(number: int, name: str) -> Callable:
    def register(fn: Callable) -> Callable:
        CHECKS.append((number, name, fn))
        return fn
    return register


EVIDENCE_COLUMNS = ["record_id", "key", "detail"]


def _fmt(value: object) -> str:
    if isinstance(value, list):
        return ",".join(map(str, value))
    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()
    if value is None or pd.isna(value):
        return ""
    return str(value)


def evidence(df: pd.DataFrame, table: str, *fields: str, id_col: str = "id", key_col: str | None = None) -> pd.DataFrame:
    """One row per affected record: its record id, business key and the fields that show the defect."""
    if df.empty:
        return pd.DataFrame(columns=EVIDENCE_COLUMNS)
    key = key_col or BUSINESS_KEY[table]
    details = ["; ".join(f"{f}={_fmt(row[f])}" for f in fields) for _, row in df.iterrows()]
    return pd.DataFrame({
        "record_id": df[id_col].astype(str).to_numpy(),
        "key": df[key].astype(str).to_numpy(),
        "detail": details,
    })


def group_id(key: str) -> str:
    """Stable, non-reversible label for a duplicate group, so keys like emails stay out of outputs."""
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]


def normalise_email(value: str) -> str:
    local, _, domain = str(value).strip().lower().partition("@")
    local = local.split("+", 1)[0]
    if domain in {"gmail.com", "googlemail.com"}:
        local, domain = local.replace(".", ""), "gmail.com"
    return f"{local}@{domain}"


def normalise_name(value: str) -> str:
    return re.sub(r"[^a-z]+", " ", str(value).lower()).strip()


def normalise_phone(value: str) -> str:
    return re.sub(r"\D", "", str(value))[-10:]


def filled(series: pd.Series) -> pd.Series:
    """Non-empty per Airtable semantics: absent keys load as NA; link lists are never empty lists."""
    return series.map(lambda v: len(v) > 0 if isinstance(v, list) else not pd.isna(v)).astype(bool)


def is_categorical(series: pd.Series) -> bool:
    values = series.dropna()
    if values.empty or not all(isinstance(v, str) for v in values):
        return False
    distinct = values.nunique()
    return (
        distinct <= CATEGORICAL_MAX_DISTINCT
        and distinct / len(values) <= CATEGORICAL_MAX_DISTINCT_RATIO
        and values.str.len().median() <= CATEGORICAL_MAX_MEDIAN_LENGTH
    )


# ============================================================== shared context


class Context:
    """Frames, normalised keys and joined views shared by every check."""

    def __init__(self, frames: dict[str, pd.DataFrame]) -> None:
        self.frames = frames
        self.rows = {table: len(df) for table, df in frames.items()}
        self.departments = frames["Departments"]
        self.people = frames["People"]
        self.openings = frames["Job Openings"]
        self.apps = frames["Applications"]
        self.offers = frames["Offers"]
        self.interviews = frames["Interviews"]

        cands = frames["Candidates"].copy()
        cands["email_norm"] = cands["Email"].map(normalise_email)
        cands["name_phone"] = cands["Full Name"].map(normalise_name) + "|" + cands["Phone"].map(normalise_phone)
        self.candidates = cands

        cand_cols = cands[["id", "Candidate ID", "Source", "name_phone", "Created On", "Notes"]].rename(
            columns={"id": "cand_id", "Created On": "cand_created_on"})
        open_cols = self.openings[["id", "Req ID", "Status", "Opened On", "Headcount", "Salary Band Min", "Salary Band Max"]].rename(
            columns={"id": "open_id", "Status": "opening_status", "Opened On": "opening_opened_on"})
        # If an application ever has two offers, joins use the latest; check 3 reports the duplication.
        latest_offer = self.offers.sort_values(["Offered On", "Offer ID"]).drop_duplicates("Application", keep="last")
        offer_cols = latest_offer[["id", "Offer ID", "Application", "Status", "Offered On", "Decision On", "Proposed Start Date"]].rename(
            columns={"id": "offer_id", "Application": "offer_app", "Status": "offer_status", "Offered On": "offer_offered_on",
                     "Decision On": "offer_decision_on", "Proposed Start Date": "offer_start"})
        app_cols = self.apps[["id", "Application ID", "Candidate", "Opening", "Stage", "Status", "Applied On", "Offered On",
                              "Closed On", "Rejection Reason"]].rename(
            columns={"id": "app_id", "Status": "app_status", "Offered On": "app_offered_on", "Closed On": "app_closed_on"})

        a = self.apps.merge(cand_cols, left_on="Candidate", right_on="cand_id", how="left")
        a = a.merge(open_cols, left_on="Opening", right_on="open_id", how="left")
        a = a.merge(offer_cols, left_on="id", right_on="offer_app", how="left")
        a["n_interviews"] = a["Interviews"].map(lambda v: len(v) if isinstance(v, list) else 0)
        self.app_x = a  # one row per application

        o = self.offers.merge(app_cols, left_on="Application", right_on="app_id", how="left")
        o = o.merge(open_cols, left_on="Opening", right_on="open_id", how="left")
        self.offer_x = o.merge(cand_cols[["cand_id", "Candidate ID", "name_phone"]], left_on="Candidate", right_on="cand_id", how="left")

        iv = self.interviews.merge(app_cols[["app_id", "Application ID", "Stage", "Applied On"]], left_on="Application", right_on="app_id", how="left")
        iv = iv.merge(offer_cols, left_on="Application", right_on="offer_app", how="left")
        iv["event_on"] = iv["Completed On"].fillna(iv["Scheduled On"])
        self.iv_x = iv  # one row per interview

    # ---- mapping any table's records onto yardstick inputs

    def apps_for(self, table: str, ids) -> set:
        ids = set(ids)
        if table == "Applications":
            return ids
        if table == "Candidates":
            return set(self.apps.loc[self.apps["Candidate"].isin(ids), "id"])
        if table == "Offers":
            return set(self.offers.loc[self.offers["id"].isin(ids), "Application"].dropna())
        if table == "Interviews":
            return set(self.interviews.loc[self.interviews["id"].isin(ids), "Application"].dropna())
        if table == "Job Openings":
            return set(self.apps.loc[self.apps["Opening"].isin(ids), "id"])
        return set()

    def offers_for(self, table: str, ids) -> set:
        if table == "Offers":
            return set(ids)
        return set(self.offers.loc[self.offers["Application"].isin(self.apps_for(table, ids)), "id"])

    # ---- scenario builders

    def exclude(self, table: str, ids, label: str) -> Scenario:
        return Scenario(label, drop_apps=self.apps_for(table, ids), drop_offers=self.offers_for(table, ids))

    def dedupe_applications(self, groups: list, label: str) -> Scenario:
        """Keep the earliest application in each group; drop the rest and their offers."""
        scenario = Scenario(label)
        for group in groups:
            members = self.app_x[self.app_x["id"].isin(group)].sort_values(["Applied On", "Application ID"])
            extra = members.iloc[1:]
            scenario.drop_apps |= set(extra["id"])
            scenario.drop_offers |= set(extra["offer_id"].dropna())
        return scenario

    def merge_candidates(self, groups: list, label: str) -> Scenario:
        """Merge each group into its earliest-created record: its Source wins, repeat openings collapse."""
        cands = self.candidates.set_index("id")
        scenario = Scenario(label)
        for group in groups:
            ordered = cands.loc[list(group)].sort_values(["Created On", "Candidate ID"])
            keep_source = ordered["Source"].iloc[0]
            members = self.app_x[self.app_x["Candidate"].isin(ordered.index)].sort_values(["Applied On", "Application ID"])
            for app_id in members.loc[members["Candidate"] != ordered.index[0], "id"]:
                scenario.app_source[app_id] = keep_source
            repeat = members[members.duplicated("Opening")]
            scenario.drop_apps |= set(repeat["id"])
            scenario.drop_offers |= set(repeat["offer_id"].dropna())
        return scenario


# ============================================================== yardsticks and materiality

YARDSTICK_LABEL = {
    "channel": "Job Board share of hires",
    "accept_all": "accepted/all offers",
    "accept_decided": "accepted/decided offers",
}


def _pct(fraction: tuple) -> float:
    num, den = fraction
    return 100.0 * num / den if den else float("nan")


class Yardsticks:
    def __init__(self, ctx: Context) -> None:
        index = ctx.app_x["id"].astype(object).to_numpy()
        self.app_stage = pd.Series(ctx.app_x["Stage"].astype(object).to_numpy(), index=index)
        self.app_source = pd.Series(ctx.app_x["Source"].astype(object).to_numpy(), index=index)
        self.app_label = pd.Series((ctx.app_x["Application ID"].astype(str) + "/" + ctx.app_x["Candidate ID"].astype(str)).to_numpy(), index=index)
        self.offer_status = pd.Series(ctx.offers["Status"].astype(object).to_numpy(), index=ctx.offers["id"].astype(object).to_numpy())
        self.baseline = self.evaluate(Scenario("baseline"))

    def apply(self, s: Scenario) -> tuple:
        """Stage and channel of every surviving application, and status of every surviving offer."""
        stage = self.app_stage.drop(labels=[i for i in s.drop_apps if i in self.app_stage.index]).replace(s.stage_remap)
        source = self.app_source.loc[stage.index].copy()
        for app_id, value in s.app_source.items():
            if app_id in source.index:
                source[app_id] = value
        status = self.offer_status.drop(labels=[i for i in s.drop_offers if i in self.offer_status.index]).copy()
        for offer_id, value in s.offer_status.items():
            if offer_id in status.index:
                status[offer_id] = value
        return stage, source.replace(s.source_remap), status.replace(s.status_remap)

    def evaluate(self, s: Scenario) -> dict:
        stage, source, status = self.apply(s)
        counts = source[stage == "Hired"].value_counts()
        leaders = sorted(counts[counts == counts.max()].index) if len(counts) else []
        accepted, declined = int((status == "Accepted").sum()), int((status == "Declined").sum())
        return {
            "channel": (int(counts.get("Job Board", 0)), int(counts.sum())),
            "top_channel": " = ".join(leaders),
            "accept_all": (accepted, int(len(status))),
            "accept_decided": (accepted, accepted + declined),
        }

    def _labels(self, ids: list, describe: Callable) -> str:
        shown = [f"{self.app_label[i]} {describe(i)}" for i in ids[:MECHANISM_MAX_LABELS]]
        more = len(ids) - MECHANISM_MAX_LABELS
        return ", ".join(shown) + (f", +{more} more" if more > 0 else "")

    def mechanism(self, s: Scenario) -> str:
        """One computed sentence: which hires and offers the scenario changes, and how each yardstick moves."""
        stage, source, status = self.apply(s)
        after = self.evaluate(s)
        hired_before = set(self.app_stage.index[self.app_stage == "Hired"])
        hired_after = set(stage.index[stage == "Hired"])
        removed, added = sorted(hired_before - hired_after), sorted(hired_after - hired_before)
        resourced = sorted(i for i in hired_before & hired_after if source[i] != self.app_source[i])
        parts = []
        if removed:
            parts.append(f"{len(removed)} hire(s) removed ({self._labels(removed, lambda i: self.app_source[i])})")
        if added:
            parts.append(f"{len(added)} hire(s) added ({self._labels(added, lambda i: source[i])})")
        if resourced:
            parts.append(f"{len(resourced)} hire(s) re-sourced ({self._labels(resourced, lambda i: f'{self.app_source[i]}->{source[i]}')})")
            if not removed and not added:
                parts.append(f"no hire is removed or added, so the hire denominator stays {after['channel'][1]}")
        moves = Counter()
        for offer_id, old in self.offer_status.items():
            new = status[offer_id] if offer_id in status.index else None
            if new != old:
                moves[(old, new)] += 1
        for (old, new), n in sorted(moves.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
            d_num = n * (int(new == "Accepted") - int(old == "Accepted"))
            d_den = n * (int(new in DECIDED_STATUSES) - int(old in DECIDED_STATUSES))
            parts.append(f"{n} offer(s) {old}->{new or 'dropped'} (accepted/decided numerator {d_num:+d}, denominator {d_den:+d})")
        if not parts:
            return "No hire or offer changes."
        changed = [f"{YARDSTICK_LABEL[k]} {self.baseline[k][0]}/{self.baseline[k][1]} -> {after[k][0]}/{after[k][1]}"
                   for k in YARDSTICK_LABEL if after[k] != self.baseline[k]]
        return "; ".join(parts) + (", giving " + ", ".join(changed) if changed else ", leaving every yardstick unchanged") + "."


def assess(rule: Rule, ys: Yardsticks) -> dict:
    result = {"tier": "NONE", "top_channel_changed": False, "max_abs_delta_pp": 0.0, "scenario": "", "mechanism": ""}
    if rule.scope:
        # Recorded, never scored: no scenario runs, so the rule cannot enter tie-breaking material.
        return {**result, "tier": "SCOPE", "max_abs_delta_pp": None, "materiality": f"Out of scope by PM decision: {rule.scope}"}
    if rule.count == 0 and not rule.table_level:
        placeholders = sorted(f"{t}.{f}" for t, f in rule.inspects & PLACEHOLDER_IDENTIFIER_FIELDS)
        if placeholders:
            others = sorted(f"{t}.{f}" for t, f in rule.inspects - PLACEHOLDER_IDENTIFIER_FIELDS)
            extra = f"; it also inspects {', '.join(others)}, which could have fired and did not" if others else ""
            return {**result, "tier": "NOT TESTABLE",
                    "materiality": f"Could not have fired: it inspects placeholder identifiers ({', '.join(placeholders)}){extra}."}
        return {**result, "tier": "PASS", "materiality": "Nothing found."}
    if rule.systemic:
        return {**result, "tier": "SYSTEMIC", "materiality": rule.systemic}
    if not rule.scenarios:
        return {**result, "materiality": f"Cannot move a yardstick: {rule.no_effect}"}

    best = None
    for scenario in rule.scenarios:
        after = ys.evaluate(scenario)
        deltas = {k: _pct(after[k]) - _pct(ys.baseline[k]) for k in YARDSTICK_LABEL}
        moved = round(max([abs(d) for d in deltas.values() if d == d] or [0.0]), 2)
        changed = after["top_channel"] != ys.baseline["top_channel"]
        if best is None or (changed, moved) > best[0]:
            best = ((changed, moved), scenario, after, deltas)
    (changed, moved), scenario, after, deltas = best

    tier = "HIGH" if changed or moved >= TIER_HIGH_PP else "MEDIUM" if moved >= TIER_MEDIUM_PP else "LOW" if moved > 0 else "NONE"
    parts = [
        f"{YARDSTICK_LABEL[k]} {ys.baseline[k][0]}/{ys.baseline[k][1]} -> {after[k][0]}/{after[k][1]} ({deltas[k]:+.2f}pp)"
        for k in YARDSTICK_LABEL if after[k] != ys.baseline[k]
    ]
    if changed:
        parts.append(f"top channel '{ys.baseline['top_channel']}' -> '{after['top_channel']}'")
    line = f"If {scenario.label}: " + ("; ".join(parts) if parts else "no yardstick changes")
    return {**result, "tier": tier, "top_channel_changed": changed, "max_abs_delta_pp": moved,
            "scenario": scenario.label, "materiality": line, "mechanism": ys.mechanism(scenario)}


# ============================================================== 1. coverage


@check(1, "Coverage")
def coverage(ctx: Context) -> CheckResult:
    """Row count, fill rate of every declared field (against the table's record count) and cardinality."""
    inventory, rules = [], []
    for table, df in ctx.frames.items():
        n = len(df)
        inventory.append({"table": table, "field": "(row count)", "type": "table", "rows": n, "filled": n,
                          "fill_pct": 100.0 if n else None, "distinct": None, "categorical": False})
        if n == 0:
            rules.append(Rule(
                f"1.0.{table}", f"{table} returned 0 records", table, pd.DataFrame(columns=EVIDENCE_COLUMNS),
                table_level=True,
                no_effect="no yardstick reads this table; without schema scope its fields cannot even be listed",
            ))
        for name, kind in load.SCHEMA[table].items():
            mask = filled(df[name])
            inventory.append({
                "table": table, "field": name,
                "type": f"link -> {kind.target}" if isinstance(kind, load.Link) else kind,
                "rows": n, "filled": int(mask.sum()),
                "fill_pct": round(100 * mask.sum() / n, 2) if n else None,
                "distinct": int(df.loc[mask, name].map(_fmt).nunique()),
                "categorical": kind == load.STR and is_categorical(df[name]),
            })
            missing = df[~mask]
            if len(missing):
                rules.append(Rule(
                    f"1.1.{table}.{name}", f"{table}.{name} is empty", table, evidence(missing, table, name),
                    scenarios=[ctx.exclude(table, missing["id"], f"records missing {table}.{name} are excluded")]
                    if (table, name) in YARDSTICK_FIELDS else [],
                    no_effect=f"{table}.{name} is not read by any yardstick",
                ))
    return CheckResult(rules, pd.DataFrame(inventory))


# ============================================================== 2. referential integrity

# (rule id, child table, link field, can an orphan reach a yardstick?)
REQUIRED_PARENTS = [
    ("2.1", "Applications", "Candidate", True),
    ("2.2", "Applications", "Opening", True),
    ("2.3", "Offers", "Application", True),
    ("2.4", "Interviews", "Application", False),
    ("2.5", "People", "Department", False),
]
# (rule id, parent table, child link field on the parent) where a parent with no children is suspect.
PARENTS_EXPECTING_CHILDREN = [
    ("2.7.1", "Candidates", "Applications"),
    ("2.7.2", "Job Openings", "Applications"),
    ("2.7.3", "Departments", "People"),
    ("2.7.4", "Departments", "Job Openings"),
]
YARDSTICK_TABLES = {"Applications", "Candidates", "Offers"}
ALL_TABLES = "(all tables)"


def _ids(value: object) -> list:
    if isinstance(value, list):
        return value
    return [] if value is None or pd.isna(value) else [value]


def _broken_links(ctx: Context, table: str, name: str) -> pd.Series:
    """True where the link field holds an id that is not a record of its target table."""
    targets = set(ctx.frames[load.SCHEMA[table][name].target]["id"])
    return ctx.frames[table][name].map(lambda v: any(i not in targets for i in _ids(v))).astype(bool)


@check(2, "Referential integrity")
def referential_integrity(ctx: Context) -> CheckResult:
    rules = []

    # 2.1-2.5: child records with no parent (link empty, or pointing at a missing record)
    for rule_id, table, name, reaches in REQUIRED_PARENTS:
        df = ctx.frames[table]
        orphans = df[~filled(df[name]) | _broken_links(ctx, table, name)]
        rules.append(Rule(
            rule_id, f"{table} with no {load.SCHEMA[table][name].target} ({name} empty or dangling)", table,
            evidence(orphans, table, name),
            scenarios=[ctx.exclude(table, orphans["id"], "orphans are excluded")] if reaches else [],
            no_effect=f"{table} records are not read by any yardstick",
        ))

    # 2.6: every link field in every table, ids that exist nowhere
    for table, df in ctx.frames.items():
        links = [n for n, k in load.SCHEMA[table].items() if isinstance(k, load.Link)]
        if not links:
            continue
        bad = pd.concat([df[_broken_links(ctx, table, n)].assign(link_field=n) for n in links])
        rules.append(Rule(
            f"2.6.{table}", f"{table}: a link field holds a record id missing from its target table", table,
            evidence(bad, table, "link_field"),
            scenarios=[ctx.exclude(table, bad["id"], "records with dangling links are excluded")] if table in YARDSTICK_TABLES else [],
            no_effect=f"{table} links are not read by any yardstick",
        ))

    # 2.7: parents with no children (the other direction)
    for rule_id, table, name in PARENTS_EXPECTING_CHILDREN:
        df = ctx.frames[table]
        childless = df[~filled(df[name])]
        rules.append(Rule(
            rule_id, f"{table} with no {name}", table, evidence(childless, table, name),
            no_effect="a parent with no children adds nothing to either count",
        ))

    # 2.8: declared inverse link pairs must mirror each other
    for child, child_field, parent, parent_field in INVERSE_LINKS:
        forward = {(c, p) for c, v in zip(ctx.frames[child]["id"], ctx.frames[child][child_field]) for p in _ids(v)}
        backward = {(c, p) for p, v in zip(ctx.frames[parent]["id"], ctx.frames[parent][parent_field]) for c in _ids(v)}
        mismatched = {c for c, _ in forward ^ backward}
        bad = ctx.frames[child][ctx.frames[child]["id"].isin(mismatched)]
        rules.append(Rule(
            f"2.8.{child}.{child_field}", f"{child}.{child_field} and {parent}.{parent_field} disagree", child,
            evidence(bad, child, child_field),
            scenarios=[ctx.exclude(child, bad["id"], "records with one-sided links are excluded")] if child in YARDSTICK_TABLES else [],
            no_effect=f"{child}.{child_field} is not read by any yardstick",
        ))

    # 2.9: people links should point at the declared role
    roles = ctx.people.set_index("id")["Role"]
    for (table, name), allowed in EXPECTED_ROLES.items():
        df = ctx.frames[table].assign(linked_role=lambda d: d[name].map(roles))
        bad = df[df[name].notna() & ~df["linked_role"].isin(allowed)]
        rules.append(Rule(
            f"2.9.{table}.{name}", f"{table}.{name} links a person whose Role is not in {sorted(allowed)}", table,
            evidence(bad, table, name, "linked_role"),
            no_effect="People.Role is not read by any yardstick",
        ))
    return CheckResult(rules)


# ============================================================== 3. duplicates


@check(3, "Duplicates")
def duplicates(ctx: Context) -> CheckResult:
    rules = []

    # 3.1-3.2: the same person held in more than one Candidates record. Group ids are hashed keys.
    for rule_id, title, key in [
        ("3.1", "Candidates sharing a normalised email (lower-case, trimmed, +tag removed)", "email_norm"),
        ("3.2", "Candidates sharing a normalised name + last 10 phone digits", "name_phone"),
    ]:
        dup = ctx.candidates[ctx.candidates.duplicated(key, keep=False)]
        dup = dup.assign(group=dup[key].map(group_id), group_size=dup.groupby(key)["id"].transform("size"))
        groups = dup.groupby(key)["id"].apply(list).tolist()
        rules.append(Rule(
            rule_id, title, "Candidates",
            evidence(dup.sort_values(["group", "Created On"]), "Candidates", "group", "group_size", "Source", "Created On"),
            scenarios=[ctx.merge_candidates(groups, "each group is merged into its earliest-created record")],
            inspects=KEY_INSPECTS[key], note=RULE_NOTES.get(rule_id, ""),
        ))

    # 3.3-3.4: the same application entered twice
    for rule_id, title, keys in [
        ("3.3", "Applications sharing (candidate record, opening)", ["Candidate", "Opening"]),
        ("3.4", "Applications sharing (person by name + phone, opening)", ["name_phone", "Opening"]),
    ]:
        dup = ctx.app_x[ctx.app_x.duplicated(keys, keep=False)]
        dup = dup.assign(group=(dup[keys[0]].astype(str) + "|" + dup[keys[1]].astype(str)).map(group_id))
        groups = dup.groupby(keys)["id"].apply(list).tolist()
        rules.append(Rule(
            rule_id, title, "Applications",
            evidence(dup.sort_values(["group", "Applied On"]), "Applications", "group", "Candidate ID", "Req ID", "Stage", "Applied On"),
            scenarios=[ctx.dedupe_applications(groups, "each group keeps only its earliest application")],
            inspects=KEY_INSPECTS.get(keys[0], set()),
        ))

    # 3.5: business ids that should be unique
    for table, key in BUSINESS_KEY.items():
        df = ctx.frames[table]
        if key == "id" or df.empty:
            continue
        dup = df[df[key].duplicated(keep=False)]
        rules.append(Rule(
            f"3.5.{table}", f"{table}.{key} used by more than one record", table, evidence(dup.sort_values(key), table, key),
            no_effect="yardsticks join on Airtable record ids; a report keyed on this business id would mis-join these rows",
        ))

    # 3.6: more than one offer per application
    multi = ctx.offers[ctx.offers["Application"].notna() & ctx.offers.duplicated("Application", keep=False)]
    latest = multi.sort_values(["Offered On", "Offer ID"]).drop_duplicates("Application", keep="last")
    rules.append(Rule(
        "3.6", "Applications with more than one Offer record", "Offers", evidence(multi, "Offers", "Application", "Status", "Offered On"),
        scenarios=[Scenario("only the latest offer per application counts", drop_offers=set(multi["id"]) - set(latest["id"]))],
    ))
    return CheckResult(rules)


# ============================================================== 4. categorical hygiene

NEGATION = re.compile(r"\b(no|not|non)\b")


def _collapse(value: str) -> str:
    return " ".join(value.split()).casefold()


def _synonym_key(value: str) -> str:
    return SYNONYMS.get(_collapse(value), _collapse(value))


def _canonical(values: list, counts: pd.Series) -> str:
    """Most frequent spelling in the group, ties broken alphabetically."""
    return sorted(values, key=lambda v: (-counts[v], v))[0]


def _groups(values: list, key: Callable) -> list:
    buckets: dict = {}
    for v in values:
        buckets.setdefault(key(v), []).append(v)
    return [group for group in buckets.values() if len(group) > 1]


def _near_duplicates(values: list) -> list:
    """Pairs of distinct spellings that look alike, ignoring digit-only and negation differences."""
    pairs = []
    keys = sorted({_synonym_key(v) for v in values})
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if re.sub(r"\d", "", a) == re.sub(r"\d", "", b) or bool(NEGATION.search(a)) != bool(NEGATION.search(b)):
                continue
            if difflib.SequenceMatcher(None, a, b).ratio() >= NEAR_DUPLICATE_MIN_RATIO:
                pairs.append([v for v in values if _synonym_key(v) in (a, b)])
    return pairs


def _remap_scenarios(table: str, name: str, remap: dict, label: str) -> list:
    if (table, name) == ("Candidates", "Source"):
        return [Scenario(label, source_remap=remap)]
    if (table, name) == ("Applications", "Stage"):
        return [Scenario(label, stage_remap=remap)]
    if (table, name) == ("Offers", "Status"):
        return [Scenario(label, status_remap=remap)]
    return []


def _hygiene_rule(ctx: Context, rule_id: str, title: str, table: str, name: str, remap: dict, label: str) -> Rule:
    df = ctx.frames[table]
    hit = df[df[name].isin(list(remap))]
    return Rule(
        f"{rule_id}.{table}.{name}", f"{title}: {table}.{name}", table,
        evidence(hit.assign(maps_to=hit[name].map(remap)), table, name, "maps_to"),
        scenarios=_remap_scenarios(table, name, remap, label),
        no_effect=f"{table}.{name} is not read by any yardstick",
    )


HYGIENE_KINDS = {
    "4.1": "case variants",
    "4.2": "leading, trailing or repeated whitespace",
    "4.3": "synonym variants (declared SYNONYMS)",
    "4.4": f"near-duplicate spellings (similarity >= {NEAR_DUPLICATE_MIN_RATIO}, for review)",
}


@check(4, "Categorical hygiene")
def categorical_hygiene(ctx: Context) -> CheckResult:
    """Raw value inventory of every enum-like field, read from raw JSON before any normalisation."""
    inventory, found = [], {rule_id: [] for rule_id in HYGIENE_KINDS}
    fields_checked = 0
    for table in config.TABLES:
        records = load.load_raw(table)
        for name, kind in load.SCHEMA[table].items():
            if kind != load.STR or not is_categorical(ctx.frames[table][name]):
                continue
            fields_checked += 1
            counts = pd.Series([r["fields"][name] for r in records if name in r["fields"]], dtype=object).value_counts()
            values = list(counts.index)

            remaps = {rule_id: {} for rule_id in HYGIENE_KINDS}
            for group in _groups(values, _collapse):
                if len({" ".join(v.split()) for v in group}) > 1:
                    canonical = _canonical(group, counts)
                    remaps["4.1"].update({v: canonical for v in group if v != canonical})
            remaps["4.2"] = {v: " ".join(v.split()) for v in values if v != " ".join(v.split())}
            for group in _groups(values, _synonym_key):
                if len({_collapse(v) for v in group}) > 1:
                    canonical = _canonical(group, counts)
                    remaps["4.3"].update({v: canonical for v in group if v != canonical})
            for group in _near_duplicates(values):
                canonical = _canonical(group, counts)
                remaps["4.4"].update({v: canonical for v in group if v != canonical})

            for rule_id, remap in remaps.items():
                if remap:
                    found[rule_id].append(_hygiene_rule(
                        ctx, rule_id, HYGIENE_KINDS[rule_id], table, name, remap, f"{HYGIENE_KINDS[rule_id]} are normalised"))
            for value, n in counts.items():
                inventory.append({
                    "table": table, "field": name, "raw_value": repr(value), "count": int(n),
                    "pct_of_filled": round(100 * n / counts.sum(), 2),
                    **{f"{rule_id} {HYGIENE_KINDS[rule_id].split(' (')[0]}": remaps[rule_id].get(value, "") for rule_id in HYGIENE_KINDS},
                })

    rules = []
    for rule_id, title in HYGIENE_KINDS.items():
        rules.extend(found[rule_id] or [Rule(
            rule_id, f"{title} (all {fields_checked} enum-like fields)", "(enum-like fields)", pd.DataFrame(columns=EVIDENCE_COLUMNS))])
    for table, name, value, overlaps in TAXONOMY_OVERLAPS:
        rules.append(_hygiene_rule(
            ctx, "4.5", f"taxonomy overlap, '{value}' can also count as '{overlaps}' (declared)", table, name,
            {value: overlaps}, f"'{value}' is counted as '{overlaps}'"))
    return CheckResult(rules, pd.DataFrame(inventory))


# ============================================================== helpers for checks 5-8


def _mask(series: pd.Series) -> pd.Series:
    """Nullable comparisons -> plain booleans, with missing treated as False."""
    return series.fillna(False).astype(bool)


def _is(series: pd.Series, value: object) -> pd.Series:
    return _mask(series.eq(value))


def _isin(series: pd.Series, values) -> pd.Series:
    return _mask(series.isin(list(values)))


def _per_table_rules(rule_id: str, title: str, hits: dict, no_effect: str, scope: str) -> list:
    """One rule per table with hits; a single PASS rule if no table has any."""
    rules = [
        Rule(f"{rule_id}.{table}", f"{title} ({table})", table, ev, no_effect=no_effect)
        for table, ev in hits.items() if len(ev)
    ]
    return rules or [Rule(rule_id, f"{title} ({scope})", scope, pd.DataFrame(columns=EVIDENCE_COLUMNS))]


# ============================================================== 5. temporal logic

DATES_NOT_READ = "all-time yardsticks do not read dates; this moves records in or out of windowed cuts such as trailing 12 months"


@check(5, "Temporal logic")
def temporal_logic(ctx: Context) -> CheckResult:
    rules = []
    a, o, iv = ctx.app_x, ctx.offer_x, ctx.iv_x
    hires = a[_is(a["Stage"], "Hired")]

    # 5.1-5.3: the three sequences named in the brief
    bad = o[_mask(o["Offered On"] < o["Applied On"])]
    rules.append(Rule(
        "5.1", "Offer dated before its application (Offers.Offered On < Applications.Applied On)", "Offers",
        evidence(bad, "Offers", "Offered On", "Applied On", "Application ID"),
        scenarios=[ctx.exclude("Offers", bad["id"], "offers dated before their application are excluded as mis-linked")],
    ))
    bad = iv[_is(iv["offer_status"], "Accepted") & _mask(iv["event_on"] > iv["offer_decision_on"])]
    rules.append(Rule(
        "5.2", "Interview held after its offer was accepted (interview date > Offers.Decision On)", "Interviews",
        evidence(bad, "Interviews", "Round", "event_on", "offer_decision_on", "Offer ID"),
        scenarios=[Scenario("those acceptances are treated as unconfirmed (offer and hire excluded)",
                            drop_apps=set(bad["Application"].dropna()), drop_offers=set(bad["offer_id"].dropna()))],
    ))
    bad = hires[_mask(hires["Closed On"] < hires["opening_opened_on"])]
    rules.append(Rule(
        "5.3", "Hire closed before its requisition opened (Closed On < Job Openings.Opened On)", "Applications",
        evidence(bad, "Applications", "Closed On", "opening_opened_on", "Req ID"),
        no_effect="hire count and channel do not depend on which requisition a hire sits on; affects time-to-fill",
    ))

    # 5.4-5.6: impossible calendar values in every date field
    future, after_created, epoch = {}, {}, {}
    for table, df in ctx.frames.items():
        created_day = df["createdTime"].dt.tz_convert(None).dt.normalize()
        for name in [n for n, k in load.SCHEMA[table].items() if k == load.DATE]:
            epoch[table] = pd.concat([epoch.get(table, pd.DataFrame(columns=EVIDENCE_COLUMNS)),
                                      evidence(df[_mask(df[name] < EPOCH_CUTOFF)], table, name)])
            if (table, name) in FORWARD_LOOKING_DATES:
                continue
            future[table] = pd.concat([future.get(table, pd.DataFrame(columns=EVIDENCE_COLUMNS)),
                                       evidence(df[_mask(df[name] > SNAPSHOT_DAY)], table, name)])
            after_created[table] = pd.concat([after_created.get(table, pd.DataFrame(columns=EVIDENCE_COLUMNS)),
                                              evidence(df[_mask(df[name] > created_day)], table, name)])
    rules += _per_table_rules("5.4", f"Backward-looking date later than the snapshot day {SNAPSHOT_DAY.date()}", future, DATES_NOT_READ, "all tables")
    rules += _per_table_rules("5.5", "Backward-looking date later than the day the record was created (createdTime)", after_created, DATES_NOT_READ, "all tables")
    rules += _per_table_rules("5.6", f"Date before {EPOCH_CUTOFF.date()} (epoch / default values)", epoch, DATES_NOT_READ, "all tables")

    # 5.7: the application pipeline must run in order, including across skipped steps
    pairs = [(x, y) for i, x in enumerate(PIPELINE_ORDER) for y in PIPELINE_ORDER[i + 1:]]
    bad = pd.concat([a[_mask(a[x] > a[y])].assign(violation=f"{x} > {y}") for x, y in pairs])
    rules.append(Rule("5.7", "Application pipeline dates out of order", "Applications",
                      evidence(bad, "Applications", "violation"), no_effect=DATES_NOT_READ))

    # 5.8-5.13: other sequences that cannot happen
    sequences = [
        ("5.8", "Interview scheduled before its application was made", "Interviews", iv, "Scheduled On", "Applied On"),
        ("5.9", "Interview completed before it was scheduled", "Interviews", iv, "Completed On", "Scheduled On"),
        ("5.10", "Application made before its candidate record was created (Candidates.Created On)", "Applications", a, "Applied On", "cand_created_on"),
        ("5.11", "Application made before its requisition opened", "Applications", a, "Applied On", "opening_opened_on"),
        ("5.12", "Offer decided before it was made", "Offers", o, "Decision On", "Offered On"),
        ("5.13", "Proposed start date before the offer decision", "Offers", o, "Proposed Start Date", "Decision On"),
        ("5.14", "Hire closed before its offer was accepted (Closed On < Offers.Decision On)", "Applications", hires, "Closed On", "offer_decision_on"),
        ("5.15", "Requisition target close before it opened", "Job Openings", ctx.openings, "Target Close", "Opened On"),
    ]
    for rule_id, title, table, df, earlier_field, later_field in sequences:
        bad = df[_mask(df[earlier_field] < df[later_field])]
        rules.append(Rule(rule_id, title, table, evidence(bad, table, earlier_field, later_field), no_effect=DATES_NOT_READ))

    # 5.16-5.18: the same date stored twice disagrees with itself
    sched = ctx.interviews.groupby("Application")["Scheduled On"].agg(first_scheduled="min", last_scheduled="max")
    ax = a.merge(sched, left_on="id", right_index=True, how="left")
    copies = [
        ("5.16", "Applications.First Interview On differs from its earliest Interviews.Scheduled On", ax, "Applications", "First Interview On", "first_scheduled"),
        ("5.17", "Applications.Final Interview On differs from its latest Interviews.Scheduled On", ax, "Applications", "Final Interview On", "last_scheduled"),
        ("5.18", "Applications.Offered On differs from Offers.Offered On", o, "Offers", "app_offered_on", "Offered On"),
    ]
    for rule_id, title, df, table, left, right in copies:
        bad = df[df[left].notna() & df[right].notna() & _mask(df[left] != df[right])]
        rules.append(Rule(rule_id, title, table, evidence(bad, table, left, right), no_effect=DATES_NOT_READ))
    return CheckResult(rules)


# ============================================================== 6. state-machine contradictions


@check(6, "State-machine contradictions")
def state_contradictions(ctx: Context) -> CheckResult:
    rules = []
    a, o, iv = ctx.app_x, ctx.offer_x, ctx.iv_x
    hires = a[_is(a["Stage"], "Hired")]

    # 6.1: rejected or withdrawn application with an accepted offer
    bad = o[_is(o["Status"], "Accepted") & _isin(o["Stage"], REJECTED_STAGES)]
    rules.append(Rule(
        "6.1", "Application Rejected/Withdrawn but its offer is Accepted", "Offers", evidence(bad, "Offers", "Status", "Stage"),
        scenarios=[Scenario("the rejection stands: offer counted as Declined, hire removed",
                            offer_status={i: "Declined" for i in bad["id"]}, drop_apps=set(bad["app_id"]))],
    ))

    # 6.2: closed requisition with a live pipeline
    live = a[_isin(a["opening_status"], CLOSED_REQUISITION_STATUSES) & _is(a["Status"], "Active")]
    reqs = ctx.openings[ctx.openings["id"].isin(live["Opening"])]
    reqs = reqs.assign(active_applications=reqs["id"].map(live.groupby("Opening").size()),
                       active_stages=reqs["id"].map(live.groupby("Opening")["Stage"].agg(lambda s: ",".join(sorted(set(s))))))
    pending = live[_is(live["offer_status"], "Pending")]
    rules.append(Rule(
        "6.2", "Requisition Filled/Cancelled but still has Active applications", "Job Openings",
        evidence(reqs, "Job Openings", "Status", "active_applications", "active_stages"),
        scenarios=[Scenario("Pending offers on closed requisitions are counted as Declined",
                            offer_status={i: "Declined" for i in pending["offer_id"]})] if len(pending) else [],
        no_effect="no Active application on these requisitions holds a Pending offer, and hires are already Closed",
    ))

    # 6.3-6.4: offer outcome and application stage must agree
    bad = o[_is(o["Status"], "Accepted") & ~_is(o["Stage"], "Hired")]
    rules.append(Rule(
        "6.3", "Offer Accepted but the application is not at Stage Hired", "Offers", evidence(bad, "Offers", "Status", "Stage"),
        scenarios=[Scenario("the stage stands: offer counted as Declined", offer_status={i: "Declined" for i in bad["id"]})],
    ))
    bad = hires[~_is(hires["offer_status"], "Accepted")]
    rules.append(Rule(
        "6.4", "Application at Stage Hired without an Accepted offer", "Applications", evidence(bad, "Applications", "Stage", "offer_status"),
        scenarios=[Scenario("the offer stands: those hires are removed", drop_apps=set(bad["id"]))],
    ))

    # 6.5: stage and status must agree on whether the application is finished
    bad = a[(_isin(a["Stage"], TERMINAL_STAGES) & _is(a["Status"], "Active")) | (_isin(a["Stage"], OPEN_STAGES) & _is(a["Status"], "Closed"))]
    rules.append(Rule(
        "6.5", "Stage and Status disagree (terminal stage but Active, or open stage but Closed)", "Applications",
        evidence(bad, "Applications", "Stage", "Status", "offer_status"),
        no_effect="neither Stage = Hired nor Offers.Status changes; see offer_status in the evidence for what each row holds",
    ))

    # 6.6-6.8: offer status and its own decision fields
    bad = o[_is(o["Status"], "Pending") & o["Decision On"].notna()]
    ids = set(bad["id"])
    rules.append(Rule(
        "6.6", "Offer Pending but it carries a Decision On date", "Offers", evidence(bad, "Offers", "Status", "Decision On"),
        scenarios=[
            Scenario("they were in fact declined", offer_status={i: "Declined" for i in ids}),
            Scenario("they were in fact accepted", offer_status={i: "Accepted" for i in ids}),
            Scenario("they are excluded as unreliable", drop_offers=ids),
        ],
    ))
    bad = o[_isin(o["Status"], {"Accepted", "Declined"}) & o["Decision On"].isna()]
    rules.append(Rule("6.7", "Offer Accepted/Declined with no Decision On", "Offers", evidence(bad, "Offers", "Status"),
                      no_effect="the recorded status is what the yardsticks read; only the date is missing"))
    bad = o[(_is(o["Status"], "Declined") & o["Decline Reason"].isna()) | (~_is(o["Status"], "Declined") & o["Decline Reason"].notna())]
    rules.append(Rule("6.8", "Decline Reason missing on a Declined offer, or present on a non-Declined one", "Offers",
                      evidence(bad, "Offers", "Status", "Decline Reason"), no_effect="Decline Reason is not read by any yardstick"))

    # 6.9-6.10: rejection reason and stage
    bad = a[a["Rejection Reason"].notna() & ~_isin(a["Stage"], REJECTED_STAGES)]
    rules.append(Rule(
        "6.9", "Rejection Reason set on an application that is not Rejected/Withdrawn", "Applications",
        evidence(bad, "Applications", "Stage", "Rejection Reason", "offer_status"),
        scenarios=[Scenario("the rejection reason is right: those hires are removed and their offers counted as Declined",
                            drop_apps=set(bad.loc[_is(bad["Stage"], "Hired"), "id"]),
                            offer_status={i: "Declined" for i in bad["offer_id"].dropna()})],
    ))
    bad = a[_isin(a["Stage"], REJECTED_STAGES) & a["Rejection Reason"].isna()]
    rules.append(Rule("6.10", "Application Rejected/Withdrawn with no Rejection Reason", "Applications",
                      evidence(bad, "Applications", "Stage"), no_effect="Rejection Reason is not read by any yardstick"))

    # 6.11-6.12: an offer record exists exactly when the stage says it should
    bad = a[_isin(a["Stage"], {"Offer", "Hired"}) & a["offer_id"].isna()]
    rules.append(Rule("6.11", "Application at Stage Offer/Hired with no Offer record", "Applications", evidence(bad, "Applications", "Stage"),
                      scenarios=[Scenario("hires without an offer record are removed", drop_apps=set(bad.loc[_is(bad["Stage"], "Hired"), "id"]))]))
    bad = o[~_isin(o["Stage"], {"Offer", "Hired"})]
    rules.append(Rule("6.12", "Offer record on an application that is not at Stage Offer/Hired", "Offers", evidence(bad, "Offers", "Status", "Stage"),
                      scenarios=[ctx.exclude("Offers", bad["id"], "offers on applications at other stages are excluded")]))

    # 6.13-6.14: hiring against requisitions that are not hiring
    bad = hires[_isin(hires["opening_status"], NOT_HIRING_REQUISITION_STATUSES)]
    rules.append(Rule(
        "6.13", "Hire on a Cancelled or On Hold requisition", "Applications", evidence(bad, "Applications", "Req ID", "opening_status", "Source"),
        scenarios=[ctx.exclude("Applications", bad["id"], "hires on requisitions that are not hiring are excluded")],
    ))
    bad = o[_is(o["Status"], "Pending") & _isin(o["opening_status"], NOT_HIRING_REQUISITION_STATUSES)]
    rules.append(Rule(
        "6.14", "Offer still Pending on a Cancelled or On Hold requisition", "Offers", evidence(bad, "Offers", "Req ID", "opening_status"),
        scenarios=[Scenario("Pending offers on requisitions that are not hiring are counted as Declined",
                            offer_status={i: "Declined" for i in bad["id"]})],
    ))

    # 6.15-6.17: headcount against hires
    hires_per_req = hires.groupby("Opening").size()
    reqs = ctx.openings.assign(hires=ctx.openings["id"].map(hires_per_req).fillna(0).astype(int))
    over = reqs[_mask(reqs["hires"] > reqs["Headcount"])]
    excess = set()
    for req_id, req in over.set_index("id").iterrows():
        on_req = hires[hires["Opening"] == req_id].sort_values(["Closed On", "Application ID"])
        excess |= set(on_req["id"].iloc[int(req["Headcount"]):])
    rules.append(Rule("6.15", "Requisition with more hires than Headcount", "Job Openings", evidence(over, "Job Openings", "Status", "Headcount", "hires"),
                      scenarios=[ctx.exclude("Applications", excess, "hires beyond headcount (latest first) are excluded")]))
    bad = reqs[_is(reqs["Status"], "Filled") & _mask(reqs["hires"] < reqs["Headcount"])]
    rules.append(Rule("6.16", "Requisition Filled with fewer hires than Headcount", "Job Openings", evidence(bad, "Job Openings", "Headcount", "hires"),
                      no_effect="a requisition's status is not read by any yardstick"))
    bad = reqs[_is(reqs["Status"], "Open") & _mask(reqs["hires"] >= reqs["Headcount"])]
    rules.append(Rule("6.17", "Requisition still Open although hires already meet Headcount", "Job Openings", evidence(bad, "Job Openings", "Headcount", "hires"),
                      no_effect="a requisition's status is not read by any yardstick"))

    # 6.18-6.19: two records of the same referral disagree
    bad = a[a["Referred By"].notna() & ~_is(a["Source"], "Referral")]
    rules.append(Rule(
        "6.18", "Application has Referred By but the candidate's Source is not Referral", "Applications",
        evidence(bad, "Applications", "Source", "Stage", "Candidate ID"),
        scenarios=[Scenario("Referred By wins: those applications count as Referral", app_source={i: "Referral" for i in bad["id"]})],
    ))
    bad = a[_is(a["Source"], "Referral") & a["Referred By"].isna()]
    rules.append(Rule(
        "6.19", "Candidate Source is Referral but the application has no Referred By", "Applications",
        evidence(bad, "Applications", "Source", "Stage", "Candidate ID"),
        scenarios=[Scenario("their true channel is unknown: those hires are excluded", drop_apps=set(bad["id"]))],
    ))

    # 6.20: one person hired more than once
    repeat = hires[hires.duplicated("name_phone", keep=False)]
    rules.append(Rule(
        "6.20", "Same person (name + phone) hired more than once", "Applications",
        evidence(repeat.assign(group=repeat["name_phone"].map(group_id)), "Applications", "group", "Candidate ID", "Req ID", "Closed On", "Source"),
        scenarios=[ctx.dedupe_applications(repeat.groupby("name_phone")["id"].apply(list).tolist(), "each person keeps only their earliest hire")],
        inspects=KEY_INSPECTS["name_phone"],
    ))

    # 6.21-6.23: interview records against their own outcome and the application stage
    result_fields = ["Completed On", "Score", "Recommendation", "Feedback"]
    has_any, has_all = iv[result_fields].notna().any(axis=1), iv[result_fields].notna().all(axis=1)
    bad = iv[(~_is(iv["Outcome"], "Completed") & has_any) | (_is(iv["Outcome"], "Completed") & ~has_all)]
    rules.append(Rule("6.21", "Interview result fields contradict Outcome (not Completed but scored, or Completed but unscored)", "Interviews",
                      evidence(bad, "Interviews", "Outcome", *result_fields[:3]), no_effect="interviews are not read by any yardstick"))
    polarity = iv["Recommendation"].astype(object).map(RECOMMENDATION_POLARITY)
    bad = iv[((polarity == 1) & _mask(iv["Score"] <= POSITIVE_RECOMMENDATION_MIN_SCORE))
             | ((polarity == -1) & _mask(iv["Score"] >= NEGATIVE_RECOMMENDATION_MAX_SCORE))]
    rules.append(Rule("6.22", "Recommendation contradicts Score", "Interviews", evidence(bad, "Interviews", "Recommendation", "Score"),
                      no_effect="interviews are not read by any yardstick"))
    bad = a[(_isin(a["Stage"], {"Applied", "Screening"}) & (a["n_interviews"] > 0))
            | (_isin(a["Stage"], {"Interview", "Offer", "Hired"}) & (a["n_interviews"] == 0))]
    rules.append(Rule("6.23", "Interviews exist before Stage Interview, or Stage Interview+ has none", "Applications",
                      evidence(bad, "Applications", "Stage", "n_interviews"), no_effect="interview counts are not read by any yardstick"))
    return CheckResult(rules)


# ============================================================== 7. outliers

NON_NEGATIVE_FIELDS = [("Offers", "Joining Bonus"), ("Candidates", "Notice Period Days"), ("Candidates", "Years Experience")]


@check(7, "Outliers")
def outliers(ctx: Context) -> CheckResult:
    rules = []
    a, o, iv = ctx.app_x, ctx.offer_x, ctx.iv_x
    hires = a[_is(a["Stage"], "Hired")]

    # 7.1-7.2: pay at zero, or an order of magnitude away from the field's median
    for table, name in MONEY_FIELDS:
        df = ctx.frames[table]
        median = df[name].median()
        zero = df[_mask(df[name] <= 0)]
        far = df[_mask((df[name] >= MAGNITUDE_FACTOR * median) | (df[name] <= median / MAGNITUDE_FACTOR))]
        for rule_id, title, bad in [
            (f"7.1.{table}.{name}", f"{table}.{name} at or below zero", zero),
            (f"7.2.{table}.{name}", f"{table}.{name} at least {MAGNITUDE_FACTOR}x above or below its median ({median:,.0f})", far),
        ]:
            rules.append(Rule(
                rule_id, title, table, evidence(bad, table, name),
                scenarios=[ctx.exclude(table, bad["id"], "offers with implausible pay are excluded as bogus")] if table == "Offers" else [],
                no_effect=f"{table}.{name} is not read by any yardstick",
            ))

    # 7.3: fields that cannot be negative
    for table, name in NON_NEGATIVE_FIELDS:
        df = ctx.frames[table]
        rules.append(Rule(f"7.3.{table}.{name}", f"{table}.{name} negative", table, evidence(df[_mask(df[name] < 0)], table, name),
                      no_effect=f"{table}.{name} is not read by any yardstick"))

    # 7.4-7.5: pay against the requisition's band
    bad = o[_mask(o["Base CTC"] < o["Salary Band Min"]) | _mask(o["Base CTC"] > o["Salary Band Max"])]
    rules.append(Rule("7.4", "Offer Base CTC outside its requisition's salary band", "Offers",
                      evidence(bad, "Offers", "Base CTC", "Salary Band Min", "Salary Band Max", "Status", "Decline Reason"),
                      no_effect="pay is not read by any yardstick; relevant when explaining declines"))
    bad = ctx.openings[_mask(ctx.openings["Salary Band Min"] > ctx.openings["Salary Band Max"])]
    rules.append(Rule("7.5", "Requisition Salary Band Min above Max", "Job Openings", evidence(bad, "Job Openings", "Salary Band Min", "Salary Band Max"),
                      no_effect="salary bands are not read by any yardstick"))

    # 7.6-7.7: durations that are negative or implausibly long (7.6 overlaps rules 5.9, 5.12-5.14 by design)
    durations = [
        ("time to hire (Applied On -> Closed On)", "Applications", hires, "Applied On", "Closed On"),
        ("offer decision (Offered On -> Decision On)", "Offers", o, "Offered On", "Decision On"),
        ("interview completion (Scheduled On -> Completed On)", "Interviews", iv, "Scheduled On", "Completed On"),
        ("offer to start (Decision On -> Proposed Start Date)", "Offers", o, "Decision On", "Proposed Start Date"),
        ("offer to hire record (Decision On -> Closed On)", "Applications", hires, "offer_decision_on", "Closed On"),
    ]
    for label, table, df, start, end in durations:
        days = (df[end] - df[start]).dt.days
        df = df.assign(days=days)
        rules.append(Rule(f"7.6.{label.split(' (')[0]}", f"Negative duration: {label}", table, evidence(df[_mask(days < 0)], table, "days", start, end),
                          no_effect="durations are not read by any yardstick"))
        if label in MAX_DURATION_DAYS:
            limit = MAX_DURATION_DAYS[label]
            rules.append(Rule(f"7.7.{label.split(' (')[0]}", f"Duration over {limit} days: {label}", table,
                              evidence(df[_mask(days > limit)], table, "days", start, end), no_effect="durations are not read by any yardstick"))

    # 7.8: people attributes outside plausible ranges
    c = ctx.candidates
    bad = c[_mask(c["Years Experience"] > MAX_YEARS_EXPERIENCE) | _mask(c["Notice Period Days"] > MAX_NOTICE_PERIOD_DAYS)]
    rules.append(Rule("7.8", f"Years Experience > {MAX_YEARS_EXPERIENCE} or Notice Period > {MAX_NOTICE_PERIOD_DAYS} days", "Candidates",
                      evidence(bad, "Candidates", "Years Experience", "Notice Period Days"), no_effect="candidate attributes are not read by any yardstick"))
    bad = c[_mask(c["Expected CTC"] < c["Current CTC"])]
    rules.append(Rule("7.9", "Candidate Expected CTC below Current CTC", "Candidates", evidence(bad, "Candidates", "Current CTC", "Expected CTC"),
                      no_effect="candidate pay is not read by any yardstick"))

    # 7.10-7.12: interview counts
    bad = a[a["n_interviews"] > MAX_INTERVIEWS_PER_APPLICATION]
    rules.append(Rule("7.10", f"Application with more than {MAX_INTERVIEWS_PER_APPLICATION} interviews", "Applications",
                      evidence(bad, "Applications", "n_interviews"), no_effect="interview counts are not read by any yardstick"))
    bad = hires[hires["n_interviews"] == 0]
    rules.append(Rule("7.11", "Hire with zero interviews", "Applications", evidence(bad, "Applications", "n_interviews", "Source"),
                      scenarios=[ctx.exclude("Applications", bad["id"], "hires with no interview are excluded as unverified")]))
    per_day = iv.groupby(["Interviewer", "Scheduled On"])["id"].transform("size")
    bad = iv[per_day > MAX_INTERVIEWS_PER_INTERVIEWER_DAY]
    rules.append(Rule("7.12", f"Interviewer with more than {MAX_INTERVIEWS_PER_INTERVIEWER_DAY} interviews on one day", "Interviews",
                      evidence(bad, "Interviews", "Interviewer", "Scheduled On"), no_effect="interview load is not read by any yardstick"))
    return CheckResult(rules)


# ============================================================== 8. test and synthetic records

# Share of a table above which a placeholder pattern is base-wide rather than a few bad rows.
PLACEHOLDER_SHARE = 0.9
# PM decision, 2026-09-15: base-wide placeholder identifiers are SCOPE, not SYSTEMIC. Reason as recorded by the PM.
SCOPE_PLACEHOLDER_IDENTIFIERS = (
    "the graders built this base and know what is in it, and anonymised identifiers do not touch the internal structural "
    "relationships every claim decision rests on")
TEXT_FIELDS = {
    "Candidates": ["Full Name", "Email", "Current Company", "Notes"],
    "People": ["Full Name", "Work Email"],
    "Job Openings": ["Title", "Req ID"],
    "Departments": ["Name"],
}
NOTE_REFERRED = "Referred internally. Available for a call after 6pm."
NOTE_CONFERENCE = "Sourced from a conference list. Responsive over email."
NOTE_CONSOLIDATED = "Applied to two openings; consolidated onto the more senior one."
NOTE_EARLIER_REJECTION = "Reached out again after an earlier rejection."
INBOUND_SOURCES = {"Job Board", "Career Site"}
LEVEL_ORDER = {"Junior": 0, "Mid": 1, "Senior": 2, "Lead": 3}


def _boilerplate_scope(ctx: Context, table: str, name: str) -> str:
    values = ctx.frames[table][name].dropna()
    return (f"{table}.{name} holds {values.nunique()} distinct strings across {len(values)} filled records, which makes it generator "
            f"boilerplate, not evidence, for every rule built on it; excluded from all Job Board / Referral tie-breaking material")


def _placeholder_phone(value: str) -> bool:
    digits = re.sub(r"\D", "", str(value))[-10:]
    return len(set(digits)) <= 2 or digits in "01234567890123456789" or digits in "98765432109876543210"


@check(8, "Test and synthetic records")
def synthetic_records(ctx: Context) -> CheckResult:
    rules = []
    c, a = ctx.candidates, ctx.app_x

    # 8.1: test tokens in human-entered text (the matched token is reported, not the value)
    for table, fields in TEXT_FIELDS.items():
        df = ctx.frames[table]
        tokens = df[fields].apply(lambda col: col.map(lambda v: ",".join(sorted({m.lower() for m in TEST_TOKENS.findall(v)})) if isinstance(v, str) else ""))
        matched = tokens.apply(lambda row: "; ".join(f"{f}:{t}" for f, t in row.items() if t), axis=1)
        bad = df.assign(matched=matched)[matched != ""]
        rules.append(Rule(f"8.1.{table}", f"Test/dummy tokens in {table} text fields", table, evidence(bad, table, "matched"),
                          scenarios=[ctx.exclude(table, bad["id"], "records containing test tokens are excluded")] if table in YARDSTICK_TABLES else [],
                          no_effect=f"{table} is not read by any yardstick", inspects={(table, f) for f in fields}))

    # 8.2-8.3: placeholder contact details
    for table, name in [("Candidates", "Email"), ("People", "Work Email")]:
        df = ctx.frames[table]
        domain = df[name].str.split("@").str[-1].str.lower()
        bad = df.assign(domain=domain)[_isin(domain, PLACEHOLDER_EMAIL_DOMAINS)]
        share = len(bad) / len(df) if len(df) else 0
        rules.append(Rule(
            f"8.2.{table}", f"{table}.{name} on a reserved placeholder domain", table, evidence(bad, table, "domain"),
            scenarios=[ctx.exclude(table, bad["id"], "records with placeholder emails are excluded")] if table in YARDSTICK_TABLES else [],
            no_effect=f"{table} is not read by any yardstick", inspects={(table, name)},
            scope=(f"{len(bad)}/{len(df)} {table}.{name} values use {sorted(set(bad['domain']))}; "
                   f"{SCOPE_PLACEHOLDER_IDENTIFIERS}") if share >= PLACEHOLDER_SHARE else "",
        ))
    bad = c[c["Phone"].map(_placeholder_phone)]
    rules.append(Rule("8.3", "Candidate phone is a placeholder (<=2 distinct digits or a run like 1234567890)", "Candidates",
                      evidence(bad, "Candidates", "Source"),
                      scenarios=[ctx.exclude("Candidates", bad["id"], "candidates with placeholder phones are excluded")],
                      inspects={("Candidates", "Phone")}))

    # 8.4: every record created in one burst
    stamps = pd.concat([df[["id", "createdTime"]].assign(table=t, key=df[BUSINESS_KEY[t]] if len(df) else None)
                        for t, df in ctx.frames.items() if len(df)], ignore_index=True)
    span = (stamps["createdTime"].max() - stamps["createdTime"].min()).total_seconds()
    burst = stamps if span <= BULK_CREATION_MAX_SECONDS else stamps.iloc[0:0]
    rules.append(Rule(
        "8.4", f"All {len(stamps)} records created within {span:.0f}s (bulk import or seeding)", ALL_TABLES,
        evidence(burst.assign(created=burst["createdTime"].astype(str)), "Applications", "table", "created", key_col="key"),
        no_effect="createdTime is not read by any yardstick; it also rules createdTime out as a fallback for event dates",
    ))

    # 8.5: free text drawn from a handful of templates
    for table, df in ctx.frames.items():
        for name, kind in load.SCHEMA[table].items():
            if kind != load.STR or name in (BUSINESS_KEY[table],):
                continue
            values = df[name].dropna()
            if len(values) >= TEMPLATED_TEXT_MIN_VALUES and values.nunique() <= TEMPLATED_TEXT_MAX_DISTINCT and not is_categorical(df[name]):
                bad = df[df[name].notna()].assign(template=lambda d: d[name].map({v: i for i, v in enumerate(sorted(values.unique()), 1)}))
                rules.append(Rule(f"8.5.{table}.{name}", f"{table}.{name}: {len(values)} values drawn from {values.nunique()} fixed strings", table,
                                  evidence(bad, table, "template"), inspects={(table, name)},
                                  no_effect="free text is not read by any yardstick; it is the evidence that the field is boilerplate"))

    # 8.6-8.9: candidate notes that contradict the structured record
    referred_any = a.groupby("Candidate")["Referred By"].agg(lambda s: s.notna().any())
    c = c.assign(referred_any=c["id"].map(referred_any).fillna(False).astype(bool), n_apps=c["Applications"].map(len))

    bad = c[_is(c["Notes"], NOTE_REFERRED) & ~_is(c["Source"], "Referral") & ~c["referred_any"]]
    # PM decisions, 2026-09-15 (8.6 in Stage 1; 8.7-8.11 in Stage 1B): every rule built on Notes or Feedback is SCOPE and
    # carries no scenario, so none of them can appear in Job Board / Referral tie-breaking material.
    rules.append(Rule("8.6", f"Note says '{NOTE_REFERRED[:20]}...' but Source is not Referral and no Referred By exists", "Candidates",
                      evidence(bad, "Candidates", "Source"), scope=_boilerplate_scope(ctx, "Candidates", "Notes"), inspects={("Candidates", "Notes")}))

    bad = c[_is(c["Notes"], NOTE_CONFERENCE) & _isin(c["Source"], INBOUND_SOURCES)]
    apps = a[a["Candidate"].isin(bad["id"])]
    rules.append(Rule("8.7", f"Note says '{NOTE_CONFERENCE[:30]}...' but Source is an inbound channel {sorted(INBOUND_SOURCES)}", "Candidates",
                      evidence(bad, "Candidates", "Source"), scope=_boilerplate_scope(ctx, "Candidates", "Notes"), inspects={("Candidates", "Notes")}))

    bad = c[_is(c["Notes"], NOTE_CONSOLIDATED) & (c["n_apps"] > 1)]
    apps = a[a["Candidate"].isin(bad["id"])].assign(level=lambda d: d["Opening"].map(ctx.openings.set_index("id")["Level"]).map(LEVEL_ORDER))
    less_senior = apps.sort_values(["Candidate", "level"]).groupby("Candidate").head(1)
    rules.append(Rule("8.8", "Note says the candidate was consolidated onto one opening but two applications remain", "Candidates",
                      evidence(bad, "Candidates", "n_apps"), scope=_boilerplate_scope(ctx, "Candidates", "Notes"), inspects={("Candidates", "Notes")}))

    rejected_before = a[_is(a["Stage"], "Rejected")].groupby("Candidate")["Closed On"].min()
    last_applied = a.groupby("Candidate")["Applied On"].max()
    earlier = c["id"].map(rejected_before) < c["id"].map(last_applied)
    bad = c[_is(c["Notes"], NOTE_EARLIER_REJECTION) & ~_mask(earlier)]
    rules.append(Rule("8.9", "Note says the candidate re-applied after an earlier rejection but no earlier rejection exists", "Candidates",
                      evidence(bad, "Candidates", "n_apps"), scope=_boilerplate_scope(ctx, "Candidates", "Notes"), inspects={("Candidates", "Notes")}))

    # 8.10-8.11: interview feedback text against its own recommendation
    iv = ctx.interviews
    text_polarity = iv["Feedback"].astype(object).map(FEEDBACK_POLARITY)
    rec_polarity = iv["Recommendation"].astype(object).map(RECOMMENDATION_POLARITY)
    bad = iv[text_polarity.notna() & rec_polarity.notna() & (text_polarity != rec_polarity)]
    rules.append(Rule("8.10", "Feedback text contradicts Recommendation (declared FEEDBACK_POLARITY)", "Interviews",
                      evidence(bad, "Interviews", "Recommendation", "Score"), scope=_boilerplate_scope(ctx, "Interviews", "Feedback"),
                      inspects={("Interviews", "Feedback")}))
    bad = iv[iv["Feedback"].notna() & text_polarity.isna()]
    rules.append(Rule("8.11", "Feedback string with no declared polarity (not classified)", "Interviews",
                      evidence(bad, "Interviews", "Recommendation"), scope=_boilerplate_scope(ctx, "Interviews", "Feedback"),
                      inspects={("Interviews", "Feedback")}))
    return CheckResult(rules)


# ============================================================== runner


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _check_csv(result: CheckResult) -> pd.DataFrame:
    if result.table is not None:
        return result.table
    parts = [r.evidence.assign(rule_id=r.rule_id, rule=r.title, table=r.table) for r in result.rules if len(r.evidence)]
    parts += [pd.DataFrame([{"rule_id": r.rule_id, "rule": r.title, "table": r.table, "record_id": "(note)", "key": "", "detail": r.note}])
              for r in result.rules if r.note]
    if not parts:
        return pd.DataFrame(columns=["rule_id", "rule", "table", *EVIDENCE_COLUMNS])
    out = pd.concat(parts, ignore_index=True)[["rule_id", "rule", "table", *EVIDENCE_COLUMNS]]
    out["rule_id"] = RULE_ID_PREFIX + out["rule_id"].astype(str)
    return out


def rule_counts(frames: dict) -> dict:
    ctx = Context(frames)
    return {r.rule_id: r.count for _, _, fn in CHECKS for r in fn(ctx).rules}


def identifier_sensitive_rules(frames: dict) -> set:
    """Rules whose findings change when defects are injected into placeholder identifier fields and nothing else."""
    base = rule_counts(frames)
    mutated = {t: df.copy() for t, df in frames.items()}
    cands, people = mutated["Candidates"], mutated["People"]
    rows = cands.index[cands["Candidate ID"] >= "CAND-00200"][:5]   # well away from the seeded duplicates at CAND-00001-00012
    cands.loc[rows[0], "Email"] = cands.loc[rows[1], "Email"]       # duplicate email
    cands.loc[rows[2], "Email"] = "test.account@example.com"        # test token in an email
    cands.loc[rows[3], "Full Name"] = "Test Dummy"                  # test token in a name
    cands.loc[rows[4], "Phone"] = "+91 0000000000"                   # placeholder phone
    people.loc[people.index[0], "Full Name"] = "Test Person"
    people.loc[people.index[1], "Work Email"] = "dummy@example.com"
    after = rule_counts(mutated)
    return {rule_id for rule_id, n in base.items() if after.get(rule_id) != n}


def run() -> pd.DataFrame:
    frames = load.load_all()
    ctx = Context(frames)
    ys = Yardsticks(ctx)
    config.AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    all_rows = sum(ctx.rows.values())

    summary, record_sets, declared = [], {}, {}
    for number, name, fn in sorted(CHECKS, key=lambda c: c[0]):
        result = fn(ctx)
        path = config.AUDIT_DIR / f"audit_{number}_{_slug(name)}.csv"
        _check_csv(result).to_csv(path, index=False)
        for rule in result.rules:
            record_sets[rule.rule_id] = (rule.table, frozenset(rule.evidence["record_id"])) if rule.count else None
            declared[rule.rule_id] = bool(rule.inspects & PLACEHOLDER_IDENTIFIER_FIELDS)
            rows = all_rows if rule.table == ALL_TABLES else ctx.rows.get(rule.table)
            summary.append({
                "check": f"{number}. {name}", "rule_id": rule.rule_id, "rule": rule.title, "table": rule.table,
                "count": rule.count, "table_rows": rows,
                "pct_of_table": round(100 * rule.count / rows, 2) if rows else None,
                **assess(rule, ys), "note": rule.note, "evidence_csv": path.name,
            })

    # NOT TESTABLE rests on the declared `inspects`; injecting defects into identifier fields must move exactly those rules.
    sensitive = identifier_sensitive_rules(frames)
    undeclared = sorted(sensitive - {r for r, d in declared.items() if d})
    unexercised = sorted(r for r, d in declared.items() if d and r not in sensitive and not record_sets[r])
    if undeclared or unexercised:
        raise RuntimeError(f"identifier sensitivity check failed: moved but undeclared {undeclared}; declared, clean and not moved {unexercised}")

    df = pd.DataFrame(summary)
    df = df.assign(_tier=df["tier"].map(TIER_ORDER.index)).sort_values(
        ["_tier", "max_abs_delta_pp", "top_channel_changed", "count"], ascending=[True, False, False, False], kind="mergesort"
    ).drop(columns="_tier").reset_index(drop=True)
    df.insert(0, "rank", range(1, len(df) + 1))
    df["identifier_sensitive"] = df["rule_id"].isin(sensitive)
    # Rules flagging the identical record set are one defect: the first by rank is canonical.
    canonical = {}
    for rule_id in df["rule_id"]:
        key = record_sets[rule_id]
        if key is not None:
            canonical.setdefault(key, rule_id)
    df["same_defect_as"] = [canonical[record_sets[r]] if record_sets[r] is not None and canonical[record_sets[r]] != r else "" for r in df["rule_id"]]
    df["rule_id"] = RULE_ID_PREFIX + df["rule_id"]
    df["same_defect_as"] = df["same_defect_as"].map(lambda s: RULE_ID_PREFIX + s if s else "")
    df.to_csv(config.AUDIT_DIR / "audit_summary.csv", index=False)
    return df


def main() -> int:
    df = run()
    print(f"audit: {len(df)} rules across {len(CHECKS)} checks; baseline yardsticks "
          f"channel 7/26, accepted/all 26/36, accepted/decided 26/31 (see module docstring)")
    print("tiers:", df["tier"].value_counts().reindex(TIER_ORDER, fill_value=0).to_dict())
    distinct = df[df["same_defect_as"] == ""]["tier"].value_counts().reindex(TIER_ORDER, fill_value=0).to_dict()
    print("distinct defects per tier (rules flagging identical records counted once):", distinct)
    with pd.option_context("display.width", 250, "display.max_colwidth", 110):
        shown = df[df["tier"] != "PASS"]
        print(shown[["rank", "tier", "rule_id", "count", "table_rows", "pct_of_table", "max_abs_delta_pp", "rule"]].to_string(index=False))
    print(f"\nwrote {config.AUDIT_DIR}/audit_<n>_<check>.csv x {len(CHECKS)} and audit_summary.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
