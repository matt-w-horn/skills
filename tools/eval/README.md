# Skill evals

Two things decide whether a skill is worth having: whether Claude reaches for
it when it should, and whether the run produces something worth having. This
directory measures both, separately, because a skill can route perfectly and
produce nothing, or produce beautifully and never fire.

Nothing here runs in CI except the linter and the unit tests. The sweeps need
the `claude` CLI and cost time and money, so they are run deliberately.

## Running it

```bash
python3 tools/eval/lint_evals.py              # corpus quality gate (also in CI)
python3 tools/eval/grade.py --calibrate       # test the judge before trusting it
python3 tools/eval/run_trigger.py --split graded
python3 tools/eval/run_exec.py --runs 2
```

Everything is stdlib. CI pins Python 3.12.

Results land under `results/`, one file per run. An interrupted sweep resumes
instead of restarting, and the raw stream for any number survives the number.

## Trigger evals

68 queries: 36 for `financial-planning`, 32 for `life-paths`. Of life-paths'
32, twenty-four are graded (11 that should fire it, 12 that should not, made
up of 8 near-misses and 4 where the *other* skill should win, plus 1 marked
either) and 8 are sealed, split 14 train / 10 validation / 8 sealed.
financial-planning carries the same 32 plus four demand-modeled queries
(`fp-t33`–`fp-t36`, two positives and two near-misses patterned on how
people actually prompt LLMs for money advice — see the citation at the
bottom), giving it 28 graded split 16 train / 12 validation. Each query
carries expectations for *both* skills, because the two skills overlap on
purpose and the interesting question is which one wins.

```json
{"id": "fp-t01", "query": "...", "why": "...", "split": "train",
 "expect": {"financial-planning": true, "life-paths": false}}
```

Model behaviour is not deterministic, so each query runs three times and scores
a trigger rate rather than a yes or no. A rate of 2/3 and a rate of 3/3 are
different facts about a description, and collapsing them hides the difference
between "marginal" and "fine". Queries pass at a rate of 0.5 or better on the
right side.

`expect` also allows `"either"`, for the handful of queries where a domain
expert would genuinely accept both skills. It marks a skill whose firing is
defensible but not required, so it places no constraint on that skill while
every definite expectation in the same query still has to hold. Only when a
query is `either` all the way down does the rule become "something must fire",
which is what stops the label from excusing a total miss. The linter caps it at
8 across the corpus; the three that exist each pair with a definite `true`.

Splits are written into the files rather than computed from a seed. A
seed-based split reshuffles the whole corpus the moment a query is added, which
destroys comparability against every earlier run without saying so.

The sealed split answers one question: does a description generalize past what
it was tuned against? That answer is worth having once. Running it again after
a change makes it another training set, so a second run needs `--force` and
gets recorded.

## Execution evals

Eight evals across the two skills, 104 assertions, in two shapes. Three of
the assertions (ids `pd*`) form a labelled non-blind tier described under
Blinding below.

**Seeded-defect audits** hand over a flawed artifact and ask for a check. The
defects were planted, so ground truth is known rather than argued about, and
`eval.json` maps each planted defect to the assertion that must catch it.

**Finish-the-job** runs hand over a person's own notes and ask for the
deliverable. The prompt carries the person's confirmation in their own words,
because both skills stop and check before doing hours of work, and a run that
correctly stops to ask a question produces nothing to grade.

Every eval runs with the skill and without it. A pass rate with no baseline is
uninterpretable: if a competent model produces the same document unaided, the
skill is spending tokens and latency to change nothing.

The per-assertion cross-tab is the useful output, not the headline. An
assertion that passes in both configurations inflates the score while measuring
nothing, and `run_exec.py` names those so they get cut or sharpened.

## Keeping the two configurations apart

Both skills are symlinked into `~/.claude/skills` on the author's machine, so a
naive baseline would still see them. The configurations differ by one flag:

```
without_skill   --setting-sources project
with_skill      --setting-sources project --plugin-dir <repo>
```

`--setting-sources project` drops the user's own skills directory, and an empty
working directory has no project settings, so only Claude Code's built-ins
remain. Loading the repo as a plugin adds the two under test, named
`skills:financial-planning` and `skills:life-paths`.

This was established by measurement rather than assumed, in a probe kept in
`harness.py`'s module docstring: on a query that fires the skill five seconds
in with the plugin loaded, the baseline configuration worked for 226 seconds
and made no `Skill` call at all. That probe is not committed here, so treat it
as one observation, not a guarantee. The check that runs every time is
stronger: the harness voids any baseline run that does invoke a skill under
test, because one that does means isolation leaked and every baseline number in
that sweep describes something else.

Two other failure modes get their own handling. A timeout or a subprocess error
is recorded as an error, never as a no-trigger; a harness that conflates them
reports a confident zero when it is simply broken. And a run is never called a
no-trigger just because some other tool was used first, since a model may read
a file or two before deciding.

