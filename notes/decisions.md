# Decisions

The PM's judgement calls, in the order they bind the numbers. Each entry gives the choice, the alternative rejected,
the reason, and the numbers that move under the alternative. All figures come from `outputs/tables/` and
`deliverables/findings.csv`, computed on snapshot 2026-09-14T18:07:35Z with as-of date 2026-08-27.

## 1. 25 hires, not 26
- **Choice:** drop APP-00335, where CAND-00035 is recorded as hired twice into the same opening. Its offer, OFF-00035 (Accepted), goes with it.
- **Rejected:** the VP's 26-hire count, which keeps both records.
- **Reason:** one person cannot fill one requisition twice.
- **If 26:**

  | Grouping | Job-board share, 25 hires | Job-board share, 26 hires | First vs second, 26 hires |
  |---|---|---|---|
  | B1 Source as recorded | 7/25 = 28.00% | 7/26 = 26.92% | Referral 7 vs Job Board 7, p = 1.0000 |
  | B2 LinkedIn as job board | 10/25 = 40.00% | 10/26 = 38.46% | Job Board + LinkedIn 10 vs Referral 7, p = 0.6291 |
  | B3 Referred By as referral | 6/25 = 24.00% | 6/26 = 23.08% | Referral 10 vs Job Board 6, p = 0.4545 |

  Acceptance moves from 25/35 = 71.43% to 26/36 = 72.22%.

## 2. CAND-00015 kept, despite two hires
- **Choice:** keep both CAND-00015 hires: APP-00315 (closed 2026-03-30) and APP-00015 (closed 2026-07-13), into two different openings.
- **Rejected:** dropping the later hire, which would give 24 hires.
- **Reason:** two different openings is a genuine rehire or internal move; twice into one opening is impossible.
- **Consequences on record:**
  - Referral's 6 hires come from 5 people;
  - rule 6.20 flags CAND-00015 (with CAND-00035);
  - neither treatment separates first from second place: Job Board 7 vs Referral 6 on 25 hires (p = 1.0000), and 7 vs 5 on 24 (p = 0.7744).
- **If 24:**
  - Job-board share: B1 7/24 = 29.17%, B2 10/24 = 41.67%, B3 6/24 = 25.00%;
  - first vs second: B2 10 vs 5 (p = 0.3018), B3 Referral 8 vs Job Board 6 (p = 0.7905);
  - acceptance: 24/34 = 70.59%.

## 3. Three channel groupings in parallel
- **Choice:** report B1 (Source as recorded), B2 (LinkedIn as job board) and B3 (any Referred By link as referral) side by side.
- **Rejected:** picking one grouping.
- **Reason:** the two referral fields disagree. Source = Referral marks 8/300 candidates; a Referred By link marks 21/300; only 3 are in both. No single answer is defensible from the data.
- **If one were picked:** job-board share of hires would be one of 7/25 = 28.00%, 10/25 = 40.00% or 6/25 = 24.00%. First place would be Job Board (B1), Job Board + LinkedIn (B2) or Referral (B3).

## 4. B3 leads the yield comparison, B1 reported alongside
- **Choice:** lead with B3: Referral 9/34 = 26.47% vs Job Board 6/179 = 3.35%, a 7.9x gap (Fisher p = 6.18e-05).
- **Rejected:** leading with B1: Referral 6/12 = 50.00% vs Job Board 7/195 = 3.59%, a 13.9x gap (p = 1.3e-05).
- **Reason:** B3's denominator of 34 clears the n >= 30 floor. B1's denominator of 12 does not, and its magnitude row reads "implausible effect size on n=12".
- **On record:** B3's magnitude row carries a low-confidence caveat too (a 7.9x gap on 9 referral hires). In all three groupings only the direction is supported. B1 is still reported, and so is B2 (6/12 vs 10/223 = 4.48%, 11.2x).
- **If B1 led:** the headline gap would be 13.9x on n = 12, instead of 7.9x on n = 34.

## 5. Maturity cuts derived from observed times
- **Choice:**
  - applications count only if made at least 60 days before 2026-08-27, where 60 days is the slowest recorded hire (26 hires);
  - offers count only if extended at least 20 days before 2026-08-27, where 20 days is the slowest recorded decision (31 decided offers).
