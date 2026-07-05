# Stage 1: Intake

Goal: three inputs, each with known provenance. The situation (what they have), the life shape (what the money must finance), and the jurisdiction (which rules apply). Provenance matters as much as the values: the deliverable will label every number as actual, estimate, or assumption, and that labeling starts here.

## Two entry modes

**From life-paths.** If a `life-paths-workspace/` exists, read its `dossier.md`, `finances/`, and the chosen path from `LIFE_PATHS.md` before asking anything. Most of intake is already done; confirm rather than re-collect, and ask only what the full plan needs beyond the stage-2 quick pass (usually: account-level detail, spending actuals if the quick pass ran on estimates, and the specifics of the chosen path's income timeline).

**Standalone.** Gather everything below, plus a compressed life shape: no career analysis, just the financial skeleton of the next decades as the person currently intends it. "Walk me through the next thirty years as you picture them: when income changes, when it stops, what big one-time costs are coming" gets most of it in one answer.

## The situation

- Income: every source, gross and take-home, with expected trajectory (their own expectation, labeled as such).
- Assets by account type, because tax treatment drives drawdown order: taxable, tax-deferred, tax-free, employer plans, equity compensation with vesting dates, property, cash.
- Debts with rates and terms.
- Insurance and current healthcare arrangement.
- Pensions and state benefits they expect, with whatever statements exist (ask for the official benefit statement; most systems provide one and it beats any estimate).
- Household structure: whose plan is this, one person or two, and what happens to it if one income or one person is removed. Ask this plainly; single-survivor math is part of an honest plan, not a morbid extra.

## Spending, done properly

Ask for exports: card and bank statements, a year or more if possible, or the person's own tracking if they keep it. Categorize enough to separate housing, recurring living costs, and discretionary; precision beyond that rarely changes the plan. Where only estimates exist, take them, and mark every downstream result estimate-grade. Then the check that catches the most common error in self-built plans: compare the retirement spending target against the current actual run-rate, and if the target implies a lifestyle cut, make the person choose explicitly between "the cut is intended, here is what it consists of" and "the target is wrong, raise it." Do not let that gap survive intake unnamed.

## The life shape

Whatever the source (chosen path or standalone sketch), reduce it to a timeline the model can consume: income phases with amounts and end dates, savings capacity per phase, exit or downshift dates, sabbaticals and part-time stretches, lumpy events (home purchase, education, family support, relocations), and the spending trajectory including any intended lifecycle shape (many people want higher spending in early retirement; model what they actually intend, and note that a declared taper is an assumption like any other). Write it as a table in `intake.md`.

## Jurisdiction

Country, and state or province where sub-national tax exists. Any planned moves, since relocation before or during drawdown can be one of the largest levers in a plan. Do not assume the US or any other country; the verification stage keys entirely off this answer.

## Existing model

If they brought one, read the whole thing before commenting, extract its assumptions into `assumptions.md` as the starting register, and note its headline results; stage 3 reproduces them before improving on them. Treat the model's author with respect regardless of what the audit later finds: a person who built their own Monte Carlo model did the hard part, and the audit exists to sharpen it, which is worth saying to them in roughly those words.

Close the stage by reflecting the three inputs back in a short summary and getting confirmation. Wrong intake poisons everything downstream, and this is the cheap place to catch it.
