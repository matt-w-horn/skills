# Stage 2: The financial picture

Goal: an honest answer to two questions. When does work become optional, as a range with a floor, not a point estimate? And what constraints does money place on each path between now and then? Everything else in this stage serves those two answers.

Money is the enabling layer, not the point of the process. Do not optimize the portfolio, sell products, or drift into general financial planning; produce the answers the paths need and return to the person.

## Two modes

**Audit mode**, when they bring a model (a spreadsheet, a FIRE calculator output, a planner's document): your job is to find where it is wrong or fragile, not to rebuild it. Run the audit checks below against it, reproduce its headline result with `scripts/fi_model.py` to confirm you understand it, then run the sensitivity variants.

**Build mode**, when they have nothing: gather the inputs below, build a config, and run the simulator. Keep it proportionate; a person in light mode gets one config and a sensitivity pass, not a modeling seminar.

## Inputs to gather

Income (all sources, gross and take-home), investable assets by account type (tax treatment matters), debts, housing (own or rent, and the plan), dependents and their timelines, expected inheritances or windfalls they consider real, pensions and state benefits (country-specific: get their jurisdiction and verify the rules by web search, not memory), insurance and healthcare arrangements, and spending.

Spending deserves special care because it is where models most often lie. Ask for actuals: card and bank exports, a year of statements, whatever exists. If only estimates are available, take them, then mark the resulting model as estimate-grade in `finances.md`.

## The audit checks

These are the failure modes that recur in self-built retirement models. Check each one; report only the ones that bite.

1. **Target versus run-rate.** Compare stated retirement spending against current actual spending. A large implied lifestyle cut with no stated mechanism is the most common silent error, and every headline number inherits it. If found, make the person choose: is the cut a real intention, or is the target wrong?
2. **Return assumptions.** Compare the assumed real return against the historical record for their allocation and against current institutional forward estimates (search for current ones; they drift). Do not argue about the future; run the model at the assumption, at one point lower, and at one and a half points lower, and show what each does to the date. Sensitivity beats debate.
3. **"100% success" claims.** Dynamic-withdrawal models (spending guardrails) cannot deplete by construction; they convert depletion risk into spending risk. When a model advertises perfect survival, redirect attention to the spending floor: the 10th-percentile lifetime spending, and the worst stretch before any state benefits arrive. That floor, against their actual run-rate, is the real underwriting question.
4. **Healthcare bridge.** Between employer coverage and public eligibility age lies the gap that kills early-retirement plans, and the rules move with politics. Check what the plan assumes, verify current law for their country, and check the interaction with their drawdown strategy (in some systems, the withdrawals themselves change subsidy eligibility).
5. **Horizon.** Models that stop at average life expectancy quietly underfund the joint survivorship tail. Extend to at least 95 for the analysis and note what it changes, usually little at the median and something real at the 10th percentile.
6. **Stale facts.** Contribution limits, tax brackets, benefit formulas: verify the current year's numbers by search. Models age from the day they are written.
7. **Sequence and tails.** Independent lognormal years understate how bad decades cluster. Note it once; if the tooling allows a historical-sequence pass, run it; do not turn this into a lecture.

## Running the simulator

`scripts/fi_model.py` is a dependency-free Monte Carlo simulator with its own test suite; run `python3 -m unittest discover tests` once per session before using it. Write a JSON config (schema documented at the top of the script), run:

```
python3 scripts/fi_model.py --config finances/config.json --sensitivity
```

It reports portfolio survival, percentile trajectories at five-year checkpoints, and the lifetime spending distribution, then repeats the headline results at return assumptions 1.0 and 1.5 points lower. Save raw output to `finances/` and write the human summary to `finances/finances.md`. If a modeling question outgrows the bundled script, write a small bespoke module and test it before trusting it (a hand-checkable deterministic case at minimum); untested numbers stay out of `finances.md`.

## Scope, and the handoff

This stage answers what the paths need: the work-optional window and the constraints money puts on timing. It is deliberately not the full plan. Once the person has chosen a path (or whenever they ask for the complete treatment: verified tax facts, historical-sequence stress, decision rules, an auditable document), hand off to the companion `financial-planning` skill if it is installed; it reads this workspace's `dossier.md` and `finances/` directly and writes its headline back here so the two stay consistent. Mention the handoff once at the end of this stage, and again at delivery if a path gets chosen.

## The output

`finances.md` states, in plain language: the work-optional window as a range with the assumptions that move it; the spending floor in bad sequences and whether it clears their actual lifestyle; the binding dependencies (healthcare bridge, a partner's income or benefits, housing decisions); and the constraint each of these places on path timing, phrased so the path agents can consume it directly ("any exit before age X requires Y"). One line noting that a professional should verify before irreversible decisions. Confirm the summary with the person before stage 5; their finances shape every path, and a wrong number here poisons everything downstream.
