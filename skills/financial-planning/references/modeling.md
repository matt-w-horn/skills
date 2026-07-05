# Stage 3: Modeling

Goal: a model of this household's plan, composed from the tested scaffolding in `scripts/simcore.py` plus small bespoke code written for this run, with the bespoke code tested before its numbers are believed.

## The composition pattern

`simcore` provides the primitives: return generation (lognormal Monte Carlo, historical sequences, block bootstrap), a year-ledger engine that applies returns and policy-driven cashflows, a guardrail spending policy, blending and summarizing utilities. What it deliberately does not provide is the person: their phases, their accounts, their jurisdiction's rules. Write that as a short module in `model/` (typically 50-150 lines) that builds the flow policy from intake's life-shape table and runs the engine across many simulations. Copy `scripts/simcore.py` into the workspace's `model/` directory (or add its path) so the run is self-contained and reproducible later.

Start from the worked example below and reshape it; do not reinvent the primitives, and do not extend simcore itself mid-run (bespoke logic lives in the bespoke module, so the tested core stays tested).

```python
# model/run_plan.py (sketch; stock_seq/bond_seq wrap simcore generators)
import simcore as sc

def flows_for(phase_table, facts, spend_policy):
    """Return a policy fn(t, wealth) -> net flow, built from the intake
    life-shape table, with spend_policy handling the drawdown phase."""
    ...

paths, spends = [], []
for i in range(N):
    r = sc.rng(seed=i)
    returns = sc.blend(stock_seq(r), bond_seq(r), w_stock)
    spend = sc.GuardrailPolicy(spending=target, income=benefits_by_year)
    policy = flows_for(phases, facts, spend)
    wealth, realized = sc.simulate_ledger(start_wealth, returns, policy)
    paths.append(wealth); spends.append(spend.realized_spending)
print(sc.summarize(paths, start_age), sc.spending_summary(spends))
```

## Modeling decisions, with reasons

- **Real terms throughout.** Model in today's money with real returns, so inflation lives inside the return assumption and every output is directly readable. Note this convention in the plan; it is the single most misread aspect of these models.
- **Historical data with provenance.** For historical-sequence and bootstrap runs, obtain a long annual real-return series at run time from a citable source (Shiller's public dataset and Damodaran's annual-returns pages are the usual ones); save the CSV to `data/` and log source and retrieval date in `facts.md`. Do not type a return series from memory. If the environment has no web access, run Monte Carlo only and say so in the plan's limitations.
- **Taxes at the materiality-appropriate level.** Default: effective-rate knobs per phase (accumulation, bridge, late retirement), with the rates justified from the verified register. Model account buckets and conversion mechanics explicitly only where they change a decision, and the usual place they do is the bridge years of an early exit, where drawdown order, conversion income, penalty-free-access rules, and healthcare subsidies interact. When that applies, the bespoke module models those years explicitly; elsewhere the effective rate is honest enough and vastly more auditable.
- **The healthcare bridge is a modeled expense**, not a footnote: a per-year cost from the verified register between exit and public eligibility, coupled to the drawdown strategy where the jurisdiction couples them.
- **Horizon to at least 95**, and to 100 in the sensitivity set for couples; the plan document reports what the extension changes, which at the median is usually little and at the 10th percentile is usually real.
- **Income streams** (state benefits, pensions, part-time phases) enter at their verified values and dates; a claimed intention to work part-time is an assumption and goes in the register as one.

## The testing rule

Before any bespoke module's output enters results, write `model/test_run_plan.py` and pass it. Minimum bar, chosen because these two tests catch most modeling bugs:

1. **Zero-volatility analytic case.** Fix returns at a constant (std 0), shrink to a toy scenario (small numbers, few years), and assert exact wealth values computed by hand in the test's comments.
2. **Conservation.** For any simulated path, end wealth equals start wealth plus returns plus net flows, year by year, within float tolerance; simcore exposes the ledger so this is a three-line assertion.

Add tests for whatever bespoke logic carries risk: the phase-table translation, the tax knob application, the bridge-year coupling. Also run the scaffolding's own suite once (`python3 -m unittest discover tests` from the skill directory) so an environment problem surfaces before results do. Test failures block results; there is no such thing as a number from failing code with a caveat attached.

## Reproduce before improving

When auditing a brought model, the first modeled result is a reproduction of its headline under its own assumptions, close enough to show the model is understood (exact matching is rarely possible across engines; get the shape and the magnitudes). Report the reproduction in the plan, then diverge deliberately, one named change at a time, so every difference between their number and yours has a stated cause. This ordering is what makes the audit persuasive rather than a rival opinion.
