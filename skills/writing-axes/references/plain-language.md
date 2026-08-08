# Plain language

**When:** technical text whose reader is executing, troubleshooting, or scanning under
pressure. Primary on the Instruction axis, and on Orientation for technical material.

**When not:** Standing, Argument where persuasion is the point, and blog or launch prose.
These rules delete persuasion by design. Apply them to the docs a landing page links to,
never to the landing page.

This is an adaptation of ASD-STE100 Simplified Technical English, the controlled language
used for aircraft maintenance manuals. It keeps the mechanics that transfer outside
aerospace and drops the compliance apparatus: no rule numbers, no approved-word
dictionary, no strict mode. Applying this file does not make a text ASD-STE100 compliant;
never claim in output that it does. The standard is a free download at asd-ste100.org.

## Classify first

Every rule below depends on this fork, so make it before counting anything.

| | Procedural | Descriptive |
|---|---|---|
| Doing what | Telling the reader what to do | Explaining what a thing is or does |
| Verb form | Imperative: "Run the migration." | Simple present, past, or future |
| Sentence budget | 20 words | 25 words |
| Unit rule | One instruction per sentence | One topic per paragraph, six sentences maximum |

Do not mix the two inside one passage. A "Getting started" section is procedural; an
"Architecture" section is descriptive; a note inside a procedure is descriptive, takes the
25-word budget, and carries no imperative.

## Counting convention

This is what makes the budgets usable on software text. Each of these counts as **one
word**: backticked code, identifiers, numbers with units, quoted text, titles and labels,
and proper nouns. `sqlpipe run --config sqlpipe.yaml` is one word, not four, so long
identifiers never blow the budget. A hyphenated word is one word. Text inside parentheses
counts as one word.

Break noun chains longer than three words with prepositions:

- **Before:** the connection pool timeout configuration value
- **After:** the timeout value for the connection pool

## The modal ladder

| You wrote | Write instead |
|---|---|
| should (requirement) | must |
| should (recommendation) | Delete it, or state it as fact: "X is better because Y." |
| may, might, could (possibility) | can |
| may (permission) | can |
| would (hypothetical) | Restructure: "If X occurs, Y occurs." |

This matters double in text a model will execute: a model reads "should" as optional. In a
prompt, a skill, or an AGENTS.md, every "should" is either a "must" or a deletion.

## Term rotations

Universal rule 8 says one term, one concept. These are the rotations that actually show up;
collapse each to a single term and hold it for the whole document set.

- check / verify / confirm / validate / ensure
- config / configuration / settings / options
- delete / remove / drop / destroy (one per meaning, then kept)
- error / issue / problem / failure ("error" for errors, "failure" for failed operations)
- run / execute / invoke / launch
- show / display / render / present

Pick the verb and the noun **before** drafting, not during the edit pass. Choosing mid-draft
is how a document ends up with three of them.

## Slop substitutions

The lexical complement to `tells.md`, which hunts syntactic shapes and explicitly cannot
catch these. If a word on the left carries no fact, delete it rather than replacing it.

| Slop | Write instead |
|---|---|
| leverage, utilize | use |
| in order to | to |
| prior to | before |
| ensure | make sure that |
| it is worth noting that | (delete) |
| it's important to, crucially | (delete, and state the fact) |
| simply, just, easily, seamlessly, effortlessly | (delete) |
| robust, powerful, comprehensive, performant | (delete, or give the measurable property) |
| functionality | function, feature |
| enables you to, allows you to | you can |
| is designed to, aims to | (delete, and say what it does) |
| facilitate | help, make possible |
| dive into, delve into | read, examine |
| when it comes to | for |
| in the event that | if |
| due to the fact that | because |
| as needed, as necessary | (state the condition) |
| and/or | Pick one, or write "X, or Y, or both" |
| e.g., i.e., etc. | for example, that is, (name the items) |
| gracefully handles | (say what it does: "retries three times, then stops") |
| out of the box | by default |
| under the hood | internally |
| blazingly fast, state-of-the-art | fast, with the number (or delete) |
| streamline | make simpler, make faster |
| plethora, myriad | many |
| addresses the issue, tackles | corrects the fault, removes the error |

## Genre adaptations

Same rules, different targets. The mode column sets the budget.

| Genre | Mode | The adaptation |
|---|---|---|
| Error messages, CLI output | Procedural | State what happened (simple past), the cause if known, then the fix as an imperative. No "Oops", no "Please ensure", no apology filler. The highest-value target: an error message is a 2 a.m. instruction to a stressed reader. |
| Runbooks | Procedural | The home turf. Every step imperative, conditions first, warnings before the step. Hold 20 words hard: an operator under pager stress reads each sentence once. |
| Incident reports | Descriptive | Simple past only. A timeline in present perfect hides when things happened. "We have identified an issue that may have impacted some users" becomes "Between 14:02 and 14:31 UTC, 12% of requests failed." State what is known and write "unknown" for the rest. |
| Commit messages, PRs | Imperative subject, descriptive body | Convention already matches. Apply the substitution table to the body and delete "this PR aims to". |
| Release notes | Descriptive | One entry, one change. "Breaking:" entries lead with the command: "Update your calls to `v2/users`. The `name` field split into `first_name` and `last_name`." |
| Agent instructions | Procedural | A prompt is a procedure for a reader that cannot ask questions. One instruction per sentence keeps rules independently quotable and hard to half-follow. Condition first: models drop trailing conditions. |
| Status pages, support macros | Descriptive | 25 words. No "we sincerely apologize for any inconvenience this may have caused". Write "The API was down for 18 minutes. Uploads made during this time were saved and will process today." |
| Translation prep | Descriptive | The original purpose. One meaning per word plus complete grammar (keep articles, keep "that") removes most translation ambiguity. |

## Self-check

Four searches, run on the draft before delivering. Every hit outside code blocks and quoted
text is a finding.

1. **Budgets.** Count the three longest sentences under the counting convention above. Over
   20 procedural or 25 descriptive: split them.
2. **Grep the tense and modal set:** `has been`, `have been`, `is being`, `should`, and
   `-ing` clauses used as verbs (`, making`, `, allowing`, `, enabling`, `, ensuring`).
   Each becomes a simple tense or a new sentence with a real subject.
3. **Grep every `if` and `when`.** Each stands at the start of its sentence, before the
   command, with a comma. "Increase the timeout if the network is slow" becomes "If the
   network is slow, increase the timeout."
4. **Grep the terms you did not pick** from the rotation list. Replace every hit.

## Two rules deliberately not imported

The source standard carries these; they lose to rules that outrank them here, and a merged
skill cannot hold both sides.

- **The contraction ban.** STE expands every contraction. Universal rule 17 makes
  contraction rate a register-matching decision instead, and a uniformly expanded document
  in a casual register reads as style transfer. Rule 17 governs.
- **The semicolon ban.** STE writes two sentences instead. The semicolon and the colon are
  the working replacements for the em-dash in this author's voice, so the ban would fire on
  the fix rather than the defect.

## Pointers

One home per fact. This file does not restate them:

- Condition before command, one worked path, failure modes, code font, placeholders,
  and the warning pattern: the Instruction section of `axes.md`.
- Syntactic tells (frame monotony, negative parallelism, cadence, prefab phrases):
  `tells.md`. Lexical slop is this file's job; shapes are that one's.
- One term one concept, checkable numbers, literal requirements: universal rules 8 to 11
  in `SKILL.md`.
- Whether a bulk application of these rules changed what the text claims: `meaning-gate.md`.
  Register conversion is the single most productive source of those defects.
