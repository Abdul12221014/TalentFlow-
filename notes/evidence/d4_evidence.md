# D4 evidence: data quality

Confidence labels are from `deliverables/findings.csv`. Cite = the file under `outputs/tables/` holding the number. UNCITED = no file under `outputs/tables/` holds it; the mark says whether it is arithmetic on cited numbers or computed from data/raw, and gives the derivation.

## Ratings

| Rating | Rules | Distinct defects | Cite |
|---|---|---|---|
| SYSTEMIC | 0 | 0 | `outputs/tables/audit/audit_summary.csv` |
| HIGH | 12 | 11 | `outputs/tables/audit/audit_summary.csv` |
| MEDIUM | 0 | 0 | `outputs/tables/audit/audit_summary.csv` |
| SCOPE | 8 | 8 | `outputs/tables/audit/audit_summary.csv` |
| LOW | 0 | 0 | `outputs/tables/audit/audit_summary.csv` |
| NONE | 46 | 37 | `outputs/tables/audit/audit_summary.csv` |
| PASS | 83 | 83 | `outputs/tables/audit/audit_summary.csv` |
| NOT TESTABLE | 4 | 4 | `outputs/tables/audit/audit_summary.csv` |

## HIGH: 12 rules, 11 distinct defects

| Rank | Rule | Finding | Count | Table rows | % of table | Largest move (pp) | Yardstick effect | Same defect as | Cite |
|---|---|---|---|---|---|---|---|---|---|
| 1 | R4.5.Candidates.Source | taxonomy overlap, 'LinkedIn' can also count as 'Job Board' (declared): Candidates.Source | 31 | 300 | 10.33% | 11.54 | Job Board share of hires 7/26 -> 10/26 (+11.54pp); top channel 'Job Board = Referral' -> 'Job Board' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_4_categorical_hygiene.csv` |
| 2 | R6.6 | Offer Pending but it carries a Decision On date | 4 | 36 | 11.11% | 11.11 | accepted/all offers 26/36 -> 30/36 (+11.11pp); accepted/decided offers 26/31 -> 30/35 (+1.84pp) |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 3 | R6.19 | Candidate Source is Referral but the application has no Referred By | 10 | 350 | 2.86% | 9.92 | Job Board share of hires 7/26 -> 7/19 (+9.92pp); top channel 'Job Board = Referral' -> 'Job Board' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 4 | R6.9 | Rejection Reason set on an application that is not Rejected/Withdrawn | 4 | 350 | 1.14% | 8.87 | Job Board share of hires 7/26 -> 7/24 (+2.24pp); accepted/all offers 26/36 -> 24/36 (-5.56pp); accepted/decided offers 26/31 -> 24/32 (-8.87pp); top channel 'Job Board = Referral' -> 'Job Board' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 5 | R6.15 | Requisition with more hires than Headcount | 4 | 24 | 16.67% | 6.41 | Job Board share of hires 7/26 -> 7/21 (+6.41pp); accepted/all offers 26/36 -> 21/31 (-4.48pp); accepted/decided offers 26/31 -> 21/26 (-3.10pp); top channel 'Job Board = Referral' -> 'Job Board' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 6 | R6.14 | Offer still Pending on a Cancelled or On Hold requisition | 2 | 36 | 5.56% | 5.08 | accepted/decided offers 26/31 -> 26/33 (-5.08pp) |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 7 | R6.13 | Hire on a Cancelled or On Hold requisition | 4 | 350 | 1.14% | 4.20 | Job Board share of hires 7/26 -> 5/22 (-4.20pp); accepted/all offers 26/36 -> 22/32 (-3.47pp); accepted/decided offers 26/31 -> 22/27 (-2.39pp); top channel 'Job Board = Referral' -> 'Referral' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 8 | R6.18 | Application has Referred By but the candidate's Source is not Referral | 24 | 350 | 6.86% | 3.85 | Job Board share of hires 7/26 -> 6/26 (-3.85pp); top channel 'Job Board = Referral' -> 'Referral' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 9 | R3.2 | Candidates sharing a normalised name + last 10 phone digits | 12 | 300 | 4.00% | 3.85 | Job Board share of hires 7/26 -> 8/26 (+3.85pp); top channel 'Job Board = Referral' -> 'Job Board' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_3_duplicates.csv` |
| 10 | R6.20 | Same person (name + phone) hired more than once | 4 | 350 | 1.14% | 2.24 | Job Board share of hires 7/26 -> 7/24 (+2.24pp); accepted/all offers 26/36 -> 24/34 (-1.63pp); accepted/decided offers 26/31 -> 24/29 (-1.11pp); top channel 'Job Board = Referral' -> 'Job Board' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 11 | R3.3 | Applications sharing (candidate record, opening) | 6 | 350 | 1.71% | 1.08 | Job Board share of hires 7/26 -> 7/25 (+1.08pp); accepted/all offers 26/36 -> 25/35 (-0.79pp); accepted/decided offers 26/31 -> 25/30 (-0.54pp); top channel 'Job Board = Referral' -> 'Job Board' |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_3_duplicates.csv` |
| 12 | R3.4 | Applications sharing (person by name + phone, opening) | 6 | 350 | 1.71% | 1.08 | Job Board share of hires 7/26 -> 7/25 (+1.08pp); accepted/all offers 26/36 -> 25/35 (-0.79pp); accepted/decided offers 26/31 -> 25/30 (-0.54pp); top channel 'Job Board = Referral' -> 'Job Board' | R3.3 | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_3_duplicates.csv` |

