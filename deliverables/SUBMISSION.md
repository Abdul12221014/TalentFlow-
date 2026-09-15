# Submission

<!-- Assembly: every number carries a trailing citation comment. Sources are notes/evidence/ (d1–d5) and settled entries in notes/decisions.md, except where a comment names another file: the brief, deliverables/findings.csv, src/audit.py or an outputs/tables/ CSV. D3 keeps the draft's inline citations. Snapshot 2026-09-14T18:07:35Z, as-of date 2026-08-27 (notes/decisions.md header). -->

## D1 — Verdict on the VP's two claims

Confidence levels: high = n ≥ 100 and a 95% interval no wider than 15 points; medium = n ≥ 30 and no wider than 25 points; low = otherwise. Fewer than 5 records in the rarer outcome forces low; fewer than 20 caps the level at medium. <!-- decisions.md #9 -->

### Claim 1

> "First — job boards are our biggest channel by a wide margin and they bring in 26.9% of our hires. I want the job-board integration work brought forward." <!-- the brief: the VP People's email -->

Settled bases:
- Hires: 25. APP-00335, CAND-00035 hired a second time into the same opening, is dropped. <!-- decisions.md #1 -->
- CAND-00015's two hires, into two different openings, are both kept. <!-- decisions.md #2 -->
- Channel groupings, reported side by side: B1 Source as recorded; B2 LinkedIn counted as Job Board; B3 any Referred By link counts as Referral. <!-- decisions.md #3 -->
- Applications count if made at least 60 days (the slowest recorded hire) before 2026-08-27; with APP-00335 also dropped, that leaves 298 applications. <!-- decisions.md #5, #1; d1_evidence.md → populations.csv -->

#### (a) Volume

Job-board share of applications, B1: **195/298 = 65.44% (95% CI 59.87–70.61), high confidence.** <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->

Channel ranking by application volume, 298 applications. <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->

**B1 Source as recorded**

| Rank | Channel | Applications | Share | 95% CI | Confidence |
|---|---|---|---|---|---|
| 1 | Job Board | 195/298 | 65.44% | 59.87–70.61 | high | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 2 | Agency | 33/298 | 11.07% | 7.99–15.14 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 3 | LinkedIn | 28/298 | 9.40% | 6.58–13.24 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 4 | Career Site | 26/298 | 8.72% | 6.02–12.48 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 5 | Referral | 12/298 | 4.03% | 2.32–6.91 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 6 | Campus | 4/298 | 1.34% | 0.52–3.40 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->

**B2 LinkedIn counted as Job Board**

| Rank | Channel | Applications | Share | 95% CI | Confidence |
|---|---|---|---|---|---|
| 1 | Job Board + LinkedIn | 223/298 | 74.83% | 69.61–79.42 | high | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 2 | Agency | 33/298 | 11.07% | 7.99–15.14 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 3 | Career Site | 26/298 | 8.72% | 6.02–12.48 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 4 | Referral | 12/298 | 4.03% | 2.32–6.91 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 5 | Campus | 4/298 | 1.34% | 0.52–3.40 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->

**B3 any Referred By link counts as Referral**

| Rank | Channel | Applications | Share | 95% CI | Confidence |
|---|---|---|---|---|---|
| 1 | Job Board | 179/298 | 60.07% | 54.41–65.47 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 2 | Referral | 34/298 | 11.41% | 8.28–15.52 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 3 | Agency | 30/298 | 10.07% | 7.14–14.01 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 4 | LinkedIn | 28/298 | 9.40% | 6.58–13.24 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 5 | Career Site | 23/298 | 7.72% | 5.20–11.31 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| 6 | Campus | 4/298 | 1.34% | 0.52–3.40 | not rated | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->

#### (b) The 26.9% figure <!-- the brief: the VP People's email -->

| Item | Value | Confidence |
|---|---|---|
| VP's 26.9% reproduced by | 7/26 = 26.92% | high | <!-- d1_evidence.md → claim1_vp_figure_reproduced.csv -->
| Distinct fractions rounding to 26.9% | 1 of 441 | | <!-- d1_evidence.md: UNCITED, arithmetic — count of fraction rows in claim1_vp_figure_reproduced.csv; 441 is in that file -->
| Definitions producing that fraction | 11 of 2,580 | | <!-- d1_evidence.md → claim1_vp_figure_reproduced.csv -->
| Of those, all-time | 2 of 11 | | <!-- d1_evidence.md → claim1_vp_figure_reproduced.csv -->

The all-time reproducing definitions, in full:

| Event | Window | Unit | Attribution | Channel | Result |
|---|---|---|---|---|---|
| hired: Applications.Stage = Hired | all time | application rows | Candidates.Source as recorded | raw Source = Job Board | 7/26 = 26.92% | <!-- d1_evidence.md → exploration/claim1_definitions.csv -->
| offer accepted: Offers.Status = Accepted | all time | application rows | Candidates.Source as recorded | raw Source = Job Board | 7/26 = 26.92% | <!-- d1_evidence.md → exploration/claim1_definitions.csv -->

Under that definition (26 hires, Source as recorded), Referral ties Job Board: <!-- d1_evidence.md → exploration/time_channel_hire_rates.csv, claim1_vp_figure_reproduced.csv -->

| Channel | Share of hires |
|---|---|
| Job Board | 7/26 = 26.92% | <!-- d1_evidence.md → exploration/time_channel_hire_rates.csv, claim1_vp_figure_reproduced.csv -->
| Referral | 7/26 = 26.92% | <!-- d1_evidence.md → exploration/time_channel_hire_rates.csv, claim1_vp_figure_reproduced.csv -->

Job-board share of hires on the 25-hire basis, Wilson 95% intervals: <!-- decisions.md #1 -->

| Grouping | Channel | Share | 95% CI | Confidence |
|---|---|---|---|---|
| B1 Source as recorded | Job Board | 7/25 = 28.00% | 14.28–47.58 | low | <!-- d1_evidence.md → claim1_job_board_share_of_hires.csv -->
| B2 LinkedIn counted as Job Board | Job Board + LinkedIn | 10/25 = 40.00% | 23.40–59.26 | low | <!-- d1_evidence.md → claim1_job_board_share_of_hires.csv -->
| B3 any Referred By link counts as Referral | Job Board | 6/25 = 24.00% | 11.50–43.43 | low | <!-- d1_evidence.md → claim1_job_board_share_of_hires.csv -->

First vs second place, exact two-sided binomial, every basis:

