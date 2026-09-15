# D3 evidence: what the offer acceptance definition must resolve

Confidence labels are from `deliverables/findings.csv`. Cite = the file under `outputs/tables/` holding the number. UNCITED = no file under `outputs/tables/` holds it; the mark says whether it is arithmetic on cited numbers or computed from data/raw, and gives the derivation.

Baseline: 26/36 = 72.22% (all offer records, Status = Accepted, Pending counted as not accepted, all time).

| Item | Affected records | Resolution | 26/36 becomes | Cite |
|---|---|---|---|---|
| Pending treatment | 5 of 36 | Pending counted as not accepted | 26/36 = 72.22% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_4_categorical_hygiene.csv` |
| Pending treatment | 5 of 36 | Pending excluded | 26/31 = 83.87% | `outputs/tables/exploration/claim2_definitions.csv` |
| Pending treatment | 5 of 36 | Pending counted as accepted | 31/36 = 86.11% | `outputs/tables/exploration/claim2_definitions.csv` |
| No Rescinded status | 0 of 36 ('Accepted' 26, 'Pending' 5, 'Declined' 5) | proxy: offer on a Cancelled opening, excluded | 22/30 = 73.33% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_4_categorical_hygiene.csv` |
| No Rescinded status | 6 offers on Cancelled openings | proxy: offer on a Cancelled opening, not accepted | 22/36 = 61.11% | UNCITED, arithmetic on cited numbers: affected count 6 = 36 − 30, from the excluded row (inputs: `outputs/tables/exploration/claim2_definitions.csv`) |
| No Rescinded status | 3 offers on applications with a Rejection Reason | proxy: application Rejection Reason, excluded | 24/33 = 72.73% | UNCITED, arithmetic on cited numbers: affected count 3 = 36 − 33 (inputs: `outputs/tables/exploration/claim2_definitions.csv`) |
| No Rescinded status | 3 offers on applications with a Rejection Reason | proxy: application Rejection Reason, not accepted | 24/36 = 66.67% | `outputs/tables/exploration/claim2_definitions.csv` |

| Item | Affected records | Resolution | 26/36 becomes | Cite |
|---|---|---|---|---|
| Counting unit | 36 in denominator | offer records | 26/36 = 72.22% | `outputs/tables/exploration/claim2_definitions.csv` |
| Counting unit | 32 in denominator | candidates: accepted if any offer accepted | 24/32 = 75.00% | `outputs/tables/exploration/claim2_definitions.csv` |
| Counting unit | 32 in denominator | candidates: outcome of latest offer (Offered On) | 22/32 = 68.75% | `outputs/tables/exploration/claim2_definitions.csv` |
| Counting unit | 31 in denominator | persons (name+phone): accepted if any offer accepted | 24/31 = 77.42% | `outputs/tables/exploration/claim2_definitions.csv` |
| Counting unit | 18 in denominator | requisitions: share with >=1 accepted offer | 16/18 = 88.89% | `outputs/tables/exploration/claim2_definitions.csv` |
| Counting unit | 18 in denominator | requisitions: mean of per-requisition rates | 13.25/18 = 73.61% | `outputs/tables/exploration/claim2_definitions.csv` |

| Item | Affected records | Resolution | 26/36 becomes | Cite |
|---|---|---|---|---|
| Pending with a decision date | 4 of 36 | counted as accepted | 30/36 (+11.11pp from 26/36) | `outputs/tables/audit/audit_summary.csv` |
| Pending with a decision date | 4 of 36 | counted as declined | 26/36 = 72.22% | UNCITED, arithmetic on cited numbers: already not accepted in the baseline; unchanged |
| Pending with a decision date | 4 of 36 | excluded | 26/32 = 81.25% | UNCITED, arithmetic on cited numbers: 26 accepted / (36 − 4) |
| Pending with a decision date | 4 of 36 | counted as not accepted, other Pending excluded | 26/35 = 74.29% | `outputs/tables/exploration/claim2_definitions.csv` |
| Pending on On Hold or Cancelled openings | 2 of 36 | counted as declined | 26/36 = 72.22% | UNCITED, arithmetic on cited numbers: already not accepted in the baseline; unchanged (decided basis 26/31 -> 26/33 is in audit_summary.csv) (inputs: `outputs/tables/audit/audit_summary.csv`) |
| Pending on On Hold or Cancelled openings | 2 of 36 | excluded | 26/34 = 76.47% | UNCITED, arithmetic on cited numbers: 26 accepted / (36 − 2) |

| Item | Affected records | Resolution | 26/36 becomes | Cite |
|---|---|---|---|---|
| Cohort date | 1 offer without Decision On | Offers.Offered On, trailing 12m to 2026-08-27 | 26/36 = 72.22% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Decision On, trailing 12m to 2026-08-27 | 26/35 = 74.29% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Offered On, trailing 6m to 2026-08-27 | 16/24 = 66.67% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Decision On, trailing 6m to 2026-08-27 | 16/23 = 69.57% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Offered On, trailing 3m to 2026-08-27 | 12/16 = 75.00% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Decision On, trailing 3m to 2026-08-27 | 12/17 = 70.59% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Offered On, calendar 2025 | 7/8 = 87.50% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Decision On, calendar 2025 | 6/6 = 100.00% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Offered On, 2026 YTD to 2026-09-14 | 19/28 = 67.86% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |
| Cohort date | 1 offer without Decision On | Offers.Decision On, 2026 YTD to 2026-09-14 | 20/29 = 68.97% | `outputs/tables/exploration/claim2_definitions.csv`, `outputs/tables/audit/audit_summary.csv` |

| Item | Value | n | Cite |
|---|---|---|---|
| Decision time, min (days) | 2 | 31 | `outputs/tables/claim2_slowest_offer_decision.csv` |
| Decision time, median (days) | 10 | 31 | `outputs/tables/claim2_slowest_offer_decision.csv` |
| Decision time, p90 (days) | 17 | 31 | `outputs/tables/claim2_slowest_offer_decision.csv` |
| Decision time, max (days) | 20 | 31 | `outputs/tables/claim2_slowest_offer_decision.csv` |
| Offers extended at least 20 days before 2026-08-27 | 36 | 36 | `outputs/tables/exploration/time_offer_cohorts.csv` |
| Acceptance in that cohort | 26/36 | 36 | `outputs/tables/exploration/time_offer_cohorts.csv` |

| Item | Affected records | Resolution | 26/36 becomes | Cite |
|---|---|---|---|---|
| Rejection Reason on a non-rejected application | 4 of 350 applications, 3 with offers | the reason is right: offers Declined, hires removed | 24/36 (-5.56pp from 26/36) | UNCITED, arithmetic on cited numbers: 'with offers' count = rule 6.9 rows carrying an offer_status in the cited evidence file (inputs: `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv`) |
| Rejection Reason on a non-rejected application | 4 of 350 | the reason is wrong | 26/36 = 72.22% | UNCITED, arithmetic on cited numbers: baseline unchanged |
