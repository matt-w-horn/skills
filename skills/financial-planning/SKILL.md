---
name: financial-planning
description: Build a grounded, verified long-horizon financial plan for a person - accumulation, financial-independence timing, drawdown, and the decision rules to run it by. Use this whenever someone asks when they can retire or go work-optional, wants a FIRE or retirement plan built or reviewed, brings a spreadsheet or planner document to audit, asks about safe withdrawal rates, savings schedules, drawdown strategy, or whether their money supports a life change (quitting, sabbatical, going independent, relocating). Trigger even for partial asks like "check my retirement math" or "how much do I need to leave my job" - the pieces need the whole model. Pairs with the life-paths skill (this skill prices a chosen life; that one chooses it), but runs fully standalone.
---

# Financial Planning

Produce a financial plan a careful skeptic would sign: every fact verified, every assumption named with its sensitivity, risk expressed as the spending floor the person would actually live on, and the whole thing operable through written decision rules rather than a one-time forecast.

## Why this skill exists

Self-built retirement models, including sophisticated ones with Monte Carlo engines and dynamic withdrawal rules, fail in recurring ways: spending targets that quietly contradict the person's actual spending, a single return assumption at the optimistic edge with no sensitivity shown, "100% success" claims that are true by construction because the model cuts spending instead of depleting, healthcare bridges and their tax interactions left unmodeled, horizons that stop at average life expectancy, and tax facts that were stale the year after they were typed. Professional plans fail differently: generic assumptions, no connection to the life actually being planned. This skill exists to produce the plan neither of those produces, and every stage below traces to one of those failures.

## Core principles

- **Verified beats recalled.** Any fact that changes or varies by jurisdiction (contribution limits, tax brackets, benefit ages and formulas, healthcare rules) gets checked by web search at plan time and logged with source and date. A plan resting on remembered numbers is wrong on arrival or wrong within a year; the verified-facts register (see `references/verification.md`) is what separates this plan from the one it replaces.
- **Actuals beat estimates.** Spending comes from statements and exports wherever they exist. The gap between what people say they spend and what they spend is the single most common silent error, and it propagates into every headline number.
- **Sensitivity is a first-class result.** Never present one future. The deliverable's headline is a range with the assumptions that move it, and the return assumption always appears at the user's value and at least two more conservative values.
- **The floor is the risk metric.** For any plan with adaptive spending, report the 10th-percentile lifetime spending and the worst pre-benefit stretch, judged against the person's actual lifestyle. Survival percentages are reported but never headlined.
- **A plan is a document plus decision rules.** The forecast will be wrong; the plan should say, in observable if-then form, what to do when it is. Deliverable structure in `references/deliverable.md`.
- **The model serves a life.** Income phases, exits, sabbaticals, part-time years, and lumpy expenses come from the life being planned. When a `life-paths` workspace exists, consume its chosen path and finances files as input; when standalone, elicit the life shape in intake. If the person has not actually chosen what life they are financing and the conversation keeps sliding into "but what should I do," that is the life-paths skill's job; suggest it once and continue with the shape they give you.

## Code policy

The bundled `scripts/simcore.py` is scaffolding: tested primitives (return generators, a ledger engine, spending policies, summarizers), not a finished model. Plan-specific logic - the person's phases, their tax buckets, their jurisdiction's interactions - is written on the fly per run, composed from the scaffolding. This is deliberate: a fixed model flexible enough for every household would be a config language nobody can audit; small bespoke code on tested primitives is both flexible and checkable.

The rule that makes on-the-fly code safe: any bespoke module gets its own tests before its outputs are trusted, at minimum a zero-volatility analytic case (returns fixed, arithmetic checkable by hand) and a conservation check (wealth change equals returns plus flows). Run the scaffolding's own suite once per run (`python3 -m unittest discover tests`) so a modified environment fails loudly. Numbers from untested code do not enter the deliverable.

## Workspace

Default `./financial-plan-workspace/` (or the life-paths workspace's `finances/` directory when running as part of that flow):

```
financial-plan-workspace/
  intake.md            - situation, life shape, jurisdiction, data provenance
  facts.md             - verified-facts register (fact, value, source, date)
  assumptions.md       - assumptions register (value, basis, sensitivity)
  data/                - spending actuals, historical return series (with source)
  model/               - bespoke run code and its tests
  results/             - simulation outputs
  FINANCIAL_PLAN.md    - the deliverable
  notes.md             - open questions, where you left off
```

## Stages

Read each reference at its stage.

1. **Intake** - situation, actuals, accounts, the life shape being priced, jurisdiction. Interactive. Read `references/intake.md`.
2. **Fact verification** - search-verify everything jurisdiction- or year-dependent; build the register. Read `references/verification.md`.
3. **Modeling** - compose the model from scaffolding plus tested bespoke code; obtain historical return data with provenance. Read `references/modeling.md`.
4. **Stress and sensitivity** - the sensitivity matrix, historical sequences, named stress scenarios, floor analysis. Read `references/stress-and-sensitivity.md`.
5. **Red team** - a fresh-context auditor agent tries to break the plan; findings get fixed, sensitized, or documented. Read `references/red-team.md`.
6. **Deliverable** - assemble `FINANCIAL_PLAN.md`, walk the person through the headline range and the decision rules. Read `references/deliverable.md`.

Stage 1 is a conversation (small question batches, end turns). Stages 2-5 run autonomously once inputs are confirmed; announce the handoff. If the person brought an existing model, stages 2-5 double as its audit: reproduce its headline first so you know you understand it, then improve on it, and report the differences explicitly - people trust a critique of their model far more when you have first shown you can reproduce it.

## Boundaries

This is educational modeling, not licensed financial advice; say so once, where the stakes justify it, and include the professional-handoff questions in the deliverable rather than repeating disclaimers. Do not recommend specific securities or products. If intake surfaces acute financial distress (imminent insolvency, debt crisis), the long-horizon plan is the wrong tool; deal with the near term plainly and offer to return to planning later.
