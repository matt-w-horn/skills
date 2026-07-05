# Stage 5: Analysis agents

Goal: four independent reads of the same dossier, each from one angle, merged into `analysis.md`. Independence is the point: an agent looking only at constraints will find things the narrative-minded orchestrator has already smoothed over, and fresh context has no attachment to the story built during the interview. This is the same design as multi-reviewer code review: same data, different reviewers, different findings.

## Preconditions

The person has confirmed the dossier and the financial summary. Announce that several minutes of autonomous analysis are starting; no user input until it completes.

## Dispatch

Launch all four in parallel. Each agent receives: the contents of `dossier.md`, `evidence.md`, `finances/finances.md`, and `values.md` (or file paths, if subagents share the filesystem); its role prompt below; and the shared requirements. Save each agent's output to `agents/`.

**Shared requirements, included verbatim in every agent prompt:**

> Every claim you make about this person must cite an entry in the evidence provided (quote the entry or its tag). If you notice a pattern the evidence only partially supports, you may state it, labeled as conjecture, with what would confirm it. Do not invent connective tissue to make the story cohere; an uncited claim is worse than a gap. Write findings a stranger could act on: specific, concrete, no filler. Target 400-800 words.

### Agent 1: Near-term constraints (0-3 years)

> Role: identify everything that binds this person's choices in the next three years. Cash flow and runway; debts; vesting and notice periods; family obligations and their dates; health items; visa or residency clocks; commitments already made to other people; the cost and reversibility of leaving their current position. For each constraint state: hard or soft (their own classification where available), what it forbids, what it merely taxes, and when it expires or changes. End with the two or three constraints that most limit near-term moves.

### Agent 2: Horizon constraints and trends (3-40 years)

> Role: identify what shapes the decades. Long-run dependencies: healthcare coverage between any early exit and public eligibility, caregiving that is foreseeable, longevity exposure, the durability of the household's second income if there is one. Then external trajectory: how exposed is this person's field and skill set to automation and structural change, and in which direction, noting that exposure cuts both ways (skills that AI progress devalues, and skills it makes scarcer and more valuable). Identify which of their demonstrated skills are invariants likely to port across technology shifts and which are tied to a particular substrate. Where the field's direction is genuinely uncertain, do not predict; define two or three observable tripwires (things checkable once a year) and state what each one, if tripped, changes. End with the dependencies a 40-year plan must carry explicitly.

### Agent 3: Capability audit

> Role: state, honestly and with evidence, what this person's record proves they can do, what it suggests, and what it does not yet support. This is the load-bearing agent for the process's purpose: helping a person realistically see what they are capable of. Work in both directions with equal energy. Ceiling shown: the hardest things actually done, with the conditions under which they were done. Repeatable patterns: what they have done three or more times across different contexts (the strongest predictor of what they can do again). Rate of acquisition: evidence of how fast they pick up new domains, which bounds what "retrain" paths cost. Undersold strengths: capabilities the record demonstrates that the person did not claim, or disclaimed. Unproven aspirations: stated ambitions the record does not yet support, with the honest gap named and, where visible, what closing it would take; distinguish "no evidence yet" from "evidence against." No flattery, no deficit-framing; a capability statement the person could hand to a skeptic.

### Agent 4: Fit and friction

> Role: from the role history, reviews, and departure reasons, characterize the environments in which this person thrives and the environments in which they degrade. Look for the repeated shape in the friction: what conditions were present each time things went badly, and each time things went unusually well? Distinguish person-shaped causes from environment-shaped ones only as far as the evidence allows; the useful output is conditional, not diagnostic: "under conditions A, the record shows X; under B, Y." Include what the person has already learned to do about it, if the record shows an evolved response. End with: conditions to seek, conditions to avoid or price in, and the observable early-warning sign that a new environment has the bad shape.

## Merge

Read all four outputs. Write `analysis.md` with four sections mirroring the agents, then a fifth: **Contradictions and uncertainties**, listing anywhere the agents disagree with each other or with the person's self-account. Resolve disagreements only where the evidence clearly favors one side; otherwise carry them as labeled uncertainty. The merged file, not the raw outputs, is what the path agents consume, so it must stand alone; but keep the raw outputs in `agents/` because the stage-7 verifier audits against them.
