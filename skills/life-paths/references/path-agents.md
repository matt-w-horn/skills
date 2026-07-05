# Stage 6: Path generation agents

Goal: several genuinely different paths, produced by parallel agents that see the same complete picture but each optimize through one lens. The lens structure exists to defeat the strongest failure mode of plan-writing: producing one path in different costumes. An agent told to find "the best independent path" cannot converge with an agent told to find "the best institutional path"; forced divergence at generation time is what makes the final options real.

## Dispatch

Launch four to six agents in parallel, one lens each. Every agent receives the same bundle: `dossier.md`, `evidence.md`, `finances/finances.md`, `values.md`, `analysis.md`, its lens prompt, and the shared requirements. Save each draft to `paths-draft/`.

**Shared requirements, included verbatim in every agent prompt:**

> Build the strongest version of a path through your assigned lens for this specific person. Requirements:
> - Ground it: at least three citations from the evidence showing why this path is theirs and not generic. If your lens genuinely has no strong version for this person, say so in three sentences and stop; a forced path wastes everyone's time.
> - Respect the hard constraints and financial dependencies in the analysis; where your path strains a soft constraint, price it explicitly.
> - Optimize for what values.md says this person actually values, in your lens's way.
> - Deliver: (1) the bet, one paragraph: what this path optimizes for and where its enjoyment and impact come from; (2) a phased schedule from now into their 70s, with ages and concrete moves, including exactly what changes at the work-optional date from the financial summary; (3) the falsifier: the observable sign, checkable within a few years, that this path is wrong for them; (4) the destination: a half-page sketch of the record at the end (what they are known for, what exists because of them, the texture of an ordinary week at 70); (5) the main risk, stated honestly, including this path's exposure to the tripwires in the analysis.
> - Commit. You are this path's best advocate; the synthesis stage does the judging. But advocate with evidence, not brochure copy: the horoscope test applies (any sentence that would fit a random person of their profession gets cut).

## The lenses

Default set below; choose which to run based on the person (a 24-year-old and a 58-year-old need different sets), and rename freely. Four minimum, six maximum.

1. **Continuity.** The strongest version of not changing course: their current trajectory continued deliberately, priced correctly, with drift replaced by decisions. This lens keeps the process honest; sometimes the best path is the one they are on, chosen on purpose.
2. **Institutional depth.** The deepest version inside organizations: seniority, scope, becoming the person institutions cannot replace. Impact through position; enjoyment through mastery and hard problems supplied at scale.
3. **Public artifact.** Impact through things that outlive any employer: a book, a body of work, open tools, a standard, a practice with their name on it. For people whose record shows unprompted making and writing, this lens usually has deep evidence to draw on.
4. **Independence.** No institutions: solo practice, craft, portfolio life. Optimizes autonomy and time; must engage seriously with the financial dependencies and with whether the record shows self-directed finishing.
5. **Reinvention.** The discontinuous option: a different field, founding something, a retrain, a geographic reset. This agent's job is the path the person has not considered but their record makes possible; the capability audit's rate-of-acquisition and undersold-strengths findings are its raw material. It must still be evidence-bound: reinvention grounded in demonstrated transfer, not fantasy.
6. **Service and meaning** (run when values.md shows fairness, community, or mission ranking high): public service, teaching, movement or standards work, care. Often the lens that surfaces what the other five structurally cannot.

## After the drafts return

Skim all drafts before moving to synthesis. If two lenses converged on essentially the same bet, that is information (note it; convergence across independent lenses is a strong signal about the person) but also a coverage gap; consider one additional agent with a lens chosen to fill the abandoned territory. If an agent returned "no strong version," record why; the absence is itself a finding that belongs in the final document's reasoning.
