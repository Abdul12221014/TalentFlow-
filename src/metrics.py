"""Claim metrics, computed from the cached snapshot only.

Current scope: reverse-engineer the VP People's two figures by enumerating every plausible
definition available in this data and computing each one. Nothing here asserts which is right.

  Claim 1  "Job boards ... bring in 26.9% of our hires"  -> outputs/tables/exploration/claim1_definitions.csv
  Claim 2  "Our offer acceptance rate is around 72%"     -> outputs/tables/exploration/claim2_definitions.csv

Everything this script writes is exploration output (outputs/tables/exploration/). Cited numbers get
their own tables from report.py in outputs/tables/.

Match rule: a definition reproduces a figure if it rounds to the precision the VP quoted.
26.9 is quoted to one decimal (26.85 <= pct < 26.95); "around 72" to a whole number
(71.5 <= pct < 72.5). The grids are large and the denominators small, so some matches will be
arithmetic coincidence; every row is kept so that can be judged.
"""
from __future__ import annotations

import pandas as pd

import config
import load

CLAIM1_TARGET, CLAIM1_TOL = 26.9, 0.05
CLAIM2_TARGET, CLAIM2_TOL = 72.0, 0.5
SMALL_N = 30

# 2026-08-27: every record's createdTime and the latest Applied On. 2026-09-14: snapshot day.
ANCHORS = ("2026-08-27", "2026-09-14")


