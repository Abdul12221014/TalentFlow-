"""Render figures and citation tables from the cached snapshot. Standard library + pandas only.

    python src/report.py              # figure + one CSV per cited number   (make report)
    python src/report.py --findings   # also (over)writes the deliverables/findings.csv draft   (make findings)

Citation tables: every number the submission cites has a CSV at outputs/tables/<claim>_<metric>.csv,
and a row in the findings draft whose metric column names the same <metric>. Values are taken
from the functions in metrics.py, never retyped.

Writes outputs/figures/time_coverage.html: applications, offers and hires per month as three
small-multiple column charts on one shared month axis (never a dual axis). Each panel shades the
window too recent to have resolved, measured with metrics.resolution_times(). Hover shows the
month's count, and a table view carries every value. Colours are the dataviz reference palette's
slot 1, validated in both modes.
"""
from __future__ import annotations

import argparse
import calendar
import html
from functools import cached_property
from typing import Callable

import pandas as pd

import config
import load
import metrics

FIGURES_DIR = config.OUTPUTS_DIR / "figures"

PLOT_LEFT, PLOT_RIGHT, PANEL_HEIGHT, PLOT_TOP, PLOT_BOTTOM = 44, 16, 150, 40, 22
BAND = 42
BAR_WIDTH = 24
RADIUS = 4

STYLE = """
.viz-root { color-scheme: light; --surface-1:#fcfcfb; --page:#f9f9f7; --text-primary:#0b0b0b; --text-secondary:#52514e;
  --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7; --series-1:#2a78d6; --wash:rgba(137,135,129,0.14);
  --border:rgba(11,11,11,0.10); }
@media (prefers-color-scheme: dark) { :root:where(:not([data-theme="light"])) .viz-root { color-scheme: dark;
  --surface-1:#1a1a19; --page:#0d0d0d; --text-primary:#ffffff; --text-secondary:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --axis:#383835; --series-1:#3987e5; --wash:rgba(137,135,129,0.20); --border:rgba(255,255,255,0.10); } }
:root[data-theme="dark"] .viz-root { color-scheme: dark; --surface-1:#1a1a19; --page:#0d0d0d; --text-primary:#ffffff;
  --text-secondary:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835; --series-1:#3987e5;
  --wash:rgba(137,135,129,0.20); --border:rgba(255,255,255,0.10); }
html { background:#f9f9f7; }
@media (prefers-color-scheme: dark) { html:not([data-theme="light"]) { background:#0d0d0d; } }
html[data-theme="dark"] { background:#0d0d0d; }
body { margin:0; }
.viz-root { font:14px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif; color:var(--text-primary); background:var(--page);
  padding:24px 16px; max-width:900px; margin:0 auto; }
h1 { font-size:18px; font-weight:600; margin:0 0 4px; }
p.sub { color:var(--text-secondary); margin:0 0 16px; }
.card { background:var(--surface-1); border:1px solid var(--border); border-radius:12px; padding:12px 12px 4px; margin-bottom:12px; }
.scroll { overflow-x:auto; }
svg text { fill:var(--muted); font-size:11px; font-variant-numeric:tabular-nums; }
svg .title { fill:var(--text-primary); font-size:13px; font-weight:600; font-variant-numeric:normal; }
svg .note { fill:var(--text-secondary); font-size:11px; font-variant-numeric:normal; }
svg .value { fill:var(--text-primary); font-size:11px; }
.grid { stroke:var(--grid); stroke-width:1; }
.axis { stroke:var(--axis); stroke-width:1; }
.bar { fill:var(--series-1); }
.wash { fill:var(--wash); }
.hit { fill:transparent; }
.hit:hover + .bar, .hit:hover { fill:rgba(137,135,129,0.08); }
#tip { position:fixed; pointer-events:none; background:var(--surface-1); color:var(--text-primary); border:1px solid var(--border);
  border-radius:8px; padding:6px 8px; font-size:12px; box-shadow:0 2px 8px rgba(0,0,0,0.12); display:none; }
table { border-collapse:collapse; width:100%; font-size:12px; font-variant-numeric:tabular-nums; }
th, td { text-align:right; padding:4px 8px; border-bottom:1px solid var(--grid); }
th:first-child, td:first-child { text-align:left; }
th { color:var(--text-secondary); font-weight:600; }
details summary { cursor:pointer; color:var(--text-secondary); margin:8px 0; }
"""

SCRIPT = """
const tip = document.getElementById('tip');
document.querySelectorAll('.hit').forEach(el => {
  el.addEventListener('mousemove', e => {
    tip.textContent = el.dataset.tip; tip.style.display = 'block';
    tip.style.left = (e.clientX + 12) + 'px'; tip.style.top = (e.clientY + 12) + 'px';
  });
  el.addEventListener('mouseleave', () => { tip.style.display = 'none'; });
});
"""


