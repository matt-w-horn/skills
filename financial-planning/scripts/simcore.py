#!/usr/bin/env python3
"""simcore: scaffolding primitives for financial-plan simulation.

Pure standard library. This module is deliberately primitives-only: return
generators, a year-ledger engine driven by a flow policy, a guardrail
spending policy, and summary utilities. Plan-specific logic (phases,
accounts, jurisdiction rules) is written per run as a small module that
composes these pieces, and that bespoke module must ship with its own tests
(see references/modeling.md). Do not extend this file mid-run; bespoke
logic lives beside it so the tested core stays tested.

Conventions:
- Real (inflation-adjusted) terms everywhere; returns are real returns.
- Returns are decimals (0.06 == 6%).
- Ledger order within a year: apply the return, then the net flow.
  Positive flow = contribution; negative flow = withdrawal.
- Wealth is clamped at zero; the realized flow record preserves the exact
  accounting identity even when a withdrawal is truncated by depletion.

Run this module's tests before trusting anything built on it:
    python3 -m unittest discover tests
"""

import csv
import math
import random
import statistics

PCTS = (10, 25, 50, 75, 90)


# ---------------------------------------------------------------- randomness

def rng(seed=None):
    """A seedable random source; pass one per simulation for reproducibility."""
    return random.Random(seed)


def lognormal_params(mean, std):
    """Fit lognormal on (1+r) from the arithmetic mean/std of the return.

    Returns (mu, sigma) such that exp(N(mu, sigma)) - 1 has arithmetic mean
    `mean` and standard deviation `std`.
    """
    m = 1.0 + mean
    sigma2 = math.log(1.0 + (std * std) / (m * m))
    return math.log(m) - sigma2 / 2.0, math.sqrt(sigma2)


def lognormal_returns(r, mean, std, n_years):
    """n_years of lognormal real returns with the given arithmetic moments."""
    mu, sig = lognormal_params(mean, std)
    return [math.exp(r.gauss(mu, sig)) - 1.0 for _ in range(n_years)]


# ---------------------------------------------------------- historical data

def load_returns_csv(path, value_col=1):
    """Load an annual return series from CSV (header row; returns as decimals).

    Expected shape: year,value rows, e.g. "1966,-0.132". Record the source
    and retrieval date of any series you load in the facts register.
    """
    out = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            if row and row[value_col].strip():
                out.append(float(row[value_col]))
    return out


def historical_windows(returns, n_years):
    """All overlapping n_years-long windows, oldest start first.

    This is the 'your plan, started in every year of history' pass; the
    number of windows is len(returns) - n_years + 1.
    """
    if n_years > len(returns):
        raise ValueError("window longer than series")
    return [returns[i:i + n_years] for i in range(len(returns) - n_years + 1)]


def block_bootstrap(r, returns, n_years, block=5):
    """Sample n_years by drawing contiguous blocks, preserving short-run
    clustering that independent draws destroy."""
    out = []
    while len(out) < n_years:
        start = r.randrange(0, max(1, len(returns) - block + 1))
        out.extend(returns[start:start + block])
    return out[:n_years]


def blend(series_a, series_b, weight_a):
    """Year-by-year weighted blend of two return series (e.g. stocks/bonds)."""
    if len(series_a) != len(series_b):
        raise ValueError("series lengths differ")
    wb = 1.0 - weight_a
    return [weight_a * a + wb * b for a, b in zip(series_a, series_b)]


# ------------------------------------------------------------------- ledger

def simulate_ledger(start_wealth, returns, policy):
    """Run the year ledger. `policy(t, wealth)` returns the requested net
    flow for year t given wealth *after* that year's return.

    Returns (wealth_path, realized_flows). The identity
        wealth[t] == wealth[t-1] * (1 + returns[t]) + realized_flows[t]
    holds exactly; when depletion truncates a withdrawal, realized_flows
    records the truncated amount, so conservation checks always pass and
    realized spending can be recovered honestly.
    """
    path, realized = [], []
    w = float(start_wealth)
    for t, r in enumerate(returns):
        grown = w * (1.0 + r)
        flow = policy(t, grown)
        w = grown + flow
        if w < 0.0:
            flow = -grown
            w = 0.0
        path.append(w)
        realized.append(flow)
    return path, realized