## What the numbers license

Three runs per query gives a per-query rate from the set {0, ⅓, ⅔, 1}. That
catches a query that never fires. It cannot tell 0.55 from 0.8.

At the aggregate level the honest arithmetic depends on which n you mean. Pooled
across both skills that is 48 graded queries; per skill it is 24. On the current
result of 48/48, the rule of three puts the 95% lower bound on the true pass
rate near 94% pooled, and near 88% for a single skill. Detecting a *change*
compares two such estimates, which is a weaker test than either one: at 48
queries a drop needs to be around 15 points before it clears noise, and at 24 it
needs closer to 20. A five-point drift will not show up here.

Two runs per configuration on the execution side licenses almost no statistical
claim at all. Its value is catching a skill that stops producing a deliverable,
plus the transcripts. Read those before believing any of it.

## Blinding, and what it buys

The queries and assertions were written by agents given the skill's `name`, its
verbatim `description`, and a domain brief drawn from public practice. They were
not given the SKILL.md body, the reference files, or the scripts.

The honest claim that supports: assertions come from the skill's public contract
and outside domain knowledge rather than from paraphrasing the skill's own
instructions. That heads off the tautology where a rubric tests whether a skill
can follow itself, and the case where a query quotes the description back at it
and inflates the score.

It does not guarantee that an assertion discriminates. That is an empirical
property, established by the cross-tab, not conferred by how the assertion was
written.

One labelled exception. Three assertions (ids `pd1`/`pd2`, marked
`"source": "llm-advice-paper"` in their rubrics) were added after the first
run, derived not from the skill body but from published measurements of how
LLM financial advice fails (the paper cited below): sustainability argued
from a fixed withdrawal-rate rule, portfolio allocation left to drift
unaddressed, and spending advice that collapses with income instead of using
the buffer. They are sourced independently of the skill text, but they are
not blind in the original sense: the skills were edited against the same
paper in the same change, so these assertions and the skill share an
ancestor. The cross-tab treats them like any other assertion; the label
exists so nobody mistakes them for the blind tier.

The linter's leakage rule is what makes any of this checkable rather than
asserted: it fails the corpus if a query or assertion shares a five-word phrase
with any skill body that appears in no description. It cannot prove an author
never looked, because paraphrase walks straight past it. What it catches is the
specific failure blinding exists to prevent, an eval written by restating the
skill's own words.

## Known confounds

Two worth stating, because they bound what the execution numbers mean.

Every fixture file carries a line marking it synthetic, which the linter
enforces so invented personal records never read as real ones. That line is
inside the material the model under test reads, so the model can tell it is
being evaluated. Moving the marker into filenames or a manifest the model never
sees would remove the confound and lose the safeguard; for now the safeguard
wins and the confound is written down.

In the finish-the-job evals the synthetic client's own notes ask for much of
what the rubric checks, because a blind author had to put the requirements
somewhere gradeable. A baseline that simply follows written instructions
therefore passes a good share of those assertions, and the measured difference
between configurations rides on the few that the client never asks for. Read
the cross-tab rather than the headline; it names which is which.

## Where the rules came from

Sizes, balance, the near-miss requirement, three runs per query, the 0.5
threshold, the train/validation split, binary assertions with cited evidence,
and grading outcomes rather than trajectories all come from Anthropic's
[skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents),
and agentskills.io on [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
and [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills).

Two deliberate departures:

Those sources recommend writing assertions *after* seeing first outputs. That is
the tautology risk above, so assertions here are written blind and the criteria
that emerge later go to the dev tier, never to the sealed one. Shankar et al. on
[criteria drift](https://arxiv.org/abs/2404.12272) is why the tiers have to be
separate rather than why blinding should be abandoned.

The trigger harness shipped with Anthropic's `skill-creator` registers a
synthetic slash command and counts a trigger only when that synthetic name
appears, so a skill installed under its own name scores zero on every row with
no warning. This one scans the whole event stream for a `Skill` call matching
either the bare or the plugin-namespaced name, and also counts a `Read` of that
skill's own `SKILL.md`, which is the other way a model reaches a skill's
instructions.

The demand-modeled trigger queries and the `pd` assertion tier come from
[Choukhmane, de Silva, Lin & Akuzawa, "AI Financial Advice: Supply, Demand,
and Life Cycle Implications" (working paper, July
2026)](https://www.timdesilva.me/files/papers/llm_advice.pdf), which surveys
952 U.S. adults on what they actually ask LLMs for financial advice and
simulates lifetime outcomes of following it. Real prompts are short (mean 27
words for the advice asks), colloquial, and dominated by budgeting and
where-do-I-park-this asks; the new near-misses are patterned on those, and
the new positives on the paper's persona-wrapped and permission-to-spend
prompts. The same paper measures within-person stochasticity by repeating
identical prompts five times (median SD of 6.5 points of equity share per
person), which is the multi-run reasoning this suite applies to triggering.
