# D1 evidence: the two claims

Confidence labels are from `deliverables/findings.csv`. Cite = the file under `outputs/tables/` holding the number. UNCITED = no file under `outputs/tables/` holds it; the mark says whether it is arithmetic on cited numbers or computed from data/raw, and gives the derivation.

## Claim 1, part one: volume

### Applications by channel, applied on or before 2026-06-28, APP-00335 dropped

**B1 Source as recorded**

| Rank | Channel | Value | Fraction | 95% CI | n | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| 1 | Job Board | 65.44% | 195/298 | 59.87–70.61 | 298 | high | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 2 | Agency | 11.07% | 33/298 | 7.99–15.14 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 3 | LinkedIn | 9.40% | 28/298 | 6.58–13.24 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 4 | Career Site | 8.72% | 26/298 | 6.02–12.48 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 5 | Referral | 4.03% | 12/298 | 2.32–6.91 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 6 | Campus | 1.34% | 4/298 | 0.52–3.4 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |

**B2 LinkedIn merged into Job Board**

| Rank | Channel | Value | Fraction | 95% CI | n | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| 1 | Job Board + LinkedIn | 74.83% | 223/298 | 69.61–79.42 | 298 | high | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 2 | Agency | 11.07% | 33/298 | 7.99–15.14 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 3 | Career Site | 8.72% | 26/298 | 6.02–12.48 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 4 | Referral | 4.03% | 12/298 | 2.32–6.91 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 5 | Campus | 1.34% | 4/298 | 0.52–3.4 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |

**B3 any Referred By link counts as Referral**

| Rank | Channel | Value | Fraction | 95% CI | n | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| 1 | Job Board | 60.07% | 179/298 | 54.41–65.47 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 2 | Referral | 11.41% | 34/298 | 8.28–15.52 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 3 | Agency | 10.07% | 30/298 | 7.14–14.01 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 4 | LinkedIn | 9.40% | 28/298 | 6.58–13.24 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 5 | Career Site | 7.72% | 23/298 | 5.2–11.31 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |
| 6 | Campus | 1.34% | 4/298 | 0.52–3.4 | 298 | not rated | `outputs/tables/claim1_conversion_by_channel.csv`, `outputs/tables/populations.csv` |

## Claim 1, part two: the hire-share figure

| Item | Value | Fraction | 95% CI | n | Confidence | Cite |
|---|---|---|---|---|---|---|
| VP's 26.9% reproduced | 26.92% | 7/26 |  | 26 | high | `outputs/tables/claim1_vp_figure_reproduced.csv` |
| Distinct fractions rounding to 26.9% | 1 | 1/441 |  | 441 |  | UNCITED, arithmetic on cited numbers: numerator = number of fraction rows in the cited file; 441 is in the file (inputs: `outputs/tables/claim1_vp_figure_reproduced.csv`) |
| Definitions producing that fraction | 11 | 11/2580 |  | 2580 |  | `outputs/tables/claim1_vp_figure_reproduced.csv` |
| of which all-time | 2 |  |  | 11 |  | `outputs/tables/claim1_vp_figure_reproduced.csv` |

### The all-time reproducing definitions, in full

| Event | Window | Unit | Attribution | Channel | Value | Fraction | Cite |
|---|---|---|---|---|---|---|---|
| hired: Applications.Stage = Hired | all time | application rows | Candidates.Source as recorded | raw Source = Job Board | 26.92% | 7/26 | `outputs/tables/exploration/claim1_definitions.csv` |
| offer accepted: Offers.Status = Accepted | all time | application rows | Candidates.Source as recorded | raw Source = Job Board | 26.92% | 7/26 | `outputs/tables/exploration/claim1_definitions.csv` |

### Under that definition (26 hires, Source as recorded)

| Channel | Value | Fraction | n | Cite |
|---|---|---|---|---|
| Job Board | 26.92% | 7/26 | 26 | `outputs/tables/exploration/time_channel_hire_rates.csv`, `outputs/tables/claim1_vp_figure_reproduced.csv` |
| Referral | 26.92% | 7/26 | 26 | `outputs/tables/exploration/time_channel_hire_rates.csv`, `outputs/tables/claim1_vp_figure_reproduced.csv` |

