---
name: life-paths
description: Structured process for mapping realistic long-term life and career paths for a person, grounded in their actual record and finances rather than generic advice. Use this whenever someone asks for help figuring out what to do with their life or career, wants a long-term or phased plan, mentions retirement or FIRE timing alongside career choices, asks whether they could realistically become or achieve something, wants purpose or direction, is at a crossroads (job offer, layoff, burnout, sabbatical, windfall, relocation), or asks to compare possible futures. Trigger even when they ask only a piece of it, like "review my retirement model and tell me when I can quit," "should I take this offer or go independent," or "what am I actually good at" - the pieces connect, and this skill covers the whole.
---

# Life Paths

A process for helping a person see, realistically, what they are capable of and what futures are genuinely available to them, then mapping a few concretely different paths through the decades ahead.

## Why this skill exists

Career and life advice fails in predictable ways, and this skill is built against each failure:

1. **Generic output.** Advice that would fit anyone helps no one. Every claim in this process must be specific enough that it would be false for a random other person.
2. **Built on self-report alone.** People are often wrong about what they enjoy and what they are good at, in both directions. Some people know their own introspection is unreliable and will tell you so. The record (what they built, finished, abandoned, got praised or dinged for, did unprompted on weekends) is evidence; a feeling recalled in an interview is a weaker signal. Collect both, and when they conflict, say so and weight the record.
3. **Flattery and its opposite.** "You can do anything" and "be realistic, lower your sights" are both failures of evidence. The person deserves an honest capability audit: what their record proves, what it does not yet support, and what it would take to close the gap.
4. **One path in four costumes.** Options that differ only in tone are not options. Paths must be genuinely different bets about where enjoyment and impact come from.
5. **Money handled separately from meaning.** Financial reality determines when choices open up and what risks are survivable. A plan that ignores the finances is a wish; a financial model that ignores the person is a spreadsheet. This process does both, together.

Hold these five failures in mind at every stage; when in doubt, the move that avoids them is the right one.

## Core principles

- **Ground every claim.** Before asserting anything about the person, in analysis, paths, or the final document, be able to point to its source: a quote from them, an artifact they provided, or a pattern across artifacts. If you cannot cite it, do not claim it. This is the single most important rule in the skill.
- **Commit to a recommendation.** The deliverable ends with your actual bet and the reasoning for it, stated before the conclusion, plus what evidence would change it. Balanced non-answers waste the person's time.
- **Plans are instruments, not prophecies.** Every path gets a falsifier (the observable sign it is wrong for them) and the plan gets decision gates and external tripwires. The document should get more useful when reality diverges from it, not less.
- **The person owns the decision.** You map the territory and place a bet; they choose. Never pressure, and treat their disagreement with the recommendation as data, not error.
- **Depth follows appetite.** A full run takes hours across multiple sessions; some people want direction in thirty minutes. Ask early which they want, and scale (see "Light mode" below). Do not force a long interrogation on someone who came for a sketch.

## Workspace and memory

Create a working directory at the start (default `./life-paths-workspace/`, or where the user prefers) and treat it as the memory system across sessions:

```
life-paths-workspace/
  dossier.md        - the person: history, patterns, constraints, self-knowledge notes
  evidence.md       - claim log: each entry is a fact + its source tag
  finances/         - inputs, model config, simulation outputs, finances.md summary
  values.md         - output of the outcome-ranking stage
  analysis.md       - merged constraint/capability/fit analysis
  agents/           - raw subagent outputs, kept for the verification pass
  paths-draft/      - raw path drafts from the lens agents
  LIFE_PATHS.md     - the final deliverable
  notes.md          - process lessons, open questions, where you left off
```

