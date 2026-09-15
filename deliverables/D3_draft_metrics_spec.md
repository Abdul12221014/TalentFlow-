# D3 draft: offer acceptance rate specification

Draft for the PM's rewrite. Every threshold except the revision window, which is a policy choice (section 2), is derived from the committed snapshot (pulled 2026-09-14T18:07:35Z, as-of date 2026-08-27). File names in backticks are under `outputs/tables/`. An arithmetic step is shown inline where no file holds the result.

## 1. Metric

- **Name:** offer acceptance rate.
- **Owner:** TalentFlow product, recruiting analytics.
- **Source data:** the customer's Offers, Applications and Job Openings tables.
- **Question answered:** of the offers a customer extended that have had time to be decided, what share did candidates accept?

## 2. Thresholds and their derivations

| Symbol | Value on this snapshot | Derivation | Source |
|---|---|---|---|
| T, decision timeout | 20 days | The largest Decision On − Offered On, in days, among Accepted and Declined offers (n = 31; min 2, median 10, p90 17, max 20). | `claim2_slowest_offer_decision.csv` |
| N_report, reporting floor | 314 decided offers | The sample for a 95% interval of ±5 points: n = z_0.975² × p(1 − p) / 0.05² = 3.841459 × 0.204082 / 0.0025 = 313.59, rounded up, with p = 25/35. | `claim2_offers_needed_for_5pt_move.csv` |
| N_compare, comparison floor | 1,210 decided offers per period | Two-proportion sample size for 71.43% → 76.43%, two-sided alpha 0.05, power 80%, pooled variance in the alpha term, unpooled in the power term, no continuity correction: 1,209.07 before rounding up. | `claim2_sample_size_derivation.csv` |

- **Recomputing T:** at every publication, from all Accepted and Declined offers in the customer's history.
- **When T grows:** earlier published cohorts are not recomputed. A longer T changes the waiting rule and no recorded fact about any offer. A Rescinded status (section 7) is different: it records a fact that changes the offer's own state, so a cohort published before it counted a company withdrawal as a candidate decision, and that cohort is recomputed.
  - T growth cannot demature a published month.
  - T applies when a cohort is assessed for maturity at a publication. Once published, a month stays published at the T in force at that publication.
  - The T used is recorded alongside each published cohort.
- **When an offer's recorded status changes after publication:** the principle in the previous bullet decides this case, and no new rule is added. A Lapsed offer that later becomes Accepted changes a recorded fact about the offer. It falls on the Rescinded side of the line, not the T-growth side, so the published value of the cohort that contains it is restated, within the revision window below, for that offer and for every other offer on its pair whose section 3 state changes.
- **Scope of recomputation:** these are different rules for different scopes.
  - A schema change, such as adding Rescinded to Offers.Status, recomputes every published cohort regardless of the revision window, because the metric definition changed. The recomputation works from each offer's recorded state history, not from current records. An offer already carrying a dated adjustment keeps it and is not re-absorbed, because re-absorbing it would count the correction twice.
  - A status change to one offer respects the revision window of each offer it moves, because only the records of that offer's pair changed.
- **Restatement rewrites the changed offer and every other offer on the pair whose section 3 state changes, never the month:** the stated record is the pair, not the single offer.
  - Section 3 already defines a pair's state across all its offers, so a correction to one offer is a correction to the pair, and adjusting only the touched offer leaves the pair in a state section 3 does not permit.
  - Each moved offer gets its own dated delta attached to its own cohort, with the prior value retained. That delta is a restatement of the cohort's published value while the offer is within its revision window, and an adjustment line once the offer is past it.
  - No offer outside the pair is touched, and no month is recounted.
  - The freeze exists so a published number changes only for a stated reason attached to a stated record, and a recount changes numbers for records nobody touched.
- **Restatement is never silent:** the prior published value is kept and the restatement is dated, so a number that moved can be explained. The restated cohort displays the prior published value and the revision date next to the restated value.
- **After the revision window closes:** a correction to an offer does not restate its cohort.
  - Each moved offer stays in its Offered On cohort permanently, so the cohort rule in section 6 is never violated.
  - The correction never changes a closed month's published value, because that month is frozen. For the changed offer and every other offer on the pair whose section 3 state changes, it appears once per offer, as a dated adjustment line issued at the next publication and attached to that offer's own cohort, and each closed cohort keeps its prior published value. No double count is possible.
  - No offer is reassigned to a different month. Reassignment would rewrite history silently, which is what the audit trail exists to prevent.