### Job-board share of hires, 25 hires

| Grouping | Channel | Value | Fraction | 95% CI | n | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| B1 Source as recorded | Job Board | 28.00% | 7/25 | 14.28–47.58 | 25 | low | `outputs/tables/claim1_job_board_share_of_hires.csv` |
| B2 LinkedIn merged into Job Board | Job Board + LinkedIn | 40.00% | 10/25 | 23.40–59.26 | 25 | low | `outputs/tables/claim1_job_board_share_of_hires.csv` |
| B3 any Referred By link counts as Referral | Job Board | 24.00% | 6/25 | 11.50–43.43 | 25 | low | `outputs/tables/claim1_job_board_share_of_hires.csv` |

### First vs second place, exact two-sided binomial

| Basis | Grouping | First | Second | Value | n | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| 25 hires | B1 Source as recorded | Job Board 7/25 | Referral 6/25 | p = 1.0000 | 25 | high | `outputs/tables/claim1_first_vs_second_place.csv` |
| 25 hires | B2 LinkedIn merged into Job Board | Job Board + LinkedIn 10/25 | Referral 6/25 | p = 0.4545 | 25 | high | `outputs/tables/claim1_first_vs_second_place.csv` |
| 25 hires | B3 any Referred By link counts as Referral | Referral 9/25 | Job Board 6/25 | p = 0.6072 | 25 | high | `outputs/tables/claim1_first_vs_second_place.csv` |
| 26 hires (VP basis) | B1 Source as recorded | Referral 7/26 | Job Board 7/26 | p = 1.0000 | 26 | not rated | `outputs/tables/claim1_referral_and_ranking_inputs.csv`, `outputs/tables/populations.csv` |
| 26 hires (VP basis) | B2 LinkedIn merged into Job Board | Job Board + LinkedIn 10/26 | Referral 7/26 | p = 0.6291 | 26 | not rated | `outputs/tables/claim1_referral_and_ranking_inputs.csv`, `outputs/tables/populations.csv` |
| 26 hires (VP basis) | B3 any Referred By link counts as Referral | Referral 10/26 | Job Board 6/26 | p = 0.4545 | 26 | not rated | `outputs/tables/claim1_referral_and_ranking_inputs.csv`, `outputs/tables/populations.csv` |
| 24 hires (CAND-00015's later hire also dropped) | B1 Source as recorded | Job Board 7/24 | Referral 5/24 | p = 0.7744 | 24 | not rated | `outputs/tables/claim1_referral_and_ranking_inputs.csv`, `outputs/tables/populations.csv` |
| 24 hires (CAND-00015's later hire also dropped) | B2 LinkedIn merged into Job Board | Job Board + LinkedIn 10/24 | Referral 5/24 | p = 0.3018 | 24 | not rated | `outputs/tables/claim1_referral_and_ranking_inputs.csv`, `outputs/tables/populations.csv` |
| 24 hires (CAND-00015's later hire also dropped) | B3 any Referred By link counts as Referral | Referral 8/24 | Job Board 6/24 | p = 0.7905 | 24 | not rated | `outputs/tables/claim1_referral_and_ranking_inputs.csv`, `outputs/tables/populations.csv` |

### Hires to confirm a leader if these shares held (80% power), at the volume in this base

| Grouping | Value | Years at the volume in this base | Hires/month in this base | Confidence | Cite |
|---|---|---|---|---|---|
| B1 Source as recorded | 2,544 hires | 101.8 | 2.08 | low | `outputs/tables/claim1_hires_needed_to_separate_leader.csv` |
| B2 LinkedIn merged into Job Board | 189 hires | 7.6 | 2.08 | low | `outputs/tables/claim1_hires_needed_to_separate_leader.csv` |
| B3 any Referred By link counts as Referral | 320 hires | 12.8 | 2.08 | low | `outputs/tables/claim1_hires_needed_to_separate_leader.csv` |

## Claim 1, part three: the deciding number

| Item | Value | Fraction | 95% CI | n | Hires | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| Job-board conversion (B1) | 3.59% | 7/195 | 1.75–7.22 | 195 | 7 | medium | `outputs/tables/claim1_conversion_by_channel.csv` |

### Yield comparison

**B3**

| Item | Value | Fraction | 95% CI | n | Hires | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| Referral conversion (B3) | 26.47% | 9/34 | 14.6–43.12 | 34 | 9 | low | `outputs/tables/claim1_conversion_by_channel.csv` |
| Job Board conversion (B3) | 3.35% | 6/179 | 1.55–7.12 | 179 | 6 | not rated | `outputs/tables/claim1_conversion_by_channel.csv` |
| B3 any Referred By link counts as Referral: Referral / Job Board magnitude | 7.9x |  |  | 34 |  | low (a 7.9x gap resting on 9 referral hires out of 34 applications (95% interval 14.60-43.12); only the direction is supported) | UNCITED, arithmetic on cited numbers: (9/34) / (6/179) (inputs: `outputs/tables/claim1_conversion_by_channel.csv`) |
| B3 any Referred By link counts as Referral: direction, Fisher exact vs Job Board | p = 6.18e-05 | 9/34 vs 6/179 |  |  |  | high | `outputs/tables/claim1_conversion_vs_job_board_p.csv` |

**B1**

| Item | Value | Fraction | 95% CI | n | Hires | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| Referral conversion (B1) | 50.00% | 6/12 | 25.38–74.62 | 12 | 6 | low (implausible effect size on n=12 (13.9x Job Board); only the direction is supported, see conversion_vs_job_board_p) | `outputs/tables/claim1_conversion_by_channel.csv` |
| Job Board conversion (B1) | 3.59% | 7/195 | 1.75–7.22 | 195 | 7 | medium | `outputs/tables/claim1_conversion_by_channel.csv` |
| B1 Source as recorded: Referral / Job Board magnitude | 13.9x |  |  | 12 |  | low (implausible effect size on n=12) | UNCITED, arithmetic on cited numbers: (6/12) / (7/195) (inputs: `outputs/tables/claim1_conversion_by_channel.csv`) |
| B1 Source as recorded: direction, Fisher exact vs Job Board | p = 1.3e-05 | 6/12 vs 7/195 |  |  |  | high | `outputs/tables/claim1_conversion_vs_job_board_p.csv` |

**B2**

| Item | Value | Fraction | 95% CI | n | Hires | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| Referral conversion (B2) | 50.00% | 6/12 | 25.38–74.62 | 12 | 6 | not rated | `outputs/tables/claim1_conversion_by_channel.csv` |
| Job Board + LinkedIn conversion (B2) | 4.48% | 10/223 | 2.45–8.06 | 223 | 10 | medium | `outputs/tables/claim1_conversion_by_channel.csv` |
| B2 LinkedIn merged into Job Board: Referral / Job Board + LinkedIn magnitude | 11.2x |  |  | 12 |  | low (implausible effect size on n=12) | UNCITED, arithmetic on cited numbers: (6/12) / (10/223) (inputs: `outputs/tables/claim1_conversion_by_channel.csv`) |
| B2 LinkedIn merged into Job Board: direction, Fisher exact vs Job Board + LinkedIn | p = 2.68e-05 | 6/12 vs 10/223 |  |  |  | high | `outputs/tables/claim1_conversion_vs_job_board_p.csv` |

| Item | Value | Fraction | n | Confidence | Cite |
|---|---|---|---|---|---|
| Campus conversion (B1) | not reported: n < 10 | 0/4 | 4 | low | `outputs/tables/claim1_conversion_by_channel.csv` |

## Claim 2

| Item | Value | Fraction | 95% CI | n | Confidence | Cite |
|---|---|---|---|---|---|---|
| VP's ~72% reproduced (all offer records, Pending as not accepted) | 72.22% | 26/36 |  | 36 | medium | `outputs/tables/claim2_vp_figure_reproduced.csv` |
| Definitions landing in 71.5–72.5% | 192 | 192/9018 |  | 9018 |  | `outputs/tables/claim2_vp_figure_reproduced.csv` |
| Distinct fractions in that band | 9 | 18/25, 23/32, 11.5/16, 26/36, 13/18, 6.5/9, 9.33/13, 21/29, 12.17/17 |  |  |  | UNCITED, arithmetic on cited numbers: the count = number of fraction rows in the cited file; each fraction is in the file (inputs: `outputs/tables/claim2_vp_figure_reproduced.csv`) |
| Defended: stale Pending counted as not accepted | 71.43% | 25/35 | 54.95–83.67 | 35 | low | `outputs/tables/claim2_offer_acceptance.csv` |
| Pending on On Hold requisitions excluded | 75.76% | 25/33 | 58.98–87.17 | 33 | low | `outputs/tables/claim2_offer_acceptance.csv` |
| Decided offers only (all Pending excluded) | 83.33% | 25/30 | 66.44–92.66 | 30 | low | `outputs/tables/claim2_offer_acceptance.csv` |
| Upper bound: every Pending offer accepted | 85.71% | 30/35 | 70.62–93.74 | 35 | medium | `outputs/tables/claim2_offer_acceptance.csv` |

### Deciding number, scale-free

| Item | Value | Confidence | Cite |
|---|---|---|---|
| Offers per period to detect 71.43% -> 76.43% (two-sided alpha 0.05, power 80%) | 1,210 | high | `outputs/tables/claim2_offers_needed_for_5pt_move.csv` |

Derivation (pooled variance in the alpha term, unpooled in the power term; reproduces 1,209.07 before rounding up): n = (z_0.975·√(2·p̄·(1−p̄)) + z_0.80·√(p1(1−p1) + p2(1−p2)))² / (p2 − p1)², no continuity correction.

| Term | Value | Cite |
|---|---|---|
| p1 = 25/35 (defended rate) | 0.714286 | `outputs/tables/claim2_sample_size_derivation.csv` |
| p2 = p1 + 0.05 | 0.764286 | `outputs/tables/claim2_sample_size_derivation.csv` |
| p̄ = (p1 + p2)/2 | 0.739286 | `outputs/tables/claim2_sample_size_derivation.csv` |
| z_0.975 | 1.959964 | `outputs/tables/claim2_sample_size_derivation.csv` |
| z_0.80 | 0.841621 | `outputs/tables/claim2_sample_size_derivation.csv` |
| z_0.975·√(2·p̄·(1−p̄)) | 1.216891 | `outputs/tables/claim2_sample_size_derivation.csv` |
| z_0.80·√(p1(1−p1) + p2(1−p2)) | 0.521693 | `outputs/tables/claim2_sample_size_derivation.csv` |
| n before rounding up | 1209.07 | `outputs/tables/claim2_sample_size_derivation.csv` |

### Scale-dependent illustration, at the volume in this base

| Item | Value | Confidence | Cite |
|---|---|---|---|
| Offers per month in this base (trailing 12 months) | 2.92 | medium | `outputs/tables/claim2_offer_volume.csv` |
| Offers for both periods | 2,420 |  | `outputs/tables/claim2_offers_needed_for_5pt_move.csv` |
| Months for both periods at that volume | 829.7 |  | `outputs/tables/claim2_offers_needed_for_5pt_move.csv` |
| Years per period at ten times that volume | 3.46 |  | UNCITED, arithmetic on cited numbers: 1,210 / (10 × 2,420 / 829.7 offers per month) / 12 (inputs: `outputs/tables/claim2_offers_needed_for_5pt_move.csv`) |

### Declines by reason

| Reason | Value | n | Confidence | Cite |
|---|---|---|---|---|
| Counter Offer | 3 | 5 | low | `outputs/tables/claim2_declines_by_reason.csv`, `outputs/tables/audit/audit_4_categorical_hygiene.csv` |
| Location | 1 | 5 | low | `outputs/tables/claim2_declines_by_reason.csv`, `outputs/tables/audit/audit_4_categorical_hygiene.csv` |
| Compensation | 1 | 5 | low | `outputs/tables/claim2_declines_by_reason.csv`, `outputs/tables/audit/audit_4_categorical_hygiene.csv` |