def _nice_ceiling(value: int) -> tuple[int, int]:
    """(axis max, tick step) with at most four clean ticks above zero."""
    for step in (1, 2, 5, 10, 20, 25, 50, 100):
        if value / step <= 4:
            return max(step, -(-value // step) * step), step
    return value, value


def _column(x: float, y: float, w: float, h: float) -> str:
    """Column with a 4px rounded data-end, square at the baseline."""
    r = min(RADIUS, h, w / 2)
    return (f"M{x:.1f},{y + h:.1f} V{y + r:.1f} Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f} "
            f"H{x + w - r:.1f} Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f} V{y + h:.1f} Z")


def _date_x(day: pd.Timestamp, months: list[pd.Period]) -> float:
    i = months.index(day.to_period("M"))
    return PLOT_LEFT + i * BAND + (day.day - 1) / calendar.monthrange(day.year, day.month)[1] * BAND


def panel(months: list[pd.Period], values: list[int], title: str, noun: str, as_of: pd.Timestamp,
          shade: tuple[pd.Timestamp, pd.Timestamp] | None = None, note: str = "") -> str:
    width = PLOT_LEFT + BAND * len(months) + PLOT_RIGHT
    height = PLOT_TOP + PANEL_HEIGHT + PLOT_BOTTOM
    base = PLOT_TOP + PANEL_HEIGHT
    top, step = _nice_ceiling(max(values) or 1)
    y = lambda v: base - v / top * PANEL_HEIGHT  # noqa: E731

    parts = [f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" '
             f'aria-label="{html.escape(title)}">', f'<text class="title" x="0" y="14">{html.escape(title)}</text>']
    for tick in range(0, top + 1, step):
        parts.append(f'<line class="grid" x1="{PLOT_LEFT}" x2="{width - PLOT_RIGHT}" y1="{y(tick):.1f}" y2="{y(tick):.1f}"/>')
        parts.append(f'<text x="{PLOT_LEFT - 8}" y="{y(tick) + 4:.1f}" text-anchor="end">{tick}</text>')
    if shade:
        start, end = shade
        x0, x1 = _date_x(start, months), _date_x(end, months) + BAND / calendar.monthrange(end.year, end.month)[1]
        parts.append(f'<rect class="wash" x="{x0:.1f}" y="{PLOT_TOP}" width="{x1 - x0:.1f}" height="{PANEL_HEIGHT}"/>')
    if note:
        # The note rides the title line, clear of any peak label above the columns.
        parts.append(f'<text class="note" x="{width - PLOT_RIGHT}" y="14" text-anchor="end">{html.escape(note)}</text>')
    peak = values.index(max(values))
    for i, (month, v) in enumerate(zip(months, values)):
        bx = PLOT_LEFT + i * BAND + (BAND - BAR_WIDTH) / 2
        label = f"{month.strftime('%b %Y')}: {v} {noun}" + (f" (partial month, data ends {as_of.date()})" if month == as_of.to_period("M") else "")
        parts.append(f'<rect class="hit" x="{PLOT_LEFT + i * BAND}" y="{PLOT_TOP}" width="{BAND}" height="{PANEL_HEIGHT}" data-tip="{html.escape(label)}"/>')
        if v:
            parts.append(f'<path class="bar" d="{_column(bx, y(v), BAR_WIDTH, base - y(v))}" pointer-events="none"/>')
        if i == peak and v:
            parts.append(f'<text class="value" x="{bx + BAR_WIDTH / 2:.1f}" y="{y(v) - 5:.1f}" text-anchor="middle">{v}</text>')
        tick = month.strftime("%b") + (f" {month.strftime('%y')}" if month.month == 1 or i == 0 else "")
        parts.append(f'<text x="{PLOT_LEFT + i * BAND + BAND / 2:.1f}" y="{base + 15}" text-anchor="middle">{tick}</text>')
    parts.append(f'<line class="axis" x1="{PLOT_LEFT}" x2="{width - PLOT_RIGHT}" y1="{base}" y2="{base}"/>')
    parts.append("</svg>")
    return f'<div class="card scroll">{"".join(parts)}</div>'


def render_time_coverage(frames: dict[str, pd.DataFrame]) -> str:
    volume = metrics.monthly_volume(frames)
    times = metrics.resolution_times(frames)
    as_of = metrics.as_of_date(frames)
    months = [pd.Period(m, "M") for m in volume["month"]]
    hire_days = int(times.loc[metrics.TIME_TO_HIRE, "max"])
    decision_days = int(times.loc[metrics.OFFER_DECISION, "max"])
    # A record is too recent when it is younger than the slowest resolution on record. Shade only where
    # such records exist; the wash is by day, the columns are whole months.
    app_start, offer_start = as_of - pd.Timedelta(days=hire_days - 1), as_of - pd.Timedelta(days=decision_days - 1)
    recent_apps = int((frames["Applications"]["Applied On"] >= app_start).sum())
    recent_offers = int((frames["Offers"]["Offered On"] >= offer_start).sum())
    app_note = f"shaded: {recent_apps} applied in the last {hire_days} days (slowest recorded hire), outcome not yet due"
    offer_note = (f"shaded: {recent_offers} offered in the last {decision_days} days (slowest recorded decision)" if recent_offers
                  else f"no offer extended in the last {decision_days} days (slowest recorded decision)")

    panels = [
        panel(months, volume["applications"].tolist(), "Applications per month (Applied On)", "applications", as_of,
              (app_start, as_of) if recent_apps else None, app_note),
        panel(months, volume["offers"].tolist(), "Offers per month (Offers.Offered On)", "offers", as_of,
              (offer_start, as_of) if recent_offers else None, offer_note),
        panel(months, volume["hires"].tolist(), "Hires per month (Applications.Closed On, Stage = Hired)", "hires", as_of),
    ]
    header = "".join(f"<th>{html.escape(c)}</th>" for c in volume.columns)
    rows = "".join("<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in r) + "</tr>" for r in volume.itertuples(index=False))
    return f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Acme pipeline time coverage</title>
<style>{STYLE}</style>
<div class="viz-root">
  <h1>Records per month, {months[0].strftime('%b %Y')} to {months[-1].strftime('%b %Y')}</h1>
  <p class="sub">Acme Airtable snapshot. Data ends {as_of.date()} (latest Applied On, also the day every record was created),
  so {as_of.strftime('%b %Y')} is a partial month. Each panel has its own scale. Totals: {int(volume['applications'].sum())} applications,
  {int(volume['offers'].sum())} offers, {int(volume['hires'].sum())} hires.</p>
  {''.join(panels)}
  <details><summary>Table view: every month, including the alternate hire and acceptance dates</summary>
  <div class="card scroll"><table><thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table></div></details>
</div>
<div id="tip" role="tooltip"></div>
<script>{SCRIPT}</script>
"""


# ============================================================== citations: one CSV per cited number

CLAIMS = {
    "claim1": "C1 job boards: biggest channel, 26.9% of hires",
    "claim2": "C2 offer acceptance around 72%",
    "both": "Both: data provenance",
}
FINDINGS_COLUMNS = ["claim", "metric", "value", "method", "confidence"]
FINDINGS_PATH = config.ROOT / "deliverables" / "findings.csv"

HIRES_25 = "Applications with Stage='Hired', dropping APP-00335 (CAND-00035 hired again into the same opening): 25 hires"
BUCKET_METHOD = {
    "B1 Source as recorded": "channel = linked Candidates.Source",
    "B2 LinkedIn merged into Job Board": "channel = Candidates.Source with 'LinkedIn' counted as 'Job Board'",
    "B3 any Referred By link counts as Referral": "channel = Candidates.Source, set to 'Referral' when the application has Referred By",
}
BONFERRONI = metrics.ALPHA / 4  # four channel-vs-Job-Board comparisons per bucketing
SMALL_N_FLOOR = metrics.SMALL_N  # below this, a Referral magnitude is called implausible outright
SCALE_LABEL = "illustration at the volume in this base"
SCALE_METHOD = ("; calendar time is an illustration at the volume in this base, which placeholder data cannot establish as "
                "Acme's real scale, shown with the same figure at ten times that volume")


class Inputs:
    """Computed once, shared by every citation."""

    def __init__(self, frames: dict[str, pd.DataFrame]) -> None:
        self.frames = frames

    @cached_property
    def as_of(self) -> pd.Timestamp:
        return metrics.as_of_date(self.frames)

    @cached_property
    def times(self) -> pd.DataFrame:
        return metrics.resolution_times(self.frames)

    @cached_property
    def hire_days(self) -> int:
        return int(self.times.loc[metrics.TIME_TO_HIRE, "max"])

    @cached_property
    def cutoff(self) -> pd.Timestamp:
        return self.as_of - pd.Timedelta(days=self.hire_days)

    @cached_property
    def claim1_grid(self) -> pd.DataFrame:
        return metrics.claim1_table(self.frames)

    @cached_property
    def claim2_grid(self) -> pd.DataFrame:
        return metrics.claim2_table(self.frames)

    @cached_property
    def shares(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        return metrics.channel_shares(self.frames)

    @cached_property
    def volume(self) -> pd.DataFrame:
        return metrics.volume_and_yield(self.frames)

    @cached_property
    def offer(self) -> dict[str, pd.DataFrame]:
        return metrics.offer_view(self.frames)

    @cached_property
    def view_apps(self) -> pd.DataFrame:
        return metrics.view_applications(self.frames)


CITATIONS: list = []


def citation(claim: str, metric: str) -> Callable:
    """Register a function returning (table, [(variant, value, method, confidence), ...])."""
    def register(fn: Callable) -> Callable:
        CITATIONS.append((claim, metric, fn))
        return fn
    return register


def frac(k: float, n: int) -> str:
    return f"{k:g}/{n} = {100 * k / n:.2f}%"


def with_ci(k: int, n: int) -> str:
    lo, hi = metrics.wilson(k, n)
    return f"{frac(k, n)} (95% CI {100 * lo:.2f}-{100 * hi:.2f})"


RARE_FORCES_LOW = 5      # below this many records in the rarer outcome, one record moves the rate by more than 20% of itself
RARE_CAPS_MEDIUM = 20    # below this many, one record moves it by more than 5% of itself (was 10 until 2026-09-15, Stage 3B)


def rate_confidence(k: int, n: int, unit: str) -> str:
    """high: n >= 100 and interval <= 15 points; medium: n >= 30 and <= 25 points; otherwise low.

    The rarer outcome (hires, or non-hires; accepted, or not accepted) caps it: fewer than RARE_FORCES_LOW
    records is low, fewer than RARE_CAPS_MEDIUM is at most medium.
    """
    lo, hi = metrics.wilson(k, n)
    width, events = 100 * (hi - lo), min(k, n - k)
    level = "high" if n >= 100 and width <= 15 else "medium" if n >= 30 and width <= 25 else "low"
    if events < RARE_FORCES_LOW:
        level = "low"
    elif events < RARE_CAPS_MEDIUM and level == "high":
        level = "medium"
    rarer = f", only {events} {'in the numerator' if k <= n - k else 'outside the numerator'}" if events < RARE_CAPS_MEDIUM else ""
    return f"{level}: {n} {unit}, 95% interval {width:.0f} points wide{rarer}"


# ---------------------------------------------------------------- claim 1


@citation("claim1", "vp_figure_reproduced")
def _c1_vp(inp: Inputs):
    grid = inp.claim1_grid
    hits = grid[grid["reproduces"]]
    fractions = hits[["numerator", "denominator", "pct"]].drop_duplicates()
    distinct = len(grid.dropna(subset=["pct"])[["numerator", "denominator"]].drop_duplicates())
    table = fractions.assign(definitions_reproducing=len(hits), definitions_evaluated=len(grid),
                             distinct_fractions_evaluated=distinct, all_time_definitions=int((hits["window"] == "all time").sum()))
    value = "; ".join(frac(int(r.numerator), int(r.denominator)) for r in fractions.itertuples())
    others = len(fractions) - 1
    confidence = (f"high: the only one of {distinct} distinct fractions ({len(grid):,} definitions) rounding to 26.9%" if others == 0
                  else f"medium: {len(fractions)} of {distinct} distinct fractions round to 26.9%")
    method = ("Applications with Stage='Hired', all dates, duplicate kept; channel = linked Candidates.Source; "
              "Source='Job Board' rows / all rows")
    return table, [("", value, method, confidence)]


@citation("claim1", "job_board_share_of_hires")
def _c1_jb_share(inp: Inputs):
    shares, _ = inp.shares
    table = shares[[row.channel == metrics.JOB_BOARD_CHANNEL[row.bucketing] for row in shares.itertuples()]]
    rows = [(r["bucketing"], with_ci(r["hires"], r["of hires"]),
             f"{HIRES_25}; {BUCKET_METHOD[r['bucketing']]}; job-board hires / {r['of hires']}; Wilson 95% interval",
             rate_confidence(r["hires"], r["of hires"], "hires")) for r in table.to_dict("records")]
    return table, rows


@citation("claim1", "channel_ranking_by_hires")
def _c1_ranking(inp: Inputs):
    shares, separation = inp.shares
    rows = []
    for bucketing, group in shares.groupby("bucketing", sort=False):
        ranking = ", ".join(f"{r.rank}. {r.channel} {r.hires}" for r in group.itertuples())
        rows.append((bucketing, ranking, f"{HIRES_25}; {BUCKET_METHOD[bucketing]}; hires per channel, ties share a rank",
                     "low: 25 hires, and first and second place are not separable (see first_vs_second_place)"))
    return shares, rows


@citation("claim1", "first_vs_second_place")
def _c1_separation(inp: Inputs):
    _, separation = inp.shares
    col = "exact binomial p (first vs second)"
    rows = []
    for r in separation.to_dict("records"):
        k1, k2 = (int(x.split()[-1].split("/")[0]) for x in (r["first"], r["second"]))
        p = metrics.binom_two_sided(k1, k1 + k2)
        verdict = "separable" if p < metrics.ALPHA else "not separable"
        level = "high" if p >= 0.2 or p < 0.01 else "medium"
        rows.append((r["bucketing"], f"{r['first']} vs {r['second']}: p = {p:.4f}, {verdict} at 0.05",
                     f"{HIRES_25}; {BUCKET_METHOD[r['bucketing']]}; exact two-sided binomial test of first-place hires "
                     f"against a 50/50 split of first + second place hires", f"{level}: p = {p:.2f}, far from the 0.05 line"
                     if level == "high" else f"{level}: p = {p:.2f}, near the 0.05 line"))
    return separation.rename(columns={col: "exact_binomial_p"}), rows


@citation("claim1", "hires_needed_to_separate_leader")
def _c1_needed(inp: Inputs):
    _, separation = inp.shares
    cols = ["bucketing", "first", "second", "hires needed if these shares held (80% power)",
            "years at current hire volume", "current hires per month (trailing 12m)"]
    table = separation[cols]
    per_month = metrics._per_month(inp.view_apps.loc[inp.view_apps["hired"], "Closed On"], inp.as_of, 12)
    rows = [(r["bucketing"], f"{int(r[cols[3]]):,} hires ({SCALE_LABEL}: {r[cols[4]]} years at {r[cols[5]]} hires/month; "
                             f"{int(r[cols[3]]) / (10 * per_month) / 12:.1f} years at ten times that volume)",
             "n = (z_0.975 + z_0.80)^2 * (pA + pB - d^2) / d^2 with the observed first/second shares of 25 hires; "
             "hires/month = hires closed in the 12 months to 2026-08-27 / 12" + SCALE_METHOD,
             "low: assumes the observed shares are the true shares") for r in table.to_dict("records")]
    return table, rows


@citation("claim1", "job_board_share_of_applications")
def _c1_jb_apps(inp: Inputs):
    v = inp.volume
    table = v[[row.channel == metrics.JOB_BOARD_CHANNEL[row.bucketing] for row in v.itertuples()]].iloc[:2]
    total = int(v[v["bucketing"] == table.iloc[0]["bucketing"]]["applications"].sum())
    rows = [(r["bucketing"], with_ci(int(r["applications"]), total),
             f"Applications applied on or before {inp.cutoff.date()} ({inp.hire_days} days, the slowest recorded hire, before "
             f"{inp.as_of.date()}), dropping APP-00335: {total}; {BUCKET_METHOD[r['bucketing']]}; job-board applications / {total}; Wilson 95%",
             rate_confidence(int(r["applications"]), total, "applications")) for r in table.to_dict("records")]
    return table, rows


def _conversion_rows(inp: Inputs, picks: list[tuple[str, str]]) -> list:
    v = inp.volume.set_index(["bucketing", "channel"])
    rows = []
    for bucketing, channel in picks:
        r = v.loc[(bucketing, channel)]
        k, n = int(r["hires"]), int(r["applications"])
        method = (f"Applications applied on or before {inp.cutoff.date()}, dropping APP-00335; {BUCKET_METHOD[bucketing]}; "
                  f"Stage='Hired' / applications in channel; Wilson 95%; not reported below {metrics.MIN_N_FOR_RATE} applications")
        if n < metrics.MIN_N_FOR_RATE:
            rows.append((f"{bucketing}: {channel}", f"not reported ({k}/{n})", method, f"low: {n} applications cannot carry a rate"))
        else:
            rows.append((f"{bucketing}: {channel}", with_ci(k, n), method, rate_confidence(k, n, "applications")))
    return rows


@citation("claim1", "conversion_by_channel")
def _c1_conversion(inp: Inputs):
    b1 = [("B1 Source as recorded", ch) for ch in inp.volume[inp.volume["bucketing"] == "B1 Source as recorded"]["channel"]]
    picks = b1 + [("B2 LinkedIn merged into Job Board", "Job Board + LinkedIn"), ("B3 any Referred By link counts as Referral", "Referral")]
    rows = _conversion_rows(inp, picks)
    # PM decisions, 2026-09-15: the Referral yield finding is split. The direction stays with conversion_vs_job_board_p at its
    # own confidence; each grouping's magnitude gets a separate low-confidence row (B1 in Stage 1, B2 and B3 in Stage 1B),
    # and the B1 Referral rate row carries the magnitude caveat instead of an interval-only reason.
    v = inp.volume.set_index(["bucketing", "channel"])
    magnitude = {}
    for bucketing in ("B1 Source as recorded", "B2 LinkedIn merged into Job Board", "B3 any Referred By link counts as Referral"):
        jb_channel = metrics.JOB_BOARD_CHANNEL[bucketing]
        ref, jb = v.loc[(bucketing, "Referral")], v.loc[(bucketing, jb_channel)]
        rk, rn, jk, jn = int(ref["hires"]), int(ref["applications"]), int(jb["hires"]), int(jb["applications"])
        ratio = (rk / rn) / (jk / jn)
        magnitude[bucketing] = (rn, ratio)
        if rn < SMALL_N_FLOOR:
            caveat = f"low: implausible effect size on n={rn}"
        else:
            lo, hi = metrics.wilson(rk, rn)
            caveat = (f"low: a {ratio:.1f}x gap resting on {rk} referral hires out of {rn} applications "
                      f"(95% interval {100 * lo:.2f}-{100 * hi:.2f}); only the direction is supported")
        rows.append((f"{bucketing}: Referral vs {jb_channel}, magnitude", f"{frac(rk, rn)} vs {frac(jk, jn)}: {ratio:.1f}x",
                     "Referral conversion divided by job-board conversion, same applications as the rows above; the direction is "
                     "reported separately in conversion_vs_job_board_p", caveat))
    n_b1, ratio_b1 = magnitude["B1 Source as recorded"]
    rows = [(variant, value, method, f"low: implausible effect size on n={n_b1} ({ratio_b1:.1f}x Job Board); only the direction "
             f"is supported, see conversion_vs_job_board_p") if variant == "B1 Source as recorded: Referral" else (variant, value, method, conf)
            for variant, value, method, conf in rows]
    return inp.volume, rows


@citation("claim1", "conversion_vs_job_board_p")
def _c1_fisher(inp: Inputs):
    v = inp.volume.set_index(["bucketing", "channel"])
    picks = [("B1 Source as recorded", c) for c in ("Referral", "Career Site", "Agency", "LinkedIn")]
    picks += [(b, c) for b in ("B2 LinkedIn merged into Job Board", "B3 any Referred By link counts as Referral") for c in ("Referral", "Career Site")]
    records, rows = [], []
    for bucketing, channel in picks:
        r, jb = v.loc[(bucketing, channel)], v.loc[(bucketing, metrics.JOB_BOARD_CHANNEL[bucketing])]
        k, n, jk, jn = int(r["hires"]), int(r["applications"]), int(jb["hires"]), int(jb["applications"])
        p = metrics.fisher_two_sided(k, n - k, jk, jn - jk)
        records.append({"bucketing": bucketing, "channel": channel, "conversion": f"{k}/{n}", "job_board_conversion": f"{jk}/{jn}",
                        "fisher_p": p, "below_0.05": p < metrics.ALPHA, "below_bonferroni_0.0125": p < BONFERRONI})
        confidence = ("high: below the Bonferroni threshold 0.0125 for 4 comparisons" if p < BONFERRONI
                      else "medium: below 0.05 but not after Bonferroni" if p < metrics.ALPHA
                      else "low: no difference from Job Board detectable at 0.05")
        rows.append((f"{bucketing}: {channel} vs {metrics.JOB_BOARD_CHANNEL[bucketing]}", f"p = {p:.3g} ({k}/{n} vs {jk}/{jn})",
                     f"Fisher's exact test, two-sided, hires vs non-hires in the channel against the job-board channel, "
                     f"applications applied on or before {inp.cutoff.date()}", confidence))
    return pd.DataFrame(records), rows


@citation("claim1", "referral_fields_on_hires")
def _c1_referral_fields(inp: Inputs):
    hires = inp.view_apps[inp.view_apps["hired"]]
    is_ref = hires["source"] == "Referral"
    table = pd.crosstab(hires["source"], hires["referred"].map({True: "has Referred By", False: "no Referred By"})).reset_index()
    rows = [
        ("Source='Referral' hires with a Referred By link", f"{int((is_ref & hires['referred']).sum())} of {int(is_ref.sum())}",
         f"{HIRES_25}; count hires by Candidates.Source = 'Referral' and Applications.Referred By present",
         "high: exact count; which of the two fields is correct cannot be determined"),
        ("other hires with a Referred By link", f"{int((~is_ref & hires['referred']).sum())} of {int((~is_ref).sum())}",
         f"{HIRES_25}; hires whose Source is not 'Referral' but whose application has Referred By",
         "high: exact count; which of the two fields is correct cannot be determined"),
    ]
    return table, rows


@citation("claim1", "duplicate_hire_records")
def _c1_duplicates(inp: Inputs):
    apps = inp.frames["Applications"]
    dropped = apps[apps["id"].isin(metrics.duplicate_hire_applications(inp.frames))]
    kept = apps[apps.set_index(["Candidate", "Opening"]).index.isin(dropped.set_index(["Candidate", "Opening"]).index) & ~apps["id"].isin(dropped["id"])]
    table = pd.concat([kept.assign(role="kept"), dropped.assign(role="dropped")])[["role", "id", "Application ID", "Stage", "Applied On", "Closed On"]]
    ids = ", ".join(dropped["Application ID"])
    return table, [("", f"{len(dropped)} record dropped ({ids})",
                    "Stage='Hired' applications sharing (Candidate, Opening) with an earlier hired application; the earliest is kept",
                    "medium: same person and requisition months apart; a genuine re-hire cannot be ruled out")]


@citation("claim1", "recent_applications_excluded")
def _c1_tail(inp: Inputs):
    tail = metrics.application_tail(inp.frames, inp.as_of, inp.times)
    r = tail[tail["cohort"].str.contains("slowest observed hire")].iloc[0]
    return tail, [("", f"{r['tail applications']} applied after {r['applied_on_or_before']}: {r['tail hires']} hires, "
                   f"{r['tail still Active']} still Active",
                   f"Applied On later than {inp.as_of.date()} minus {inp.hire_days} days (slowest Applied On -> Closed On among Stage='Hired')",
                   f"medium: exact counts, but the {inp.hire_days}-day window rests on {int(inp.times.loc[metrics.TIME_TO_HIRE, 'n'])} hires")]


@citation("claim1", "stale_active_applications")
def _c1_stale(inp: Inputs):
    tail = metrics.application_tail(inp.frames, inp.as_of, inp.times)
    r = tail[tail["cohort"].str.contains("slowest observed hire")].iloc[0]
    active = int((inp.frames["Applications"]["Status"] == "Active").sum())
    return tail, [("", f"{r['cohort still Active']} of {active} Active applications applied on or before {r['applied_on_or_before']}",
                   f"Applications with Status='Active' and Applied On at least {inp.hire_days} days (slowest recorded hire) before {inp.as_of.date()}",
                   "high: exact counts")]


# ---------------------------------------------------------------- claim 2

OFFERS_35 = "Offers dropping APP-00335's offer, all offered at least 20 days (slowest recorded decision) before 2026-08-27: 35 offers"


@citation("claim2", "vp_figure_reproduced")
def _c2_vp(inp: Inputs):
    grid = inp.claim2_grid
    hits = grid[grid["reproduces"]]
    fractions = hits[["numerator", "denominator", "pct"]].drop_duplicates()
    table = fractions.assign(definitions_reproducing=len(hits), definitions_evaluated=len(grid))
    offers = inp.frames["Offers"]
    k, n = int((offers["Status"] == "Accepted").sum()), len(offers)
    return table, [("", frac(k, n), "All Offers records, duplicate kept; Status='Accepted' / all, Pending counted as not accepted "
                    "(equals Applications Stage='Hired' / Stage in ('Hired','Offer'))",
                    f"medium: reproduces exactly, but {len(fractions) - 1} other distinct fractions also round to 72%")]


@citation("claim2", "offer_acceptance")
def _c2_acceptance(inp: Inputs):
    table = inp.offer["acceptance"]
    methods = {
        "DEFENDED": f"{OFFERS_35}; Status='Accepted' / 35, stale Pending counted as not accepted; Wilson 95%",
        "sensitivity: Pending on On Hold": f"{OFFERS_35}; as defended but Pending offers on On Hold requisitions removed; Wilson 95%",
        "sensitivity: Pending excluded": f"{OFFERS_35}; Accepted / (Accepted + Declined); Wilson 95%",
        "bound: every Pending": f"{OFFERS_35}; (Accepted + Pending) / 35; Wilson 95%",
    }
    rows = []
    for r in table.to_dict("records"):
        key = next((k for k in methods if r["definition"].startswith(k)), None)
        if key:
            label = "defended" if key == "DEFENDED" else r["definition"].split(":")[0] + ": " + r["definition"].split(": ", 1)[1]
            rows.append((label, with_ci(r["accepted"], r["offers"]), methods[key], rate_confidence(r["accepted"], r["offers"], "offers")))
    return table, rows


@citation("claim2", "pending_offers")
def _c2_pending(inp: Inputs):
    table = metrics.unresolved_offers(inp.frames, inp.as_of, metrics.snapshot_date())
    age = table[f"age days at {inp.as_of.date()}"]
    return table, [("", f"{len(table)} of 35 offers Pending, aged {age.min()}-{age.max()} days at {inp.as_of.date()}; "
                    f"{int(table['has Decision On'].sum())} carry a Decision On", "Offers with Status='Pending'; age = as-of date minus Offered On",
                    "high: exact counts")]


@citation("claim2", "slowest_offer_decision")
def _c2_decision(inp: Inputs):
    t = inp.times.loc[[metrics.OFFER_DECISION]].reset_index()
    r = t.iloc[0]
    return t, [("", f"{r['max']} days (median {r['p50']}, n = {r['n']} decided offers)",
                "Decision On minus Offered On for all Offers records with Status in ('Accepted','Declined')",
                "medium: only decided offers are observed, so the true slowest may be longer")]


@citation("claim2", "offer_volume")
def _c2_volume(inp: Inputs):
    per_12, per_6 = inp.offer["sample_size"].attrs["rates"]
    table = pd.DataFrame([{"window": "trailing 12 months", "offers_per_month": round(per_12, 2)},
                          {"window": "trailing 6 months", "offers_per_month": round(per_6, 2)}]).assign(as_of=inp.as_of.date())
    return table, [("", f"{per_12:.2f} offers/month (trailing 12 months), {per_6:.2f} (trailing 6 months)",
                    "Offers dropping APP-00335's offer with Offered On in the 12 (6) months to 2026-08-27, divided by 12 (6)",
                    "medium: past volume; future volume may differ")]


@citation("claim2", "offers_needed_for_5pt_move")
def _c2_sample(inp: Inputs):
    table = inp.offer["sample_size"].copy()
    acc = inp.offer["acceptance"].iloc[0]
    p, (lo, hi) = acc["accepted"] / acc["offers"], metrics.wilson(int(acc["accepted"]), int(acc["offers"]))
    span = [metrics.n_two_proportions(b, b + metrics.TARGET_MOVE) for b in (lo, hi)]
    table.attrs = {}
    rows = []
    for r in table.to_dict("records")[:4]:
        if r["question"].startswith("compare two periods") and "->" in r["question"] and float(r["question"].split("-> ")[1][:-1]) < 100 * p:
            continue  # the downward move is kept in the CSV; the submission cites the upward one
        confidence = (f"high: out of reach at any baseline in the 95% interval ({min(span):,}-{max(span):,} per period)"
                      if r["question"].startswith("compare") else "medium: ignores uncertainty in the baseline rate"
                      if r["question"].startswith("one new period") else "high: standard formula; describes precision, not a test")
        per_month = r["offers in total"] / r["months at trailing-12m volume"]
        per_period_months = r["offers per period"] / per_month
        if r["periods"] > 1:
            size = (f"{r['offers per period']:,} offers per period ({r['offers in total']:,} total); {SCALE_LABEL}: "
                    f"~{per_period_months:.0f} months per period (~{r['months at trailing-12m volume']:.0f} for both) at "
                    f"{per_month:.2f} offers/month; ~{per_period_months / 10 / 12:.1f} years per period at ten times that volume")
        else:
            size = (f"{r['offers in total']:,} offers; {SCALE_LABEL}: ~{per_period_months:.0f} months at {per_month:.2f} offers/month; "
                    f"~{per_period_months / 10 / 12:.1f} years at ten times that volume")
        rows.append((r["question"], size,
                     f"Baseline {p:.2%} (defended acceptance); normal approximation, two-sided alpha 0.05, power 80%, no continuity "
                     f"correction; months = offers / offers per month" + SCALE_METHOD, confidence))
    return table, rows


@citation("claim2", "minimum_detectable_move")
def _c2_mde(inp: Inputs):
    table = inp.offer["sample_size"]
    r = table[table["question"].str.startswith("smallest")].iloc[0]
    acc = inp.offer["acceptance"].iloc[0]
    p = acc["accepted"] / acc["offers"]
    d = metrics.mde_two_proportions(p, int(r["offers per period"]))
    value = ("no move below 100% is detectable" if d is None
             else f"{100 * d:.1f} points ({p:.1%} -> {p + d:.1%})") + f" comparing two 12-month periods of ~{r['offers per period']} offers ({SCALE_LABEL})"
    return table[table["question"].str.startswith("smallest")], [
        ("", value,
         "Smallest upward move d with per-period n for p -> p + d (alpha 0.05 two-sided, power 80%) <= offers in 12 months at trailing-12m volume",
         "medium: the normal approximation is rough at ~35 offers per period")]


@citation("claim2", "declines_by_reason")
def _c2_declines(inp: Inputs):
    table = inp.offer["declines"]
    declined = table[table["group"] == "Declined offers"]
    pending = table[table["group"] != "Declined offers"]
    return table, [
        ("Declined offers", ", ".join(f"{r.reason} {r.offers}" for r in declined.itertuples()) + f" (of {int(declined['offers'].sum())})",
         f"{OFFERS_35}; Status='Declined', grouped by Decline Reason", "low: 5 declines cannot rank reasons; counts only, no percentages"),
        ("Pending offers without a reason", f"{int(pending['offers'].sum())} non-accepted Pending offers have no Decline Reason",
         f"{OFFERS_35}; Status='Pending', by requisition status and application Rejection Reason", "high: exact count"),
    ]


# ---------------------------------------------------------------- both claims: provenance


@citation("both", "placeholder_contact_data")
def _b_placeholder(inp: Inputs):
    records = []
    for table, field in [("Candidates", "Email"), ("People", "Work Email")]:
        domain = inp.frames[table][field].str.split("@").str[-1].str.lower()
        records.append({"table": table, "field": field, "records": len(domain), "example_com": int((domain == "example.com").sum())})
    table = pd.DataFrame(records)
    value = "; ".join(f"{r['example_com']}/{r['records']} {r['table']}.{r['field']} on example.com" for r in records)
    return table, [("", value, "Domain after '@' in Candidates.Email and People.Work Email",
                    "high: exact count; whether the base is anonymised or generated is unknown")]


@citation("both", "bulk_created_records")
def _b_bulk(inp: Inputs):
    stamps = pd.concat([df["createdTime"] for df in inp.frames.values() if len(df)])
    span = (stamps.max() - stamps.min()).total_seconds()
    table = pd.DataFrame([{"records": len(stamps), "first_created": stamps.min(), "last_created": stamps.max(), "span_seconds": span}])
    return table, [("", f"{len(stamps)} records created within {span:.0f} seconds on {stamps.min().date()} (UTC)",
                    "Max minus min of the top-level createdTime across every record in every table", "high: exact")]


@citation("both", "templated_free_text")
def _b_templates(inp: Inputs):
    records = [{"table": t, "field": f, "values": int(inp.frames[t][f].notna().sum()), "distinct": int(inp.frames[t][f].nunique())}
               for t, f in [("Candidates", "Notes"), ("Interviews", "Feedback")]]
    return pd.DataFrame(records), [("", "; ".join(f"{r['table']}.{r['field']}: {r['values']} values from {r['distinct']} distinct strings" for r in records),
                                    "Non-empty values and distinct strings per field", "high: exact counts")]


@citation("both", "findings_table_records")
def _b_findings(inp: Inputs):
    n = len(inp.frames["Findings"])
    return pd.DataFrame([{"table": "Findings", "records": n}]), [
        ("", f"{n} records", "Record count of the Findings table in data/raw/findings.json",
         "high: exact; its fields cannot be listed without schema scope")]


# ============================================================== supporting citation tables (Stage 3B)


def _chain(population: str, frame: pd.DataFrame, steps: list) -> list:
    """One row per filter step with the count after it. steps: (label, keep-mask function)."""
    rows = [{"population": population, "step": 0, "rule": "start", "removed": "", "count_after": len(frame)}]
    for i, (label, keep) in enumerate(steps, 1):
        kept = frame[keep(frame)]
        rows.append({"population": population, "step": i, "rule": label, "removed": len(frame) - len(kept), "count_after": len(kept)})
        frame = kept
    return rows


def populations_table(inp: Inputs) -> pd.DataFrame:
    """The derivation of every cited denominator."""
    apps, offers, interviews = inp.frames["Applications"], inp.frames["Offers"], inp.frames["Interviews"]
    openings = inp.frames["Job Openings"].set_index("id")["Status"]
    dup = metrics.duplicate_hire_applications(inp.frames)
    dup_label = ", ".join(apps.loc[apps["id"].isin(dup), "Application ID"])
    dup_offer = ", ".join(offers.loc[offers["Application"].isin(dup), "Offer ID"])
    p90_days = int(inp.times.loc[metrics.TIME_TO_HIRE, "p90"])
    decision_days = int(inp.times.loc[metrics.OFFER_DECISION, "max"])
    cut = lambda days: inp.as_of - pd.Timedelta(days=days)  # noqa: E731
    not_dup = (f"not a duplicate hire record ({dup_label}: CAND-00035 hired again into the same opening)", lambda d: ~d["id"].isin(dup))
    cand_id = inp.frames["Candidates"].set_index("id")["Candidate ID"]
    c15_later = apps[(apps["Candidate"].map(cand_id) == "CAND-00015") & (apps["Stage"] == "Hired")].sort_values("Applied On")["id"].iloc[1:]
    rows = []
    rows += _chain("applications, conversion cohort (denominator of 195/298)", apps, [
        (f"Applied On on or before {cut(inp.hire_days).date()} ({inp.as_of.date()} minus {inp.hire_days} days, the slowest recorded hire)",
         lambda d: d["Applied On"] <= cut(inp.hire_days)), not_dup])
    rows += _chain("applications, p90 cut (denominator of 25/303)", apps, [
        (f"Applied On on or before {cut(p90_days).date()} ({inp.as_of.date()} minus {p90_days} days, the p90 time to hire)",
         lambda d: d["Applied On"] <= cut(p90_days)), not_dup])
    rows += _chain("applications, no cut (denominator of 25/349)", apps, [not_dup])
    rows += _chain("hires (denominator of 7/25)", apps, [("Stage = Hired", lambda d: d["Stage"] == "Hired"), not_dup])
    rows += _chain("hires, CAND-00015 alternative (denominator of 10/24)", apps, [
        ("Stage = Hired", lambda d: d["Stage"] == "Hired"), not_dup,
        ("not CAND-00015's later hire (" + ", ".join(apps.loc[apps["id"].isin(c15_later), "Application ID"]) + ")", lambda d: ~d["id"].isin(c15_later))])
    offer_steps = [
        (f"not the offer on the duplicate hire record ({dup_offer})", lambda d: ~d["Application"].isin(dup)),
        (f"Offered On on or before {cut(decision_days).date()} ({inp.as_of.date()} minus {decision_days} days, the slowest recorded decision)",
         lambda d: d["Offered On"] <= cut(decision_days))]
    rows += _chain("offers, defended (denominator of 25/35)", offers, offer_steps)
    rows += _chain("offers, decided only (denominator of 25/30)", offers, offer_steps + [("Status is not Pending", lambda d: d["Status"] != "Pending")])
    rows += _chain("offers, On Hold Pending excluded (denominator of 25/33)", offers, offer_steps + [
        ("not a Pending offer on an On Hold requisition",
         lambda d: ~((d["Status"] == "Pending") & (d["Application"].map(apps.set_index("id")["Opening"]).map(openings) == "On Hold")))])
    rows += _chain("Active applications (82/105)", apps, [
        ("Status = Active", lambda d: d["Status"] == "Active"),
        (f"Applied On on or before {cut(inp.hire_days).date()}", lambda d: d["Applied On"] <= cut(inp.hire_days))])
    rows += _chain("completed interviews (denominator of 4/142)", interviews, [("Completed On present", lambda d: d["Completed On"].notna())])
    return pd.DataFrame(rows)


def ranking_inputs_table(inp: Inputs) -> pd.DataFrame:
    """Numbers behind the D2 ranking and the referral argument, previously computed only in session scripts."""
    import audit  # noqa: WPS433 (the audit module owns the note text and the name + phone key)
    frames = inp.frames
    cands, apps = frames["Candidates"], frames["Applications"]
    view = inp.view_apps
    hires = view[view["hired"]]
    rows = []

    def add(metric, k, n, definition, value=None):
        rows.append({"metric": metric, "numerator": k, "denominator": n,
                     "value": value if value is not None else f"{100 * k / n:.2f}%", "definition": definition})

    by_source = set(cands.loc[cands["Source"] == "Referral", "id"])
    by_link = set(apps.loc[apps["Referred By"].notna(), "Candidate"])
    add("candidates with Source = Referral", len(by_source), len(cands), "Candidates.Source == 'Referral'")
    add("candidates with a Referred By link on any application", len(by_link), len(cands), "any Applications.Referred By present")
    add("candidates in both", len(by_source & by_link), len(cands), "intersection of the two sets above")
    referred_any = apps.groupby("Candidate")["Referred By"].agg(lambda s: s.notna().any())
    rule86 = cands[(cands["Notes"] == audit.NOTE_REFERRED) & (cands["Source"] != "Referral") & ~cands["id"].map(referred_any).fillna(False).astype(bool)]
    add("rule 8.6 records (SCOPE)", len(rule86), len(cands), "Notes = 'Referred internally...', Source not Referral, no Referred By on any application")
    two = set(cands.loc[cands["Applications"].map(len) == 2, "id"])
    add("candidates with 2 applications", len(two), len(cands), "len(Candidates.Applications) == 2")
    add("applications belonging to them", int(apps["Candidate"].isin(two).sum()), len(apps), "Applications.Candidate in that set")
    add("hires whose candidate has 2 applications", int(hires["Candidate"].isin(two).sum()), len(hires), "25-hire basis")
    ref_no_link = hires[(hires["source"] == "Referral") & ~hires["referred"]]
    link_other = hires[(hires["source"] != "Referral") & hires["referred"]]
    add("hires with Source = Referral and no Referred By", len(ref_no_link), len(hires), "25-hire basis")
    add("hires with a Referred By link and Source not Referral", len(link_other), len(hires), "25-hire basis")
    add("hires where the two referral fields disagree", len(ref_no_link) + len(link_other), len(hires), "sum of the two rows above")
    name_phone = audit.Context(frames).candidates.set_index("id")["name_phone"]
    dup_people = set(name_phone[name_phone.duplicated(keep=False)].index)
    add("hires among rule 3.2 candidate records", int(hires["Candidate"].isin(dup_people).sum()), len(hires), "candidates sharing name + last 10 phone digits")
    cand_id = cands.set_index("id")["Candidate ID"]
    c15_later = hires[hires["Candidate"].map(cand_id) == "CAND-00015"].sort_values("Applied On")["id"].iloc[1:]
    bases = {"24 hires": view[~view["id"].isin(c15_later)], "26 hires": apps.assign(
        source=lambda d: d["Candidate"].map(cands.set_index("id")["Source"]).astype(object),
        referred=lambda d: d["Referred By"].notna().astype(bool), hired=lambda d: (d["Stage"] == "Hired").astype(bool))}
    for basis, frame in bases.items():
        basis_hires = frame[frame["hired"]]
        for name, bucket in metrics.BUCKETINGS.items():
            counts = bucket(basis_hires).value_counts()
            jb = int(counts.get(metrics.JOB_BOARD_CHANNEL[name], 0))
            if basis == "24 hires":
                add(f"job-board share, {basis}, {name}", jb, len(basis_hires), "decision 2 alternative: CAND-00015's later hire also dropped")
            (c1, k1), (c2, k2) = list(counts.items())[:2]
            add(f"first vs second, {basis}, {name}: {c1} {int(k1)} vs {c2} {int(k2)}", int(k1), int(k1 + k2),
                "exact two-sided binomial of first-place hires against a 50/50 split", f"p = {metrics.binom_two_sided(int(k1), int(k1 + k2)):.4f}")
    return pd.DataFrame(rows)


def sample_size_derivation(inp: Inputs) -> pd.DataFrame:
    """The 1,210 offers per period, term by term."""
    acc = inp.offer["acceptance"].iloc[0]
    p1 = acc["accepted"] / acc["offers"]
    p2 = p1 + metrics.TARGET_MOVE
    pbar = (p1 + p2) / 2
    term_a = metrics.Z_ALPHA * (2 * pbar * (1 - pbar)) ** 0.5
    term_b = metrics.Z_POWER * (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5
    raw = (term_a + term_b) ** 2 / (p2 - p1) ** 2
    rows = [
        ("p1", f"accepted / offers = {acc['accepted']}/{acc['offers']} (defended rate)", p1),
        ("p2", "p1 + 0.05 (the 5-point move)", p2),
        ("p_bar", "(p1 + p2) / 2, the pooled proportion", pbar),
        ("z_0.975", "standard normal quantile for two-sided alpha 0.05", metrics.Z_ALPHA),
        ("z_0.80", "standard normal quantile for 80% power", metrics.Z_POWER),
        ("alpha_term", "z_0.975 * sqrt(2 * p_bar * (1 - p_bar)), pooled variance", term_a),
        ("power_term", "z_0.80 * sqrt(p1 * (1 - p1) + p2 * (1 - p2)), unpooled variance", term_b),
        ("n_before_rounding", "(alpha_term + power_term)^2 / (p2 - p1)^2, no continuity correction", raw),
        ("n_per_period", "n_before_rounding rounded up; equals metrics.n_two_proportions and claim2_offers_needed_for_5pt_move.csv",
         float(metrics.n_two_proportions(p1, p2))),
    ]
    return pd.DataFrame([{"term": t, "formula": f, "value": round(v, 6)} for t, f, v in rows])


# ============================================================== writers and entry point


def build_citations(frames: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    inp = Inputs(frames)
    tables, findings = {}, []
    for claim, metric, fn in CITATIONS:
        table, rows = fn(inp)
        tables[f"{claim}_{metric}.csv"] = table
        for variant, value, method, confidence in rows:
            findings.append({"claim": CLAIMS[claim], "metric": f"{metric} [{variant}]" if variant else metric,
                             "value": value, "method": method, "confidence": confidence})
    return tables, pd.DataFrame(findings, columns=FINDINGS_COLUMNS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--findings", action="store_true", help="also write the deliverables/findings.csv draft")
    args = parser.parse_args()

    frames = load.load_all()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    figure = FIGURES_DIR / "time_coverage.html"
    figure.write_text(render_time_coverage(frames), encoding="utf-8")
    print(f"wrote {figure}")

    tables, findings = build_citations(frames)
    inp = Inputs(frames)
    tables.update({
        "populations.csv": populations_table(inp),
        "claim1_referral_and_ranking_inputs.csv": ranking_inputs_table(inp),
        "claim2_sample_size_derivation.csv": sample_size_derivation(inp),
    })
    for name, table in tables.items():
        table.to_csv(config.TABLES_OUT_DIR / name, index=False)
    print(f"wrote {len(tables)} citation tables to {config.TABLES_OUT_DIR} ({len(findings)} cited numbers)")
    if args.findings:
        findings.to_csv(FINDINGS_PATH, index=False)
        print(f"wrote {FINDINGS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