def windows() -> list[tuple[str, pd.Timestamp | None, pd.Timestamp | None]]:
    out = [("all time", None, None)]
    for anchor in ANCHORS:
        end = pd.Timestamp(anchor)
        for months in (12, 6, 3):
            out.append((f"trailing {months}m to {anchor}", end - pd.DateOffset(months=months) + pd.Timedelta(days=1), end))
    out.append(("calendar 2025", pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31")))
    out.append(("2026 YTD to 2026-09-14", pd.Timestamp("2026-01-01"), pd.Timestamp("2026-09-14")))
    return out


def _row(num: float, den: int, target: float, tol: float, **definition: object) -> dict:
    pct = 100.0 * num / den if den else float("nan")
    return {
        "pct": round(pct, 2) if den else None,
        "numerator": num,
        "denominator": den,
        "abs_diff_pp": round(abs(pct - target), 2) if den else None,
        "reproduces": bool(den) and target - tol <= pct < target + tol,
        "small_n": den < SMALL_N,
        **definition,
    }


def _sorted(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df = df.sort_values(["abs_diff_pp", "denominator"], ascending=[True, False], na_position="last", kind="mergesort")
    return df.reset_index(drop=True)


def candidate_frame(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Candidates plus a person key (name + phone digits) and the person's earliest-created Source."""
    c = frames["Candidates"].copy()
    c["person"] = c["Full Name"].str.strip().str.lower() + "|" + c["Phone"].str.replace(r"\D", "", regex=True)
    first = c.sort_values(["Created On", "Candidate ID"]).drop_duplicates("person")
    c["person_source"] = c["person"].map(first.set_index("person")["Source"])
    return c


# ---------------------------------------------------------------- claim 1: job-board share of hires

CHANNELS = {
    "raw Source = Job Board": {"Job Board"},
    "bucket: Job Board + LinkedIn": {"Job Board", "LinkedIn"},
    "bucket: Job Board + LinkedIn + Career Site": {"Job Board", "LinkedIn", "Career Site"},
}
ATTRIBUTION = ("Candidates.Source as recorded", "Applications.Referred By overrides Source")
UNIT_KEYS = {
    "application rows": None,
    "distinct candidate+opening": ["Candidate", "Opening"],
    "distinct candidate record": ["Candidate"],
    "distinct person (name+phone)": ["person"],
}
ALL_UNITS = tuple(UNIT_KEYS)
DATE_LABEL = {
    "Closed On": "Applications.Closed On",
    "Applied On": "Applications.Applied On",
    "offer_decision_on": "Offers.Decision On",
    "offer_offered_on": "Offers.Offered On",
    "offer_start": "Offers.Proposed Start Date",
    "cand_created": "Candidates.Created On",
}


def application_frame(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per application with its candidate, opening and (at most one) offer attached."""
    cands = candidate_frame(frames)[["id", "Source", "person", "person_source", "Created On"]]
    offers = frames["Offers"].rename(columns={
        "id": "offer_id", "Status": "offer_status", "Offered On": "offer_offered_on",
        "Decision On": "offer_decision_on", "Proposed Start Date": "offer_start",
    })[["offer_id", "Application", "offer_status", "offer_offered_on", "offer_decision_on", "offer_start"]]
    openings = frames["Job Openings"][["id", "Status"]].rename(columns={"id": "opening_id", "Status": "opening_status"})

    a = frames["Applications"].merge(
        cands.rename(columns={"id": "cand_id", "Created On": "cand_created"}),
        left_on="Candidate", right_on="cand_id", how="left", validate="many_to_one",
    )
    a = a.merge(offers, left_on="id", right_on="Application", how="left", validate="one_to_one")
    a = a.merge(openings, left_on="Opening", right_on="opening_id", how="left", validate="many_to_one")
    a["referred"] = a["Referred By"].notna()
    return a


def _accepted_started_by(anchor: str):
    return lambda a: (a["offer_status"] == "Accepted") & (a["offer_start"] <= pd.Timestamp(anchor))


def _everything(a: pd.DataFrame) -> pd.Series:
    return pd.Series(True, index=a.index)


# (event label, row mask, date columns usable for windowing, units)
CLAIM1_EVENTS = [
    ("hired: Applications.Stage = Hired", lambda a: a["Stage"] == "Hired",
     ["Closed On", "Applied On", "offer_decision_on", "offer_start"], ALL_UNITS),
    ("offer accepted: Offers.Status = Accepted", lambda a: a["offer_status"] == "Accepted",
     ["offer_decision_on", "offer_offered_on", "offer_start"], ALL_UNITS),
    *[(f"hire started: Accepted and Proposed Start Date <= {d}", _accepted_started_by(d), ["offer_start"], ALL_UNITS)
      for d in ANCHORS],
    ("hire on a Filled opening: Stage = Hired and Opening.Status = Filled",
     lambda a: (a["Stage"] == "Hired") & (a["opening_status"] == "Filled"), ["Closed On"], ALL_UNITS),
    ("offer extended: any Offer record", lambda a: a["offer_id"].notna(), ["offer_offered_on"], ALL_UNITS),
    ("application: every Applications row", _everything, ["Applied On"], ALL_UNITS),
    ("candidate: every Candidates record", _everything, ["cand_created"], ALL_UNITS[2:]),
]


def claim1_table(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    a = application_frame(frames)
    rows = []
    for event, mask, date_cols, units in CLAIM1_EVENTS:
        base = a[mask(a).fillna(False).astype(bool)]
        for window, start, end in windows():
            for date_col in [None] if start is None else date_cols:
                pop = base if date_col is None else base[base[date_col].between(start, end)]
                for unit in units:
                    keys = UNIT_KEYS[unit]
                    if keys is None:
                        source, referred = pop["Source"], pop["referred"]
                    else:
                        g = pop.groupby(keys).agg(
                            source=("Source", "first"), person_source=("person_source", "first"), referred=("referred", "any")
                        )
                        source = g["person_source"] if keys == ["person"] else g["source"]
                        referred = g["referred"].astype(bool)
                    for attribution in ATTRIBUTION:
                        effective = source.where(~referred, "Referral") if "overrides" in attribution else source
                        for channel, bucket in CHANNELS.items():
                            rows.append(_row(
                                int(effective.isin(bucket).sum()), len(effective), CLAIM1_TARGET, CLAIM1_TOL,
                                event=event, window=window,
                                date_basis=DATE_LABEL[date_col] if date_col else "none (all time)",
                                unit=unit, attribution=attribution, channel=channel,
                            ))
    return _sorted(rows)


# ---------------------------------------------------------------- claim 2: offer acceptance rate

PENDING_RULES = (
    "Pending excluded",
    "Pending counted as not accepted",
    "Pending with a Decision On counted as not accepted; other Pending excluded",
    "Pending counted as accepted",
)
# The data has no Rescinded status. The two proxies are constructions, not recorded facts.
RESCIND_RULES = {
    "none (no Rescinded status exists)": (None, None),
    "proxy: offer on a Cancelled opening -> excluded": ("cancelled_opening", "drop"),
    "proxy: offer on a Cancelled opening -> not accepted": ("cancelled_opening", "not"),
    "proxy: application carries a Rejection Reason -> excluded": ("rejection_reason", "drop"),
    "proxy: application carries a Rejection Reason -> not accepted": ("rejection_reason", "not"),
}
NUMERATOR_RULES = ("Status = Accepted", *[f"Accepted and Proposed Start Date <= {d}" for d in ANCHORS])
CLAIM2_UNITS = (
    "offer records",
    "candidates: accepted if any offer accepted",
    "candidates: outcome of latest offer (Offered On)",
    "persons (name+phone): accepted if any offer accepted",
    "requisitions: share with >=1 accepted offer",
    "requisitions: mean of per-requisition rates",
)
OFFER_DATE_LABEL = {"Offered On": "Offers.Offered On", "app_offered_on": "Applications.Offered On", "Decision On": "Offers.Decision On"}


def offer_frame(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    apps = frames["Applications"][["id", "Candidate", "Opening", "Offered On", "Rejection Reason"]].rename(
        columns={"id": "app_id", "Offered On": "app_offered_on"}
    )
    cands = candidate_frame(frames)[["id", "person"]].rename(columns={"id": "cand_id"})
    openings = frames["Job Openings"][["id", "Status"]].rename(columns={"id": "opening_id", "Status": "opening_status"})
    o = frames["Offers"].merge(apps, left_on="Application", right_on="app_id", how="left", validate="one_to_one")
    o = o.merge(cands, left_on="Candidate", right_on="cand_id", how="left", validate="many_to_one")
    return o.merge(openings, left_on="Opening", right_on="opening_id", how="left", validate="many_to_one")


def offer_outcomes(o: pd.DataFrame, pending_rule: str, rescind_rule: str, numerator_rule: str) -> pd.Series:
    """Per offer: 'acc' (numerator and denominator), 'not' (denominator only) or 'drop'."""
    out = o["Status"].astype(object).map({"Accepted": "acc", "Declined": "not", "Pending": "pending"})
    proxy, action = RESCIND_RULES[rescind_rule]
    if proxy:
        flagged = o["opening_status"] == "Cancelled" if proxy == "cancelled_opening" else o["Rejection Reason"].notna()
        out = out.mask(flagged.fillna(False).astype(bool), action)
    pending = out == "pending"
    has_decision = o["Decision On"].notna()
    if pending_rule == PENDING_RULES[0]:
        out = out.mask(pending, "drop")
    elif pending_rule == PENDING_RULES[1]:
        out = out.mask(pending, "not")
    elif pending_rule == PENDING_RULES[2]:
        out = out.mask(pending & has_decision, "not").mask(pending & ~has_decision, "drop")
    else:
        out = out.mask(pending, "acc")
    if numerator_rule != NUMERATOR_RULES[0]:
        cutoff = pd.Timestamp(numerator_rule.rsplit(" ", 1)[1])
        out = out.mask((out == "acc") & ~(o["Proposed Start Date"] <= cutoff), "not")
    return out


def aggregate_offers(d: pd.DataFrame, unit: str) -> tuple[float, int]:
    if unit == "candidates: outcome of latest offer (Offered On)":
        d = d.sort_values(["Offered On", "Offer ID"]).groupby("Candidate").tail(1)
    d = d[d["out"] != "drop"]
    accepted = d["out"] == "acc"
    if unit in ("offer records", "candidates: outcome of latest offer (Offered On)"):
        return int(accepted.sum()), len(d)
    key = {"candidates: accepted if any offer accepted": "Candidate",
           "persons (name+phone): accepted if any offer accepted": "person"}.get(unit, "Opening")
    grouped = accepted.groupby(d[key])
    if unit == "requisitions: mean of per-requisition rates":
        return round(float(grouped.mean().sum()), 2), grouped.ngroups
    any_accepted = grouped.any()
    return int(any_accepted.sum()), len(any_accepted)


def claim2_table(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    o = offer_frame(frames)
    cohorts = []
    for window, start, end in windows():
        for date_col in [None] if start is None else OFFER_DATE_LABEL:
            keep = pd.Series(True, index=o.index) if date_col is None else o[date_col].between(start, end)
            cohorts.append((window, OFFER_DATE_LABEL[date_col] if date_col else "none (all time)", keep))

    rows = []
    for pending_rule in PENDING_RULES:
        for rescind_rule in RESCIND_RULES:
            for numerator_rule in NUMERATOR_RULES:
                out = offer_outcomes(o, pending_rule, rescind_rule, numerator_rule)
                scored = o.assign(out=out)
                for window, date_basis, keep in cohorts:
                    cohort = scored[keep]
                    for unit in CLAIM2_UNITS:
                        num, den = aggregate_offers(cohort, unit)
                        rows.append(_row(
                            num, den, CLAIM2_TARGET, CLAIM2_TOL, unit=unit, numerator_rule=numerator_rule,
                            pending_rule=pending_rule, rescinded_rule=rescind_rule, date_basis=date_basis, window=window,
                        ))

    # Counting from the Applications table alone: Stage = Offer holds both Pending and Declined offers.
    apps = frames["Applications"]
    stage_based = {
        "applications: Stage = Hired / Stage in (Hired, Offer)": apps[apps["Stage"].isin(["Hired", "Offer"])],
        "applications: Stage = Hired / Applications.Offered On present": apps[apps["Offered On"].notna()],
    }
    for unit, base in stage_based.items():
        for window, start, end in windows():
            pop = base if start is None else base[base["Offered On"].between(start, end)]
            rows.append(_row(
                int((pop["Stage"] == "Hired").sum()), len(pop), CLAIM2_TARGET, CLAIM2_TOL, unit=unit,
                numerator_rule="Applications.Stage = Hired",
                pending_rule="n/a: Stage cannot separate Pending from Declined",
                rescinded_rule="n/a", date_basis="none (all time)" if start is None else "Applications.Offered On",
                window=window,
            ))
    return _sorted(rows)


# ---------------------------------------------------------------- time coverage and right-censoring

# Event dates that describe the recruiting pipeline, used for the time axis. People.Joined On
# (employee tenure) and the forward-looking Target Close / Proposed Start Date are left off.
PIPELINE_DATES = [
    ("Candidates", "Created On"), ("Job Openings", "Opened On"), ("Applications", "Applied On"),
    ("Applications", "Screened On"), ("Applications", "First Interview On"), ("Applications", "Final Interview On"),
    ("Applications", "Offered On"), ("Applications", "Closed On"), ("Interviews", "Scheduled On"),
    ("Interviews", "Completed On"), ("Offers", "Offered On"), ("Offers", "Decision On"),
]
OFFER_DECISION = "offer decision: Offered On -> Decision On (Accepted/Declined offers)"
APPLICATION_OUTCOME = "application outcome: Applied On -> Closed On (Status = Closed)"
TIME_TO_HIRE = "time to hire: Applied On -> Closed On (Stage = Hired)"
SENSITIVITY_DAYS = (30, 60, 90)


def as_of_date(frames: dict[str, pd.DataFrame]) -> pd.Timestamp:
    """The data's own 'today': the latest Applied On (also the day every record was created in Airtable)."""
    return frames["Applications"]["Applied On"].max()


def snapshot_date() -> pd.Timestamp:
    import json
    return pd.Timestamp(json.loads(config.MANIFEST_PATH.read_text(encoding="utf-8"))["pull_finished_utc"][:10])


def monthly_volume(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Records per calendar month across the pipeline's full date span.

    applications = Applications.Applied On; offers = Offers.Offered On; hires = Applications.Closed On
    where Stage = Hired. Two alternates are kept for comparison: hires by their Applied On month, and
    accepted offers by Offers.Decision On.
    """
    dates = pd.concat([frames[t][n] for t, n in PIPELINE_DATES]).dropna()
    months = pd.period_range(dates.min(), dates.max(), freq="M")
    apps, offers = frames["Applications"], frames["Offers"]
    hires = apps[apps["Stage"] == "Hired"]

    def per_month(series: pd.Series) -> pd.Series:
        return series.dropna().dt.to_period("M").value_counts().reindex(months, fill_value=0)

    out = pd.DataFrame({
        "applications": per_month(apps["Applied On"]),
        "offers": per_month(offers["Offered On"]),
        "hires": per_month(hires["Closed On"]),
        "hires_by_applied_month": per_month(hires["Applied On"]),
        "accepted_by_decision_month": per_month(offers.loc[offers["Status"] == "Accepted", "Decision On"]),
    }, index=months)
    return out.rename_axis("month").reset_index().assign(month=lambda d: d["month"].astype(str))


def resolution_times(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """How long resolved records took. Quantiles use observed values (interpolation='higher')."""
    apps, offers = frames["Applications"], frames["Offers"]
    decided = offers[offers["Status"].isin(["Accepted", "Declined"])]
    closed = apps[apps["Status"] == "Closed"]
    hired = apps[apps["Stage"] == "Hired"]
    rows = []
    for measure, days in [
        (OFFER_DECISION, (decided["Decision On"] - decided["Offered On"]).dt.days),
        (APPLICATION_OUTCOME, (closed["Closed On"] - closed["Applied On"]).dt.days),
        (TIME_TO_HIRE, (hired["Closed On"] - hired["Applied On"]).dt.days),
    ]:
        d = days.dropna()
        rows.append({"measure": measure, "n": len(d), "min": int(d.min()), "p50": int(d.quantile(0.5, interpolation="higher")),
                     "p90": int(d.quantile(0.9, interpolation="higher")), "max": int(d.max()), "small_n": len(d) < SMALL_N})
    return pd.DataFrame(rows).set_index("measure")


def unresolved_offers(frames: dict[str, pd.DataFrame], as_of: pd.Timestamp, snapshot: pd.Timestamp) -> pd.DataFrame:
    o = frames["Offers"]
    pending = o[o["Status"] == "Pending"].sort_values("Offered On")
    return pd.DataFrame({
        "Offer ID": pending["Offer ID"].to_numpy(),
        "Offered On": pending["Offered On"].dt.date.to_numpy(),
        "has Decision On": pending["Decision On"].notna().to_numpy(),
        f"age days at {as_of.date()}": (as_of - pending["Offered On"]).dt.days.to_numpy(),
        f"age days at {snapshot.date()}": (snapshot - pending["Offered On"]).dt.days.to_numpy(),
    })


def offer_cohorts(frames: dict[str, pd.DataFrame], as_of: pd.Timestamp, times: pd.DataFrame) -> pd.DataFrame:
    """Acceptance among offers extended at least N days before the as-of date."""
    offers = frames["Offers"]
    t = times.loc[OFFER_DECISION]
    cutoffs = [("before: every offer", 0),
               (f"after: offered >= p90 decision time ({t.p90}d) before as-of", t.p90),
               (f"after: offered >= slowest observed decision ({t['max']}d) before as-of", t["max"])]
    cutoffs += [(f"sensitivity: offered >= {d}d before as-of", d) for d in SENSITIVITY_DAYS]
    rows = []
    for label, days in cutoffs:
        cutoff = as_of - pd.Timedelta(days=int(days))
        c = offers[offers["Offered On"] <= cutoff]
        acc, dec, pend = (int((c["Status"] == s).sum()) for s in ("Accepted", "Declined", "Pending"))
        rows.append({
            "cohort": label, "offered_on_or_before": cutoff.date(), "offers": len(c), "accepted": acc, "declined": dec,
            "pending": pend, "pending_with_decision_date": int(((c["Status"] == "Pending") & c["Decision On"].notna()).sum()),
            "accepted/all": f"{acc}/{len(c)}", "accepted/all %": round(100 * acc / len(c), 2) if len(c) else None,
            "accepted/decided": f"{acc}/{acc + dec}", "accepted/decided %": round(100 * acc / (acc + dec), 2) if acc + dec else None,
            "small_n": len(c) < SMALL_N,
        })
    return pd.DataFrame(rows)


def application_cutoffs(times: pd.DataFrame) -> list[tuple[str, int]]:
    hire, outcome = times.loc[TIME_TO_HIRE], times.loc[APPLICATION_OUTCOME]
    return [("before: every application", 0),
            (f"after: applied >= p90 time to hire ({hire.p90}d) before as-of", hire.p90),
            (f"after: applied >= slowest observed hire ({hire['max']}d) before as-of", hire["max"]),
            (f"after: applied >= slowest observed outcome ({outcome['max']}d) before as-of", outcome["max"])]


def application_tail(frames: dict[str, pd.DataFrame], as_of: pd.Timestamp, times: pd.DataFrame) -> pd.DataFrame:
    """For each cutoff: the recent tail that has not had time to resolve, and stale Active records in the rest."""
    apps = frames["Applications"]
    active = apps["Status"] == "Active"
    hired = apps["Stage"] == "Hired"
    rows = []
    for label, days in application_cutoffs(times):
        cutoff = as_of - pd.Timedelta(days=int(days))
        tail = apps["Applied On"] > cutoff
        rows.append({
            "cohort": label, "applied_on_or_before": cutoff.date(),
            "cohort applications": int((~tail).sum()), "cohort hires": int((~tail & hired).sum()),
            "cohort hire rate %": round(100 * (~tail & hired).sum() / (~tail).sum(), 2),
            "cohort still Active": int((~tail & active).sum()),
            "tail applications": int(tail.sum()), "tail still Active": int((tail & active).sum()), "tail hires": int((tail & hired).sum()),
        })
    return pd.DataFrame(rows)


def channel_hire_rates(frames: dict[str, pd.DataFrame], as_of: pd.Timestamp, times: pd.DataFrame) -> pd.DataFrame:
    """Application -> hire rate per raw Candidates.Source, for each cutoff and for resolved applications only."""
    cands = frames["Candidates"].set_index("id")["Source"]
    apps = frames["Applications"].assign(Source=lambda d: d["Candidate"].map(cands))
    populations = [(label, apps[apps["Applied On"] <= as_of - pd.Timedelta(days=int(days))]) for label, days in application_cutoffs(times)]
    populations.append(("resolved only: Status = Closed", apps[apps["Status"] == "Closed"]))
    rows = []
    for label, pop in populations:
        for source, group in [*sorted(pop.groupby("Source")), ("All channels", pop)]:
            n, h = len(group), int((group["Stage"] == "Hired").sum())
            rows.append({"population": label, "channel": source, "applications": n, "hires": h,
                         "hire rate": f"{h}/{n}", "hire rate %": round(100 * h / n, 2) if n else None, "small_n": n < SMALL_N})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- our view: estimates with uncertainty
#
# Choices, each traced to an earlier finding:
#   unit       one hire per (candidate, opening): APP-00335 repeats CAND-00035's hire into the same
#              requisition five months later (audit 3.3 / 6.20), so it and its offer are dropped.
#   channels   three bucketings survive the audit: Source as recorded; LinkedIn merged into Job Board
#              (audit 4.5); Source with any Referred By link counted as Referral (audit 6.18/6.19, where
#              the two referral fields never agree on a hire). Career Site stays separate: it is an
#              owned channel, not a job board.
#   maturity   conversion uses applications old enough to have converted (>= slowest recorded hire);
#              acceptance uses offers old enough to have been decided (>= slowest recorded decision).
#   intervals  Wilson score 95% intervals, per channel (not simultaneous). First vs second place uses an
#              exact conditional binomial test; conversion vs Job Board uses Fisher's exact test.
#   limits     a rate on fewer than MIN_N_FOR_RATE records is not reported.

from math import ceil, comb, sqrt
from statistics import NormalDist

ALPHA, POWER = 0.05, 0.80
Z_ALPHA = NormalDist().inv_cdf(1 - ALPHA / 2)
Z_POWER = NormalDist().inv_cdf(POWER)
MIN_N_FOR_RATE = 10
TARGET_MOVE = 0.05

BUCKETINGS = {
    "B1 Source as recorded": lambda a: a["source"],
    "B2 LinkedIn merged into Job Board": lambda a: a["source"].replace({"Job Board": "Job Board + LinkedIn", "LinkedIn": "Job Board + LinkedIn"}),
    "B3 any Referred By link counts as Referral": lambda a: a["source"].where(~a["referred"], "Referral"),
}
JOB_BOARD_CHANNEL = {"B1 Source as recorded": "Job Board", "B2 LinkedIn merged into Job Board": "Job Board + LinkedIn",
                     "B3 any Referred By link counts as Referral": "Job Board"}


def wilson(k: int, n: int, z: float = Z_ALPHA) -> tuple[float, float]:
    centre = (k + z * z / 2) / (n + z * z)
    half = z * sqrt(k * (n - k) / n + z * z / 4) / (n + z * z)
    return max(0.0, centre - half), min(1.0, centre + half)


def binom_two_sided(k: int, n: int, p: float = 0.5) -> float:
    """Exact two-sided binomial test: total probability of outcomes no more likely than the observed one."""
    probs = [comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(n + 1)]
    return min(1.0, sum(q for q in probs if q <= probs[k] * (1 + 1e-9)))


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Fisher's exact test on [[a, b], [c, d]], two-sided by the same rule as binom_two_sided."""
    row1, col1, n = a + b, a + c, a + b + c + d
    denom = comb(n, col1)
    probs = {x: comb(row1, x) * comb(n - row1, col1 - x) / denom for x in range(max(0, col1 - (n - row1)), min(row1, col1) + 1)}
    return min(1.0, sum(q for q in probs.values() if q <= probs[a] * (1 + 1e-9)))


def n_two_proportions(p1: float, p2: float) -> int:
    """Per-group n to detect p1 vs p2 (two-sided ALPHA, POWER), normal approximation without continuity correction."""
    pbar = (p1 + p2) / 2
    num = Z_ALPHA * sqrt(2 * pbar * (1 - pbar)) + Z_POWER * sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return ceil(num ** 2 / (p1 - p2) ** 2)


def n_one_proportion(p0: float, p1: float) -> int:
    num = Z_ALPHA * sqrt(p0 * (1 - p0)) + Z_POWER * sqrt(p1 * (1 - p1))
    return ceil(num ** 2 / (p1 - p0) ** 2)


def n_for_half_width(p: float, half_width: float) -> int:
    return ceil(Z_ALPHA ** 2 * p * (1 - p) / half_width ** 2)


def mde_two_proportions(p: float, n_per_group: int) -> float | None:
    """Smallest upward move detectable with n_per_group per period, to 0.1pp; None if not even to 100%."""
    for step in range(1, 1001):
        d = step / 1000
        if p + d >= 1:
            return None
        if n_two_proportions(p, p + d) <= n_per_group:
            return d
    return None


def duplicate_hire_applications(frames: dict[str, pd.DataFrame]) -> set:
    """Applications repeating a (candidate, opening) the candidate was already hired into. The earliest is kept."""
    apps = frames["Applications"]
    hired = apps[apps["Stage"] == "Hired"].sort_values(["Applied On", "Application ID"])
    return set(hired.loc[hired.duplicated(["Candidate", "Opening"]), "id"])


def view_applications(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    cands = frames["Candidates"].set_index("id")["Source"]
    apps = frames["Applications"]
    return apps[~apps["id"].isin(duplicate_hire_applications(frames))].assign(
        source=lambda d: d["Candidate"].map(cands).astype(object),
        referred=lambda d: d["Referred By"].notna().astype(bool),
        hired=lambda d: (d["Stage"] == "Hired").astype(bool),
    )


def _per_month(dates: pd.Series, as_of: pd.Timestamp, months: int) -> float:
    start = as_of - pd.DateOffset(months=months)
    return float(((dates > start) & (dates <= as_of)).sum()) / months


def _pct(x: float | None) -> float | None:
    return None if x is None else round(100 * x, 2)


def channel_shares(frames: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Share of hires per channel with 95% intervals, and whether first and second place separate."""
    a = view_applications(frames)
    hires = a[a["hired"]]
    hires_per_month = _per_month(hires["Closed On"], as_of_date(frames), 12)
    share_rows, separation_rows = [], []
    for name, bucket in BUCKETINGS.items():
        counts = bucket(hires).value_counts().reindex(sorted(set(bucket(a))), fill_value=0)
        counts = counts.sort_values(ascending=False, kind="mergesort")
        n = int(counts.sum())
        ranks = counts.rank(method="min", ascending=False).astype(int)
        for channel, k in counts.items():
            lo, hi = wilson(int(k), n)
            share_rows.append({"bucketing": name, "rank": int(ranks[channel]), "channel": channel, "hires": int(k), "of hires": n,
                               "share %": _pct(k / n), "ci95 low %": _pct(lo), "ci95 high %": _pct(hi), "small_n": n < SMALL_N})
        (first, k1), (second, k2) = list(counts.items())[:2]
        gap = (k1 - k2) / n
        needed = ceil((Z_ALPHA + Z_POWER) ** 2 * ((k1 + k2) / n - gap ** 2) / gap ** 2) if gap > 0 else None
        separation_rows.append({
            "bucketing": name, "first": f"{first} {k1}/{n}", "second": f"{second} {k2}/{n}",
            "exact binomial p (first vs second)": round(binom_two_sided(int(k1), int(k1 + k2)), 4),
            "separable at 0.05": binom_two_sided(int(k1), int(k1 + k2)) < ALPHA,
            "hires needed if these shares held (80% power)": needed,
            "years at current hire volume": round(needed / hires_per_month / 12, 1) if needed else None,
            "current hires per month (trailing 12m)": round(hires_per_month, 2),
        })
    return pd.DataFrame(share_rows), pd.DataFrame(separation_rows)


def volume_and_yield(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Applications, hires and application->hire conversion per channel, on applications old enough to convert."""
    a = view_applications(frames)
    cutoff = as_of_date(frames) - pd.Timedelta(days=int(resolution_times(frames).loc[TIME_TO_HIRE, "max"]))
    matured = a[a["Applied On"] <= cutoff]
    rows = []
    for name, bucket in BUCKETINGS.items():
        channel = bucket(matured)
        jb = JOB_BOARD_CHANNEL[name]
        jb_n, jb_k = int((channel == jb).sum()), int((matured["hired"] & (channel == jb)).sum())
        for ch in channel.value_counts().index:
            n_c, k_c = int((channel == ch).sum()), int((matured["hired"] & (channel == ch)).sum())
            lo_v, hi_v = wilson(n_c, len(matured))
            reportable = n_c >= MIN_N_FOR_RATE
            lo, hi = wilson(k_c, n_c) if reportable else (None, None)
            rows.append({
                "bucketing": name, "channel": ch, "applications": n_c, "share of applications %": _pct(n_c / len(matured)),
                "applications ci95 %": f"{_pct(lo_v)}-{_pct(hi_v)}", "hires": k_c, "share of hires %": _pct(k_c / int(matured['hired'].sum())),
                "conversion": f"{k_c}/{n_c}", "conversion %": _pct(k_c / n_c) if reportable else None,
                "conversion ci95 %": f"{_pct(lo)}-{_pct(hi)}" if reportable else f"not reported: n < {MIN_N_FOR_RATE}",
                "fisher p vs Job Board": round(fisher_two_sided(k_c, n_c - k_c, jb_k, jb_n - jb_k), 4) if reportable and ch != jb else None,
                "small_n": n_c < SMALL_N, "applied on or before": cutoff.date(),
            })
    return pd.DataFrame(rows)


def offer_view(frames: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Acceptance under the defended definition, its sensitivities, the sample size question, and declines."""
    as_of = as_of_date(frames)
    decision_days = int(resolution_times(frames).loc[OFFER_DECISION, "max"])
    apps = frames["Applications"][["id", "Opening", "Rejection Reason"]].rename(columns={"id": "app_id", "Rejection Reason": "app_rejection_reason"})
    openings = frames["Job Openings"][["id", "Status"]].rename(columns={"id": "open_id", "Status": "opening_status"})
    offers = frames["Offers"][~frames["Offers"]["Application"].isin(duplicate_hire_applications(frames))]
    offers = offers.merge(apps, left_on="Application", right_on="app_id", how="left").merge(openings, left_on="Opening", right_on="open_id", how="left")
    cohort = offers[offers["Offered On"] <= as_of - pd.Timedelta(days=decision_days)]
    status = cohort["Status"]
    acc, dec, pend, n = int((status == "Accepted").sum()), int((status == "Declined").sum()), int((status == "Pending").sum()), len(cohort)
    on_hold_pending = int(((status == "Pending") & (cohort["opening_status"] == "On Hold")).sum())

    def row(label: str, k: int, m: int, note: str) -> dict:
        lo, hi = wilson(k, m)
        return {"definition": label, "accepted": k, "offers": m, "rate %": _pct(k / m), "ci95 low %": _pct(lo), "ci95 high %": _pct(hi),
                "small_n": m < SMALL_N, "note": note}

    acceptance = pd.DataFrame([
        row("DEFENDED: accepted / offers past the slowest recorded decision; stale Pending count as not accepted", acc, n,
            f"{pend} Pending, all offered >= {decision_days}d before {as_of.date()}; {len(offers) - n} offers still in flight"),
        row("sensitivity: Pending on On Hold requisitions excluded (company-side pause)", acc, n - on_hold_pending, f"{on_hold_pending} excluded"),
        row("sensitivity: Pending excluded (decided offers only)", acc, acc + dec, f"{pend} excluded"),
        row("bound: every Pending offer was in fact accepted", acc + pend, n, "upper bound"),
        row("reference: VP-reproducing raw count (duplicate hire kept)", int((frames['Offers']['Status'] == 'Accepted').sum()),
            len(frames["Offers"]), "from metrics claim-2 grid"),
    ])

    p = acc / n
    offers_12m, offers_6m = _per_month(offers["Offered On"], as_of, 12), _per_month(offers["Offered On"], as_of, 6)

    def timing(label: str, per_period: int | None, periods: int, note: str) -> dict:
        total = None if per_period is None else per_period * periods
        return {"question": label, "offers per period": per_period, "periods": periods, "offers in total": total,
                "months at trailing-12m volume": None if total is None else round(total / offers_12m, 1),
                "months at trailing-6m volume": None if total is None else round(total / offers_6m, 1), "note": note}

    one_year = int(round(offers_12m * 12))
    mde = mde_two_proportions(p, one_year)
    sample_size = pd.DataFrame([
        timing(f"compare two periods, detect {p:.1%} -> {p + TARGET_MOVE:.1%}", n_two_proportions(p, p + TARGET_MOVE), 2,
               f"two-sided alpha {ALPHA}, power {POWER:.0%}"),
        timing(f"compare two periods, detect {p:.1%} -> {p - TARGET_MOVE:.1%}", n_two_proportions(p, p - TARGET_MOVE), 2,
               f"two-sided alpha {ALPHA}, power {POWER:.0%}"),
        timing(f"one new period against {p:.1%} treated as known, detect +5pp", n_one_proportion(p, p + TARGET_MOVE), 1,
               "optimistic: ignores the uncertainty in the baseline itself"),
        timing("estimate the rate to within +/-5pp (95% interval half-width)", n_for_half_width(p, TARGET_MOVE), 1, "precision, not a test"),
        timing(f"smallest upward move detectable comparing two 12-month periods (~{one_year} offers each)", one_year, 2,
               f"minimum detectable move = {'none below 100%' if mde is None else f'{mde:.1%} ({p:.1%} -> {p + mde:.1%})'}"),
    ])
    sample_size.attrs["rates"] = (offers_12m, offers_6m)

    declined = cohort[status == "Declined"]
    not_accepted = cohort[status != "Accepted"]
    reasons = declined["Decline Reason"].fillna("(no reason recorded)").value_counts()
    declines = pd.DataFrame(
        [{"group": "Declined offers", "reason": r, "offers": int(k)} for r, k in reasons.items()]
        + [{"group": "Stale Pending offers (not accepted under the defended definition)",
            "reason": f"no decline reason; opening {os_}; application rejection reason {rr}", "offers": int(k)}
           for (os_, rr), k in not_accepted[not_accepted["Status"] == "Pending"]
           .assign(rr=lambda d: d["app_rejection_reason"].fillna("none"))
           .groupby(["opening_status", "rr"]).size().items()]
    )
    declines.attrs["summary"] = (f"{len(declined)} declined offers, {int(declined['Decline Reason'].notna().sum())} with a reason; "
                                 f"{len(not_accepted)} offers not accepted in total. Percentages are not reported: n < {MIN_N_FOR_RATE}.")
    return {"acceptance": acceptance, "sample_size": sample_size, "declines": declines}


# ---------------------------------------------------------------- entry point

def pair_summary(df: pd.DataFrame, dims: list[str]) -> pd.DataFrame:
    """Collapse definitions to distinct numerator/denominator pairs, closest first.

    For each pair: how many definitions produce it, how many are all-time, and every value each
    definition dimension takes among them.
    """
    grouped = df.dropna(subset=["pct"]).groupby(["numerator", "denominator"], sort=False)
    out = grouped.agg(
        pct=("pct", "first"), abs_diff_pp=("abs_diff_pp", "first"), reproduces=("reproduces", "first"),
        definitions=("pct", "size"), all_time=("window", lambda w: int((w == "all time").sum())),
    )
    for dim in dims:
        out[dim] = grouped[dim].agg(lambda s: " | ".join(sorted(set(s))))
    out = out.reset_index().sort_values(["abs_diff_pp", "denominator"], ascending=[True, False], kind="mergesort")
    return out.reset_index(drop=True)


def _summarise(name: str, df: pd.DataFrame, target: str, dims: list[str], csv_name: str, top: int = 12) -> None:
    matches = df[df["reproduces"]]
    pairs = pair_summary(df, dims)
    pairs.to_csv(config.EXPLORATION_DIR / csv_name, index=False)
    print(f"\n=== {name} (target {target}) ===")
    print(f"definitions evaluated: {len(df)}; reproducing: {len(matches)} "
          f"(all-time: {int((matches['window'] == 'all time').sum())}); "
          f"distinct numerator/denominator pairs: {len(pairs)}, of which reproducing: {int(pairs['reproduces'].sum())}")
    with pd.option_context("display.width", 250, "display.max_colwidth", 60):
        print(pairs.head(top)[["pct", "numerator", "denominator", "reproduces", "definitions", "all_time"]].to_string())


CLAIM1_DIMS = ["event", "window", "date_basis", "unit", "attribution", "channel"]
CLAIM2_DIMS = ["unit", "numerator_rule", "pending_rule", "rescinded_rule", "date_basis", "window"]


def main() -> int:
    frames = load.load_all()
    config.EXPLORATION_DIR.mkdir(parents=True, exist_ok=True)

    c1 = claim1_table(frames)
    c1.to_csv(config.EXPLORATION_DIR / "claim1_definitions.csv", index=False)
    _summarise("Claim 1: job-board share of hires", c1, "26.9%", CLAIM1_DIMS, "claim1_pairs.csv")

    c2 = claim2_table(frames)
    c2.to_csv(config.EXPLORATION_DIR / "claim2_definitions.csv", index=False)
    _summarise("Claim 2: offer acceptance rate", c2, "~72%", CLAIM2_DIMS, "claim2_pairs.csv")

    as_of, snapshot = as_of_date(frames), snapshot_date()
    times = resolution_times(frames)
    outputs = {
        "time_monthly_volume.csv": monthly_volume(frames),
        "time_resolution_times.csv": times.reset_index(),
        "time_unresolved_offers.csv": unresolved_offers(frames, as_of, snapshot),
        "time_offer_cohorts.csv": offer_cohorts(frames, as_of, times),
        "time_application_tail.csv": application_tail(frames, as_of, times),
        "time_channel_hire_rates.csv": channel_hire_rates(frames, as_of, times),
    }
    print(f"\n=== Time coverage (as-of {as_of.date()} = latest Applied On; snapshot {snapshot.date()}) ===")
    with pd.option_context("display.width", 250, "display.max_colwidth", 80, "display.max_columns", 20):
        for name, df in outputs.items():
            df.to_csv(config.EXPLORATION_DIR / name, index=False)
            print(f"\n-- {name} --")
            print(df.to_string(index=False))

    shares, separation = channel_shares(frames)
    offer = offer_view(frames)
    view = {
        "view_claim1_channel_shares.csv": shares, "view_claim1_first_vs_second.csv": separation,
        "view_claim1_volume_yield.csv": volume_and_yield(frames), "view_claim2_acceptance.csv": offer["acceptance"],
        "view_claim2_sample_size.csv": offer["sample_size"], "view_claim2_declines.csv": offer["declines"],
    }
    print(f"\n=== Our view (duplicate hire applications dropped: {sorted(duplicate_hire_applications(frames))}) ===")
    print("offers per month, trailing 12m / 6m: %.2f / %.2f" % offer["sample_size"].attrs["rates"])
    print(offer["declines"].attrs["summary"])
    with pd.option_context("display.width", 280, "display.max_colwidth", 110, "display.max_columns", 20):
        for name, df in view.items():
            df.to_csv(config.EXPLORATION_DIR / name, index=False)
            print(f"\n-- {name} --")
            print(df.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