Update files as you go rather than holding everything in context. If a session ends mid-process, `notes.md` records where to resume. Evidence entries use source tags: `[artifact: <name>]`, `[stated]`, `[behavior]` (something they did, per record or their account), `[observer]` (a third party's read), `[model]` (simulation output). Sensitive documents stay in the workspace; never quote them into external outputs without need.

## The stages

Read each reference file when you reach its stage; do not front-load them all.

| Stage | What happens | Mode | Read |
|---|---|---|---|
| 1. Intake | Artifacts gathered, structured interview, dossier built | Interactive | `references/intake.md` |
| 2. Finances | Full financial picture; audit their model or build one; simulate | Interactive, then compute | `references/financial.md` |
| 3. Drill-down | Resolve contradictions and gaps that would change paths | Interactive | `references/drilldown.md` |
| 4. Outcome ranking | Concrete future vignettes ranked; values extracted from reactions | Interactive | `references/outcome-ranking.md` |
| 5. Analysis | Four parallel agents: near-term constraints, horizon constraints and trends, capability audit, fit and friction. Merged into analysis.md | Autonomous | `references/analysis-agents.md` |
| 6. Path generation | Parallel agents, one lens each, same data; genuinely different path drafts | Autonomous | `references/path-agents.md` |
| 7. Synthesis | Dedup, select 3-5 paths, write the deliverable, verify claims, present | Autonomous, then present | `references/synthesis.md` |

Stages 1-4 can interleave in practice (finances often surface mid-interview; a contradiction can be chased the moment it appears). The order above is the dependency order, not a script. What must hold: no agent dispatch (stage 5+) until the person confirms the dossier and financial summary read true to them.

## Interaction boundaries

Stages 1-4 are conversations. Ask in small batches (one to three questions), end your turn, and wait; a wall of twenty questions kills the interview. If the environment has an option-selection or form UI, use it for rankings and multiple-choice; free text for open questions.

Stages 5-7 are autonomous. Announce what is about to happen and roughly how long it takes, then run without pausing. Pause only for input that only the person can provide. Before dispatching stage 5, get the explicit confirmation described above; that is the last checkpoint before several minutes of autonomous work.

## Evidence discipline for agents

Every subagent prompt in this skill includes the same requirement, and it applies to you directly as well: claims about the person must cite the evidence log or dossier. When you or a subagent write the person's story, the temptation is narrative coherence, inventing the connective tissue that makes a life read well. Resist it. A pattern asserted from two cited instances beats an elegant theory asserted from none. In the final deliverable, apply the horoscope test: if a sentence would be true of most people, cut it.

## Money notes

Financial modeling in this skill is educational analysis, not licensed financial advice; when the stakes of a decision are large (quitting, large purchases, cross-border moves), say once that a professional should verify the numbers, and move on without repeating it. Contribution limits, tax rules, benefit ages, and healthcare rules change and vary by country: verify current-year, current-jurisdiction facts with web search rather than memory. Ask the person's country early; do not assume the US. Stage 2 here is the quick pass a path decision needs; the companion `financial-planning` skill, if installed, builds the full verified plan and is the right tool once a path is chosen (it reads this skill's workspace directly).

## Code policy

`scripts/fi_model.py` ships with its tests (`python3 -m unittest discover tests`); run them once before trusting its output in a session, so a changed environment fails loudly. Any code written on the fly during a run gets its own tests before its numbers enter the dossier or deliverable, at minimum a hand-checkable deterministic case; untested code produces drafts, not findings.

## Care notes

This process asks people to look hard at their own record, and sometimes what surfaces is not a planning problem: acute distress, a crisis at home, health news, an unsafe situation. If that happens, stop being a process and be present; planning resumes later or not at all, at their pace. Similarly, if the capability audit or finances contain hard news (the record does not support an aspiration; the retirement date is further than they hoped), deliver it plainly and without cushioning it into vagueness, but deliver it as one finding among several, next to what the record does support. Honest and kind are compatible; the skill requires both.

## Light mode

When the person wants a fast pass: artifacts plus 15-20 minutes of interview, finances from their top-line numbers (run the simulator once with sensitivity flags rather than a full audit), fold outcome ranking into four to six vignettes presented inline, run two analysis agents (capability audit, constraints combined) and three path lenses, and produce a shorter deliverable without resumes. Tell them what a full run would add, once, and let them choose.

## Deliverable

The final artifact is `LIFE_PATHS.md` (structure specified in `references/synthesis.md`): the evidence summary, three to five paths each with the case, a phased schedule with ages, a falsifier, and a sketch of where it ends; external tripwires; a committed recommendation; decision gates with a behavior-based rubric. Offer conversion to PDF or docx after they have read it, not before.
