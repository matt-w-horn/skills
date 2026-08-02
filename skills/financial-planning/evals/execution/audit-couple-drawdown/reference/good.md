*Synthetic test data — not a real person. Reference example used to calibrate this eval's grader.*

# Audit of the drawdown spreadsheet and planner result

Your instinct is right: £2.2m at 85 from £805k while drawing £42k a year is
too good, and the reason is that the model contains several errors that all
flatter the result. The two "independent methods" don't corroborate each
other, either — the online planner can't fail by construction, so its 100% is
not evidence. Here's the full list, then a corrected picture, then the answer
to "can we retire this summer."

## Errors in the spreadsheet

**1. Spending never rises, but the return is nominal.** Every row spends
£42,000, for 26 years, while the 6.5% growth is a nominal figure (your funds'
actual stated average). That mismatch is where most of the £2.2m comes from.
At ~2.5% inflation, £42,000 in 2051 buys what about £22,700 buys today —
the sheet quietly assumes your standard of living halves. Keeping today's
£42,000 of purchasing power means spending about **£77,900 in 2051's money**.
Fix: either inflate the spending row, or restate the whole sheet in today's
money with a *real* return of roughly 6.5% − 2.5% ≈ **4% real** — itself on
the optimistic side of a defensible planning range.

**2. The horizon stops at 85 — for a couple.** In 2051 you're 85 but Sam is
83, and for a couple the plan must run to the *second* death, which is
materially later than either individual expectancy. Roughly half of people
outlive their cohort's average, and for a healthy 58-year-old the odds that
at least one of you is alive in your mid-90s are substantial. Planning to 85
means the plan expires while one of you is quite likely still alive. Run it
to at least Sam's 95 (2063) — that's twelve more funded years than the sheet
contains.

**3. The same return every year hides sequence risk.** Averages are the
wrong input for drawdown: with withdrawals going out, *when* the bad years
land matters as much as the average. A crash in 2026–27, fully recovered in
the long-run average, still forces you to sell depleted assets to eat, and
the portfolio may never catch up. Example from your own numbers: a −20% then
−10% start, followed by returns *higher* than the corrected average, runs the
money out around Sam's age 94 in a plan that "averages" fine. You retire into
one sequence, not into the average — the plan needs to be tested against bad
sequences, and needs a pre-agreed spending response for them.

**4. Both State Pension inputs are stale.** For birth years 1966 and 1968
the State Pension age is **67, not 66** — pension start moves to 2033 (you)
and 2035 (Sam), removing £10,600–21,200 from two early, high-risk years. And
£203.85/week is the **2023/24** rate; it has been uprated every year since
(2025/26 was already £230.25). The deeper problem is that neither figure in
the sheet carries a source or date, so nothing statutory in it can be
re-checked. Verify both of your figures on gov.uk — ages via the State
Pension age tool, amounts and your NI records via your State Pension
forecasts — and date-stamp them in the sheet.

**5. Everything is gross-of-tax — and £685k of the £805k is pensions.**
"Sort tax later" is the one simplification you can't make: beyond the 25%
tax-free portion, every pound drawn from the SIPP and the workplace pension
is taxed as income. Netting £42,000 for the two of you will take roughly
**£45,500–47,000 gross** depending on how you split withdrawals — a
permanent ~10% increase in the drawdown the sheet doesn't show. The split
matters too: you have two personal allowances, two pensions, ISAs (tax-free
on the way out), and cash, and the *order* you draw them in changes the
lifetime tax bill — e.g. covering part of spending from ISAs while drawing
each pension up to useful thresholds, and using low-income years before
State Pension starts. The one-pot model can't see any of this.

## The planner's 100% is theatre

RetireSure's own note says the plan "uses FlexSpend": in poor markets
it cuts spending by up to 25% until the portfolio recovers. A model that
responds to trouble by cutting spending **cannot register failure** — 100%
success is close to true by construction, and it does not show that £42,000
is sustainable. What it actually tested is "some spending between £31,500 and
£42,000." The questions that matter are the ones the free summary omits: how
low spending goes in the bad scenarios (the floor is **£31,500** — could you
live on that?), how often cuts happen, and how many consecutive years they
last. The 10th-percentile ending balance of £238,000 against a median of
£1.91m is the same distribution telling you the downside paths are real.

## A corrected picture

Restated in today's money, to Sam's 95, with taxed withdrawals (~£46,500
gross real), State Pension of ~£12,000 each (today's money) from 67:

| Real return | Outcome |
|---|---|
| 4% (your 6.5% less inflation) | survives; ~£860k left at Sam's 95 |
| 3% | survives; ~£400k left |
| 2% | survives with ~£73k — effectively zero margin |
| −20%, −10% start, then above-average | **depleted around Sam's age 94** |

## So: can you retire this summer?

**Probably yes — but not on the basis this model gives you, and not with the
margin you think you have.** The honest position: £805k plus two State
Pensions supports roughly £42,000 of today's-money spending on *middling or
better* return sequences, and fails on bad ones — a viable plan with real
downside, not a 100% certainty. Before handing in notice: fix the sheet (real
terms throughout, horizon to Sam's 95, tax modelled, statutory figures
verified and dated), agree in writing what you'd cut spending to in a bad
market and confirm £31,500 is livable, keep 2–3 years of spending in cash and
ISAs to avoid selling pension assets into a crash, and check both State
Pension forecasts for missing NI years — buying voluntary years is often the
cheapest risk reduction available to you.
