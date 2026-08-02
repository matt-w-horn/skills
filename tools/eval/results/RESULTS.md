# First run, August 2026

Claude Code 2.1.220, session default model, three runs per trigger query and two
per execution configuration. Raw data sits beside this file: `summary.json` per
sweep, `grading.json` per run with the judge's quoted evidence, and
`calibration.json` for the judge check.

## Triggering: 64 of 64

| split | queries | passed |
|---|---|---|
| graded (train + validation) | 48 | 48 |
| sealed | 16 | 16 |

By class, across the graded set: 22/22 positives, 16/16 near-miss negatives,
8/8 cross-skill disambiguation, 2/2 either. The routing matrix separates
cleanly, with 45 runs firing `financial-planning` where it was expected, 45
firing `life-paths` where it was expected, and 48 firing nothing on the
near-misses. No skill fired on a query where neither should.

The negatives were not soft. `fp-t30` says "retirement plan" and "withdrawal"
while asking for 72(t) calculation mechanics; `fp-t22` says "retirement
dollars" while asking which of two index funds has the lower ongoing charge.
Both drew zero triggers across three runs each. A keyword matcher fails those.

**What this does not show.** A perfect score means the corpus is saturated: it
can catch a regression from here but cannot show an improvement, and it left
nothing for description iteration to work on. Neither description was changed.

The sealed split has now been spent and is recorded in `sealed-runs.json`.
Running it again after a description change would make it another training set.

## Execution: 95% against a baseline of 88%

Eight evals, each run with the skill and without it, graded by an LLM judge one
assertion at a time with cited evidence required.

| eval | skill | with | without |
|---|---|---|---|
| `audit-flawed-model` | financial-planning | 100% | 82% |
| `audit-couple-drawdown` | financial-planning | 100% | 96% |
| `write-the-plan` | financial-planning | 100% | 86% |
| `plan-career-break` | financial-planning | 100% | 89% |
| `map-the-paths` | life-paths | 89% | 79% |
| `crossroads-offer` | life-paths | 93% | 89% |
| `audit-coach-report` | life-paths | 92% | 88% |
| `audit-career-plan` | life-paths | 86% | 86% |

Every financial-planning eval reaches 100% with the skill loaded. The skill is
never worse at eval level. One run was excluded as truncated, and that exclusion
favours the skill, since it was a with-skill run cut off at the deadline.

### Most of the rubric measures nothing

Of the 101 assertions, **12 discriminate**, 86 pass in both configurations, one
inverts, and two never pass either way. A headline pass rate is therefore
mostly reporting what a competent model does unaided.

The 12 that carry the difference cluster tightly on what the skills claim to
add. `audit-flawed-model`'s entire lead comes from four: naming the 7% real
return as optimistic, reporting the outcome at a materially lower return,
catching inflation-adjusted returns mixed with nominal salary growth, and
flagging a stale contribution limit as needing verification. Each ran 100% with
the skill and 50% without.

### The judge moves more than most of these deltas

Grading one fixed artifact four times returned 100%, 82%, 82% and 73%. The
spread comes from single assertions flipping rather than wholesale
disagreement: across three consecutive trials, eight assertions passed every
time, two failed every time, and one flipped.

So judge variance is roughly ±10 to ±15 points on a single run, which is
comparable to or larger than every per-eval delta in the table except
`audit-flawed-model`. **Read the small deltas as noise.** What survives is the
financial-planning column sitting at 100% across every grading it has had, and
the 86%/86% null on `audit-career-plan`.

Fixing this needs more runs per configuration and more gradings per run, not a
better prompt. Two runs was chosen for cost and it shows.

### The clearest evidence is not a score

On `audit-flawed-model`, the with-skill run made 84 tool calls over 25 minutes
and produced a workspace holding a plan document, an assumptions register, a
facts register, and genuinely downloaded historical return series and
healthcare cost curves. The baseline made 10 tool calls over 6 minutes and
wrote no files at all.

Both answered in about 10,500 characters of prose, so a pass rate can miss that
difference entirely. It does not depend on the judge.

## Known limitations

**The finish-the-job fixtures ask for what the rubric checks.** A blind author
had to put the requirements somewhere gradeable and put them in the synthetic
client's notes, so a baseline that follows written instructions passes much of
those rubrics. Those four evals partly measure instruction-following.

**The model can tell it is being evaluated.** Every fixture carries a line
marking it synthetic, which the linter enforces so invented personal records
never read as real. That line sits inside what the model reads.

**Two runs per configuration licenses very little.** Combined with the judge
variance above, only the largest effects here are worth acting on.

**Coverage gaps.** An unblinded review found commitments no assertion tests,
including the single-survivor scenario that `financial-planning` calls
mandatory and both couple fixtures would exercise. Those were deliberately not
added: they were derived by reading the skill bodies, and adding them would
convert blind assertions into spec-derived ones. They are the obvious next
work.

## Instrument defects found and fixed during the run

Recorded because each would have produced a confident wrong number.

- The judge graded "do the figures match the person's records" without ever
  being shown the records.
- A skill that corrected a file in place had that work hidden from the judge,
  because fixture paths were excluded by name rather than by content.
- 50KB of the skill's own Python crowded the plan document out of the graded
  artifact. Before the fix, `write-the-plan` showed seven inverted assertions;
  after it, 100% against an 86% baseline.
- A run killed at the deadline reported `triggered` and was graded as complete.
- The trigger scorer mishandled mixed `either` labels badly enough to fail a
  correctly routed query and to pass one where the required skill never fired.
- Three runs hit total judge outages and were correctly refused rather than
  cached as all-undecided.
