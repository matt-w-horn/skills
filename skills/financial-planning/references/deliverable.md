# Stage 6: The deliverable

Goal: `FINANCIAL_PLAN.md`, a document the household runs their finances by for years, plus a short handoff conversation. The document's job is to survive being wrong: forecasts decay, so the plan's durable parts are its registers, its decision rules, and its review cadence.

## Structure

```
# Financial Plan - [household] - [date]
Intro: what this plan covers, the real-terms convention (all amounts in
today's money; inflation lives in the return assumption), data grades
(which inputs are actuals vs estimates), and one line on educational
scope with professional verification advised before irreversible moves.

## The headline
The work-optional window as a range, with the two or three assumptions
that move it and by how much. Then the floor: 10th-percentile lifetime
spending and the worst pre-benefit stretch, judged against actual
lifestyle in one honest sentence. Ranges and floors here, never a
single date or a survival percentage.

## The life being financed
The phase table from intake: income phases, exits, lumpy events,
spending trajectory. This section ties the model to the life; a reader
should see their plan, not a generic retirement.

## Assumptions register
Every assumption: value, basis (chosen by user / default / derived),
which direction it is likely wrong, and its sensitivity (link to the
matrix row). This register is the plan's honesty; nothing modeled may
rest on an assumption absent from it.

## Verified facts register
From facts.md: fact, value, jurisdiction, source, date checked,
volatility. Facts with annual volatility are flagged for the review
checklist.

## Results
Base case percentile trajectories at checkpoints; first-year and
lifetime spending distributions; the sensitivity matrix as a table;
historical-sequence results with the worst starting years named; the
stress scenarios each with its outcome in a sentence.

## Decision rules
The plan as an instrument: observable if-then rules the household can
execute without re-deriving the model. Examples of the form (adapt the
substance): "At each annual review, if the portfolio is below X at age
Y, the exit moves one year later"; "If spending drifts more than Z%
above target for two consecutive years, the target is re-set from
actuals and the model rerun"; "If [the load-bearing assumption] fails,
[the pre-decided response]." Guardrail spending rules, if used, are
written out here in plain words with their floor.

## Annual review checklist
Ten-minute yearly pass: re-verify annual-volatility facts, compare
actual spending to modeled, mark portfolio against the trajectory
bands, check the named tripwires and legislative items, note whether
any decision rule triggered. Date the first review.

## Questions for a professional
The specific, plan-derived questions a fee-only advisor or tax
professional should answer, each tied to a register entry or scenario
(plan features to confirm, tax mechanics to validate, insurance gaps
to price). A generic "see an advisor" helps nobody; a list of eight
sharp questions makes the professional hour count.

## Limitations
What the model does not capture, in plain words, including unresolved
red-team findings verbatim and the data-grade caveats. Short and
unflinching; this section is why the rest can be trusted.
```

## Presentation

Deliver the file. In the accompanying message, give the headline range, the floor judgment, and the single most consequential finding (often the target-versus-run-rate gap or a stale fact from a brought model), then stop; the document carries the rest. If the plan audited a brought model, lead with the reproduction ("your model's numbers reproduce under its assumptions") before the differences, and frame every difference by its cause. Offer conversion to PDF or a spreadsheet of the phase table on request. Set the expectation that the plan is an annual instrument: the review checklist, not the forecast, is the part that will still be earning its keep in year ten. If this run was part of a life-paths flow, copy the headline range and the binding constraints back into that workspace's `finances/finances.md` so the two documents agree.
