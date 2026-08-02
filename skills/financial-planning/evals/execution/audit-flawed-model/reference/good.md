*Synthetic test data — not a real person. Reference example used to calibrate this eval's grader.*

# Audit of your exit-at-45 model

Short answer: the $14.5M ending balance is an artifact of the assumptions, not
a forecast, and the plan as built does not support quitting at 45. Your
instinct to be suspicious was right. The arithmetic in the spreadsheet is
internally consistent — every row compounds correctly — but five of the inputs
are wrong or untested, and they all push the same direction.

## 1. Your spending assumption contradicts your own records

The plan assumes $52,000/yr. Your 2025 category export totals **$66,854** —
about $15,000/yr (29%) more than the budget, and that was a year with employer
health coverage and no extra leisure time. The $52,000 figure is a hope; the
$66,854 is evidence. Until you've lived on the lower number for a year or two,
the plan has to be priced at what you actually spend. Every headline number
below moves when this one does.

## 2. There is no healthcare line at all

From the day you quit at 45 until Medicare at 65 you buy your own coverage,
and neither the budget nor the projection contains a dollar for it — the note
says "healthcare is through work," which stops being true in 2031. Budget
roughly $9,000–15,000/yr for premiums plus out-of-pocket, unsubsidized.

It's worse than a missing line item, because the cost is coupled to the rest
of the plan: ACA premium subsidies are set by your reported income (MAGI), so
how much you withdraw, and from which accounts, partly determines what
insurance costs you. Realizing capital gains or doing Roth conversions in a
given year raises that year's premium. Healthcare and withdrawal strategy have
to be designed together, not added separately.

## 3. One return number, and an aggressive one

7% real is above what a diversified portfolio can reasonably be planned on —
it is roughly the best-case historical equity average, taken as certain, with
no bad decade allowed. Two problems:

- **Level.** Planning assumptions for a balanced portfolio sit meaningfully
  lower; ~4–5% real is a defensible planning range. Re-running your sheet at
  **4.5% real** gives $1.09M at 45 instead of $1.21M, and with your $52k
  spending you end at ~$535k at 95 — alive but thin, with zero margin for the
  other problems below.
- **Shape.** A single compounded rate hides sequence risk entirely: a
  retiree drawing down cares about the *order* of returns, and a bad first
  decade with the same long-run average produces a completely different
  outcome than your smooth line. A plan needs a range of outcomes, not one
  path — at minimum, projections at conservative and pessimistic rates and a
  look at bad-early-sequence cases.

## 4. The sheet mixes real and nominal money

You state the 7% is after inflation, i.e. the sheet is in today's dollars —
but salary grows 3%/yr. Raises at roughly the inflation rate are not real
growth; in a today's-dollars model your salary and match should be
approximately flat. As built, the sheet counts inflation twice in your favor
on the contribution side. The effect is small over five years (~$3k of
phantom contributions) but it signals the frame isn't being applied
consistently — check every line for which currency it's in.

## 5. Withdrawals are untaxed, and mostly locked

$610k of your $735k is traditional pre-tax 401(k). Two separate problems:

- **Tax.** Every dollar you draw from it is ordinary income, and the sheet
  taxes nothing. To net $67k of spending mostly from pre-tax money you'll
  gross roughly $73–78k depending on bracket and state.
- **Access.** You can't freely spend 401(k) money at 46. Before 59½ you need
  a mechanism — 72(t)/SEPP payments, a Roth conversion ladder (with the
  five-year seasoning per conversion), or you pay the 10% penalty. The rule
  of 55 doesn't apply if you separate in the year you turn 45. Your
  penalty-free bridge money is the $85k brokerage plus $40k of Roth basis:
  about two years of real spending, against a five-plus-year seasoning
  timeline. This is a sequencing problem the model doesn't know exists.

## 6. The $22,500 limit is stale

$22,500 was the 2023 employee limit; it has been raised every year since
(it was $23,500 in 2025) and indexes upward. The sheet holds it flat through
2030 with no source or date. Small in dollars, but it means the statutory
inputs weren't checked — verify the current-year limit, and date-stamp every
statutory figure in the model so it can be re-checked next year.

## What the corrected model says

Using your evidence-based spending and a defensible return:

| Scenario | Result |
|---|---|
| As built: 7% real, $52k, no tax/health | $14.5M at 95 |
| 4.5% real, $52k | ~$535k left at 95 |
| 4.5% real, $67k (your records) | **depleted at age 75** |
| 4.5% real, ~$78k gross ($67k net + health + tax) | **depleted at age 68** |
| 5% real, ~$78k gross | depleted at 71 |

## Verdict and what would change it

**Quitting at the end of 2030 does not hold up** on your own spending
evidence: under defensible assumptions the money is gone in your late 60s to
mid 70s. It becomes plausible if some combination of these moves: actually
living at ~$52k for the next two years (measured, not budgeted), working to
~48–50, part-time income covering the pre-59½ bridge, or trimming housing.
Rebuild the sheet with taxes and healthcare as explicit rows, all figures
consistently in today's dollars, statutory numbers dated and sourced, and a
pessimistic-return column next to the expected one — then re-ask the question
each year against your measured spending.
