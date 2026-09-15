# D5 evidence: six memo numbers

Confidence labels are from `deliverables/findings.csv`. Cite = the file under `outputs/tables/` holding the number. UNCITED = no file under `outputs/tables/` holds it; the mark says whether it is arithmetic on cited numbers or computed from data/raw, and gives the derivation.

| # | Value | Fraction | 95% CI | n | Why it matters | Confidence | Cite |
|---|---|---|---|---|---|---|---|
| 1 | 65.44% | 195/298 | 59.87–70.61 | 298 | job boards are the largest source of applications | high | `outputs/tables/claim1_job_board_share_of_applications.csv`, `outputs/tables/populations.csv` |
| 2 | 3.59% | 7/195 | 1.75–7.22 | 195 | job-board applications convert to hires at the lowest rate of the rated channels | medium | `outputs/tables/claim1_conversion_by_channel.csv` |
| 3 | 1,210 offers per period |  |  |  | sample needed to see a 5-point acceptance move, independent of volume | high | `outputs/tables/claim2_offers_needed_for_5pt_move.csv` |
| 4 | 71.43% | 25/35 | 54.95–83.67 | 35 | acceptance sits where the VP says, inside a wide interval | low | `outputs/tables/claim2_offer_acceptance.csv` |
| 5 | 4 of 5 |  |  | 5 | Pending offers already carry a recorded decision date | high | `outputs/tables/audit/audit_summary.csv`, `outputs/tables/audit/audit_4_categorical_hygiene.csv`, `outputs/tables/claim2_pending_offers.csv` |
| 6 | 0 of 6 |  |  | 6 | the two referral fields never agree on a hire | high | `outputs/tables/claim1_referral_fields_on_hires.csv` |