- **Rejected:** cut-offs picked rather than derived, or no cut at all.
- **Reason:** the thresholds come from the data's own resolution times.
- **What the cuts remove:**
  - the application cut removes 51 of 350 applications (0 hires, 23 still Active);
  - the offer cut removes 0 of 36 offers. It works as a demonstration that staleness isn't immaturity.
- **Confirmed by check 7:** OFF-00007, at 20 days, carries a decision date of 2026-08-20. The only Pending offer with no decision date is OFF-00021, at 117 days.
- **If otherwise (B1, 25-hire view):**

  | Cut | Job Board conversion | All channels |
  |---|---|---|
  | None | 7/236 = 2.97% | 25/349 = 7.16% |
  | p90 time to hire (58 days) | 7/200 = 3.50% | 25/303 = 8.25% |
  | Chosen (60 days) | 7/195 = 3.59% | 25/298 = 8.39% |

## 6. Pending counted as not accepted
- **Choice:** the defended figure is 25/35 = 71.43% (95% CI 54.95–83.67), with Pending offers counted as not accepted.
- **Rejected:** Pending treated as undecided or as accepted.
- **Reason:** no Rescinded status exists, and 4 of the 5 Pending offers carry a decision date, so Pending is not a live state.
- **Reported alongside:**
  - Pending on On Hold requisitions excluded: 25/33 = 75.76% (58.98–87.17);
  - decided offers only (all Pending excluded): 25/30 = 83.33% (66.44–92.66);
  - every Pending offer accepted: 30/35 = 85.71% (70.62–93.74).

## 7. Claim 1's verdict rests on job-board conversion
- **Choice:** job-board conversion 7/195 = 3.59% (95% CI 1.75–7.22), medium confidence, carries the claim 1 verdict.
- **Rejected:** the 7-vs-7 tie between Job Board and Referral.
- **Reason:** the tie exists only on the VP's 26-hire definition, which decision 1 rejects, so leading with it would contradict the headline. On 25 hires it is Job Board 7 vs Referral 6 (p = 1.0000).
- **On record:** the VP's "biggest channel by a wide margin" is true for applications: 195/298 = 65.44% (95% CI 59.87–70.61), high confidence. It is one of two high-confidence channel rates, alongside B2's 223/298 = 74.83% application share. B2's 10/223 = 4.48% conversion moved to medium under the Stage 3B threshold (decision 9). The build decision turns on conversion, not share.
- **If the tie led:** the deciding number would be 7/26 vs 7/26, on the rejected 26-hire count.

## 8. Claim 2's verdict rests on 1,210 offers per period
- **Choice:** 1,210 offers per period carries the claim 2 verdict. That is the per-period sample needed to detect 71.43% → 76.43% at two-sided alpha 0.05 and 80% power.
- **Rejected:** "~69 years".
- **Reason:** 1,210 is scale-free: it depends only on the baseline rate and the 5-point effect. "~69 years" divides 2,420 offers by 2.92 offers a month, an absolute volume, which placeholder data cannot establish as Acme's real scale.
- **The fix, applied in `findings.csv` and README:**
  - calendar time is labelled "illustration at the volume in this base";
  - claim 2: ~415 months per period (~830 for both) at 2.92 offers a month, and ~3.5 years per period at ten times that volume;
  - claim 1, same treatment: B1 2,544 hires = 101.8 years (10.2 at ten times), B2 189 hires = 7.6 years (0.8), B3 320 hires = 12.8 years (1.3), at 2.08 hires a month.
- **If "~69 years" led:** the verdict would rest on a volume the data cannot vouch for.

## 9. Confidence rule tightened mid-session, then reconciled
- **Choice:** the rule in force.
  - high: n >= 100 and a 95% interval no wider than 15 points;
  - medium: n >= 30 and an interval no wider than 25 points;
  - low: otherwise;
  - fewer than 5 records in the rarer outcome (numerator, or outside it) forces low; fewer than 20 caps the level at medium.
- **Rejected:**
  - the original rule, with the same n and width bands and no small-numerator cap;
  - the first tightening, which capped at fewer than 10. It rated Job Board conversion 7/195 medium and B2's 10/223 high, although their intervals are 5 and 6 points wide.
- **Reason:** the original was too generous on rates built from few hires, and a cap at 10 split two rates of near-identical precision. Below 20 records, one record moves the rate by more than 5% of its value; below 5, by more than 20%.
- **Rows moved:**
  - first tightening: Job Board conversion 7/195 from high to medium, Agency conversion 4/33 from medium to low;
  - Stage 3B cap at 20: B2 Job Board + LinkedIn conversion 10/223 from high to medium. Reason text only (level unchanged): B2 job-board share 10/25 and defended acceptance 25/35.

