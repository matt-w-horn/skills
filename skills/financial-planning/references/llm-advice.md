# LLM Financial Advice: Findings from Choukhmane, de Silva, Lin, and Akuzawa (2026)

Citation: Choukhmane, Taha, Tim de Silva, Weidong Lin, and Matthew Akuzawa,
"AI Financial Advice: Supply, Demand, and Life Cycle Implications", working
paper, 2026, https://doi.org/10.2139/ssrn.6446286. Paper dated July 29, 2026;
first draft November 2025; an earlier version circulated as "How Good is
Generative AI Personal Financial Advice?".

This file was distilled in August 2026 from the full paper, main text and
internet appendix included. Page references of the form (Sec 3.2), (Fig 7),
(Table 2), (Appendix Table A2) point into that PDF.

## Contents

1. [What the study did](#what-the-study-did)
2. [What the findings do and do not license](#what-the-findings-do-and-do-not-license)
3. [The three headline facts](#the-three-headline-facts)
4. [Fact 1: advice moves people toward life cycle theory](#fact-1-advice-moves-people-toward-life-cycle-theory)
5. [Fact 2: four systematic departures from life cycle theory](#fact-2-four-systematic-departures-from-life-cycle-theory)
6. [The academic prompt benchmark](#the-academic-prompt-benchmark)
7. [Demand side: what 952 real people ask](#demand-side-what-952-real-people-ask)
8. [Fact 3: heterogeneity across groups](#fact-3-heterogeneity-across-groups)
9. [Demand versus supply: the label-randomization experiment](#demand-versus-supply-the-label-randomization-experiment)
10. [Stochasticity of advice](#stochasticity-of-advice)
11. [Robustness: other models and a direct-to-JSON pipeline](#robustness-other-models-and-a-direct-to-json-pipeline)
12. [The life cycle model: calibration and normative benchmarks](#the-life-cycle-model-calibration-and-normative-benchmarks)
13. [Implications for a planning skill](#implications-for-a-planning-skill)
14. [Limitations and open questions](#limitations-and-open-questions)
15. [What this file left out](#what-this-file-left-out)

## What the study did

Three steps (Sec 1, Fig 1):

1. **Survey.** A demographically balanced U.S. sample of 1,000 adults
   recruited on Prolific wrote three free-text prompts to an LLM financial
   advisor: (a) a description of their financial situation, (b) a request for
   advice on how much to spend over the coming year, (c) a request for advice
   on how to invest savings between stocks and safer options (Figure E1 has
   the exact survey wording). Respondents were told the LLM knows nothing
   about them except what they write; prompts (b) and (c) assume the LLM
   already has the situation description. 952 of 1,000 responses survived
   screening: 33 failed Prolific's authenticity check (which screens out
   AI-generated responses) and 15 failed a minimum specificity requirement
   that each prompt address its assigned topic (Sec 1.1, Appendix A.2).
2. **Life cycle model.** A quantitative model in the Gourinchas-Parker and
   Cocco-Gomes-Maenhout tradition, closest to Choukhmane and de Silva (2026),
   calibrated to U.S. data, provides both the simulation environment and the
   normative benchmark (Sec 1.2, Appendix B; calibration below).
3. **Simulation.** Each simulated individual, at each age from 22 to 89, is
   matched to a survey prompt from a respondent with similar employment
   status, age, and income (12 prompt buckets). State-variable mentions in
   the prompt (age, income, wealth, allocations) are replaced with the
   simulated individual's current values, the three prompts are concatenated
   and sent to the LLM with an instruction to respond in 200 words or fewer,
   and a second LLM call translates the textual advice into quantitative
   choices (consumption plus contributions, withdrawals, and transfers across
   four asset classes). Shocks then realize and the process repeats. Every
   query is independent: no memory across periods; the only link is the
   evolution of state variables (Sec 1.3, Table 1).

**Models used** (Sec 1.5): the main advice model is GPT-5.2 with reasoning
effort set to "Low", chosen to approximate the default ChatGPT experience,
because ChatGPT is the most-used model for financial advice in the survey
(71.9% of respondents with prior AI use; Google Gemini 17.4%, Grok 2.9%,
Claude 2.2%, other 5.7%; Figure E3). Translation uses GPT-5 Mini.
Robustness reruns use Gemini 3 Flash and GPT-5.6 Terra for advice, keeping
GPT-5 Mini for translation (Sec 3.4).

**Simulation design** (Sec 1.3): each run simulates the same 1,000
individuals, all starting at age 22 with zero wealth, retiring at 65, dying
by 90. A new prompt is drawn every period for every individual. Group
comparisons (by gender, literacy, AI experience) hold all exogenous shock
realizations fixed, so outcome differences are driven entirely by the prompts
and the LLM's responses (Sec 4.1).

**Prompt bucketing** (Appendix A.3, Figure A1, Table A2): 12 buckets, namely
1 retired, 2 unemployed (age halves), and 9 employed (age terciles by income
terciles). Baseline bucket counts, out of 952 prompt sets: retired 132,
unemployed 71 + 68, employed buckets 117, 60, 56, 84, 94, 49, 101, 77, 43.
Ties in the discrete income brackets go to the lower income tier.

**Variable insertion** (Appendix A.1, Table A1): every mention of a state
variable is replaced with the simulated individual's value while preserving
the author's wording and concerns. Rules include: household income and
wealth are doubled before insertion unless the prompt names more than two
working adults; hourly wages are recomputed as simulated income divided by
52 x N with N = 40 for full-time and N = 20 for part-time when hours are
unstated; ranges are replaced by midpoints; wealth is allocated across
mentioned accounts in the original within-class ratios, with a min rule for
mixed accounts (401k, mutual fund) so an account cannot exceed the simulated
holdings of its asset class; already-received lump sums are rescaled to the
same share of simulated wealth they were of self-reported wealth.
Self-reported wealth is categorical; midpoints are used, with $50,000 for
"I don't know / prefer not to answer".

**Benchmarks** (Sec 1.4): (i) respondents' observed self-reported behavior;
(ii) optimal behavior in the life cycle model under the same shock
realizations; (iii) the academic prompt (Sec 6 below). Sec 3.1 also defines
a one-shot benchmark: the advice generated once from each respondent's
original prompt and current self-reported situation, without simulation.

## What the findings do and do not license

- The results characterize the effect of **following** LLM advice, not of
  receiving it. Whether people act on the recommendations is explicitly an
  open question (Sec 3.1 summary, Sec 5, footnote 22).
- The regime tested is **one-shot, at most 200 words, low reasoning effort,
  no memory**: consumer-default chatbot advice, not an agentic or multi-turn
  planning session. The academic prompt results (Sec 3.3) show the same
  model behaves differently when given full state information and explicit
  assumptions, so the baseline numbers are properties of the interaction
  regime as much as of the model.
- Findings are for GPT-5.2 with corroboration from Gemini 3 Flash and
  GPT-5.6 Terra (Table 2, Figures E9, E15, E16). The authors state the
  advice of future model generations may differ and position the method as a
  reusable framework (intro, Sec 5).
- The supply-side demographic effects are identified only for **explicit**
  labels ("I am a woman", "I am Black"); the design cannot rule out
  differential response to subtler markers such as names or dialect
  (Sec 4.2, end of Sec 4).
- The advice domain is spending, saving, and investing; insurance, housing,
  and credit management were deliberately out of scope (intro, Sec 1.1).

## The three headline facts

1. Following LLM advice would move most respondents **toward** the broad
   prescriptions of life cycle theory relative to their observed behavior:
   near-universal participation in diversified equity funds, equity shares
   that decline with age after about 45, and savings buffers above $10,000
   by age 30 for virtually all simulated individuals (Sec 3.1).
2. The advice departs from the theory's more demanding prescriptions in four
   systematic ways: it implies unusually high patience, relies on simple
   saving and withdrawal heuristics, smooths consumption imperfectly after
   income shocks, and lets portfolios drift passively with realized returns
   (Sec 3.2).
3. The advice varies systematically with who wrote the prompt: gender,
   financial literacy, and prior AI experience each produce wealth-at-60
   differences of roughly 4 to 6 percent, arising from both demand (what
   people write) and supply (how the model responds to otherwise identical
   prompts) (Sec 4).

## Fact 1: advice moves people toward life cycle theory

Observed behavior baseline (Sec 3.1, Fig 5): one-third of respondents report
holding no equities; their average equity share is around 30%; more than 20%
of respondents in every age group report financial wealth below $10,000.

Against that baseline:

| Outcome | One-shot advice | Full life cycle simulation | Source |
|---|---|---|---|
| Stock market participation | +5 to +10pp | near-universal | Fig 5 left |
| Average equity share | about +5pp | up to +40pp vs observed | Fig 5 middle |
| Share with wealth < $10k | reduced in all age groups | virtually zero by age 30 | Fig 5 right |

Aggregate profiles under baseline advice (Sec 2.2, Fig 4, Table E3):
consumption is flatter than income over working life (though less flat than
the life cycle model prescribes); individuals save during working life and
withdraw slightly more than income in retirement; they accumulate over
$1 million by retirement at 65. Recommended equity shares average around
65%, rise early in working life while emergency buffers are built, peak in
the 70s-percent range near age 40, and decline after roughly age 45. The
glide path is less steep than a typical target-date fund but similar to the
average equity share of retirement savers making active choices (Sec 2.2).

Non-diversified assets (individual stocks; crypto, gold, commodities,
collectibles) get small allocations: participation grows with age to about
35% for individual stocks and 50% for other risky assets by retirement, but
conditional portfolio shares average 2 to 3% of financial wealth, so the
vast majority of recommended risky allocation is diversified equity
(Sec 2.2, Figure E8). Non-diversified assets are about 1% of baseline
allocations overall (Sec 4.2).

### Advice responds sensibly to prompt content

Regressing recommended outcomes on indicators for each topic category
mentioned in the prompt (controls: income, wealth, age fixed effects,
prompt-bucket fixed effects; categories appearing in at least 5% of
prompts), the LLM adjusts in directions consistent with theory (Sec 3.1,
Fig 6). Full coefficient sets:

Effect on net savings rate (percentage points, Fig 6 left):

| Topic mentioned in prompt | Coefficient |
|---|---|
| Macroeconomic | +4.44 |
| Lifestyle Goals | +3.36 |
| Tax | +3.09 |
| Budgeting | +2.65 |
| Housing | +2.40 |
| Liquidity | +2.00 |
| Long-Term Planning | +1.90 |
| Income | +1.86 |
| Gender | +0.97 |
| Family | +0.81 |
| Investment Assets | +0.63 |
| Risk Preference | +0.38 |
| Retirement | +0.02 |
| Employment Security | +0.01 |
| Investment Strategy | -0.55 |
| Discipline | -0.64 |
| Savings | -0.71 |
| Education | -1.77 |
| Debt | -2.61 |
| Financial Anxiety | -3.15 |
| Medical | -6.32 |
| Financial Hardship | -9.64 |

Effect on change in equity share (percentage points, Fig 6 right):

| Topic mentioned in prompt | Coefficient |
|---|---|
| Long-Term Planning | +0.54 |
| Employment Security | +0.40 |
| Medical | +0.38 |
| Discipline | +0.34 |
| Investment Strategy | +0.32 |
| Investment Assets | +0.18 |
| Tax | +0.16 |
| Income | +0.12 |
| Liquidity | +0.10 |
| Debt | +0.02 |
| Housing | +0.02 |
| Family | -0.11 |
| Lifestyle Goals | -0.13 |
| Budgeting | -0.19 |
| Retirement | -0.28 |
| Savings | -0.51 |
| Education | -0.64 |
| Financial Anxiety | -0.72 |
| Financial Hardship | -0.97 |
| Gender | -1.82 |
| Macroeconomic | -1.97 |
| Risk Preference | -2.07 |

Readings the paper highlights (Sec 3.1): macroeconomic mentions (inflation,
recession worry) raise saving by about 4pp and cut equity by about 2pp, a
precautionary response; financial hardship cuts the recommended saving rate
by about 10pp and equity by 1pp, an immediate-liquidity response; risk
preference mentions barely move saving (+0.4pp) but cut equity by 2.1pp,
echoing Rumpf et al. (2026), who find LLMs far more sensitive to stated risk
preferences than human advisors.

## Fact 2: four systematic departures from life cycle theory

### Departure 1: unusually high patience

The authors estimate, by simulated method of moments, the discount factor
beta and relative risk aversion gamma that make the life cycle model best
fit the LLM-generated life cycle profiles (targets: 25th/50th/75th
percentiles of the wealth-to-income ratio at ages 23-64 and of the equity
share at ages 23-88, 324 moments; grid beta 0.8 to 1.2 in steps of 0.002,
gamma 2 to 14 in steps of 0.1; identity weighting matrix; Sec 3.2,
Appendix D).

| Prompt type | LLM | beta | gamma | Source |
|---|---|---|---|---|
| Survey | GPT-5.2 | 1.034 | 5.3 | Table 2 |
| Academic | GPT-5.2 | 0.990 | 4.7 | Table 2 |
| Survey | Gemini 3 Flash | 1.054 | 5.1 | Table 2 |
| Survey | GPT-5.6 Terra | 1.032 | 5.3 | Table 2 |

Risk aversion of 5.3 is moderate and within the standard range; a discount
factor above 1 is not. It reflects the LLM recommending consumption below
income throughout working life. The authors note two readings: unmodeled
bequest motives (though bequests are rarely mentioned in prompts) or a form
of paternalism, recommending higher targets because people undershoot; but
if the advice is followed exactly, a standard life cycle model can
rationalize it only with an unrealistically high discount factor (Sec 3.2).
The estimated model matches the LLM's wealth accumulation and its equity
shares after 45, but cannot match the low, upward-sloping equity shares the
LLM recommends between ages 25 and 45, since standard models without
participation costs or correlated labor income risk imply high equity early
in life (Figure E10 Panel A, footnote 12).

### Departure 2: simple saving and withdrawal heuristics

Under survey prompts (Sec 3.2, Fig 7):

| Heuristic | Baseline LLM advice | Life cycle model |
|---|---|---|
| Saving rates at multiples of 10% of income | 31.0% | absent by construction (continuous) |
| Saving amounts at multiples of $5,000 | 34% | absent |
| Withdrawals at or below 4% of assets (ages 65+) | 98.3% | almost no one below 4% |

The withdrawal spike sits at the 4% retirement rule popularized by Cooley,
Hubbard, and Walz (1998). The life cycle model prescribes faster
decumulation than the LLM: its withdrawal-to-wealth distribution has most
mass above 4% (Fig 7 right panel, red line).

### Departure 3: consumption insufficiently smoothed

Recommended consumption closely tracks income over the life cycle (Fig 8
left). Around simulated job loss, income falls by roughly 50% and
recommended consumption falls by a similar percentage (that is, roughly
one-for-one in proportional terms), consistent with empirical consumption
responses to unemployment in Gruber (1997) and Ganong and Noel (2019). In
the life cycle model, consumption barely falls after job loss because
individuals draw down buffer stocks (Sec 3.2, Fig 8 right, Figure E11).
The failure is notable because the simulated individuals hold sizable
liquid balances the advice could have told them to spend (footnote 13:
results are similar when all state variables are appended to the prompt).

### Departure 4: passive portfolio drift

Following Calvet, Campbell, and Sodini (2009), passive drift is the change
in equity share that would occur with no active adjustment. Regressing
actual portfolio change on passive drift (Fig 9):

| Policy | Regression slope (SE) |
|---|---|
| Baseline LLM advice, survey prompts | 0.96 (0.01) |
| LLM advice, academic prompt | 0.96 (0.01) |
| Life cycle model | 0.03 (0.01) (Figure E11); 0.02 (0.01) (Figure E16) |

LLM-recommended portfolios move almost one-for-one with realized returns.
Calvet et al. estimate 0.5 for real households, so the LLM exhibits roughly
twice the inertia of observed household portfolios (footnote 14). The
inertia persists when the translation step is skipped and the LLM is given
all state variables including the existing allocation, so it is not an
artifact of missing portfolio information: the LLM advises on allocating
new savings rather than recommending rebalancing of existing holdings
(Sec 3.2, Sec 3.3, Figure E12).

## The academic prompt benchmark

The academic prompt replaces respondent-written prompts with a structured,
researcher-designed prompt (Sec 1.4, Sec 3.3; full text in Appendix A.5.1
and Table A3). Design features, summarized:

- System role: a U.S. financial advisor acting in the client's best
  interest, academically trained in household finance, modern portfolio
  theory, and life cycle planning.
- Explicit baseline assumptions, each mapped to a life cycle model
  counterpart (Table A3 Panel A): normal life expectancy, living
  expenditures, retirement age, employment and income risk; current U.S.
  tax law and Social Security rules unchanged; risk-free savings earn 2.0%
  real; real stock returns match the 60-year U.S. total market average;
  single with no dependents, no bequest motive, no utility from wealth
  after death.
- Individual-specific state each period (Table A3 Panel B, User section):
  age, employment status (including tenure, or "I am currently unemployed"
  with benefit income, or "I am retired" with Social Security income),
  annual post-tax income, average annual income since age 22 (flagged as
  determining future Social Security benefits), and balances in four
  taxable buckets: D diversified stock, I individual stocks, N nonstock
  (cash, HYSA, CDs, bonds, Treasuries, emergency fund), O other (crypto,
  gold, commodities, collectibles).
- Asks three questions (annual consumption in dollars; contribute to,
  withdraw from, or keep each account; transfers between accounts),
  instructs step-by-step thinking without outputting the reasoning, and
  demands JSON-only output with 21 numeric keys (consumption, per-bucket
  contributions and withdrawals, and all pairwise transfers), subject to
  stated source limits and a budget identity, with a self-check instruction
  to fix violated constraints before output.
- It skips the translation step entirely: the model outputs quantitative
  recommendations directly (footnote 15). Since Sec 3.4 shows that skipping
  translation and appending state variables to survey prompts reproduces
  the baseline patterns, the improvements below are attributable to the
  academic prompt's content and framing, not to the pipeline difference.

What it fixed and what it did not (Sec 3.3):

| Outcome | Survey prompts | Academic prompt | Source |
|---|---|---|---|
| Saving rates at multiples of 10% | 31.0% | 14.6% | Fig 7, Fig 10 |
| Withdrawals at or below 4% of assets | 98.3% | 8.8% | Fig 7, Fig 10 |
| SMM discount factor beta | 1.034 | 0.990 | Table 2 |
| SMM risk aversion gamma | 5.3 | 4.7 | Table 2 |
| Consumption tracks income over life | yes | no; substantial retirement decumulation | Fig 8 left |
| Consumption drop at job loss | roughly proportional to income | smaller, reverses faster | Fig 8 right |
| Passive-drift slope | 0.96 (0.01) | 0.96 (0.01), unchanged | Fig 9 |

Under the academic prompt the recommended equity share peaks around 90%+
near midlife and falls steeply late in life (Figures E13, E14), and the
unemployment event study shows consumption held near its pre-loss level
(Figure E11 right, with the life cycle model comparison). The one departure
structured prompting does not touch is rebalancing: the actual-versus-passive
slope stays at 0.96, so the lack of active rebalancing "appears to reflect a
more prevalent pattern in the LLM's financial advice", not missing state
variables or informal wording (Sec 3.3).

Caveat: the academic prompt assumes a single individual with no dependents,
while the life cycle model varies household composition by age through an
equivalence scale (footnote 5).

## Demand side: what 952 real people ask

### Prior AI use and topics

48% of respondents report having used an AI tool for financial advice or
information in the past three months (footnote 3): 14.7% multiple times,
33.1% once or twice; 38.0% have not but considered it; 14.2% have not and
are not interested (Figure E20). Among users, topics discussed with AI
tools (multiple selection, Figure E2):

| Topic | Share of AI users |
|---|---|
| Saving | 49.3% |
| Investing | 48.9% |
| Budgeting | 42.3% |
| Education | 35.4% |
| Taxes | 31.2% |
| Retirement | 25.4% |
| Credit | 24.1% |
| Crypto | 19.5% |
| Loans | 13.1% |
| Others | 4.2% |

### Prompt length and quantitative content

(Table E2; word/character counts are means; "numbers" = any digit,
"dollars" = "$" or the word "dollar".)

| Prompt / subgroup | N | Words | Chars | % with numbers | % with dollars |
|---|---|---|---|---|---|
| All three prompts combined | 952 | 96.7 | 499.2 | 76.3 | 45.1 |
| Financial situation prompt | 952 | 43.0 | 218.3 | 65.2 | 34.4 |
| Spending advice prompt | 952 | 26.7 | 137.0 | 31.1 | 17.0 |
| Investment advice prompt | 952 | 27.0 | 142.0 | 27.7 | 11.9 |
| Income low (<$50k) | 490 | 96.9 | 497.2 | 74.3 | 44.5 |
| Income mid ($50k-$100k) | 296 | 96.0 | 498.4 | 78.7 | 45.3 |
| Income high (>$100k) | 130 | 93.4 | 486.5 | 80.0 | 50.8 |
| Financial literacy low (0-3 of 5) | 253 | 88.6 | 450.0 | 70.4 | 41.1 |
| Financial literacy mid (4 of 5) | 345 | 100.8 | 519.6 | 79.1 | 45.2 |
| Financial literacy high (5 of 5) | 354 | 98.5 | 514.6 | 77.7 | 47.7 |
| No prior AI use | 497 | 90.3 | 463.3 | 73.6 | 41.9 |
| Prior AI use | 455 | 103.7 | 538.5 | 79.1 | 48.6 |
| Female | 486 | 98.2 | 501.3 | 74.5 | 44.7 |
| Male | 466 | 95.2 | 497.2 | 78.1 | 45.5 |
| Unemployed | 139 | 105.1 | 544.2 | 68.4 | 36.7 |
| Retired | 132 | 87.2 | 451.1 | 75.0 | 46.2 |
| Employed | 681 | 96.9 | 499.4 | 78.1 | 46.6 |

Note two different financial-literacy splits appear in the paper: Table E2
uses low/mid/high (0-3, 4, 5 correct of the Big Five questions), while the
heterogeneity analysis (Fig 11, Table A2) uses a two-way split, perfect
(5 of 5; 354 respondents) versus below-perfect (598).

### What the prompts and the advice talk about

Topic measurement is a keyword dictionary of 27 categories built by reading
the prompts (Sec 2.1, Appendix C, Table C1). Categories: Debt, Savings,
Retirement, Housing, Investment Strategy, Income, Employment Security,
Budgeting, Education, Family, Gender, Financial Hardship, Financial Anxiety,
Risk Preference, Medical, Long-Term Planning, Tax, Lifestyle Goals,
Macroeconomic, Investment Assets, Providers, Products, Liquidity,
Discipline, Diversification, Insurance, Inheritance. Categories are not
mutually exclusive; keywords go through the same spaCy lemmatization
pipeline as the responses (Appendix C).

Most common categories by prompt (Sec 2.1, Figure E4): describing their
situation, respondents most often mention Income (35%) and Retirement
(30%); asking for spending advice, Budgeting (45%); asking for investment
advice, Investment Assets (53%) and Risk Preference (40%). The most
prominent words across prompts are "money", "debt", "income", "pay",
"retire" (Fig 2).

The advice tracks the prompts (rank correlation across all 27 categories:
Spearman rho 0.72, p < 0.001; Figure E6) but adds topics on its own:
Liquidity appears in 84% of advice responses versus 6% of prompts,
reflecting the model's high propensity to recommend an emergency fund
(Sec 2.1). Dominant advice words: "fund", "invest", "save", "stock",
"debt", plus "essential", "insurance", "emergency" (Fig 2).

### The advice names products; users mostly do not

Mention rates, prompts (combined) versus advice (weighted per respondent)
(Fig 3 Panel A):

| Asset class | Prompts | Advice |
|---|---|---|
| Stocks (aggregate) | 49% | 86% |
| High-yield savings | 3.5% | 59% |
| Bonds (aggregate) | 10% | 55% |
| ETFs | 3.2% | 41% |
| Treasury bills/notes/bonds | 1.0% | 40% |
| Money market funds | 2.0% | 25% |
| CDs | 3.8% | 18% |
| Target-date funds | 0.2% | 15% |
| Brokerage account | 1.0% | 13% |
| Stocks (international) | 0.1% | 13% |
| Stocks (individual) | 1.5% | 12% |
| Crypto | 4.0% | 11% |
| Series I bonds | 0% | 7% |

By provider (Fig 3 Panel B): fewer than 3% of respondents name any specific
ticker, yet advice mentions Vanguard products in 7% of responses (0.4% of
prompts), iShares 3.4% (0%), crypto tokens such as Bitcoin or Ethereum 1.9%
(1.5%), Schwab 1.5% (0.1%), SPDR/State Street 1.2% (0.3%), Fidelity 1.0%
(0%), Invesco 0.7% (0.1%), JPMorgan 0.1% (0%). The authors flag that
branded recommendations raise questions about product competition and the
regulation of new advice sources (Sec 2.1).

### Prompt style varies with who writes

Illustrative contrasts, quoted fragments (Figures E19, E21): a
high-financial-literacy respondent writes as a futures trader ("3 to 4
trades per daily session", account size stated); a low-literacy respondent
writes "Hello....Im in need of some financial advice. I need to invest some
money into something that will make me money in the future." An experienced
AI user engineers the persona ("Assume you are a CFA with 20+ years of
experience"); a non-user asks the tool to "create a budget for my new pay
rate as I am starting a new job." Word clouds by group (Figures E18, E22):
high-literacy prompts over-represent "expense", "tax", "fund", "income",
"bond", "risk", "retire"; low-literacy prompts "credit", "money", "job",
"week", "card", "pay". Advice back to high-literacy users over-represents
"portfolio", "equity", "bracket", "rebalance"; to low-literacy users
"card", "phone", "starter", "week", "deposit", "crypto".

### Survey sample versus the CPS

(Table E1; March 2025 CPS.) The Prolific sample matches the CPS closely on
gender (49% male both) and broadly on age and income, but over-represents
the unemployed (15% vs 3%), under-represents the retired (14% vs 36%) and
respondents older than 70 (8% vs 11% at 70-79; 0% vs 5% at 80+), and
under-represents the lowest income bracket ($0-25k: 27% vs 35%). Race:
White 63% vs 76%, Black 11% vs 13%, Asian 6% vs 7%, Mixed 11% vs 2%,
Other 8% vs 2%.

## Fact 3: heterogeneity across groups

For each characteristic, the life cycle simulation is repeated using only
prompts written by one group at a time, with identical shock realizations
(Sec 4.1). Differences in simulated outcomes (Fig 11; standard errors in
parentheses; "FV net saving" is net saving compounded at the risk-free rate
through age 60, so it is unaffected by portfolio returns):

| Comparison | Wealth at 60 (levels) | Log wealth at 60 | Log FV net saving | Equity share 22-60 |
|---|---|---|---|---|
| Low vs high financial literacy | -$45,878 (26,282) | -4.11% (1.45) | +1.44% (1.36) | -1.64pp (0.13) |
| No vs yes prior AI use | -$99,797 (28,554) | -5.71% (1.68) | -4.32% (1.30) | +0.43pp (0.14) |
| Female vs male | -$59,890 (31,185) | -4.10% (1.61) | -0.52% (1.62) | -2.94pp (0.13) |

Mechanisms differ by characteristic (Sec 4.1):

- **Financial literacy** (Big Five test; low = at least one of five wrong):
  the roughly $46,000, or 4.1%, wealth gap is driven primarily by portfolio
  choice (1.64pp lower equity 22-60); cumulative saving goes the other way
  and would partially offset it, since the less literate group is advised to
  save more.
- **Prior AI use**: the roughly $100,000, or 5.7%, gap is driven almost
  entirely by saving behavior (FV of net saving 4.32% lower for non-users);
  the equity-share difference is economically small (0.43pp).
- **Gender**: the roughly $60,000, or 4.1%, gap is mainly portfolio choice:
  the average equity share recommended to women is 2.94pp lower, while
  cumulative net saving is nearly identical. The equity gap appears across
  all age and income groups (about 4.4pp at 25, dipping near 1pp around 45,
  rising above 7pp by 60; 3 to 4pp in every income quintile), and men are
  advised to rebalance more actively at every age (Figure E23). The
  direction is consistent with Foltyn and Olsson (2026), who find an
  average 1.8pp gender gap in equity allocations across 33 LLMs, and with
  observational and human-advice evidence (Sec 4.1).

The intro's rounding: average wealth at 60 is "around 5% higher" when
sampling prompts written by men, high-literacy respondents, or prior AI
users (p. 5). Although AI use and literacy correlate, the distinct
mechanisms (portfolio versus saving) suggest the comparisons capture
different sources of heterogeneity (footnote 19).

## Demand versus supply: the label-randomization experiment

Design (Sec 4.2): 83% of prompt sets (789 of 952, Table A2) never state the
author's gender, directly or through gendered self-description ("mother",
"wife"). Those prompts get "I am a man" or "I am a woman" randomly inserted
at each use. The regression is

Y = beta_D FemaleAuthor + beta_S FemaleLabel + bucket fixed effects,

so beta_D identifies demand (prompts written by women differ in content)
and beta_S identifies supply (the model responds to the stated gender with
content held fixed). Both are period-by-period effects on single-draw
recommendations, not cumulated life cycle differences, and the supply
channel is measured off an explicit statement, not naturally conveyed
gender (Sec 4.2). Race works the same way, dropping prompts that mention
race and inserting "I am Black" / "I am Asian" / "I am White"; the survey
lacks data on Hispanic ethnicity (footnote 21).

Full results (Table 3; changes in each outcome, percentage points, SEs in
parentheses):

| Comparison | Outcome | Author (demand) | Label (supply) | Total |
|---|---|---|---|---|
| Female vs male | Diversified equity share | -0.96 (0.15) | -0.54 (0.15) | -1.50 (0.21) |
| Female vs male | Non-diversified asset share | -0.19 (0.03) | +0.01 (0.03) | -0.19 (0.04) |
| Female vs male | Net saving rate | -0.88 (1.67) | -1.76 (1.64) | -2.63 (2.34) |
| Black vs White | Diversified equity share | +0.66 (0.21) | +0.03 (0.18) | +0.69 (0.28) |
| Black vs White | Non-diversified asset share | -0.11 (0.05) | -0.02 (0.04) | -0.13 (0.06) |
| Black vs White | Net saving rate | +3.09 (3.39) | +0.14 (2.89) | +3.24 (4.45) |
| Asian vs White | Diversified equity share | -0.65 (0.26) | -0.16 (0.18) | -0.81 (0.31) |
| Asian vs White | Non-diversified asset share | -0.16 (0.05) | -0.02 (0.04) | -0.18 (0.07) |
| Asian vs White | Net saving rate | +1.21 (4.13) | -2.44 (2.89) | -1.23 (5.04) |

Readings (Sec 4.2):

- **Gender, diversified equity**: moving from man-written man-labeled to
  woman-written woman-labeled reduces the recommended diversified equity
  share by 1.50pp per period. Approximately two-thirds is demand
  (-0.96pp) and one-third is supply (-0.54pp): the same prompt gets a
  lower equity recommendation when labeled as coming from a woman.
- **Gender, non-diversified assets**: entirely demand-driven (supply
  coefficient approximately zero).
- **Gender, saving**: not statistically distinguishable from zero, and not
  offsetting forces; both coefficients are negative but insignificant.
- **Race**: differences are smaller than the gender gap and driven by
  demand; explicit race labels leave recommendations essentially unchanged
  (supply effects near zero for both comparisons). Saving-rate differences
  by race are not statistically distinguishable from zero.
- Interpretation: supply-driven gender differences may reflect implicit
  inference (gender as a coarse signal for risk preference or labor-market
  risk) or algorithmic bias reproducing training-data stereotypes. The
  race null may reflect providers aligning models to avoid differential
  treatment by race more stringently than by gender; but "I am Black" is
  exactly the salient signal such safeguards detect, so the null does not
  rule out responses to subtler markers (names, dialect, contextual cues)
  common in real usage (Sec 4.2, end of Sec 4).

Language differences behind the demand channel (Fig 12): men's prompts
over-represent "expense", "tax", "retire", "wife", "bond", "crypto",
"strategy"; women's over-represent "husband", "money", "credit", "pay",
"job", "student", CDs and credit unions. Advice to men over-represents
"portfolio", "rebalance", "international", "core", "equity", "tolerance";
advice to women "cd", "ncua", "fdic", "insure", "debit", "apply".

## Stochasticity of advice

Same prompt, repeated (Sec 3.4, Figure E17; one-shot advice, all 952
respondents, five repetitions per exercise; the table reports the median
across respondents of the within-person standard deviation over the five
runs):

| Exercise | SD of annual consumption | SD of equity share |
|---|---|---|
| Full pipeline repeated 5 times (new advice each time) | $3,220 | 6.5pp |
| Translation only repeated 5 times (advice text held fixed) | $335 | 1.6pp |

At the median, translation-only variation is about one-tenth of
full-pipeline variation for consumption and one-quarter for equity share:
most randomness enters when the model writes new textual advice, not when
text is converted to numbers. GPT-5.2 is a reasoning model and does not
allow temperature zero (footnote 16). Rumpf et al. (2026) document similar
stochasticity in LLM financial advice.

## Robustness: other models and a direct-to-JSON pipeline

**Alternative models** (Sec 3.4, Table 2, Figures E7, E9, E10, E15, E16):
rerunning advice generation with Gemini 3 Flash and GPT-5.6 Terra (GPT-5
Mini still translating) reproduces every baseline pattern: higher
participation, higher equity shares, larger buffers versus observed
behavior; similar structural estimates (beta 1.054 / gamma 5.1 and beta
1.032 / gamma 5.3); heuristics; limited smoothing around job loss; passive
drift.

| Statistic | GPT-5.2 | Gemini 3 Flash | GPT-5.6 Terra |
|---|---|---|---|
| Saving rates at multiples of 10% | 31.0% (Fig 7) | 48.3% (Fig E15) | 28.5% (Fig E15) |
| Withdrawals at or below 4% | 98.3% (Fig 7) | 94.5% (Fig E15) | 98.2% (Fig E15) |
| Passive-drift slope (SE) | 0.96 (0.01) (Fig 9) | 0.97 (0.02) (Fig E16) | 0.98 (0.02) (Fig E16) |

**Direct-to-JSON pipeline** (Sec 3.4, Figure E12): appending state
variables to the survey prompt and asking for quantitative recommendations
directly, with no separate translation call, reproduces the baseline:
consumption and equity profiles very similar, passive-drift slope 0.95
(0.01), consumption response to job loss nearly identical. Heuristics
persist but attenuate: saving rates at multiples of 10% fall from 31.0% to
18.7%, withdrawals at or below 4% from 98.3% to 92.4%. So the main results
are not driven by the translation step or by withholding state variables
during advice generation.

**Translation prompt design** (Step 4 of Sec 1.3; full text in Appendix
A.5.2, summarized): GPT-5 Mini acts as a "deterministic extractor" that
converts advice text into one-year USD flows across consumption and the
four buckets. Key features: the simulation's state variables are supplied
as ground truth and override any income or wealth figures in the advice
text; numbers count only when tied to action verbs (save, invest,
contribute, withdraw, transfer, rebalance); annualization rules (monthly
x12, weekly x52, paycheck default biweekly x26); rules for limited-duration
and multi-year goals; percentage-base rules (withdrawal rates and portfolio
percentages apply to total wealth, save/invest percentages to post-tax
income); a default 90/10 split between diversified and individual stock
when advice says "stocks" without distinguishing; encoded common patterns
("emergency fund of X months", the 50/30/20 rule, the 4% rule, RMDs, a
target-date-style age formula for unspecified allocations); an extraction
priority order (annual dollars over lump sums over monthly over weekly over
paycheck over percentages); source limits and a budget identity; and a
deterministic repair step that scales flows to satisfy the accounting
identities, setting consumption to post-tax income with zero flows when the
advice contains no actionable spending or saving directive.

## The life cycle model: calibration and normative benchmarks

Calibration (Sec 1.2, Appendix B.6):

| Object | Value / source |
|---|---|
| Working life | ages 22 to 64 (enter 22, retire deterministically at 65) |
| Maximum age | dies by 90 (final year of life at 89) |
| Mortality | 2015 U.S. Social Security Actuarial Life Tables, age-dependent |
| Preferences | time-separable CRRA; household composition via the Lusardi, Michaud, and Mitchell (2017) equivalence scale |
| Labor states | employed, job-to-job transition, unemployed, retired |
| Income process | cubic age profile + persistent AR(1) + transitory shock, SIPP-estimated; job-to-job moves carry expected wage gains, unemployment spells persistent wage losses on reemployment |
| Initial unemployment | 22% at age 22 (SIPP share) |
| Taxes | 2025 U.S. federal schedule, single filer, standard deduction |
| Social Security | 2025 benefit formula, SSI floor; benefits tied to average lifetime earnings |
| Unemployment insurance | 40% replacement rate |
| Risk-free rate | 2% real |
| Equity premium | 6.4% (CRSP value-weighted index, CPI-adjusted, 1925-2006, minus the 2% risk-free rate) |
| Equity volatility | 20% (log returns) |
| Capital tax | flat 21% |
| Non-diversified assets | calibrated to individual-stock evidence in Bessembinder (2018): arithmetic mean 0.1474, SD 0.819; constructed so neither can improve the Sharpe ratio of a bond-plus-index portfolio, so the model benchmark optimally holds zero of them |
| Constraints | no borrowing, no leverage; equity share in [0, 1] |
| State variables | age, labor productivity, transitory shock, employment status, tenure, average lifetime income, savings |

Normative benchmarks the model supplies (all under the SMM-estimated
preferences of Table 2 unless noted):

- **Equity over the life cycle**: essentially 100% equity through the
  mid-30s, declining after 45 toward 50 to 60% late in life (Figure E10,
  orange line). High equity early in life is a standard implication absent
  participation costs or labor-income correlation (footnote 12).
- **Zero non-diversified holdings**, by construction of the return
  processes (Sec 1.4, Appendix B.3).
- **Retirement decumulation faster than 4%**: almost no model-optimal
  withdrawal rates fall below 4% of assets (Sec 3.2, Fig 7).
- **Consumption smoothing through job loss**: consumption barely moves at
  unemployment because buffers absorb the shock (Fig 8, Figure E11).
- **Active rebalancing**: actual portfolio changes essentially uncorrelated
  with passive drift (slope 0.02 to 0.03); CRRA target allocations are not
  wealth-sensitive, and portfolios are re-chosen each period (Sec 3.2).
- **Aggregate magnitudes for comparison** (Table E3, means over ages
  22-64, employed unless noted): the LLM-advised path consumes $48,842 per
  year on average versus $59,578 in the model; holds an average equity
  share of 64% versus 81%; has a net saving rate of +17% of post-tax
  earnings versus -7% (the model dissaves late in working life: its net
  saving rate for employed individuals falls from +40% at 22-29 to -98% at
  60-64, while the LLM's stays positive, +21% falling only to +7%). Stock
  market participation is 97% under both. By ages 60-64, employed LLM
  followers hold about $2.15M in liquid wealth versus about $1.32M in the
  model. Both series exceed observed behavior by far; the LLM's
  distinctive error relative to the model is over-accumulation late in
  working life and under-spending in retirement.

Selected age profiles for employed individuals (Table E3, means):

| Statistic | 22-29 | 30-39 | 40-49 | 50-59 | 60-64 |
|---|---|---|---|---|---|
| Post-tax earnings, both simulations ($) | 44,145 | 60,884 | 68,857 | 66,335 | 60,191 |
| LLM consumption ($) | 34,637 | 47,804 | 53,918 | 54,914 | 53,437 |
| Model consumption ($) | 25,450 | 43,469 | 64,936 | 85,830 | 99,249 |
| LLM liquid wealth ($) | 46,964 | 215,949 | 618,130 | 1,350,137 | 2,147,938 |
| Model liquid wealth ($) | 70,262 | 334,886 | 736,493 | 1,124,386 | 1,315,676 |
| LLM equity share (%) | 45 | 69 | 73 | 66 | 59 |
| Model equity share (%) | 86 | 97 | 82 | 67 | 57 |
| LLM net saving rate (% of earnings) | 21 | 19 | 18 | 14 | 7 |
| Model net saving rate (% of earnings) | 40 | 23 | -4 | -48 | -98 |
| Employment rate, both (%) | 90 | 91 | 91 | 85 | 61 |

The model consumes less than the LLM early (building its 100%-equity
buffer faster), then crosses over around age 40 and consumes far more
late; the two equity-share paths converge after 50 but diverge sharply
before 45. The SMM estimation excludes retirement-age wealth-to-income
moments precisely because the LLM's bunched withdrawal rules are outside
what the two-parameter model can reproduce, and it omits the first year
(zero wealth by construction) and the first and last periods for equity
shares (Appendix D).

## Implications for a planning skill

Stated as boundaries and facts, judged against the paper's evidence:

- **The failure modes are properties of unaided one-shot advice.** The
  documented regime is a 200-word, low-reasoning, no-memory reply to a
  layperson's prompt. A planning process that supplies complete state
  variables and explicit economic assumptions is operating in the regime
  the academic prompt tested, where round-number bunching fell from 31.0%
  to 14.6%, the 4%-rule spike from 98.3% to 8.8%, the implied discount
  factor from 1.034 to 0.990, and consumption smoothing became
  model-like (Sec 3.3). Information completeness and explicit framing are
  measured determinants of advice quality.
- **Rebalancing is the exception: structure does not fix it.** The
  passive-drift slope stayed at 0.96 under the academic prompt, with the
  existing allocation stated in the prompt (Fig 9). The default is to
  advise on new savings and leave existing holdings; a plan that needs
  rebalancing must carry it as an explicit rule, because it will not
  emerge from the advice.
- **Retirement decumulation is where the heuristic bites hardest.**
  98.3% of unaided withdrawal recommendations sit at or below 4% of
  assets while the calibrated model prescribes faster decumulation almost
  everywhere (Fig 7). A drawdown schedule inherited from generic LLM
  advice is predictably too conservative against this benchmark.
- **The high-patience direction is over-saving, not under-saving.** The
  advice implies beta = 1.034: consumption below income throughout
  working life and roughly $2.15M at 60-64 versus $1.32M model-optimal
  (Table 2, Table E3). The paper offers a paternalism reading (buffers
  against imperfect implementation), but if a plan's recommendations are
  followed exactly, this is a quantifiable bias.
- **Post-shock consumption rules need to be explicit.** Unaided advice
  cuts consumption roughly in proportion to income at job loss even when
  the simulated individual holds sizable liquid wealth (Fig 8). A plan's
  decision rules for drawing buffers during income interruptions cover a
  failure the advice makes by default.
- **Advice inherits the asker.** Wealth-at-60 differences of 4.1%
  (financial literacy), 5.7% (prior AI use), and 4.1% (gender) arise
  purely from who wrote the prompts (Fig 11). Two-thirds of the gender
  equity gap is demand: it survives even with identical gender labels
  (Table 3). A plan built from a user's own framing inherits demand-side
  variation; the supply channel (-0.54pp diversified equity per period
  from a female label alone) is a property of the model itself.
- **Single-query numbers are noisy.** A repeated identical query moves
  recommended annual consumption with a median SD of $3,220 and the
  equity share by 6.5pp (Figure E17). Any procedure that treats one
  generation's number as the number is sampling from that distribution.
  Deterministic computation, or aggregation across repeated queries,
  is the measured alternative; the translation-only SD ($335, 1.6pp)
  shows constrained extraction is far more stable than open generation.
- **The direction of unaided advice is not the enemy.** Relative to what
  people actually do, following even one-shot advice raises
  participation, builds buffers, and tilts toward diversified funds
  (Fig 5), and the model adjusts saving and risk in sensible directions
  in response to hardship, macro worry, and stated risk preferences
  (Fig 6). The departures are second-order relative to observed behavior
  and first-order relative to the theory benchmark.
- **Eval-relevant exact figures**: 31.0% and 34% (saving-rate and
  saving-amount bunching, Fig 7); 98.3% (withdrawals at or below 4%,
  Fig 7); 0.96 (drift slope, Fig 9); 1.034 / 5.3 and 0.990 / 4.7 (SMM,
  Table 2); 14.6% and 8.8% (academic prompt, Fig 10); -1.50 / -0.96 /
  -0.54 pp (gender equity decomposition, Table 3); $3,220 / 6.5pp and
  $335 / 1.6pp (stochasticity, Figure E17); 48% prior AI use, 71.9%
  ChatGPT share (footnote 3, Figure E3); 84% Liquidity mention rate in
  advice vs 6% in prompts (Sec 2.1).

## Limitations and open questions

- **Advice is not behavior.** The paper characterizes the effect of
  following advice; whether people act on LLM recommendations, and how
  effects compare with human advisors and robo-advisors, are open
  questions (Sec 5). Early external evidence: Moss, Wegner, and Zechman
  (2026) find investors do act on an AI adviser's recommendations, and
  greater user intervention is associated with worse risk-adjusted
  performance (footnote 22).
- **One-shot 200-word advice is not an agentic run.** No follow-up
  questions, no tools, no memory, low reasoning effort. The paper itself
  demonstrates (academic prompt, direct-to-JSON) that richer interaction
  regimes change several results.
- **Model generations change.** Results are for GPT-5.2, Gemini 3 Flash,
  and GPT-5.6 Terra; the authors frame the contribution as a reusable
  survey-and-simulation framework and a set of diagnostics (consumption
  smoothing, diversification, rebalancing) precisely because model
  behavior will move (intro, Sec 5). Closed-source models limit
  reproducibility (footnote 6).
- **Scope**: spending, saving, investing only; no insurance, housing, or
  credit management (intro). The trade-off between prompt specificity and
  external validity is acknowledged as a design choice (Methodology, p. 3).
- **Sample**: Prolific skews (unemployment over-represented, retired and
  70+ under-represented, Table E1); no Hispanic ethnicity data
  (footnote 21).
- **Supply-channel identification is label-based.** The null supply effect
  for race speaks only to explicit statements; subtler cues are untested
  (Sec 4.2).
- **The academic prompt is not a pure upper bound.** It assumes single, no
  dependents (footnote 5), and its improvements bundle content and framing
  with quantitative elicitation; the paper attributes the gains to content
  and framing because skipping translation alone reproduced the baseline
  (footnote 15, Sec 3.4).
- **Estimated preferences are a fitting device.** Beta and gamma summarize
  distance from the model on 324 moments with a two-parameter search
  (Appendix D); the model cannot fit the LLM's low early-life equity
  shares at any parameter values (footnote 12), so the estimates
  compress some misfit.

## What this file left out

Everything below exists in the paper and was cut or compressed here:

- **Full prompt texts.** The complete academic prompt (system and user
  sections, internal computation structure, all 21 JSON output keys) is in
  Appendix A.5.1 with Table A3; the complete translation prompt with every
  extraction, annualization, conflict, and repair rule is in Appendix
  A.5.2. This file summarizes their design features only.
- **The full 27-category keyword dictionary.** Category names are listed
  above; the complete keyword lists (hundreds of terms, including all
  tickers under Products and all firms under Providers) are in Table C1.
- **Life cycle model equations.** The income processes for employment,
  job-to-job, and post-unemployment states, the savings account and
  return-process equations, the non-diversified return construction
  (beta, idiosyncratic volatility, log intercept formulas), and the
  government sector are in Appendix B, equations (5) through (19).
- **Table 1's worked single-period example** (a 26-year-old's raw prompt,
  prepared prompt, full LLM advice text, extracted choices, and updated
  states), useful for seeing the pipeline concretely.
- **Word clouds** (Figs 2, 12, E5, E18, E22) beyond the term lists quoted
  here, and the per-prompt topic mention rates for all 27 categories
  (Figures E4, E6).
- **Table E3 in full**: age-group-by-employment-status means for earnings,
  consumption, wealth, participation, equity share, and saving rates in
  both simulations; only selected values appear here.
- **Figure-level detail on alternative models** (E7, E9, E10 Panels C and
  D) and the academic prompt profiles (E13, E14), beyond the summary
  statistics quoted.
- **Related-literature positioning** (intro pp. 5-7): the human-advice,
  robo-advice, and LLM-as-economic-agent literatures, including Rumpf et
  al. (2026), Fedyk et al. (2026), Ouyang et al. (2025), Cook et al.
  (2026), and Abdel Haq et al. (2026).
- **Survey instrument details**: exact survey question wording (Figure E1)
  and the demographic questionnaire beyond what Table E1 reports.

Nothing else was cut for length; every quantitative finding in the main
text's three facts, the heterogeneity and decomposition tables, the
robustness section, and the calibration appendix appears above with its
source anchor.
