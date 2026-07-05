# Stage 4: Stress and sensitivity

Goal: replace the single future with a mapped range. A plan's credibility lives here; the person should leave knowing which assumptions their outcome actually depends on, by how much, and which stress breaks the plan first.

## The sensitivity matrix

Rerun the model varying one assumption at a time, and report the effect on the two numbers the person cares about: the work-optional date (or the plan's equivalent gate) and the 10th-percentile lifetime spending.

Always in the matrix:
- **Real return**: the user's assumption, minus 1.0 point, minus 1.5 points. The return assumption is the largest lever in every one of these plans, and showing it moved is more honest and more persuasive than debating the future.
- **Spending level**: the modeled target, plus 10-20%, and the actual current run-rate if it differs from the target (this row often ends the target-versus-run-rate argument that intake started).
- **Exit date**: plus and minus one to two years around the intended date. The person should see what a year of flexibility buys, because date flexibility is usually their cheapest risk control.
- **Horizon**: the base horizon and 95/100.

Add rows for whatever intake flagged as uncertain (a pension amount, a part-time income, an inheritance counted on). Present the matrix as a table; each row cites the assumptions register.

## Historical sequences

Run the plan's cashflows against every overlapping historical window of the appropriate length from the sourced return series, so the person sees their plan started in 1929, in 1966, in 2000. Independent lognormal years understate how bad decades cluster; the historical pass is the corrective, and its worst starting years belong in the plan by name. Where Monte Carlo and history disagree about the floor, history gets the benefit of the doubt.

## Named stress scenarios

Beyond parameter wiggles, run the discrete events that actually break plans, each as a modeled scenario with its result stated plainly:

- **Bad first decade**: the historical worst-case window aligned to start at the exit date (sequence risk is concentrated there and nowhere else).
- **One survivor**: for couples, one income, one benefit stream, and the survivor's expenses, starting at a few different ages. Uncomfortable and mandatory.
- **Care shock**: multi-year long-term-care cost at current verified prices, landing late in the plan. If uninsured, this is the plan's largest unpriced tail; say what it does and whether insurance, earmarked assets, or accepted risk is the response.
- **Coverage break**: the healthcare bridge assumption fails (the covering job ends, the subsidy regime changes); what the gap costs and what absorbs it.
- **Whatever the plan leans on**: every plan has one or two assumptions doing outsized work (a specific income lasting, a house selling, an employer plan feature existing). Stage 5's red team will hunt for these; stress the ones already visible now.

## Floor analysis

Synthesize into the risk statement the deliverable headlines: the 10th-percentile lifetime spending, the worst modeled stretch before benefit income arrives, and the judgment call stated as a judgment: does that floor clear the household's actual lifestyle, and if not, by how much and with what response (later exit, lower base spending, income optionality kept warm). With guardrail-style adaptive spending, remind the reader once that survival percentages are a property of the rule, and the floor is the number being underwritten.

Save all runs to `results/` with the configs that produced them; the red team and the annual reviews both need them reproducible.