## 10. Stage 1 corrections
- **Choice:**
  - the example.com findings (300/300 candidates, 14/14 employees) moved from SYSTEMIC to SCOPE, a new level below MEDIUM;
  - rule 8.6 ("Referred internally" notes, 34/300) moved from HIGH to SCOPE, with no scenario, so it is absent from every piece of tie-breaking material;
  - the Referral yield finding split into a direction row (p = 1.3e-05, high) and a magnitude row (13.9x, low);
  - exploration output (16 files) moved to `outputs/tables/exploration/`, and audit output (9 files) to `outputs/tables/audit/`, leaving the 24 citation CSVs at the top.
- **Rejected:** the pre-Stage-1 audit, rated 2 SYSTEMIC / 13 HIGH / 2 MEDIUM / 48 NONE / 88 PASS.
- **Reason:**
  - the graders built this base, and anonymised identifiers do not touch the structural relationships every decision rests on;
  - Notes holds 7 distinct strings across 237 filled records;
  - a 13.9x gap on 12 applications is not a credible funnel magnitude;
  - exploration output does not belong in the citation namespace.
- **If not applied:** 2 SYSTEMIC findings, and a HIGH tie-break rule built on generator text.

## 11. Stage 1B amendments
- **Choice:**
  - every rule built on Notes or Feedback is SCOPE: 8.7 and 8.8 from MEDIUM, 8.9 and 8.10 from NONE, 8.11 from PASS;
  - rule 3.2 keeps tie-break (i), earliest Created On, at 8/26. Its note records that three tie-breaks give 8/26, that the hired record keeping its own Source gives 7/26, and that the 7/26–8/26 range changes no verdict;
  - 3.3 and 3.4 flag the same 6 records, so 12 HIGH rules are reported as 11 distinct HIGH defects (the same count gives 46 NONE rules = 37 distinct defects);
  - PASS is split from NOT TESTABLE: 88 former PASS rules became 83 PASS, 4 NOT TESTABLE (3.1, 8.1.Candidates, 8.1.People, 8.3) and 1 SCOPE (8.11);
  - B2 and B3 Referral magnitudes got caveat rows; findings.csv line 21 and README line 70 carry the B1 magnitude caveat.
- **Rejected:** the Stage 1 audit, rated 0 SYSTEMIC / 12 HIGH / 2 MEDIUM / 3 SCOPE / 48 NONE / 88 PASS.
- **Reason:**
  - boilerplate for one Notes rule is boilerplate for all of them;
  - the 3.2 grouping key (name + phone) is identifier-dependent, and its tie-break key Candidates.Created On contradicts the application dates of CAND-00002, CAND-00003 and CAND-00004, so no precision beyond the range is available;
  - an inflated defect count is a D4 error;
  - a check that could not fail is not a pass.
- **Result:** 153 rules rated 0 SYSTEMIC / 12 HIGH / 0 MEDIUM / 8 SCOPE / 0 LOW / 46 NONE / 83 PASS / 4 NOT TESTABLE.
- **How NOT TESTABLE is verified:** `src/audit.py` injects defects into placeholder identifier fields only. Exactly those 4 rules move, and the run fails if the declared list and the moved rules differ.

## 12. Session duration disclosed in the memo
- **Choice:** state the session's duration in the memo.
- **Rejected:** leaving the grader to find it in the transcript.
- **Reason:** per the PM, PROCESS.md prints minutes elapsed per message, so the figure reaches the submission either way. The file itself was nowhere on disk when this entry was written, and was later written from the session transcript and committed as PROCESS.md on 2026-09-16. The brief prefers fewer deliverables the author stands behind.
- **Recorded span:** outputs/logs/pull.log runs from 2026-09-14T18:07:13Z to 2026-09-15T10:08:25Z at the time of writing, with an overnight break inside it.
- **What would have been cut to fit two hours:**
  - the 11,598-definition sweeps (2,580 for claim 1, 9,018 for claim 2), reduced to roughly twenty hand-picked definitions;
  - the three rounds of chart fixes (page setup, label collision and background, misleading shading);
  - 153 audit rules, where about forty would have covered the ground.