def check_conservation(start_wealth, returns, realized_flows, path, tol=1e-6):
    """Assert the ledger identity year by year; raises AssertionError on
    violation. Use this in every bespoke module's tests."""
    w = float(start_wealth)
    for t, r in enumerate(returns):
        w = w * (1.0 + r) + realized_flows[t]
        w = max(w, 0.0)
        assert abs(w - path[t]) <= tol, f"conservation broken at year {t}"
    return True


# ----------------------------------------------------------------- policies

class GuardrailPolicy:
    """Adaptive drawdown: spend a base amount, cut when the withdrawal rate
    drifts too far above its initial value, raise when far below.

    Call with t = years since drawdown began. `income(t)` (callable, list,
    or constant) offsets the withdrawal (state benefits, part-time work).
    `realized_spending` records the intended spend each year; recover
    truncated spending from the ledger's realized flows when depletion
    matters. Survival under this policy is high by construction; the
    spending distribution is the honest risk output.
    """

    def __init__(self, spending, income=0, cut_trigger=1.2, raise_trigger=0.8,
                 adjust_pct=0.10, active_years=30, floor=None):
        self.spending = float(spending)
        self._income = income
        self.cut = cut_trigger
        self.raise_ = raise_trigger
        self.adjust = adjust_pct
        self.active_years = active_years
        self.floor = floor
        self.initial_wr = None
        self.realized_spending = []

    def income_at(self, t):
        if callable(self._income):
            return float(self._income(t))
        if isinstance(self._income, (list, tuple)):
            return float(self._income[t]) if t < len(self._income) else float(self._income[-1])
        return float(self._income)

    def __call__(self, t, wealth):
        if self.initial_wr is None:
            self.initial_wr = self.spending / wealth if wealth > 0 else None
        elif 0 < t < self.active_years and wealth > 0 and self.initial_wr:
            wr = self.spending / wealth
            if wr > self.cut * self.initial_wr:
                self.spending *= (1.0 - self.adjust)
            elif wr < self.raise_ * self.initial_wr:
                self.spending *= (1.0 + self.adjust)
            if self.floor is not None:
                self.spending = max(self.spending, float(self.floor))
        self.realized_spending.append(self.spending)
        return self.income_at(t) - self.spending


def phase_policy(phases):
    """Compose a policy from sequential phases: [(n_years, flow), ...] where
    flow is a constant net amount or a policy callable. Callable phases
    receive t relative to their own start, so a GuardrailPolicy can be a
    phase. Years beyond the last phase reuse the last phase's flow.
    """
    starts, entries = [], []
    t0 = 0
    for n_years, flow in phases:
        starts.append(t0)
        entries.append(flow)
        t0 += n_years
    ends = starts[1:] + [float("inf")]

    def policy(t, wealth):
        for start, end, flow in zip(starts, ends, entries):
            if start <= t < end:
                return flow(t - start, wealth) if callable(flow) else float(flow)
        return 0.0

    return policy


# ---------------------------------------------------------------- summaries

def percentile(values, p):
    values = sorted(values)
    k = (len(values) - 1) * p / 100.0
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return values[int(k)]
    return values[f] + (values[c] - values[f]) * (k - f)


def summarize(wealth_paths, start_age, every=5, extra_ages=()):
    """Percentile wealth at checkpoint ages across many simulated paths."""
    n_years = len(wealth_paths[0])
    ages = [start_age + i for i in range(n_years)]
    marks = {a for a in ages if (a - start_age) % every == 0} | set(extra_ages)
    out = {}
    for a in sorted(marks & set(ages)):
        col = [wp[a - start_age] for wp in wealth_paths]
        out[a] = {p: percentile(col, p) for p in PCTS}
    return out


def spending_summary(spend_lists):
    """Percentiles of first-year and lifetime-average spending across sims."""
    first = [s[0] for s in spend_lists if s]
    life = [statistics.fmean(s) for s in spend_lists if s]
    return {
        "first_year": {p: percentile(first, p) for p in PCTS},
        "lifetime_avg": {p: percentile(life, p) for p in PCTS},
    }