## SCOPE: 8 rules

| Rank | Rule | Finding | Count | Table rows | % of table | Yardstick effect | Cite |
|---|---|---|---|---|---|---|---|
| 13 | R8.2.Candidates | Candidates.Email on a reserved placeholder domain | 300 | 300 | 100.00% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 14 | R8.6 | Note says 'Referred internally....' but Source is not Referral and no Referred By exists | 34 | 300 | 11.33% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 15 | R8.9 | Note says the candidate re-applied after an earlier rejection but no earlier rejection exists | 34 | 300 | 11.33% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 16 | R8.7 | Note says 'Sourced from a conference list...' but Source is an inbound channel ['Career Site', 'Job Board'] | 26 | 300 | 8.67% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 17 | R8.2.People | People.Work Email on a reserved placeholder domain | 14 | 14 | 100.00% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 18 | R8.8 | Note says the candidate was consolidated onto one opening but two applications remain | 2 | 300 | 0.67% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 19 | R8.10 | Feedback text contradicts Recommendation (declared FEEDBACK_POLARITY) | 2 | 160 | 1.25% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 20 | R8.11 | Feedback string with no declared polarity (not classified) | 0 | 160 | 0.00% | not scored | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |

## NONE: 46 rules, 37 distinct defects

| Rank | Rule | Finding | Count | Table rows | % of table | Yardstick effect | Same defect as | Cite |
|---|---|---|---|---|---|---|---|---|
| 21 | R8.4 | All 892 records created within 53s (bulk import or seeding) | 892 | 892 | 100.00% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 22 | R1.1.Applications.Referred By | Applications.Referred By is empty | 323 | 350 | 92.29% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 23 | R1.1.Applications.Offered On | Applications.Offered On is empty | 314 | 350 | 89.71% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 24 | R1.1.Applications.Offers | Applications.Offers is empty | 314 | 350 | 89.71% | no yardstick input changes | R1.1.Applications.Offered On | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 25 | R1.1.Applications.Final Interview On | Applications.Final Interview On is empty | 300 | 350 | 85.71% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 26 | R8.5.Candidates.Notes | Candidates.Notes: 237 values drawn from 7 fixed strings | 237 | 300 | 79.00% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 27 | R1.1.Applications.First Interview On | Applications.First Interview On is empty | 207 | 350 | 59.14% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 28 | R1.1.Applications.Interviews | Applications.Interviews is empty | 207 | 350 | 59.14% | no yardstick input changes | R1.1.Applications.First Interview On | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 29 | R8.5.Interviews.Feedback | Interviews.Feedback: 142 values drawn from 12 fixed strings | 142 | 160 | 88.75% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv` |
| 30 | R1.1.Applications.Rejection Reason | Applications.Rejection Reason is empty | 132 | 350 | 37.71% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 31 | R1.1.Applications.Closed On | Applications.Closed On is empty | 105 | 350 | 30.00% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 32 | R5.10 | Application made before its candidate record was created (Candidates.Created On) | 90 | 350 | 25.71% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 33 | R1.1.Applications.Screened On | Applications.Screened On is empty | 71 | 350 | 20.29% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 34 | R1.1.Candidates.Notes | Candidates.Notes is empty | 63 | 300 | 21.00% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 35 | R5.17 | Applications.Final Interview On differs from its latest Interviews.Scheduled On | 44 | 350 | 12.57% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 36 | R1.1.Offers.Decline Reason | Offers.Decline Reason is empty | 31 | 36 | 86.11% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 37 | R1.1.Interviews.Recommendation | Interviews.Recommendation is empty | 18 | 160 | 11.25% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 38 | R1.1.Interviews.Feedback | Interviews.Feedback is empty | 18 | 160 | 11.25% | no yardstick input changes | R1.1.Interviews.Recommendation | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 39 | R1.1.Interviews.Score | Interviews.Score is empty | 18 | 160 | 11.25% | no yardstick input changes | R1.1.Interviews.Recommendation | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 40 | R1.1.Interviews.Completed On | Interviews.Completed On is empty | 18 | 160 | 11.25% | no yardstick input changes | R1.1.Interviews.Recommendation | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 41 | R5.14 | Hire closed before its offer was accepted (Closed On < Offers.Decision On) | 17 | 350 | 4.86% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 42 | R7.6.offer to hire record | Negative duration: offer to hire record (Decision On -> Closed On) | 17 | 350 | 4.86% | no yardstick input changes | R5.14 | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_7_outliers.csv` |
| 43 | R5.16 | Applications.First Interview On differs from its earliest Interviews.Scheduled On | 13 | 350 | 3.71% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 44 | R1.1.People.Reqs as Recruiter | People.Reqs as Recruiter is empty | 10 | 14 | 71.43% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 45 | R1.1.People.Reqs as Hiring Manager | People.Reqs as Hiring Manager is empty | 10 | 14 | 71.43% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 46 | R1.1.People.Applications as Recruiter | People.Applications as Recruiter is empty | 10 | 14 | 71.43% | no yardstick input changes | R1.1.People.Reqs as Recruiter | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 47 | R5.8 | Interview scheduled before its application was made | 9 | 160 | 5.62% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 48 | R6.2 | Requisition Filled/Cancelled but still has Active applications | 9 | 24 | 37.50% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 49 | R1.1.People.Interviews | People.Interviews is empty | 8 | 14 | 57.14% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 50 | R3.5.Applications | Applications.Application ID used by more than one record | 8 | 350 | 2.29% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_3_duplicates.csv` |
| 51 | R7.4 | Offer Base CTC outside its requisition's salary band | 7 | 36 | 19.44% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_7_outliers.csv` |
| 52 | R6.5 | Stage and Status disagree (terminal stage but Active, or open stage but Closed) | 5 | 350 | 1.43% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 53 | R6.17 | Requisition still Open although hires already meet Headcount | 5 | 24 | 20.83% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 54 | R5.9 | Interview completed before it was scheduled | 4 | 160 | 2.50% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 55 | R5.13 | Proposed start date before the offer decision | 4 | 36 | 11.11% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 56 | R6.21 | Interview result fields contradict Outcome (not Completed but scored, or Completed but unscored) | 4 | 160 | 2.50% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 57 | R7.6.interview completion | Negative duration: interview completion (Scheduled On -> Completed On) | 4 | 160 | 2.50% | no yardstick input changes | R5.9 | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_7_outliers.csv` |
| 58 | R7.6.offer to start | Negative duration: offer to start (Decision On -> Proposed Start Date) | 4 | 36 | 11.11% | no yardstick input changes | R5.13 | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_7_outliers.csv` |
| 59 | R7.9 | Candidate Expected CTC below Current CTC | 4 | 300 | 1.33% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_7_outliers.csv` |
| 60 | R5.5.Candidates | Backward-looking date later than the day the record was created (createdTime) (Candidates) | 3 | 300 | 1.00% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 61 | R5.11 | Application made before its requisition opened | 3 | 350 | 0.86% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 62 | R5.18 | Applications.Offered On differs from Offers.Offered On | 3 | 36 | 8.33% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv` |
| 63 | R1.1.People.Referrals Made | People.Referrals Made is empty | 2 | 14 | 14.29% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 64 | R6.16 | Requisition Filled with fewer hires than Headcount | 2 | 24 | 8.33% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| 65 | R1.1.Offers.Decision On | Offers.Decision On is empty | 1 | 36 | 2.78% | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |
| 66 | R1.0.Findings | Findings returned 0 records | 0 | 0 |  | no yardstick input changes |  | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_1_coverage.csv` |

## Method

### Check families

| Check family | Rules | SYSTEMIC | HIGH | MEDIUM | SCOPE | LOW | NONE | PASS | NOT TESTABLE | Cite |
|---|---|---|---|---|---|---|---|---|---|---|
| 1. Coverage | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0 | `outputs/tables/audit/audit_summary.csv` |
| 2. Referential integrity | 31 | 0 | 0 | 0 | 0 | 0 | 0 | 31 | 0 | `outputs/tables/audit/audit_summary.csv` |
| 3. Duplicates | 11 | 0 | 3 | 0 | 0 | 0 | 1 | 6 | 1 | `outputs/tables/audit/audit_summary.csv` |
| 4. Categorical hygiene | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 4 | 0 | `outputs/tables/audit/audit_summary.csv` |
| 5. Temporal logic | 18 | 0 | 0 | 0 | 0 | 0 | 10 | 8 | 0 | `outputs/tables/audit/audit_summary.csv` |
| 6. State-machine contradictions | 23 | 0 | 8 | 0 | 0 | 0 | 5 | 10 | 0 | `outputs/tables/audit/audit_summary.csv` |
| 7. Outliers | 27 | 0 | 0 | 0 | 0 | 0 | 5 | 22 | 0 | `outputs/tables/audit/audit_summary.csv` |
| 8. Test and synthetic records | 16 | 0 | 0 | 0 | 8 | 0 | 3 | 2 | 3 | `outputs/tables/audit/audit_summary.csv` |

### Rating meanings (`src/audit.py` docstring)

| Rating | Meaning | Cite |
|---|---|---|
| SYSTEMIC | undermines every figure and cannot be scenario-tested | `outputs/tables/audit/audit_summary.csv` |
| HIGH | top channel changes, or a yardstick moves >= 5 points | `outputs/tables/audit/audit_summary.csv` |
| MEDIUM | a yardstick moves >= 1 point | `outputs/tables/audit/audit_summary.csv` |
| SCOPE | PM decision: outside the evidence the claims rest on; reason recorded; no scenario scored | `outputs/tables/audit/audit_summary.csv` |
| LOW | a yardstick moves < 1 point | `outputs/tables/audit/audit_summary.csv` |
| NONE | no yardstick input changes | `outputs/tables/audit/audit_summary.csv` |
| PASS | nothing found, on fields that could carry the defect | `outputs/tables/audit/audit_summary.csv` |
| NOT TESTABLE | nothing found, but it inspects placeholder identifiers, so it could not fire | `outputs/tables/audit/audit_summary.csv` |

Yardsticks: Job Board share of hires 7/26, accepted/all offers 26/36, accepted/decided offers 26/31 (`outputs/tables/audit/audit_summary.csv`, materiality column).

## Output defect found in this repository: rule-id parsing

| Fact | Value | Cite |
|---|---|---|
| Audit rules | 153 | `outputs/tables/audit/audit_summary.csv` |
| Audit CSVs with a rule_id column | 6 | `outputs/tables/audit/audit_3_duplicates.csv`, `outputs/tables/audit/audit_5_temporal_logic.csv`, `outputs/tables/audit/audit_6_state_machine_contradictions.csv`, `outputs/tables/audit/audit_7_outliers.csv`, `outputs/tables/audit/audit_8_test_and_synthetic_records.csv`, `outputs/tables/audit/audit_summary.csv` |
| Of those, files whose unprefixed ids are all numeric-looking | audit_6_state_machine_contradictions.csv | `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| Distinct rule ids in that file, as text | 13 | `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| Distinct values after default parsing, unprefixed | 12 | UNCITED, arithmetic on cited numbers: re-derived from the cited file: R prefix stripped, parsed with pandas defaults (inputs: `outputs/tables/audit/audit_6_state_machine_contradictions.csv`) |
| Default dtype, unprefixed | float64 | UNCITED, arithmetic on cited numbers: same re-derivation (inputs: `outputs/tables/audit/audit_6_state_machine_contradictions.csv`) |
| Collision, unprefixed | '6.2' and '6.20' -> 6.2 (9 + 4 rows); tiers 6.2 NONE, 6.20 HIGH | UNCITED, arithmetic on cited numbers: same re-derivation; tiers from audit_summary.csv (inputs: `outputs/tables/audit/audit_6_state_machine_contradictions.csv`, `outputs/tables/audit/audit_summary.csv`) |
| Symptom that exposed it | lookup of rule 6.9 as text matched 0 of 4 rows; the d3 draft read '0 with offers' instead of 3 | UNCITED, recorded in the session transcript: observed in the Stage 3 generator run, 2026-09-15 |
| Fix | R prefix on rule_id and same_defect_as in every audit CSV (src/audit.py RULE_ID_PREFIX) | `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |
| After the fix: default dtype and distinct values | object, 13 | `outputs/tables/audit/audit_6_state_machine_contradictions.csv` |

