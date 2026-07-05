#!/usr/bin/env python3
"""Monte Carlo financial-independence simulator for the life-paths skill.

Pure standard library, no dependencies. Real (inflation-adjusted) dollars
throughout: the return assumption is a REAL return, and all amounts are in
today's money.

Usage:
    python3 fi_model.py --config config.json [--sensitivity] [--json out.json]

Config schema (JSON), annotated:
{
  "current_age": 34,
  "retire_age": 44,              // when contributions stop and withdrawals start
  "horizon_age": 95,             // simulate through this age
  "current_assets": 650000,
  "annual_savings": 150000,      // number, OR a list of yearly amounts from now
                                 // until retire_age (front-loaded schedules etc.)
  "retirement_spending": 150000, // desired annual withdrawal, gross, real
  "real_return_mean": 0.05,      // arithmetic mean real return of the portfolio
  "real_return_std": 0.12,
  "sims": 10000,
  "seed": 7,                     // optional, for reproducibility
  "income_streams": [            // optional: social security, pensions, rent...
    {"start_age": 67, "annual": 35000}
  ],                             // streams pay from start_age even before
                                 // retirement (added to wealth alongside
                                 // savings), so keep annual_savings net of
                                 // any stream income to avoid double-counting
  "guardrails": {                // optional dynamic-withdrawal rule
    "enabled": true,
    "cut_trigger": 1.2,          // spending cut when WR > trigger * initial WR
    "raise_trigger": 0.8,
    "adjust_pct": 0.10,
    "active_years": 30,
    "spending_floor": 60000      // optional hard floor on annual spending
  }
}

Output: human-readable summary to stdout; full percentile data as JSON with
--json. With --sensitivity, reruns the headline numbers at return means 1.0
and 1.5 points lower, because the return assumption is the single largest
lever in any of these models and the person deserves to see it moved.
"""

import argparse
import json
import math
import random
import statistics
import sys

PCTS = (10, 25, 50, 75, 90)


def lognormal_params(mean, std):
    """Fit lognormal on (1+r) from arithmetic mean/std of the real return."""
    m = 1.0 + mean
    sigma2 = math.log(1.0 + (std * std) / (m * m))
    mu = math.log(m) - sigma2 / 2.0
    return mu, math.sqrt(sigma2)


def savings_schedule(cfg):
    years = cfg["retire_age"] - cfg["current_age"]
    s = cfg.get("annual_savings", 0)
    if isinstance(s, list):
        sched = list(s)[:years]
        sched += [0.0] * (years - len(sched))
        return sched
    return [float(s)] * years


def run_sims(cfg, rng):
    mu, sig = lognormal_params(cfg["real_return_mean"], cfg["real_return_std"])
    ages = list(range(cfg["current_age"], cfg["horizon_age"] + 1))
    sched = savings_schedule(cfg)
    streams = cfg.get("income_streams", [])
    gr = cfg.get("guardrails", {}) or {}
    gr_on = bool(gr.get("enabled"))
    n = int(cfg.get("sims", 10000))

    wealth_paths = []          # per sim: wealth by age index
    spend_records = []         # per sim: list of realized retirement spending
    depleted = 0

    for _ in range(n):
        w = float(cfg["current_assets"])
        spend = float(cfg["retirement_spending"])
        initial_wr = None
        wealth = []
        spends = []
        retire_year_idx = None
        for i, age in enumerate(ages):
            r = math.exp(rng.gauss(mu, sig)) - 1.0
            income = sum(s["annual"] for s in streams if age >= s["start_age"])
            if age < cfg["retire_age"]:
                w = w * (1.0 + r) + sched[i] + income
            else:
                if retire_year_idx is None:
                    retire_year_idx = i
                    if w > 0:
                        initial_wr = spend / w
                if gr_on and initial_wr and w > 0:
                    yrs_in = i - retire_year_idx
                    if yrs_in < gr.get("active_years", 30):
                        wr = spend / w
                        if wr > gr.get("cut_trigger", 1.2) * initial_wr:
                            spend *= 1.0 - gr.get("adjust_pct", 0.10)
                        elif wr < gr.get("raise_trigger", 0.8) * initial_wr:
                            spend *= 1.0 + gr.get("adjust_pct", 0.10)
                        floor = gr.get("spending_floor")
                        if floor:
                            spend = max(spend, float(floor))
                net = max(spend - income, 0.0)
                w = w * (1.0 + r) - net
                realized = spend if w >= 0 else max(spend + w, income)
                spends.append(realized)
                if w < 0:
                    w = 0.0
            wealth.append(w)
        if wealth[-1] <= 0:
            depleted += 1
        wealth_paths.append(wealth)
        spend_records.append(spends)

    return ages, wealth_paths, spend_records, depleted, n


