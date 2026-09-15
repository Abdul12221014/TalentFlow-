"""Zero-dependency check: recompute the four headline offer and hire fractions from the committed snapshot.

Standard library only (json, os, sys). Runs on Python 3.8 or later with nothing installed:

    python3 verify.py

Exits 0 when all four fractions match the submission, 1 otherwise.
"""
import json
import os
import sys

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")


def load(name):
    with open(os.path.join(RAW, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def link(record, field):
    """First linked record id, or None. Airtable link fields are lists of ids; empty fields are omitted."""
    ids = record["fields"].get(field) or []
    return ids[0] if ids else None


def day_number(iso_date):
    """Days since a fixed epoch for a YYYY-MM-DD string (proleptic Gregorian), without the datetime module."""
    y, m, d = int(iso_date[0:4]), int(iso_date[5:7]), int(iso_date[8:10])
    y -= m <= 2
    era = y // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe


def show(k, n, expected, definition):
    ok = (k, n) == expected
    print("%d/%d = %.2f%%  [%s]" % (k, n, 100.0 * k / n, "match" if ok else "MISMATCH, expected %d/%d" % expected))
    print("    " + definition)
    return ok


def main():
    applications, candidates, offers = load("applications"), load("candidates"), load("offers")
    source = {c["id"]: c["fields"].get("Source") for c in candidates}
    results = []

    # 1. The VP's 26.9%: job-board share of hired applications, all dates, duplicate hire kept.
    hired = [a for a in applications if a["fields"].get("Stage") == "Hired"]
    job_board = sum(1 for a in hired if source.get(link(a, "Candidate")) == "Job Board")
    results.append(show(job_board, len(hired), (7, 26),
        "Job-board share of hires, as the VP counted it: Applications with Stage = Hired, all dates, duplicate hire kept; "
        "channel = the linked candidate's Source."))

    # 2. The VP's ~72%: accepted over all offer records.
    status = [o["fields"].get("Status") for o in offers]
    accepted, declined = status.count("Accepted"), status.count("Declined")
    results.append(show(accepted, len(offers), (26, 36),
        "Offer acceptance, as the VP counted it: Offers with Status = Accepted over all offer records; Pending counts as not accepted."))

    # 3. Decided offers only.
    results.append(show(accepted, accepted + declined, (26, 31),
        "Offer acceptance on decided offers only: Accepted over Accepted + Declined; Pending offers excluded."))

    # 4. Defended rate.
    # Duplicate hire: a Stage = Hired application repeating a (candidate, opening) already hired, ordered by Applied On then Application ID.
    seen, duplicate_apps = set(), set()
    for a in sorted(hired, key=lambda a: (a["fields"].get("Applied On", ""), a["fields"].get("Application ID", ""))):
        key = (link(a, "Candidate"), link(a, "Opening"))
        if key in seen:
            duplicate_apps.add(a["id"])
        seen.add(key)
    # As-of date: the latest Applied On. Maturity: the slowest recorded decision (Offered On -> Decision On, Accepted or Declined).
    as_of = max(a["fields"]["Applied On"] for a in applications if a["fields"].get("Applied On"))
    slowest = max(day_number(o["fields"]["Decision On"]) - day_number(o["fields"]["Offered On"])
                  for o in offers
                  if o["fields"].get("Status") in ("Accepted", "Declined") and o["fields"].get("Decision On") and o["fields"].get("Offered On"))
    cohort = [o for o in offers
              if link(o, "Application") not in duplicate_apps
              and day_number(o["fields"]["Offered On"]) <= day_number(as_of) - slowest]
    cohort_accepted = sum(1 for o in cohort if o["fields"].get("Status") == "Accepted")
    results.append(show(cohort_accepted, len(cohort), (25, 35),
        "Defended offer acceptance: offers made at least %d days (the slowest recorded decision) before %s (the latest Applied On), "
        "dropping the %d offer(s) on duplicate hire records; Accepted over all, stale Pending counted as not accepted."
        % (slowest, as_of, sum(1 for o in offers if link(o, "Application") in duplicate_apps))))

    print("all four match" if all(results) else "at least one MISMATCH")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