- **Adjustment lines carry signed deltas:** a line carries the change, such as Accepted +1 and Lapsed −1, never the offer's new state.
  - An adjustment line is published in a window only if that window also contains the cohort it adjusts, because a delta without its original is incoherent. If the window has moved past that month, the line is suppressed from the window total, and the adjustment appears in the cohort-level record alone.
  - Consequences: a Lapsed total cannot go negative, and a numerator cannot include an offer its denominator does not.
  - Intent: a trailing window that no longer contains January is not moved by a January correction, and the correction stays visible on January's cohort with its date.
- **Revision window: 90 days. This is a POLICY CHOICE, not a derivation.** A correction restates the published value of a moved offer's cohort only when the correction is recorded within 90 days of that offer's Offered On.
  - No correction latency is observable in this data, because the snapshot contains no observed correction.
  - 90 days is 4.5 times the slowest observed decision of 20 days across 31 Accepted and Declined offers (`claim2_slowest_offer_decision.csv`), and it closes a month's cohort before the third following month publishes, giving a correction at least two publication cycles to arrive.
  - The window is revisited once real corrections exist to measure.
  - The window is a policy constant and is not recomputed at each publication, unlike T, which is estimated from observed decision times.
- **Window totals:** a window total is the sum of the published values of the cohorts in the window plus the adjustment lines attached to those cohorts, never a fresh count over current records. This section governs window totals, and sections 4 to 6 defer to it.
  - If the window recounted current state at each publication, every closed cohort would be silently mutable and the audit trail would be decorative, so the freeze has to bind the window totals or it means nothing.
  - Consequence: a window total is a sum of cohorts assessed under possibly different T values. That is the cost of a stable published series, and it is accepted deliberately, not overlooked.
- **p for N_report and N_compare:** the most recently published rate. Before any rate has been published, p is the pooled rate over all decided offers in the customer's history.
- **Direction of N_compare:** it uses a 5-point rise, because the customer's goal is a higher rate. The same calculation for a 5-point fall gives 1,344 per period (`claim2_offers_needed_for_5pt_move.csv`); that figure is not used.

## 3. Unit of analysis

- **The unit is one final offer per (candidate record, requisition) pair.**
  - The pair comes from Offers.Application → Applications.Candidate and Applications.Opening.
  - A pair with one offer: that offer is final.
  - A pair with more than one offer and at least one Accepted: the Accepted offer with the earliest Offered On is final.
  - A pair with more than one offer and none Accepted: the offer with the latest Offered On is final.
  - Ties on Offered On go to the lowest Offer ID for Accepted offers and the highest Offer ID otherwise.
  - Every other offer on the pair is Superseded.
- **A candidate with offers on two requisitions contributes two units.** This snapshot has 35 pairs from 32 candidates (`populations.csv`, `exploration/claim2_definitions.csv`).
- **Candidate records are not merged on name or phone.** Rule R3.2 finds 12 of 300 candidate records sharing a name and phone. Candidates.Email is on example.com for 300 of 300 records (`audit/audit_summary.csv`, `both_placeholder_contact_data.csv`).
- **Units rejected, measured on the baseline 26/36 = 72.22% (offer records, Pending as not accepted, all time):**

  | Unit | Result |
  |---|---|
  | Candidates, accepted if any offer was accepted | 24/32 = 75.00% |
  | Candidates, outcome of the latest offer | 22/32 = 68.75% |
  | Persons (name and phone), accepted if any offer was accepted | 24/31 = 77.42% |
  | Requisitions with at least one accepted offer | 16/18 = 88.89% |
  | Mean of per-requisition rates | 13.25/18 = 73.61% |

  Source: `exploration/claim2_definitions.csv`.
- **Why requisition units are rejected:** they measure whether a requisition was filled, not how candidates responded.
- **Why candidate units are rejected:** they collapse a candidate's offers on different requisitions into one outcome.

## 4. State of each offer

Assign exactly one state to every offer, testing the conditions in this order:

| Order | State | Condition | Numerator | Denominator |
|---|---|---|---|---|
| 1 | Superseded | Not the final offer for its pair (section 3) | no | no |
| 2 | Rescinded | Status = Rescinded, once that status exists | no | no |
| 3 | Accepted | Status = Accepted | yes | yes |
| 4 | Declined | Status = Declined | no | yes |
| 5 | Lapsed, status conflict | Status = Pending and Decision On is filled | no | yes |
| 6 | Lapsed, timed out | Status = Pending, Decision On empty, and the publication date minus Offered On is at least T days | no | yes |
| 7 | Open | Status = Pending, Decision On empty, and the publication date minus Offered On is below T days | no | no |

For a published cohort, section 2 governs:
- its states change only by restatement within the revision window or by a schema-change recomputation;
- T in states 6 and 7 is the value recorded with that cohort.

## 5. Numerator and denominator

- **Numerator:** offers in state Accepted in the reported window.
- **Denominator:** offers in states Accepted, Declined and Lapsed in the reported window. These are the decided offers.
- **Window totals:** the numerator, the denominator and every count in sections 9 and 11 are summed from the published values of the cohorts in the window plus the adjustment lines attached to those cohorts, as section 2 states. They are never counted afresh over current records.
- **Rate:** numerator ÷ denominator, published as a percentage with n only when the denominator is at least N_report.
- **Interval:** the 95% Wilson interval for numerator ÷ denominator is published at every volume with at least one decided offer, as its lower and upper bounds, above and below N_report (section 9).

## 6. Time window and cohort rule

- **Cohort:** an offer belongs to the calendar month of its Offered On.
- **Why Offered On, not Decision On:** Decision On is empty on 1 of 36 offers (rule R1.1.Offers.Decision On, `audit/audit_summary.csv`), and a decision-date cohort drops it.
  - Over the trailing 12 months to 2026-08-27, an Offered On cohort gives 26/36 = 72.22% and a Decision On cohort gives 26/35 = 74.29% (`exploration/claim2_definitions.csv`).
  - Offered On is filled on 36 of 36 offers (`audit/audit_1_coverage.csv`).
- **Maturity:** a cohort month is mature when the publication date is at least T days after its last day. With T = 20, the cohort for August publishes on 20 September. An immature month is left out of the window. T is the value in force at the publication where the month is assessed. Once published, a month is never dematured by a later change in T (section 2).
- **Why the lag is T and not the median:** the median decision took 10 days and the slowest took 20 (`claim2_slowest_offer_decision.csv`). A month read at 10 days still has offers that the observed data says can be decided later.
- **Reported window:** start from the most recent mature month and add earlier whole months, one at a time, until the denominator reaches N_report. If all mature months together stay below N_report, no rate is reported as a percentage, and the window is all mature months.
  - That is the same window the rate would have used had it reached 314.
  - The four raw counts and the interval of section 9 cover all mature months.
  - The latest mature month on its own is never the window.
- **Comparison window:** a change is reported only between two non-overlapping windows that each hold at least N_compare decided offers.

## 7. Exclusions

| Excluded | Rule | Reason | Effect on this snapshot |
|---|---|---|---|
| Superseded offers | Out of numerator and denominator | A pair has one outcome, and its earlier offers would count it twice. | 1 offer, OFF-00035 on duplicate hire record APP-00335: 26/36 → 25/35 (`populations.csv`, `claim1_duplicate_hire_records.csv`) |
| Rescinded offers | Out of numerator and denominator; count displayed | The company withdrew the offer, so the candidate made no decision. | 0: Offers.Status holds Accepted 26, Pending 5, Declined 5 and no other value (`audit/audit_4_categorical_hygiene.csv`) |
| Open offers | Out of numerator and denominator; count displayed | The candidate can still decide. | 0: every Pending offer was at least 20 days old on 2026-08-27 (`claim2_pending_offers.csv`) |

- **Rescission is not inferred.** A Cancelled requisition does not mark an offer as rescinded. Neither does a Rejection Reason on the application.
  - With Pending counted as not accepted, those four proxy rules give results from 22/36 = 61.11% to 22/30 = 73.33% (`exploration/claim2_definitions.csv`).
- **When Rescinded is added to Offers.Status:** state 2 applies from the next publication, and every published cohort is recomputed and republished, regardless of the revision window (section 2). The recomputation works from each offer's recorded state history, not from current records, and an offer already carrying a dated adjustment keeps it and is not re-absorbed.

