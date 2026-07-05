# Stage 7: Synthesis and delivery

Goal: turn the drafts into one document the person can steer by for years, verify every claim in it, and hand it over with a committed recommendation.

## Select and merge

Read all drafts in `paths-draft/`. Merge any two that are the same bet in different clothes; the test is whether they optimize for the same thing and diverge only in texture. Select three to five paths that span genuinely different bets. Fewer than three is a verdict pretending to be options; more than five is a menu nobody can hold in their head. A dropped draft can still contribute a phase or an insight to a surviving path; strip it for parts before discarding.

Rewrite the survivors in one voice, plain language throughout. Introduce every idea from something already on the table before naming it (a reader should never meet a coined term before meeting the thing it names), and prefer not coining terms at all. The person will reread this document in ten years; write for that reader.

## The deliverable

`LIFE_PATHS.md`, in this structure. Adapt proportions, not the skeleton:

```
# [Person]'s Paths - [date]
Intro: what this document is, the conventions (ages, the work-optional
date and what moves it), and a one-line invitation to disagree.

## What the record shows
The evidence summary, about a page: the repeating unit of their working
life, the capability statement (both directions), the binding
constraints, the fit conditions, and how evidence was weighted for this
person and why. This section is the document's foundation; a reader who
stops here should already know themselves better.

## The paths at a glance
One short paragraph per path: the bet, in plain words.

## Path sections (one per path)
The case (why this is theirs, cited) -> the phased schedule with ages
-> the falsifier -> the destination sketch. Schedules are lists with
bolded age ranges, concrete enough to act on this quarter.

## Tripwires
The external-trend checks from the analysis (AI progress and field
automation exposure will usually be among them, in both directions:
what it threatens and what it makes more valuable). Each tripwire is
observable, checkable annually in minutes, and mapped to what it
changes per path. Include the symmetric case: what holds if nothing
trips.

## Recommendation
Your committed bet: which path, or which braid of paths, and the
reasoning before the conclusion. State what evidence would change your
mind. One bet, placed plainly; the reader can feel the difference
between a recommendation and a survey.

## Decision gates
Two or three dated checkpoints. At each, a written one-page review
against a rubric built for how this person actually reads themselves:
behavioral tests first (what did you build unprompted and finish; what
did you return to after shipping; did anyone outside adopt or read
your work without being asked; where did the discretionary hours go;
what does the trusted observer say), introspective questions only as
secondary and only if intake found their introspection reliable.

## Shared near-term actions
The moves that are correct on every path, so they can start Monday
without having decided anything.
```

## Verification pass

Before delivery, dispatch one fresh-context verifier subagent with `LIFE_PATHS.md`, `evidence.md`, `dossier.md`, and the raw agent outputs:

> Audit every factual claim about this person in the document against the evidence provided. For each claim: supported (cite the entry), conjecture-but-labeled (fine), or unsupported. Also flag: any sentence that would be true of most people in their situation; any coined term used before being introduced; any place the recommendation hedges into a survey. Return the list of findings only.

Fix or cut everything the verifier flags. Unsupported claims get evidence or get deleted; there is no third option, because one confabulated "fact" about the person costs the document its authority over everything else in it.

## Presentation

Deliver the file. In the message alongside it, lead with the recommendation and the one or two findings that most shaped it, briefly; the document carries the rest, and a wall of summary in chat teaches them not to read the artifact. Make three things explicit, once each: the document is theirs to disagree with, and their disagreement is data worth capturing in `notes.md`; the gates are the mechanism, so the document is working precisely when reality diverges from it and a gate catches that; and revisions are cheap, so reactions now are welcome. Offer PDF or docx conversion after they have read it. If the process surfaced hard findings (an unsupported aspiration, a later work-optional date than hoped), name where they live in the document rather than smoothing past them; the person paid for honesty with hours of their life, and they should get it.