def _pct_sorted(values, p):
    k = (len(values) - 1) * p / 100.0
    f, c = math.floor(k), math.ceil(k)
    if f == c:
        return values[int(k)]
    return values[f] + (values[c] - values[f]) * (k - f)


def pct(values, p):
    """Single percentile of `values` (non-empty)."""
    if not values:
        raise ValueError("percentile of empty list")
    return _pct_sorted(sorted(values), p)


def pcts(values):
    """Rounded PCTS percentiles of `values` (non-empty), sorting once."""
    if not values:
        raise ValueError("percentile of empty list")
    values = sorted(values)
    return {p: round(_pct_sorted(values, p)) for p in PCTS}


def summarize(cfg, ages, wealth_paths, spend_records, depleted, n):
    if n < 1:
        raise ValueError("no simulations run")
    out = {"config": cfg, "survival_rate": 1.0 - depleted / n}
    checkpoints = [a for a in ages if (a - ages[0]) % 5 == 0 or a == cfg["retire_age"]]
    out["wealth_percentiles"] = {}
    for a in checkpoints:
        i = a - ages[0]
        out["wealth_percentiles"][a] = pcts([wp[i] for wp in wealth_paths])
    lifetime = [statistics.fmean(s) for s in spend_records if s]
    first = [s[0] for s in spend_records if s]
    out["lifetime_spending_percentiles"] = pcts(lifetime)
    out["first_year_spending_percentiles"] = pcts(first)
    return out


def print_summary(res, label=""):
    cfg = res["config"]
    if label:
        print(f"\n=== {label} ===")
    print(f"Real return {cfg['real_return_mean']:.2%} mean / "
          f"{cfg['real_return_std']:.0%} std, {cfg.get('sims', 10000)} sims")
    print(f"Portfolio survival to age {cfg['horizon_age']}: "
          f"{res['survival_rate']:.1%}")
    print("Wealth percentiles (10/25/50/75/90) at checkpoints:")
    for age, ps in res["wealth_percentiles"].items():
        marks = " <- retire" if int(age) == cfg["retire_age"] else ""
        vals = " / ".join(f"${ps[p]:,.0f}" for p in PCTS)
        print(f"  age {age}: {vals}{marks}")
    lp = res["lifetime_spending_percentiles"]
    fp = res["first_year_spending_percentiles"]
    print("First-year retirement spending (10/50/90): "
          f"${fp[10]:,.0f} / ${fp[50]:,.0f} / ${fp[90]:,.0f}")
    print("Lifetime avg spending (10/50/90): "
          f"${lp[10]:,.0f} / ${lp[50]:,.0f} / ${lp[90]:,.0f}")
    print("Note: with guardrails enabled, survival is high by construction; "
          "the 10th-percentile spending line is the number to underwrite.")


def validate_config(cfg):
    """Raise ValueError on a config the simulation cannot run honestly."""
    for key in ("current_age", "retire_age", "horizon_age", "current_assets",
                "retirement_spending", "real_return_mean", "real_return_std"):
        if key not in cfg:
            raise ValueError(f"config missing required key: {key}")
    if cfg["horizon_age"] < cfg["current_age"]:
        raise ValueError("horizon_age is before current_age: nothing to simulate")
    if cfg["retire_age"] > cfg["horizon_age"]:
        raise ValueError("retire_age is beyond horizon_age: no retirement years "
                         "in the simulation window")
    if int(cfg.get("sims", 10000)) < 1:
        raise ValueError("sims must be >= 1")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--sensitivity", action="store_true",
                    help="rerun at return mean -1.0 and -1.5 points")
    ap.add_argument("--json", help="write full results JSON to this path")
    args = ap.parse_args()

    with open(args.config) as f:
        cfg = json.load(f)
    try:
        validate_config(cfg)
    except ValueError as e:
        sys.exit(str(e))

    all_results = []
    variants = [("base case", 0.0)]
    if args.sensitivity:
        variants += [("return -1.0pt", -0.01), ("return -1.5pt", -0.015)]

    for label, delta in variants:
        c = dict(cfg)
        c["real_return_mean"] = cfg["real_return_mean"] + delta
        rng = random.Random(c.get("seed", 7))
        ages, wp, sr, dep, n = run_sims(c, rng)
        res = summarize(c, ages, wp, sr, dep, n)
        print_summary(res, label)
        all_results.append({"label": label, "results": res})

    if args.json:
        with open(args.json, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nFull results written to {args.json}")


if __name__ == "__main__":
    main()