## 8. Edge cases

Each alternative is measured on the baseline 26/36 = 72.22%, so its effect can be read against the VP's figure. This spec gives 25/35 on the same data (section 12).

| Case | Records on this snapshot | Rule in this spec | Rejected alternative and its result |
|---|---|---|---|
| Pending with a Decision On | 4 of 36 offers: OFF-00002, OFF-00007, OFF-00013, OFF-00020 (rule R6.6, `audit/audit_6_state_machine_contradictions.csv`) | Lapsed, status conflict: not accepted, flagged. Their applications are not at Stage Hired, because an application holds at most one offer (R3.6 PASS) and every Hired application has an Accepted offer (R6.4 PASS). | Counted as accepted: 30/36 = 83.33% (`audit/audit_summary.csv`). Excluded: 26/(36 − 4) = 26/32 = 81.25%. |
| Pending with no Decision On, at least T days old | 1 of 36: OFF-00021, 117 days old (`claim2_pending_offers.csv`) | Lapsed, timed out: not accepted. | Excluded: 26/35 = 74.29% (`exploration/claim2_definitions.csv`). |
| Pending on an On Hold or Cancelled requisition | 2 of 36: OFF-00013 and OFF-00020, both On Hold (rule R6.14, `audit/audit_6_state_machine_contradictions.csv`) | Section 4 applies unchanged; both are Lapsed here. The dashboard displays their count separately. | Excluded: 26/(36 − 2) = 26/34 = 76.47%; on this spec's base, 25/33 (`populations.csv`). |
| Accepted offer on a Cancelled or On Hold requisition | 4 of 26 accepted offers, all on Cancelled requisitions (rule R6.13, `audit/audit_6_state_machine_contradictions.csv`) | Accepted. Offers.Status decides the state. | Excluded: 22/32 = 68.75% (`audit/audit_summary.csv`). |
| Rejection Reason on an application that is not Rejected or Withdrawn | 4 of 350 applications, 3 of them with offers (rule R6.9) | Offers.Status decides the state; flagged. | Reason trusted: 24/36 = 66.67% (`audit/audit_summary.csv`). |
| Re-negotiated offer on the same application | 0: no application holds more than one offer (rule R3.6 PASS) | Section 3: the final offer counts, the rest are Superseded. | Every offer counted: no change on this snapshot. |
| Two applications for the same pair, both hired | 1 pair: APP-00035 kept, APP-00335 dropped (`claim1_duplicate_hire_records.csv`); OFF-00035 superseded (`populations.csv`) | Section 3: the earliest Accepted offer is final. | Both counted: 26/36 = 72.22%, against 25/35 under this rule. |
| Internal candidate | Not identifiable: no Candidates or Applications field marks an employee, and none of the 18 Candidates.Current Company values names the customer (`audit/audit_4_categorical_hygiene.csv`) | Every offer is counted. Internal status is not inferred by matching Candidates to People: Candidates.Email is on example.com for 300 of 300 records and People.Work Email for 14 of 14 (`both_placeholder_contact_data.csv`). When an internal flag is added, internal offers get their own rate under this spec and are removed from the external rate. | None on this snapshot. |
| Offered On empty | 0 of 36 (`audit/audit_1_coverage.csv`) | Out of numerator and denominator; flagged. | None on this snapshot. |
| Decision On earlier than Offered On | 0 (rule R5.12 PASS) | State as section 4 assigns it; flagged. | None on this snapshot. |
| Offer with no linked application | 0 (rule R2.3 PASS) | Out of numerator and denominator; flagged. | None on this snapshot. |

## 9. Minimum n

The reporting floor is N_report = 314 decided offers, derived in section 2 as z_0.975² × p(1 − p) / 0.05² = 3.841459 × 0.204082 / 0.0025 = 313.59, rounded up, with p = 25/35. A window below the floor has no rate published as a percentage. The dashboard publishes, for that window, four raw counts:
- accepted;
- declined;
- pending, meaning final offers with Status = Pending, which are states Lapsed and Open;
- total decided, meaning Accepted + Declined + Lapsed.

