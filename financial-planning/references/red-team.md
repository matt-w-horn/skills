# Stage 5: Red team

Goal: an independent attempt to break the plan before the person relies on it. Fresh context matters here for the same reason it does in code review: the author of a model has already rationalized its weakest assumptions, and by this stage you are the author. The auditor gets the artifacts and a mandate to find what is wrong, with no investment in the story.

## Dispatch

One subagent, fresh context, given: the draft `FINANCIAL_PLAN.md` (or its assembled pieces), `intake.md`, `facts.md`, `assumptions.md`, the model code and its tests, and the results. Its prompt:

> You are auditing a long-horizon financial plan before it is delivered. Your job is to break it: find the errors, the fragile assumptions doing outsized work, and the unpriced risks. You have no stake in the plan being good.
>
> Work through this checklist first; each item is a failure mode that recurs in real plans:
> 1. Spending target versus documented actual spending: any unexplained gap?
> 2. Return assumptions versus the historical record and current institutional forward estimates: is the base case at the optimistic edge, and does the sensitivity set expose it?
> 3. Any survival or success percentage that is true by construction (adaptive-spending rules): is the spending floor headlined instead?
> 4. Healthcare: is the bridge to public eligibility priced from verified current rules, and is the drawdown-income interaction with subsidies modeled where the jurisdiction couples them?
> 5. Horizon: does the plan fund past average life expectancy, and does the 10th percentile survive the extension?
> 6. Facts register: spot-check entries against their sources; flag anything unverified, stale, or asserted without a source. Flag any constant in the model code that bypassed the register.
> 7. Sequence risk: were historical sequences run, and does the Monte Carlo floor disagree with the historical floor?
> 8. Single-survivor and care-shock scenarios: present, priced, and honest?
> 9. Income assumptions: any income stream (part-time work, a pension, an inheritance) treated as fact rather than assumption?
> 10. The model code: do the tests actually constrain the logic (a zero-volatility analytic case and a conservation check at minimum), and do they pass? Run them.
> 11. Load-bearing assumptions: identify the one or two assumptions whose failure most damages the plan, whether or not they appear above, and check the plan names them as such.
>
> Then go beyond the checklist: find at least one material issue not on it, or state explicitly that you looked and found none beyond the list. For every finding, give: severity (breaks the plan / changes a decision / worth documenting), the evidence, and the smallest fix. Return findings only, no praise section.

## Resolution

Triage every finding into exactly one of three outcomes, recorded in `notes.md`:

- **Fix**: the model, register, or document changes; rerun whatever the change touches.
- **Sensitize**: the finding is a real uncertainty rather than an error; it becomes a sensitivity row or named scenario in stage 4's outputs.
- **Document**: a limitation the plan carries knowingly; it goes into the plan's limitations section in the red team's words, not softened ones.

If the auditor found "breaks the plan" severity anything, dispatch a second audit pass after fixes; a plan that failed its first audit has not earned delivery on the strength of the patch alone. The deliverable's limitations section states that an independent audit ran and what its unresolved findings were, which is worth more to a skeptical reader than any amount of confidence.