| Hire basis | Grouping | First | Second | p | Confidence |
|---|---|---|---|---|---|
| 25 hires | B1 | Job Board 7/25 | Referral 6/25 | 1.0000 | high | <!-- d1_evidence.md → claim1_first_vs_second_place.csv -->
| 25 hires | B2 | Job Board + LinkedIn 10/25 | Referral 6/25 | 0.4545 | high | <!-- d1_evidence.md → claim1_first_vs_second_place.csv -->
| 25 hires | B3 | Referral 9/25 | Job Board 6/25 | 0.6072 | high | <!-- d1_evidence.md → claim1_first_vs_second_place.csv -->
| 26 hires (VP basis) | B1 | Referral 7/26 | Job Board 7/26 | 1.0000 | not rated | <!-- d1_evidence.md → claim1_referral_and_ranking_inputs.csv, populations.csv -->
| 26 hires (VP basis) | B2 | Job Board + LinkedIn 10/26 | Referral 7/26 | 0.6291 | not rated | <!-- d1_evidence.md → claim1_referral_and_ranking_inputs.csv, populations.csv -->
| 26 hires (VP basis) | B3 | Referral 10/26 | Job Board 6/26 | 0.4545 | not rated | <!-- d1_evidence.md → claim1_referral_and_ranking_inputs.csv, populations.csv -->
| 24 hires (CAND-00015's later hire also dropped) | B1 | Job Board 7/24 | Referral 5/24 | 0.7744 | not rated | <!-- d1_evidence.md → claim1_referral_and_ranking_inputs.csv, populations.csv -->
| 24 hires (CAND-00015's later hire also dropped) | B2 | Job Board + LinkedIn 10/24 | Referral 5/24 | 0.3018 | not rated | <!-- d1_evidence.md → claim1_referral_and_ranking_inputs.csv, populations.csv -->
| 24 hires (CAND-00015's later hire also dropped) | B3 | Referral 8/24 | Job Board 6/24 | 0.7905 | not rated | <!-- d1_evidence.md → claim1_referral_and_ranking_inputs.csv, populations.csv -->

Hires needed to confirm a leader if the observed shares held (80% power), at the volume in this base: <!-- d1_evidence.md → claim1_hires_needed_to_separate_leader.csv -->

| Grouping | Hires needed | Years at the volume in this base | Hires per month in this base | Confidence |
|---|---|---|---|---|
| B1 Source as recorded | 2,544 | 101.8 | 2.08 | low | <!-- d1_evidence.md → claim1_hires_needed_to_separate_leader.csv -->
| B2 LinkedIn counted as Job Board | 189 | 7.6 | 2.08 | low | <!-- d1_evidence.md → claim1_hires_needed_to_separate_leader.csv -->
| B3 any Referred By link counts as Referral | 320 | 12.8 | 2.08 | low | <!-- d1_evidence.md → claim1_hires_needed_to_separate_leader.csv -->

#### (c) Conversion

Job-board conversion, B1: **7/195 = 3.59% (95% CI 1.75–7.22), medium confidence, 7 hires in the numerator.** <!-- d1_evidence.md → claim1_conversion_by_channel.csv -->

Yield comparison. B3 leads; B1 and B2 are reported alongside. <!-- decisions.md #4 -->

| Grouping | Referral conversion (95% CI) | Job-board conversion (95% CI) | Magnitude | Magnitude confidence | Direction: Fisher exact vs job board | Direction confidence |
|---|---|---|---|---|---|---|
| B3 any Referred By link counts as Referral | 9/34 = 26.47% (14.60–43.12) | 6/179 = 3.35% (1.55–7.12) | 7.9x | low: a 7.9x gap resting on 9 referral hires out of 34 applications; only the direction is supported | p = 6.18e-05 | high | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, claim1_conversion_vs_job_board_p.csv; 7.9x UNCITED, arithmetic (9/34)/(6/179) -->
| B1 Source as recorded | 6/12 = 50.00% (25.38–74.62) | 7/195 = 3.59% (1.75–7.22) | 13.9x | low: implausible effect size on n=12 | p = 1.3e-05 | high | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, claim1_conversion_vs_job_board_p.csv; 13.9x UNCITED, arithmetic (6/12)/(7/195) -->
| B2 LinkedIn counted as Job Board | 6/12 = 50.00% (25.38–74.62) | 10/223 = 4.48% (2.45–8.06) | 11.2x | low: implausible effect size on n=12 | p = 2.68e-05 | high | <!-- d1_evidence.md → claim1_conversion_by_channel.csv, claim1_conversion_vs_job_board_p.csv; 11.2x UNCITED, arithmetic (6/12)/(10/223) -->

#### Claim 1 verdict

- Deciding number, settled: job-board conversion 7/195 = 3.59%. <!-- decisions.md #7 -->
- On record: the VP's "biggest channel by a wide margin" is true for applications, 195/298 = 65.44% (high confidence); the build decision turns on conversion, not share. <!-- decisions.md #7 -->

**Verdict: build something different.** The VP asked for the job-board integration work to be brought forward. The deciding number is job-board conversion, 7/195 = 3.59% (95% CI 1.75–7.22): the constraint is conversion, not supply. 7/195 and 195/298 are themselves degraded by Source sitting on the candidate rather than the application, which is why that defect is build 1: the number I am deciding on cannot be improved without it. <!-- decisions.md #7; 7/195: d1_evidence.md → claim1_conversion_by_channel.csv; numbers damaged by Source on the candidate: d2_evidence.md rank 1; the VP's ask: the brief's email -->

The VP is right that job boards dominate volume: 195/298 applications = 65.44% (95% CI 59.87–70.61), high confidence. That is precisely why bringing the job-board integration work forward is the wrong ask. Two thirds of the funnel already arrives through job boards, and 7/195 = 3.59% of it converts to a hire. The build decision turns on conversion, not share. The bottleneck is triage, not supply. <!-- decisions.md #7; 195/298 and 7/195: d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->

### Claim 2

> "Second — our offer acceptance rate is sitting at around 72% and the board is asking about it. I need that number moving." <!-- the brief: the VP People's email -->

Settled bases:
- Offers count if extended at least 20 days (the slowest recorded decision) before 2026-08-27; the cut removes 0 of 36 offers. <!-- decisions.md #5 -->
- OFF-00035 leaves with APP-00335, giving 35 offers. <!-- decisions.md #1 -->
- Pending offers count as not accepted. <!-- decisions.md #6 -->

#### (a) The ~72% figure <!-- the brief: the VP People's email -->

- Reproduced by 26/36 = 72.22%: all offer records, Pending counted as not accepted. Medium confidence. <!-- d1_evidence.md → claim2_vp_figure_reproduced.csv -->
- 192 of 9,018 definitions land in 71.5–72.5%. <!-- d1_evidence.md → claim2_vp_figure_reproduced.csv -->
- Those definitions give 9 distinct fractions: 18/25, 23/32, 11.5/16, 26/36, 13/18, 6.5/9, 9.33/13, 21/29, 12.17/17. <!-- d1_evidence.md: count UNCITED, arithmetic — fraction rows in claim2_vp_figure_reproduced.csv; each fraction is in that file -->

#### (b) Defended rate and variants

| Definition | Rate | 95% CI | n | Confidence |
|---|---|---|---|---|
| Defended: stale Pending counted as not accepted | 25/35 = 71.43% | 54.95–83.67 | 35 | low | <!-- d1_evidence.md → claim2_offer_acceptance.csv; decisions.md #6 -->
| Pending on On Hold requisitions excluded | 25/33 = 75.76% | 58.98–87.17 | 33 | low | <!-- d1_evidence.md → claim2_offer_acceptance.csv -->
| Decided offers only (all Pending excluded) | 25/30 = 83.33% | 66.44–92.66 | 30 | low | <!-- d1_evidence.md → claim2_offer_acceptance.csv -->
| Upper bound: every Pending offer accepted | 30/35 = 85.71% | 70.62–93.74 | 35 | medium | <!-- d1_evidence.md → claim2_offer_acceptance.csv -->

#### (c) Sample size

**1,210 offers per period** to detect 71.43% → 76.43% at two-sided alpha 0.05 and 80% power. Scale-free; high confidence. <!-- decisions.md #8; d1_evidence.md → claim2_offers_needed_for_5pt_move.csv -->

Derivation: n = (z_0.975·√(2·p̄·(1−p̄)) + z_0.80·√(p1(1−p1) + p2(1−p2)))² / (p2 − p1)², with pooled variance in the alpha term, unpooled variance in the power term and no continuity correction. <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->

| Term | Value |
|---|---|
| p1 = 25/35 (defended rate) | 0.714286 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->
| p2 = p1 + 0.05 | 0.764286 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->
| p̄ = (p1 + p2)/2 | 0.739286 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->
| z_0.975 | 1.959964 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->
| z_0.80 | 0.841621 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->
| z_0.975·√(2·p̄·(1−p̄)) | 1.216891 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->
| z_0.80·√(p1(1−p1) + p2(1−p2)) | 0.521693 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->
| n before rounding up | 1209.07 | <!-- d1_evidence.md → claim2_sample_size_derivation.csv -->

Scale-dependent: at the volume in this base, which placeholder data cannot establish as Acme's real scale. <!-- decisions.md #8 -->

| Item | Value | Confidence |
|---|---|---|
| Offers per month in this base (trailing 12 months) | 2.92 | medium | <!-- d1_evidence.md → claim2_offer_volume.csv -->
| Offers for both periods | 2,420 | | <!-- d1_evidence.md → claim2_offers_needed_for_5pt_move.csv -->
| Months for both periods at 2.92 offers per month | 829.7 | | <!-- d1_evidence.md → claim2_offers_needed_for_5pt_move.csv -->
| Years per period at ten times that volume | 3.46 | | <!-- d1_evidence.md: UNCITED, arithmetic — 1,210 / (10 × 2,420 / 829.7 offers per month) / 12, inputs claim2_offers_needed_for_5pt_move.csv -->

#### (d) Declines by reason

| Reason | Declined offers | Confidence |
|---|---|---|
| Counter Offer | 3 | low | <!-- d1_evidence.md → claim2_declines_by_reason.csv, audit/audit_4_categorical_hygiene.csv -->
| Location | 1 | low | <!-- d1_evidence.md → claim2_declines_by_reason.csv, audit/audit_4_categorical_hygiene.csv -->
| Compensation | 1 | low | <!-- d1_evidence.md → claim2_declines_by_reason.csv, audit/audit_4_categorical_hygiene.csv -->
| n | 5 | | <!-- d1_evidence.md → claim2_declines_by_reason.csv -->

#### Claim 2 verdict

- Deciding number, settled: 1,210 offers per period. <!-- decisions.md #8 -->

**Verdict: build something different.** The ~72% figure is real: 26/36 = 72.22% reproduces it, and 192 of 9,018 definitions land in 71.5–72.5%. It cannot be managed at this volume. The deciding number is 1,210 offers per period to detect a 5-point move, a figure that does not depend on volume. At the 2.92 offers a month in this base, both periods take 829.7 months, an illustration that depends on this base's volume. <!-- decisions.md #8; 26/36 and 192 of 9,018: d1_evidence.md → claim2_vp_figure_reproduced.csv; 1,210 and 829.7: d1_evidence.md → claim2_offers_needed_for_5pt_move.csv; 2.92: d1_evidence.md → claim2_offer_volume.csv -->

No. The three recorded decline reasons, Counter Offer 3, Location 1 and Compensation 1, sit outside what a recruiting-operations product can touch, and n = 5 cannot rank them. What the product can do is instrument the number (D3), surface decline reasons and cut time-to-offer. <!-- d1_evidence.md → claim2_declines_by_reason.csv; deliverables/findings.csv declines_by_reason -->

## D2 — The 6 engineer-weeks <!-- the brief -->

Budget: 6 engineer-weeks. <!-- the brief -->

### Builds, in priority order

The justifying-number column is pre-filled in d2_evidence.md's order. That file ranks defects that block a question the customer asked first, then by the share of that question's population affected. <!-- d2_evidence.md -->

| Rank | What it is | Size (engineer-weeks, estimate) | Number that justifies it | Citation |
|---|---|---|---|---|
| 1 | Move Source from the candidate to the application. | 2.5 engineer-weeks, my estimate, not derivable from the data: the largest of the three, because it changes where every application records its channel instead of validating fields that already exist. | 12/25 hires = 48.00% belong to candidates with two applications, so their channel cannot be attributed to a specific application. 50/300 candidates (16.67%) have 2 applications. | d2_evidence.md rank 1 → claim1_referral_and_ranking_inputs.csv | <!-- d2_evidence.md rank 1 → claim1_referral_and_ranking_inputs.csv -->
| 2 | Reconcile the two referral fields into one authoritative source. | 1.5 engineer-weeks, my estimate, not derivable from the data: both fields already exist, so the work is making one authoritative and reconciling existing records, not adding a field. | 9/25 hires = 36.00% where the two fields disagree. Source = Referral marks 8/300 candidates, a Referred By link marks 21/300, and 3 are in both. 24/350 applications have Referred By with Source not Referral (R6.18); 10/350 have Source Referral with no Referred By (R6.19). | d2_evidence.md rank 2 → claim1_referral_and_ranking_inputs.csv, audit/audit_summary.csv; decisions.md #3 | <!-- 9/25 and 36.00%: claim1_referral_and_ranking_inputs.csv; 8/300, 21/300, 3: decisions.md #3; 24/350, 10/350: d2_evidence.md rank 2 → audit/audit_summary.csv -->
| 3 | Offer-state validation, with a requisition-integrity check. | 2.0 engineer-weeks, my estimate, not derivable from the data: validation rules on existing Offers and Job Openings fields, plus one new status value, Rescinded. | Offer state: 4 of 5 Pending offers carry a Decision On, and no Rescinded status exists (Offers.Status holds Accepted 26, Pending 5, Declined 5). Requisition integrity: 5/26 hires are in excess of headcount = 19.23%, on 4/24 openings. | d5_evidence.md #5 → audit/audit_summary.csv, claim2_pending_offers.csv; d2_evidence.md rank 4 → audit/audit_4_categorical_hygiene.csv; d2_evidence.md rank 3 → audit/audit_summary.csv | <!-- 4 of 5: d5_evidence.md #5; statuses: d2_evidence.md rank 4 → audit/audit_4_categorical_hygiene.csv; 5/26 and 19.23%: d2_evidence.md rank 3, UNCITED arithmetic (26 − 21); 4/24: d2_evidence.md rank 3 -->

Total: 2.5 + 1.5 + 2.0 = 6.0 engineer-weeks, which fits the 6-week budget exactly. All three sizes are my estimates; the data cannot supply them. <!-- budget: the brief -->

Each build ranks by the share of the population behind a question the customer actually asked: 48.00% of hires for build 1, 36.00% for build 2, and 19.23% for build 3, from its requisition-integrity check. Build 1 also blocks the channel question outright, because no application-level source exists. <!-- ranking rule: d2_evidence.md header; shares: d2_evidence.md ranks 1–3; no application-level source: d2_evidence.md rank 1 -->

### Non-builds

Why-not numbers (key A is not used by any row below):

| Key | Number | Citation |
|---|---|---|
| A | No channel's hire share separates from second place in any grouping, 25 hires: B1 Job Board 7 vs Referral 6, p = 1.0000; B2 Job Board + LinkedIn 10 vs Referral 6, p = 0.4545; B3 Referral 9 vs Job Board 6, p = 0.6072 | d1_evidence.md → claim1_first_vs_second_place.csv | <!-- d1_evidence.md → claim1_first_vs_second_place.csv -->
| B | 1,210 offers per period to detect a 5-point acceptance move | d1_evidence.md → claim2_offers_needed_for_5pt_move.csv | <!-- d1_evidence.md → claim2_offers_needed_for_5pt_move.csv -->
| C | Campus conversion not rated: 0/4 applications, below the 10-record floor for reporting a rate | d1_evidence.md → claim1_conversion_by_channel.csv | <!-- d1_evidence.md → claim1_conversion_by_channel.csv; 10-record floor: deliverables/findings.csv conversion_by_channel method -->
| D | Agency 4/33 vs Job Board 7/195, Fisher exact p = 0.0575; LinkedIn 3/28 vs Job Board 7/195, p = 0.116; neither is below 0.05 or the Bonferroni threshold of 0.0125 | NOT IN notes/evidence: outputs/tables/claim1_conversion_vs_job_board_p.csv; deliverables/findings.csv lines 30–31 | <!-- NOT IN notes/evidence: outputs/tables/claim1_conversion_vs_job_board_p.csv; deliverables/findings.csv lines 30–31 -->

| What it is | Why not | Number behind the why-not |
|---|---|---|
| Bringing the job-board integration work forward, as the VP asked. | Job boards already supply 195/298 applications, and that volume converts at 7/195. More job-board volume does not touch the constraint, which is conversion. | 7/195 = 3.59% (95% CI 1.75–7.22) | <!-- decisions.md #7; 195/298 and 7/195: d1_evidence.md → claim1_conversion_by_channel.csv, populations.csv -->
| An offer-acceptance dashboard presented as a managed quarterly KPI. | A 5-point move cannot be detected at this volume: it needs 1,210 offers per period, and this base extends 2.92 offers a month. Instrumenting the metric (D3) is build work I would do; presenting it as movable is not. | key B, 1,210 offers per period; 2.92 offers a month, an illustration at the volume in this base | <!-- 1,210: d1_evidence.md → claim2_offers_needed_for_5pt_move.csv; 2.92: d1_evidence.md → claim2_offer_volume.csv; scale label: decisions.md #8 -->
| Channel-specific work on Campus or Agency. | Campus cannot be rated on 4 applications, and Agency and LinkedIn conversion cannot be told apart from Job Board at 0.05. | keys C and D: Campus 0/4; Agency p = 0.0575, LinkedIn p = 0.116 | <!-- Campus 0/4: d1_evidence.md → claim1_conversion_by_channel.csv; p-values: NOT IN notes/evidence, outputs/tables/claim1_conversion_vs_job_board_p.csv -->

## D3 — Metrics spec: offer acceptance rate

<!-- D3 is transferred in full from deliverables/D3_draft_metrics_spec.md with section numbering intact. Its numbers keep the draft's inline citations to outputs/tables/. Every sentence below is assistant wording; the WORDING comments say where the content is yours and where it is also mine. -->

This spec defines the offer acceptance rate: of the offers a customer extended that have had time to be decided, the share candidates accepted. TalentFlow product, recruiting analytics, owns the metric. The spec is written so that two engineers implementing it separately produce the same number from the same records. Every threshold except the revision window, which is a policy choice (section 2), is derived from the committed snapshot pulled 2026-09-14T18:07:35Z, with as-of date 2026-08-27. File names in backticks are under `outputs/tables/`, and an arithmetic step is shown inline where no file holds the result.

### 1. Metric

<!-- WORDING: ASSISTANT — content and wording both mine -->

- **Name:** offer acceptance rate.
- **Owner:** TalentFlow product, recruiting analytics.
- **Source data:** the customer's Offers, Applications and Job Openings tables.
- **Question answered:** of the offers a customer extended that have had time to be decided, what share did candidates accept?

### 2. Thresholds and their derivations

<!-- WORDING: table and the 'Recomputing T', 'p for N_report' and 'Direction of N_compare' bullets are ASSISTANT; the correction and window bullets are flagged one by one -->

| Symbol | Value on this snapshot | Derivation | Source |
|---|---|---|---|
| T, decision timeout | 20 days | The largest Decision On − Offered On, in days, among Accepted and Declined offers (n = 31; min 2, median 10, p90 17, max 20). | `claim2_slowest_offer_decision.csv` |
| N_report, reporting floor | 314 decided offers | The sample for a 95% interval of ±5 points: n = z_0.975² × p(1 − p) / 0.05² = 3.841459 × 0.204082 / 0.0025 = 313.59, rounded up, with p = 25/35. | `claim2_offers_needed_for_5pt_move.csv` |
| N_compare, comparison floor | 1,210 decided offers per period | Two-proportion sample size for 71.43% → 76.43%, two-sided alpha 0.05, power 80%, pooled variance in the alpha term, unpooled in the power term, no continuity correction: 1,209.07 before rounding up. | `claim2_sample_size_derivation.csv` |

- **Recomputing T:** at every publication, from all Accepted and Declined offers in the customer's history. <!-- WORDING: ASSISTANT — content and wording both mine -->
- **When T grows:** earlier published cohorts are not recomputed. A longer T changes the waiting rule and no recorded fact about any offer. A Rescinded status (section 7) is different: it records a fact that changes the offer's own state, so a cohort published before it counted a company withdrawal as a candidate decision, and that cohort is recomputed. <!-- WORDING: rule and sub-bullets PM-DICTATED; the reason sentences are ASSISTANT -->
  - T growth cannot demature a published month.
  - T applies when a cohort is assessed for maturity at a publication. Once published, a month stays published at the T in force at that publication.
  - The T used is recorded alongside each published cohort.
- **When an offer's recorded status changes after publication:** the principle in the previous bullet decides this case, and no new rule is added. A Lapsed offer that later becomes Accepted changes a recorded fact about the offer. It falls on the Rescinded side of the line, not the T-growth side, so the published value of the cohort that contains it is restated, within the revision window below, for that offer and for every other offer on its pair whose section 3 state changes. <!-- WORDING: PM-DICTATED content, assistant phrasing -->
- **Scope of recomputation:** these are different rules for different scopes. <!-- WORDING: PM-DICTATED content, assistant phrasing -->
  - A schema change, such as adding Rescinded to Offers.Status, recomputes every published cohort regardless of the revision window, because the metric definition changed. The recomputation works from each offer's recorded state history, not from current records. An offer already carrying a dated adjustment keeps it and is not re-absorbed, because re-absorbing it would count the correction twice.
  - A status change to one offer respects the revision window of each offer it moves, because only the records of that offer's pair changed.
- **Restatement rewrites the changed offer and every other offer on the pair whose section 3 state changes, never the month:** the stated record is the pair, not the single offer. <!-- WORDING: PM-DICTATED content, assistant phrasing; the restatement-or-adjustment-line split by revision window is ASSISTANT -->
  - Section 3 already defines a pair's state across all its offers, so a correction to one offer is a correction to the pair, and adjusting only the touched offer leaves the pair in a state section 3 does not permit.
  - Each moved offer gets its own dated delta attached to its own cohort, with the prior value retained. That delta is a restatement of the cohort's published value while the offer is within its revision window, and an adjustment line once the offer is past it.
  - No offer outside the pair is touched, and no month is recounted.
  - The freeze exists so a published number changes only for a stated reason attached to a stated record, and a recount changes numbers for records nobody touched.
- **Restatement is never silent:** the prior published value is kept and the restatement is dated, so a number that moved can be explained. The restated cohort displays the prior published value and the revision date next to the restated value. <!-- WORDING: constraint PM-DICTATED; the display sentence is ASSISTANT -->
- **After the revision window closes:** a correction to an offer does not restate its cohort. <!-- WORDING: PM-DICTATED content, assistant phrasing -->
  - Each moved offer stays in its Offered On cohort permanently, so the cohort rule in section 6 is never violated.
  - The correction never changes a closed month's published value, because that month is frozen. For the changed offer and every other offer on the pair whose section 3 state changes, it appears once per offer, as a dated adjustment line issued at the next publication and attached to that offer's own cohort, and each closed cohort keeps its prior published value. No double count is possible.
  - No offer is reassigned to a different month. Reassignment would rewrite history silently, which is what the audit trail exists to prevent.
- **Adjustment lines carry signed deltas:** a line carries the change, such as Accepted +1 and Lapsed −1, never the offer's new state. <!-- WORDING: PM-DICTATED content, assistant phrasing -->
  - An adjustment line is published in a window only if that window also contains the cohort it adjusts, because a delta without its original is incoherent. If the window has moved past that month, the line is suppressed from the window total, and the adjustment appears in the cohort-level record alone.
  - Consequences: a Lapsed total cannot go negative, and a numerator cannot include an offer its denominator does not.
  - Intent: a trailing window that no longer contains January is not moved by a January correction, and the correction stays visible on January's cohort with its date.
- **Revision window: 90 days. This is a POLICY CHOICE, not a derivation.** A correction restates the published value of a moved offer's cohort only when the correction is recorded within 90 days of that offer's Offered On. <!-- WORDING: PM-DICTATED content, assistant phrasing -->
  - No correction latency is observable in this data, because the snapshot contains no observed correction.
  - 90 days is 4.5 times the slowest observed decision of 20 days across 31 Accepted and Declined offers (`claim2_slowest_offer_decision.csv`), and it closes a month's cohort before the third following month publishes, giving a correction at least two publication cycles to arrive.
  - The window is revisited once real corrections exist to measure.
  - The window is a policy constant and is not recomputed at each publication, unlike T, which is estimated from observed decision times.
- **Window totals:** a window total is the sum of the published values of the cohorts in the window plus the adjustment lines attached to those cohorts, never a fresh count over current records. This section governs window totals, and sections 4 to 6 defer to it. <!-- WORDING: PM-DICTATED content, assistant phrasing -->
  - If the window recounted current state at each publication, every closed cohort would be silently mutable and the audit trail would be decorative, so the freeze has to bind the window totals or it means nothing.
  - Consequence: a window total is a sum of cohorts assessed under possibly different T values. That is the cost of a stable published series, and it is accepted deliberately, not overlooked.
- **Limitation:** the correction rules cover status changes only. A correction to an offer's Offered On, or to its application link, is not covered by any rule. <!-- WORDING: PM-DICTATED addition -->
- **Limitation:** no file in the evidence pack (notes/evidence/) holds these figures, which this spec cites to `outputs/tables/`, shows as inline arithmetic, or sets as policy: the reporting floor 314 and its terms 313.59, 3.841459, 0.204082 and 0.0025; 1,344; 107.7; 35 pairs; Offered On filled on 36 of 36; 83.33% for 30/36; 18 Current Company values; and the revision window's 90 days, 4.5 times and two publication cycles. The evidence pack also lacks the record IDs OFF-00002, OFF-00007, OFF-00013, OFF-00020 and APP-00035, and the fact that all four R6.13 hires sit on Cancelled requisitions.
- **p for N_report and N_compare:** the most recently published rate. Before any rate has been published, p is the pooled rate over all decided offers in the customer's history. <!-- WORDING: ASSISTANT — content and wording both mine -->
- **Direction of N_compare:** it uses a 5-point rise, because the customer's goal is a higher rate. The same calculation for a 5-point fall gives 1,344 per period (`claim2_offers_needed_for_5pt_move.csv`); that figure is not used. <!-- WORDING: ASSISTANT — content and wording both mine -->

### 3. Unit of analysis

<!-- WORDING: ASSISTANT — content and wording both mine (including the Offer ID tie-break) -->

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

### 4. State of each offer

<!-- WORDING: table ASSISTANT; the 'For a published cohort' note is PM-DICTATED content, assistant phrasing -->

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

### 5. Numerator and denominator

<!-- WORDING: Numerator, Denominator, Rate ASSISTANT; Window totals PM-DICTATED content, assistant phrasing; Interval PM-DICTATED -->

- **Numerator:** offers in state Accepted in the reported window.
- **Denominator:** offers in states Accepted, Declined and Lapsed in the reported window. These are the decided offers.
- **Window totals:** the numerator, the denominator and every count in sections 9 and 11 are summed from the published values of the cohorts in the window plus the adjustment lines attached to those cohorts, as section 2 states. They are never counted afresh over current records.
- **Rate:** numerator ÷ denominator, published as a percentage with n only when the denominator is at least N_report.
- **Interval:** the 95% Wilson interval for numerator ÷ denominator is published at every volume with at least one decided offer, as its lower and upper bounds, above and below N_report (section 9).

### 6. Time window and cohort rule

<!-- WORDING: ASSISTANT, except the last two sentences of Maturity and the all-mature-months part of Reported window, which are PM-DICTATED -->

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

### 7. Exclusions

<!-- WORDING: ASSISTANT, except the recomputation sentence in 'When Rescinded is added', which is PM-DICTATED -->

| Excluded | Rule | Reason | Effect on this snapshot |
|---|---|---|---|
| Superseded offers | Out of numerator and denominator | A pair has one outcome, and its earlier offers would count it twice. | 1 offer, OFF-00035 on duplicate hire record APP-00335: 26/36 → 25/35 (`populations.csv`, `claim1_duplicate_hire_records.csv`) |
| Rescinded offers | Out of numerator and denominator; count displayed | The company withdrew the offer, so the candidate made no decision. | 0: Offers.Status holds Accepted 26, Pending 5, Declined 5 and no other value (`audit/audit_4_categorical_hygiene.csv`) |
| Open offers | Out of numerator and denominator; count displayed | The candidate can still decide. | 0: every Pending offer was at least 20 days old on 2026-08-27 (`claim2_pending_offers.csv`) |

- **Rescission is not inferred.** A Cancelled requisition does not mark an offer as rescinded. Neither does a Rejection Reason on the application.
  - With Pending counted as not accepted, those four proxy rules give results from 22/36 = 61.11% to 22/30 = 73.33% (`exploration/claim2_definitions.csv`).
- **When Rescinded is added to Offers.Status:** state 2 applies from the next publication, and every published cohort is recomputed and republished, regardless of the revision window (section 2). The recomputation works from each offer's recorded state history, not from current records, and an offer already carrying a dated adjustment keeps it and is not re-absorbed.

### 8. Edge cases

<!-- WORDING: ASSISTANT — content and wording both mine -->

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

### 9. Minimum n

<!-- WORDING: paragraph PM-DICTATED content, assistant phrasing; the Change line is ASSISTANT -->

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

### 10. Volume constraint

<!-- WORDING: ASSISTANT; the scale-free vs calendar-time labelling is PM-DICTATED (decisions.md #8) -->

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

### 11. Dashboard display

<!-- WORDING: ASSISTANT, except the 'Window below N_report' and 'Window with zero decided offers' rows, which are PM-DICTATED -->

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

### 12. Test fixture

<!-- WORDING: table layout ASSISTANT; the displayed / not-displayed assertions are PM-DICTATED -->

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

## D4 — What in this data I would not trust

### 1. Method

153 rules in 8 check families. Findings are scored against three yardsticks: Job Board share of hires 7/26, accepted/all offers 26/36, accepted/decided offers 26/31. SCOPE rules are not scored. <!-- d4_evidence.md → audit/audit_summary.csv -->

| Check family | Rules | SYSTEMIC | HIGH | MEDIUM | SCOPE | LOW | NONE | PASS | NOT TESTABLE |
|---|---|---|---|---|---|---|---|---|---|
| 1. Coverage | 22 | 0 | 0 | 0 | 0 | 0 | 22 | 0 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 2. Referential integrity | 31 | 0 | 0 | 0 | 0 | 0 | 0 | 31 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 3. Duplicates | 11 | 0 | 3 | 0 | 0 | 0 | 1 | 6 | 1 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 4. Categorical hygiene | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 4 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 5. Temporal logic | 18 | 0 | 0 | 0 | 0 | 0 | 10 | 8 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 6. State-machine contradictions | 23 | 0 | 8 | 0 | 0 | 0 | 5 | 10 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 7. Outliers | 27 | 0 | 0 | 0 | 0 | 0 | 5 | 22 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 8. Test and synthetic records | 16 | 0 | 0 | 0 | 8 | 0 | 3 | 2 | 3 | <!-- d4_evidence.md → audit/audit_summary.csv -->

| Rating | Meaning | Rules | Distinct defects |
|---|---|---|---|
| SYSTEMIC | undermines every figure and cannot be scenario-tested | 0 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv; meaning from the src/audit.py docstring -->
| HIGH | top channel changes, or a yardstick moves ≥ 5 points | 12 | 11 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| MEDIUM | a yardstick moves ≥ 1 point | 0 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| SCOPE | PM decision: outside the evidence the claims rest on; reason recorded; no scenario scored | 8 | 8 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| LOW | a yardstick moves < 1 point | 0 | 0 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| NONE | no yardstick input changes | 46 | 37 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| PASS | nothing found, on fields that could carry the defect | 83 | 83 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| NOT TESTABLE | nothing found, but the rule inspects placeholder identifiers, so it could not fire | 4 | 4 | <!-- d4_evidence.md → audit/audit_summary.csv -->

### 2. The mutation test

- **Injected defects**, into copies of the loaded tables and into placeholder identifier fields only: <!-- src/audit.py identifier_sensitive_rules -->
  - on Candidates rows at CAND-00200 or later: one candidate's email copied onto another (duplicate email); "test.account@example.com" as an email; "Test Dummy" as a full name; "+91 0000000000" as a phone; <!-- src/audit.py identifier_sensitive_rules -->
  - on People: "Test Person" as a full name; "dummy@example.com" as a work email. <!-- src/audit.py identifier_sensitive_rules -->
- **Rules that moved:** exactly 4 of 153 — R3.1, R8.1.Candidates, R8.1.People, R8.3. <!-- d4_evidence.md → audit/audit_summary.csv (identifier_sensitive column); decisions.md #11 -->
- **Failure condition:** the run fails if a rule moves without being declared as inspecting a placeholder identifier field, or if a declared rule that found nothing does not move. <!-- src/audit.py run() -->
- **Limit:** the injection creates only the defect types those rules test for. <!-- src/audit.py identifier_sensitive_rules -->

### 3. 83 PASS vs 4 NOT TESTABLE <!-- d4_evidence.md → audit/audit_summary.csv -->

- Settled: a check that could not fail is not a pass. 88 former PASS rules became 83 PASS, 4 NOT TESTABLE and 1 SCOPE (R8.11). <!-- decisions.md #11 -->

| Rule | Finding | Why it could not fire |
|---|---|---|
| R3.1 | Candidates sharing a normalised email (lower-case, trimmed, +tag removed) | inspects placeholder identifiers (Candidates.Email) | <!-- d4_evidence.md → audit/audit_summary.csv -->
| R8.1.Candidates | Test/dummy tokens in Candidates text fields | inspects placeholder identifiers (Candidates.Email, Candidates.Full Name); it also inspects Candidates.Current Company and Candidates.Notes, which could have fired and did not | <!-- d4_evidence.md → audit/audit_summary.csv -->
| R8.1.People | Test/dummy tokens in People text fields | inspects placeholder identifiers (People.Full Name, People.Work Email) | <!-- d4_evidence.md → audit/audit_summary.csv -->
| R8.3 | Candidate phone is a placeholder (≤ 2 distinct digits or a run like 1234567890) | inspects placeholder identifiers (Candidates.Phone) | <!-- d4_evidence.md → audit/audit_summary.csv -->

- R8.1.Job Openings and R8.1.Departments stay PASS. <!-- d4_evidence.md → audit/audit_summary.csv -->

| Check family | PASS rules |
|---|---|
| 2. Referential integrity | 31 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 3. Duplicates | 6 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 4. Categorical hygiene | 4 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 5. Temporal logic | 8 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 6. State-machine contradictions | 10 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 7. Outliers | 22 | <!-- d4_evidence.md → audit/audit_summary.csv -->
| 8. Test and synthetic records | 2 | <!-- d4_evidence.md → audit/audit_summary.csv -->

### 4. HIGH: 11 distinct defects <!-- d4_evidence.md → audit/audit_summary.csv -->

Order: the audit's rank, largest yardstick movement first. On the 26-hire yardstick the top channel is a Job Board = Referral tie at 7/26. <!-- d4_evidence.md → audit/audit_summary.csv -->

| Rank | Rule | Defect | Count | % of table | Largest yardstick move (pp) | Top channel changes |
|---|---|---|---|---|---|---|
| 1 | R4.5.Candidates.Source | 'LinkedIn' can also count as 'Job Board' (taxonomy overlap) | 31 of 300 | 10.33% | 11.54 | yes, to Job Board | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_4_categorical_hygiene.csv -->
| 2 | R6.6 | Offer Pending but it carries a Decision On date | 4 of 36 | 11.11% | 11.11 | no | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 3 | R6.19 | Candidate Source is Referral but the application has no Referred By | 10 of 350 | 2.86% | 9.92 | yes, to Job Board | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 4 | R6.9 | Rejection Reason set on an application that is not Rejected/Withdrawn | 4 of 350 | 1.14% | 8.87 | yes, to Job Board | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 5 | R6.15 | Requisition with more hires than Headcount | 4 of 24 | 16.67% | 6.41 | yes, to Job Board | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 6 | R6.14 | Offer still Pending on a Cancelled or On Hold requisition | 2 of 36 | 5.56% | 5.08 | no | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 7 | R6.13 | Hire on a Cancelled or On Hold requisition | 4 of 350 | 1.14% | 4.20 | yes, to Referral | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 8 | R6.18 | Application has Referred By but the candidate's Source is not Referral | 24 of 350 | 6.86% | 3.85 | yes, to Referral | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 9 | R3.2 | Candidates sharing a normalised name + last 10 phone digits | 12 of 300 | 4.00% | 3.85 | yes, to Job Board | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_3_duplicates.csv -->
| 10 | R6.20 | Same person (name + phone) hired more than once | 4 of 350 | 1.14% | 2.24 | yes, to Job Board | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_6_state_machine_contradictions.csv -->
| 11 | R3.3 | Applications sharing (candidate record, opening) | 6 of 350 | 1.71% | 1.08 | yes, to Job Board | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_3_duplicates.csv -->

12 HIGH rules describe 11 defects: R3.4 (applications sharing person by name + phone, and opening) flags the same 6 records as R3.3. <!-- d4_evidence.md → audit/audit_summary.csv (same_defect_as); decisions.md #11 -->

### 5. SCOPE: 8 rules <!-- d4_evidence.md → audit/audit_summary.csv -->

| Rule | Finding | Count | % of table |
|---|---|---|---|
| R8.2.Candidates | Candidates.Email on a reserved placeholder domain | 300 of 300 | 100.00% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->
| R8.6 | Note says 'Referred internally...' but Source is not Referral and no Referred By exists | 34 of 300 | 11.33% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->
| R8.9 | Note says the candidate re-applied after an earlier rejection but no earlier rejection exists | 34 of 300 | 11.33% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->
| R8.7 | Note says 'Sourced from a conference list...' but Source is an inbound channel (Career Site, Job Board) | 26 of 300 | 8.67% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->
| R8.2.People | People.Work Email on a reserved placeholder domain | 14 of 14 | 100.00% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->
| R8.8 | Note says the candidate was consolidated onto one opening but two applications remain | 2 of 300 | 0.67% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->
| R8.10 | Feedback text contradicts Recommendation | 2 of 160 | 1.25% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->
| R8.11 | Feedback string with no declared polarity | 0 of 160 | 0.00% | <!-- d4_evidence.md → audit/audit_summary.csv, audit/audit_8_test_and_synthetic_records.csv -->

Why these are SCOPE, settled:
- **Placeholder identifiers (R8.2.Candidates, R8.2.People):** the graders built this base, and anonymised identifiers do not touch the structural relationships every decision rests on. <!-- decisions.md #10 -->
- **Boilerplate Notes (R8.6):** Candidates.Notes holds 7 distinct strings across 237 filled records. <!-- decisions.md #10; d4_evidence.md → audit/audit_summary.csv (R8.5.Candidates.Notes) -->
- **Every rule built on Notes or Feedback (R8.7, R8.8, R8.9, R8.10, R8.11):** boilerplate for one Notes rule is boilerplate for all of them. Interviews.Feedback holds 142 values from 12 fixed strings. <!-- decisions.md #11; d4_evidence.md → audit/audit_summary.csv (R8.5.Interviews.Feedback) -->

### 6. An output defect in this repository: rule-ID parsing

- 6 audit CSVs carry a rule_id column. <!-- d4_evidence.md → audit/audit_3_duplicates.csv, audit_5_temporal_logic.csv, audit_6_state_machine_contradictions.csv, audit_7_outliers.csv, audit_8_test_and_synthetic_records.csv, audit_summary.csv -->
- Only audit_6_state_machine_contradictions.csv had all-numeric-looking ids. Default parsing read that column as float64. <!-- d4_evidence.md: float64 UNCITED, arithmetic — re-derived from audit_6_state_machine_contradictions.csv with the R prefix stripped -->
- Its 13 distinct ids as text became 12. <!-- d4_evidence.md: 13 → audit_6_state_machine_contradictions.csv; 12 UNCITED, arithmetic — same re-derivation -->
- Rule 6.20 (4 rows, HIGH) collapsed into rule 6.2 (9 rows, NONE). Their prefixed ids today are R6.20 and R6.2. <!-- d4_evidence.md: UNCITED, arithmetic — same re-derivation; tiers from audit_summary.csv -->
- Symptom: a text lookup of rule 6.9 matched 0 of its 4 rows, and the d3 evidence draft read "0 with offers" where the answer is 3. <!-- d4_evidence.md: UNCITED, recorded in the session transcript (Stage 3 generator run, 2026-09-15) -->
- Fix: an R prefix on rule_id and same_defect_as in every audit CSV (RULE_ID_PREFIX in src/audit.py). The column now parses as text (object dtype) with 13 distinct ids. <!-- d4_evidence.md → audit/audit_6_state_machine_contradictions.csv -->

### How this changes my D1 and D2 answers

1. **It is part of why conversion carries claim 1.** Claim 1 moved to conversion because the 7-vs-7 tie between Job Board and Referral exists only on the rejected 26-hire count; on 25 hires it is Job Board 7 vs Referral 6, p = 1.0000. The audit's contribution is decision 3, which reports three channel groupings because the referral fields disagree, and whose leaders differ (Job Board 7/25 under B1, Job Board + LinkedIn 10/25 under B2, Referral 9/25 under B3); and the HIGH defects that change the top channel, including the LinkedIn overlap (R4.5) and both referral-field disagreements (R6.18, R6.19). The verdict rests on conversion, 7/195 = 3.59%. <!-- decisions.md #7, #3; 7 vs 6 and p = 1.0000: d1_evidence.md → claim1_first_vs_second_place.csv; shares: d1_evidence.md → claim1_job_board_share_of_hires.csv; channel-changing defects: d4_evidence.md HIGH table -->
2. **It moved eight findings out of the decision-relevant set entirely.** The example.com identifiers (R8.2.Candidates, R8.2.People) left because anonymised identifiers do not touch the structural relationships every decision rests on. Every rule resting on Notes or Feedback left because those fields are boilerplate, not evidence: Candidates.Notes holds 7 distinct strings across 237 records, and Interviews.Feedback 12 across 142. <!-- decisions.md #10, #11; 237/7 and 142/12: d4_evidence.md → audit/audit_summary.csv (R8.5) -->
3. **It is the reason D2 is a data-integrity roadmap rather than a feature roadmap.** Build 2 exists because the audit found the referral fields disagreeing (R6.18, 24/350; R6.19, 10/350). Build 3 exists because it found Pending offers carrying a Decision On (R6.6, 4/36) and requisitions with more hires than headcount (R6.15, 4/24). Build 1's defect is not an audit rule: Source is a Candidates field in the schema, and d2_evidence.md ranks it from claim1_referral_and_ranking_inputs.csv. The missing Rescinded status appears in the audit's categorical inventory, where no rule fires. <!-- rule counts: d4_evidence.md HIGH table; build 1 and Rescinded: d2_evidence.md ranks 1 and 4 -->

### Placeholder-data scope caveat

Inputs on record:
- 300/300 Candidates.Email and 14/14 People.Work Email are on example.com. <!-- d4_evidence.md → audit/audit_summary.csv (R8.2.Candidates, R8.2.People) -->
- All 892 records were created within 53 seconds. <!-- d4_evidence.md → audit/audit_summary.csv (R8.4) -->
- Candidates.Notes holds 237 values from 7 fixed strings; Interviews.Feedback holds 142 values from 12. <!-- d4_evidence.md → audit/audit_summary.csv (R8.5) -->
- Settled: calendar-time figures are labelled "illustration at the volume in this base", because placeholder data cannot establish absolute volume as Acme's real scale. <!-- decisions.md #8 -->
- Settled: anonymised identifiers do not touch the structural relationships every decision rests on. <!-- decisions.md #10 -->

Every candidate email (300/300) and every employee work email (14/14) is on the reserved example.com domain, all 892 records were created within 53 seconds, and the free-text fields repeat a few fixed strings (Candidates.Notes 237 values from 7, Interviews.Feedback 142 from 12). That invalidates two readings of this base. Absolute volumes do not read as Acme's real scale, which is why every calendar-time figure is labelled an illustration at the volume in this base; and Candidates.Notes and Interviews.Feedback are not evidence. It does not invalidate the structural relationships every verdict rests on: referential integrity, date ordering, state-machine consistency, and the field-level disagreements between Source and Referred By. The specific cost is four rules that could not fire on placeholder identifiers and are rated NOT TESTABLE instead of PASS: R3.1 (shared emails), R8.1.Candidates and R8.1.People (test tokens), and R8.3 (placeholder phones). <!-- counts: d4_evidence.md → audit/audit_summary.csv (R8.2, R8.4, R8.5) and NOT TESTABLE table; absolute volume: decisions.md #8; structure and Notes/Feedback: decisions.md #10, #11 -->

## D5 — Memo

<!-- One page. -->

**Duration:** approximately 20 hours across two sittings.

What would have been cut to fit the two-hour cap, settled: <!-- decisions.md #12 -->
- the 11,598-definition sweeps (2,580 for claim 1, 9,018 for claim 2), reduced to roughly twenty hand-picked definitions; <!-- decisions.md #12 -->
- the three rounds of chart fixes (page setup, label collision and background, misleading shading); <!-- decisions.md #12 -->
- 153 audit rules, where about forty would have covered the ground. <!-- decisions.md #12 -->

### What I found

1. Job-board share of applications, B1: 195/298 = 65.44% (95% CI 59.87–70.61), high confidence. <!-- d5_evidence.md → claim1_job_board_share_of_applications.csv, populations.csv -->
2. Job-board conversion, B1: 7/195 = 3.59% (95% CI 1.75–7.22), medium confidence. <!-- d5_evidence.md → claim1_conversion_by_channel.csv -->
3. Offers per period to detect a 5-point acceptance move: 1,210, scale-free, high confidence. <!-- d5_evidence.md → claim2_offers_needed_for_5pt_move.csv -->
4. Defended offer acceptance: 25/35 = 71.43% (95% CI 54.95–83.67), low confidence. <!-- d5_evidence.md → claim2_offer_acceptance.csv -->
5. Pending offers carrying a recorded Decision On: 4 of 5, high confidence. <!-- d5_evidence.md → audit/audit_summary.csv, audit/audit_4_categorical_hygiene.csv, claim2_pending_offers.csv -->
6. Hires with Source = Referral that also carry a Referred By link: 0 of 6, high confidence. <!-- d5_evidence.md → claim1_referral_fields_on_hires.csv -->

Job boards dominate volume, 195/298 applications = 65.44%, and convert at 7/195 = 3.59%. Offer acceptance is real at about 71%, 25/35 = 71.43%, and a 5-point move cannot be detected at this base's 2.92 offers a month: it needs 1,210 offers per period. The channel question could not be answered as asked, because Source sits on the candidate rather than the application. <!-- d5_evidence.md #1–#4; 2.92: d1_evidence.md → claim2_offer_volume.csv; Source on the candidate: d2_evidence.md rank 1 -->

### What I am doing about it

Moving Source from the candidate to the application, because 12/25 hires (48.00%) belong to candidates with two applications, so their channel cannot be attributed to a specific application; reconciling the two referral fields into one authoritative source, because they disagree on 9/25 hires (36.00%); and adding offer-state validation, because 4 of 5 Pending offers carry a Decision On and no Rescinded status exists, with a requisition-integrity check, because 5/26 hires are in excess of headcount (19.23%). <!-- D2 builds table and its citations -->

### What I would look at next

First, what Acme's current job-board integration costs them operationally: the data cannot show it, and it could make the VP's instinct right for reasons invisible here. Second, which referral field is authoritative, Source = Referral or the Referred By link; it decides whether Job Board or Referral leads hires. Third, how internal candidates should be identified, given that none of the 14 People full names matches a candidate full name; it decides which offers leave the external acceptance rate. <!-- notes/open_questions.md; referral leader: decisions.md #3; internal offers: D3 section 8; 0 of 14: notes/open_questions.md -->