It also publishes the full 95% Wilson interval for accepted ÷ total decided, as its lower and upper bounds, and the decline-reason breakdown with its n stated. With zero decided offers no interval is published, because the Wilson interval is undefined at n = 0; the tile shows the four counts, all zero, and the text "no decisions recorded". The breakdown carries the note "n = {declined}: this breakdown cannot rank causes". On this snapshot the dashboard publishes:
- 25 accepted, 5 declined, 5 pending and 35 total decided;
- the interval 54.95%–83.67% for 25/35;
- decline reasons Counter Offer 3, Location 1 and Compensation 1, with the note "n = 5: this breakdown cannot rank causes".

Sources: `claim2_offer_acceptance.csv`, `claim2_pending_offers.csv`, `claim2_declines_by_reason.csv`.

**Change:** no change figure is displayed unless both windows hold at least N_compare decided offers (1,210 each on this snapshot).

## 10. Volume constraint

- **Scale-free figures:** N_report = 314 and N_compare = 1,210 offers per period.
  - They depend on the rate and the 5-point move.
  - They do not depend on how many offers a customer makes.
- **Calendar-time figures depend on this base's volume** of 2.92 offers a month over the trailing 12 months (`claim2_offer_volume.csv`). They are illustrations, not properties of the metric.
  - 314 offers take 107.7 months.
  - 1,210 offers per period take 829.7 months for both periods, about 415 months per period. At ten times this volume, one period takes about 3.5 years.

  Source: `claim2_offers_needed_for_5pt_move.csv`.
- **The metric is fit for:**
  - counts of offers by state for each cohort month;
  - counts of Lapsed offers and status conflicts, as a record-keeping check;
  - a pooled rate once a window holds 314 decided offers.
- **The metric is not fit for:**
  - detecting a 5-point change for a customer with fewer than 1,210 decided offers per period;
  - month-over-month change;
  - attributing a change to a product intervention at this base's volume.

## 11. Dashboard display

| Situation | Displayed |
|---|---|
| Window at or above N_report | Rate as a percentage, its 95% Wilson interval and n, then the state counts. |
| Window below N_report | "Not enough decided offers for a rate: {denominator} of {N_report}". No rate as a percentage. The four raw counts from section 9: accepted, declined, pending and total decided. The 95% Wilson interval as its lower and upper bounds. The decline-reason breakdown with its n stated and the note "n = {declined}: this breakdown cannot rank causes". Then the state counts. |
| Window with zero decided offers | As the row above, except that no interval is displayed, because the Wilson interval is undefined at n = 0. The four counts are displayed, all zero, with the text "no decisions recorded". |
| Immature cohort months | One line per immature month: "Open until {publication date}", with its count of Open offers. |
| Comparison with either window below N_compare | "Change not measurable: {n_a} and {n_b} decided offers; {N_compare} needed in each." |
| Comparison with both windows at or above N_compare | Both rates with intervals and the difference in points. |

- **State counts displayed:**
  - Accepted.
  - Declined.
  - Lapsed, split into three parts:
    - status conflict;
    - Pending on an On Hold or Cancelled requisition;
    - timed out.
  - Open.
  - Superseded.
  - Rescinded, once the status exists.
- **Record-keeping flags displayed as counts:**
  - status conflicts;
  - Offered On empty;
  - Decision On earlier than Offered On;
  - offers with no linked application.

## 12. Test fixture

Input: the committed snapshot, publication date 2026-08-27, T = 20, N_report = 314.

| Output | Expected |
|---|---|
| Offer records | 36 |
| Superseded | 1 (OFF-00035) |
| Accepted | 25 |
| Declined | 5 |
| Lapsed | 5: 4 status conflicts, 1 timed out (OFF-00021); 2 of the 5 on On Hold requisitions |
| Open | 0 |
| Denominator | 35 |
| Headline displayed | "Not enough decided offers for a rate: 35 of 314" |
| Rate as a percentage | Not displayed, because 35 < 314. The test fails if 71.43% (25/35) appears. |
| Raw counts displayed | 25 accepted, 5 declined, 5 pending, 35 total decided |
| Wilson interval displayed | 54.95%–83.67% for 25/35 |
| Decline reasons displayed | Counter Offer 3, Location 1, Compensation 1; n = 5; note "n = 5: this breakdown cannot rank causes" |

Sources: `populations.csv`, `claim2_offer_acceptance.csv`, `claim2_pending_offers.csv`, `claim2_declines_by_reason.csv`, `audit/audit_6_state_machine_contradictions.csv`.
