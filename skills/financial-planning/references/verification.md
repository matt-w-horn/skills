# Stage 2: Fact verification

Goal: `facts.md`, the verified-facts register. Every fact in the plan that changes over time or varies by jurisdiction gets verified by web search at plan time and logged. This stage is what makes the plan trustworthy in a way memory-built plans structurally cannot be: tax and benefit rules change yearly, healthcare rules change with politics, and a model's author rarely goes back to update the constants.

## Register format

One entry per fact:

```
- fact: <what this is, in plain words>
  value: <the current value or rule>
  jurisdiction: <country/state it applies to>
  source: <URL, official source strongly preferred>
  checked: <date>
  volatility: <annual | legislative | stable>
```

The volatility field feeds the deliverable's annual review checklist: annual facts get re-verified every year, legislative facts get a news check, stable facts get left alone.

## What to verify

Scope this to the person's jurisdiction and account types from intake; the list below is the category checklist, with examples, and the examples are illustrations rather than the required set.

- **Contribution limits and account rules** for every account type they hold or should consider: employer plan limits, individual retirement account limits and income phase-outs, health savings vehicles, any after-tax-to-tax-free conversion mechanisms their system offers, and the eligibility rules and ages for penalty-free access. These change annually in most systems.
- **Tax structure**: current brackets and rates for their filing situation, capital-gains treatment, how retirement withdrawals and conversions are taxed, and any sub-national tax with material effect. Where the plan involves converting between account types over years, verify the rules governing that specifically.
- **State benefits**: the pension or social-security formula and claiming ages for their system, and how a shortened career changes the benefit; if intake obtained an official statement, the statement wins over any formula estimate.
- **Healthcare**: what covers the person now, what covers them in the gap between any early exit and public eligibility, current pricing for the gap coverage at their income, and, critically, any interaction between the plan's drawdown strategy and coverage subsidies (in some systems, withdrawal and conversion income directly changes subsidy eligibility, which couples the tax plan and the healthcare plan into one problem). This category is legislative-volatile almost everywhere; check current status, and note that this is where an old model most needs a fresh look.
- **Anything the existing model asserts as fact.** When auditing a brought model, every constant in it is a claim to verify, and finding its stale ones is among the most valuable outputs of the audit.

## Method

Search official sources first (tax authorities, benefit administrations, the regulator's own pages); secondary sources only to locate the primary one. When sources conflict or a rule is in legislative flux, record the conflict in the register rather than picking a side silently, and carry the uncertainty into stage 4 as a scenario if it is material. When a fact cannot be verified online (an employer plan's specific features, for instance), log it as user-confirmed with a note that the person should verify with the administrator, and add that to the deliverable's action list.

Do not editorialize in the register; it is a table of facts. The interpretation happens in modeling and in the plan document, where each register entry that binds gets cited by its fact line.