### NOT TESTABLE: 4 rules

| Rule | Finding | Why it could not fire | Moved when defects were injected into identifier fields | Cite |
|---|---|---|---|---|
| R3.1 | Candidates sharing a normalised email (lower-case, trimmed, +tag removed) | Could not have fired: it inspects placeholder identifiers (Candidates.Email). | True | `outputs/tables/audit/audit_summary.csv` |
| R8.1.Candidates | Test/dummy tokens in Candidates text fields | Could not have fired: it inspects placeholder identifiers (Candidates.Email, Candidates.Full Name); it also inspects Candidates.Current Company, Candidates.Notes, which could have fired and did not. | True | `outputs/tables/audit/audit_summary.csv` |
| R8.1.People | Test/dummy tokens in People text fields | Could not have fired: it inspects placeholder identifiers (People.Full Name, People.Work Email). | True | `outputs/tables/audit/audit_summary.csv` |
| R8.3 | Candidate phone is a placeholder (<=2 distinct digits or a run like 1234567890) | Could not have fired: it inspects placeholder identifiers (Candidates.Phone). | True | `outputs/tables/audit/audit_summary.csv` |

### PASS: 83 rules

| Check family | Rules | Rule ids | Cite |
|---|---|---|---|
| 2. Referential integrity | 31 | R2.1, R2.2, R2.3, R2.4, R2.5, R2.6.Departments, R2.6.People, R2.6.Job Openings, R2.6.Candidates, R2.6.Applications, R2.6.Interviews, R2.6.Offers, R2.7.1, R2.7.2, R2.7.3, R2.7.4, R2.8.Applications.Candidate, R2.8.Applications.Opening, R2.8.Applications.Recruiter, R2.8.Applications.Referred By, R2.8.Offers.Application, R2.8.Interviews.Application, R2.8.Interviews.Interviewer, R2.8.Job Openings.Department, R2.8.Job Openings.Recruiter, R2.8.Job Openings.Hiring Manager, R2.8.People.Department, R2.9.Applications.Recruiter, R2.9.Job Openings.Recruiter, R2.9.Job Openings.Hiring Manager, R2.9.Interviews.Interviewer | `outputs/tables/audit/audit_summary.csv` |
| 3. Duplicates | 6 | R3.5.Departments, R3.5.Job Openings, R3.5.Candidates, R3.5.Interviews, R3.5.Offers, R3.6 | `outputs/tables/audit/audit_summary.csv` |
| 4. Categorical hygiene | 4 | R4.1, R4.2, R4.3, R4.4 | `outputs/tables/audit/audit_summary.csv` |
| 5. Temporal logic | 8 | R5.1, R5.2, R5.3, R5.4, R5.6, R5.7, R5.12, R5.15 | `outputs/tables/audit/audit_summary.csv` |
| 6. State-machine contradictions | 10 | R6.1, R6.3, R6.4, R6.7, R6.8, R6.10, R6.11, R6.12, R6.22, R6.23 | `outputs/tables/audit/audit_summary.csv` |
| 7. Outliers | 22 | R7.1.Offers.Base CTC, R7.2.Offers.Base CTC, R7.1.Candidates.Current CTC, R7.2.Candidates.Current CTC, R7.1.Candidates.Expected CTC, R7.2.Candidates.Expected CTC, R7.1.Job Openings.Salary Band Min, R7.2.Job Openings.Salary Band Min, R7.1.Job Openings.Salary Band Max, R7.2.Job Openings.Salary Band Max, R7.3.Offers.Joining Bonus, R7.3.Candidates.Notice Period Days, R7.3.Candidates.Years Experience, R7.5, R7.6.time to hire, R7.7.time to hire, R7.6.offer decision, R7.7.offer decision, R7.8, R7.10, R7.11, R7.12 | `outputs/tables/audit/audit_summary.csv` |
| 8. Test and synthetic records | 2 | R8.1.Job Openings, R8.1.Departments | `outputs/tables/audit/audit_summary.csv` |
