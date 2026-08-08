# The four axes

One file, because most documents run on more than one axis and the collisions are only
visible when all four are in view. Open this whenever drafting or reviewing. The governing
axis sets the rules; the others tell you what the document is doing where it drifts.

Diagnose as well as accept. Infer a draft's actual axis from what the text is doing and
compare it against what it was meant to be. "This was asked for as Orientation but it is
doing Argument work" is often the single highest-value finding, and it is invisible if the
axis is only ever taken as declared.

| Axis | The reader is deciding | Signature failure |
|---|---|---|
| Argument | whether to believe or act on a claim | nothing in it could be wrong |
| Instruction | nothing, they are executing | stuck at a choice the text left open |
| Orientation | whether this thing is for them | they cannot picture using it |
| Standing | something about the writer | the writer reads as excusing themself |

The verified source library sits in `sources/`. Cite from those files, never from memory,
and open `sources/flags-and-policy.md` before naming any source: several common
attributions are wrong, apocryphal, or superseded. Quote only wording marked **Verbatim**.

---

# Argument

**When:** the reader is deciding whether to believe or act on a claim. Papers, essays,
technical blog posts, proposals, position documents, design justifications.

**The reader's question:** why should I believe this, and what would it cost me to be wrong?

**Signature failure:** nothing in it could be wrong. Every strong statement hedged, every
question left open, every claim either common knowledge or explicitly disowned. Readers
register this as amateur before they can articulate why: a document that cannot be wrong
has not said anything.

## Does an argument exist

1. Find at least one claim a knowledgeable reader could reject. If none exists, stop: there is nothing to write yet, and the honest output is to say so.
2. One ping: one reusable insight, useful to the reader. Three ideas means three documents.
3. One central contribution, communicated in the title. If the title cannot carry it, the contribution has not been identified yet.
4. Pick the stasis and hold it: fact (did it happen), definition (what is it), quality (how serious is it), or procedure (what should be done). Arguments that wander across all four wander. Demote the other three to setup for the one that governs.
5. Name the instability the reader's community already recognizes as a problem, and the cost of leaving it unresolved. Interesting-to-the-writer is not yet valuable-to-them; expert readers want their beliefs changed, not the writer's process.

## Authority

6. Spend the writer's own expertise before borrowed authority. Stakes available to anyone ("this could take down the grid") signal that the writer understands seriousness; specifics only the writer has demonstrate that they know something. The reader's implicit question is why this person is telling them this.
7. Ethos is constructed by the speech itself: demonstrated practical judgment, good character, goodwill toward the audience. It is not imported by credentials and not subtracted by disclaimers. One paragraph demonstrating judgment on the writer's home ground establishes more standing than any disclaimer removes.
8. Check the stance balance: subject, audience, speaker. When the speaker becomes the most present element, through visible uncertainty as much as through vanity, the subject recedes. Rebalance toward the argument and the audience, and the speaker's proportion falls on its own.
9. Write toward the smartest objector. Ask who would disagree and what to say to them. Prose aimed at an imagined intelligent opponent acquires tension automatically and cannot produce a frictionless arc. It also fixes hedging as a side effect: knowing where the real objections are means hedging there and nowhere else. Scope: the smartest objector attacks the claim. Forecasting responses that are not about the claim (the topic's standing debates, costs, vocabulary, genre) is a different job, done by `reception.md` before publication; neither substitutes for the other.

## Analogy and borrowed frames

10. Use an analogy; do not discuss it. An analogy earns its place by producing a question the reader could not reach without it. Everything spent situating or defending it is overhead.
11. Where the mapping breaks is the engine, not the caveat. The productive value of importing another field's vocabulary comes from the misfit: build the argument on the break rather than apologizing for it.
12. At most one sentence of disclaimer, and only where the break changes the answer.

## Structure

13. The lead contains a fact the reader wants, not an announcement that a document is beginning. It is a flashlight shining down into the piece, and it must illuminate what is actually there.
14. Structure is derived from the material, never imposed as a default shape. The frictionless arc (hook, analogy, stakes, questions, soft close) is the imposed shape, and readers now recognize it.
15. Context, content, conclusion, at document, section, and paragraph scale. The abstract or lede tells the complete story; the introduction narrows to the gap; the body is a sequence of statements that connect logically; the close returns to the gap and shows it filled.
16. Avoid zig-zag: only the central idea recurs. Everything else appears in exactly one place.
17. Parallel messages get parallel form, so the syntax becomes transparent and the reader attends to content.
18. Concrete before abstract, and invert the usual distribution: compress the generic material and put it early; expand the specific, surprising, only-the-writer's material and make it load-bearing. Distribute the war stories through the piece rather than parking them in the last third.

## Venue modifiers, when the argument is gatekept

19. State the evaluation contract in the introduction: what kind of paper this is and what class of evidence it offers, before a reviewer supplies their own and rejects against it.
20. Priority and novelty claims: state once, precisely, next to the search methodology that supports them. Repetition multiplies the targets and reads as anxiety about the one thing the writer most wants believed.
21. Notation gets a table, and one symbol keeps one meaning for the whole document. Symbol collisions in a precision argument are the failure the argument opposes, performed in its own notation.
22. Disclosure requirements are venue-specific and change. Check the current policy (`sources/flags-and-policy.md`, item 34) rather than the remembered one, and never spend the abstract's closing sentence on a disclosure. That position belongs to the strongest claim.

## Hand back to the writer

How much risk to take on the central claim is the writer's call, not the skill's.
Unfalsifiable is safe and worthless; strong is useful and can be wrong in public. Surface
the tradeoff with a recommendation, then execute what they choose.

**Sources.** `sources/rhetoric.md`: Booth (stance, rules 8, 13 of the universal set),
Aristotle item 36 (ethos, rule 7), Toulmin item 4 (qualifier and rebuttal, rule on hedges),
Burke item 5 (perspective by incongruity, rules 10 and 11), McEnerney item 6 (instability
and value, rule 5), Heath item 15 (Sinatra Test and testable credentials, rules 6 and 18),
Brooks item 16 (novelty has no merit in design), Hyland item 24 (hedging, note the flagged
limitation before citing), stasis item 28 (rule 4), Feynman (report what could make you
wrong). `sources/craft-structure.md`: McPhee item 7 (rules 13 and 14), Swales item 13
(CARS, rule 5's move structure), Clark item 14 (gold coins and emphatic order, rule 18),
Zinsser item 17 (the lead, rule 13), Halmos item 23 (notation, rule 21), Schimel item 25
(OCAR, rule 15), the "So what?" note item 32, Peyton Jones (one ping, rule 2), Mensh and
Kording (rules 1, 3, 15, 16). `sources/flags-and-policy.md`: ACM policy item 34 (rule 22)
and the corrections summary.

---

# Instruction

**When:** the reader is executing. Runbooks, procedures, install guides, migration steps,
API how-tos, recipes.

**The reader's question:** what do I do next, and how do I know it worked?

**Signature failure:** the reader gets stuck at a choice the text left open. They cannot
disagree with instructions, they can only fail, so every unresolved decision, missing
precondition, and silent failure mode lands on them.

## Executability

1. Condition before command: "if X, do Y", never the reverse. A reader who executes the command before reaching the condition has already done the wrong thing.
2. One worked path, end to end. A concrete example with real values and real output beats any volume of accurate description, because the reader can diff their situation against it.
3. Resolve every decision the reader lacks information to make. Options belong to the second reading; the first reading needs one recommended path with the reasoning stated in a clause, not a menu.
4. Name the entry point. Seven choices and "pick whichever" hands the reader a decision they cannot yet make. Name a starting one or two, say why, and note that the rest exist for later.
5. Name failure modes alongside the happy path. Happy-path-only instructions fail silently, and the reader assumes the failure is theirs.
6. Give the reader a way to verify each step succeeded. A step with no observable outcome cannot be followed with confidence, and errors compound invisibly until something distant breaks.

## Sequence and reference

7. Numbered lists for sequences, bullets for unordered items, parallel in form throughout. Broken parallelism reads as a change in meaning.
8. Name things rather than pointing: "the setup step", not "the section above". Pointers break when the document is excerpted, reordered, or read out of order, which is how instructions are actually read.
9. Special case first, generalize after. Introduce the concrete instance, get it working, then spiral back to widen it. Generality before the reader has anything running is load without payoff.
10. Never start a sentence with a symbol; the reader cannot tell where the sentence begins.
11. Code elements in code font, qualified with a noun: "the `config.yaml` file". The noun tells the reader what kind of thing they are looking at before they parse the name.
12. Visible placeholders (PROJECT_ID), each with a note on what replaces it.

## Language

13. Write for a second-language reader: short sentences, simple words, active voice with an explicit actor. The actor matters, since "the installer writes the file" and "write the file" assign the work to different parties.
14. Put the action in the verb, not a nominalization. State things affirmatively; a negated instruction forces the reader to compute the complement.
15. Ban "simply", "easy", "just", and "quickly" from procedures. They convert a stuck reader's confusion into shame, and they carry no information.
16. Unambiguous dates (2026-08-04 or August 4, 2026), timezone when it matters.
17. Carry meaning in the text itself, never in color or layout alone.
18. Do not mix explanation into procedure. When the reader needs the why, mark it and set it aside: a reader mid-execution who hits a paragraph of rationale loses their place.
19. Warnings and cautions lead with the command or the condition, then give the risk. Never bury the instruction behind its explanation, because a reader who has already acted cannot un-act. Label the level so injury and damage are distinguishable at a glance: "CAUTION: Do not use the `--force` flag against production. The flag deletes rows that do not match the source."

## Register

`plain-language.md` sets the numbers this axis assumes: 20 words per procedural sentence,
25 for descriptive text and for notes, plus the counting convention that keeps identifiers
and backticked commands from consuming the budget. It also carries the modal ladder (rule
15's ban on "simply" and "just" is one row of a longer table), the term rotations, and the
slop substitutions. Open it with this file whenever the text is technical.

## Hand back to the writer

How much to assume about the reader's environment and prior knowledge is the writer's
scoping call. Assuming too much strands beginners; assuming too little buries experts.
Surface the choice with a recommendation and take their answer.

**Sources.** `sources/craft-structure.md`: Halmos item 23 (symbol rules and the spiral
method behind rules 9 and 10), Zinsser item 17 (the step-by-step ladder for technical
material, rule 9's pacing). `sources/reader-research.md`: Diátaxis item 8 (rule 18: how-to
and explanation are different modes and degrade when mixed), progressive disclosure item 29
(rule 3's defer-the-options logic). `scripts/style_scan.py` reports "simply/just/easy/
quickly" counts for rule 15.

---

# Orientation

**When:** the reader is deciding whether this thing is for them. READMEs, landing pages,
project overviews, announcements, docs home pages, abstracts read in isolation.

**The reader's question:** what is this, and is it for me?

**Signature failure:** the reader cannot picture using it. They are not resisting a claim,
they do not yet know what claim is on offer. Sharpening the argument does not fix this;
answering their questions in order does.

## First contact

1. Trunk test: dropped onto this page cold, can the reader answer what this is and what they can do here, without effort? If not, nothing else in the document gets read.
2. One sentence, first, that tells them whether to keep reading. The best one-line description is often hiding in the Related Work or the closing section.
3. Answer first, then support. The reader may stop after paragraph one, and most do.
4. Lead with the concrete failure the thing prevents, not with the design rationale. Rationale answers a question the reader has not reached yet, and a good argument in the wrong seat is still a failure of order.
5. Differentiation in the first ten seconds. A reader who already knows the alternatives needs to know how this differs before anything else; positioning parked in a final "related work" section arrives after they have stopped caring.

## Ordering

6. Match the document's order to the reader's question order: what is this, will it work for me, how do I try it, why is it built this way, how do I contribute. Write the question list first, then check the ordering against it. Documents default to the order of the author's discovery, which is nearly the reverse.
7. Front-load. Readers scan in an F-shape: the first two paragraphs and the left edge of each line carry disproportionate weight, so the load-bearing words go there.
8. Progressive disclosure: surface the minimum needed to decide, and defer the rest behind a marked path. Everything visible competes with everything else visible.
9. Trust-building material belongs where trust is still being decided, not in the last section anyone reads. "Extracted from the toolchain rather than recalled" is credibility; scattered across Installing, Sources, and Contributing it is invisible.

## Content

10. Cut happy talk, meaning introductory content-free text that welcomes the reader and says the thing is great. Readers hear "blah blah blah" and their trust drops with every line of it.
11. Vocabulary wall: the first scannable element must not read as an insider club. A dozen coined terms in the first table is where evaluators bounce, and the author cannot see it, because the curse of knowledge removes access to not-knowing.
12. Do not mix the four documentation modes (tutorial, how-to, reference, explanation) without marking them. Reference inside a tutorial and steps inside an explanation degrade both.
13. Say what it does not do. Scope boundaries are orienting information, not defensive hedging; the reader deciding fit needs the edges as much as the center.
14. The only reliable instrument for this axis is a real person who does not know the domain, watched for where they stop. Introspection cannot simulate them.

## Hand back to the writer

How much to sell versus describe is a stance about the project, not a writing decision.
Surface it with a recommendation and take the writer's answer.

**Sources.** `sources/reader-research.md`: Krug item 10 (trunk test, happy talk: rules 1
and 10), Nielsen item 12 (scanning, F-pattern, inverted pyramid: rules 3 and 7), Redish
item 9 (content as conversation, question order: rule 6), Pinker item 11 (curse of
knowledge and the real-reader remedy: rules 11 and 14), Diátaxis item 8 (the four modes:
rule 12), progressive disclosure item 29 (rule 8, note the corrected attribution to Carroll
at IBM). `sources/craft-structure.md`: Minto item 33 (answer-first pyramid: rule 3), Swales
item 13 (discourse community, who the insiders actually are, rule 11's calibration).

---

# Standing

**When:** the text acts on a relationship, and the reader is judging the writer. Explaining
a job history, addressing a mistake, community introductions, apologies, negotiations,
difficult emails.

**The reader's question:** what kind of person is this, and can I trust them?

**Signature failure:** the writer reads as excusing themself. Length, hedging, and repeated
reassurance all feed the same reading, because on this axis the manner of the telling is
evidence.

## Framing

1. Excuse or justification, the highest-leverage call on this axis. An excuse admits the outcome was bad and denies responsibility; a justification accepts responsibility and denies the outcome was bad. Justifications are almost always available and always stronger, because they do not ask the reader to absolve anyone. "I left because the role relocated and I chose not to move" is a decision; "the instability made it hard to commit" is a circumstance that happened to someone.
2. Pattern leads; chronology follows. Chronology is the order of the writer's memory, not of the reader's question. Establish the through-line first, so each item reads as a variation on a pattern instead of raw material the reader assembles, uncharitably, themselves.
3. Situation, complication, question, answer: name the context the reader would agree with, the thing that changed, the question that raises, then the answer. Then support it.
4. Bottom line up front. The reader may stop after the first paragraph, and the forwarded version often is only the first paragraph.
5. End on a fact, not a self-characterization. Handing the reader evidence lets them conclude; asking them to accept the writer's assessment of the writer's own conduct makes them resist it.
6. No unverifiable self-assessment in a strong position. "Known for delivering impact" occupies the highest-value slot with the weakest kind of claim.

## Disclosure

7. Disclose before the other side raises it. Revealing negative information yourself measurably reduces its impact, and pre-exposure to the weakened form builds resistance to the strong form arriving later.
8. Bound the disclosure. The credibility advantage depends on brevity; sprawl inverts it and starts confirming the concern. The story that needs its full length belongs in a call, where tone and follow-up exist.
9. Say it once. The same reassurance offered twice is covering, and covering is legible as covering: the reader hears the anxiety about the inference before they hear the content meant to prevent it.
10. Forward test: every paragraph must survive being read alone, by a stranger, with none of its neighbors. The reader being written to is rarely the reader who decides.

## Posture

11. Attention outward. Track what the reader needs to know and decide, not how the writer is being received. Self-consciousness is not cured by willpower; it is crowded out by having somewhere else to put attention, the same mechanism that fixes self-conscious acting.
12. Never invite the reader into a shared judgment of a third party. It presumes agreement, it is unrecoverable if forwarded, and it gains nothing the facts do not already provide.

## Hand back to the writer, always

13. What to disclose is the writer's call.
14. What characterization to accept about anyone not in the room is the writer's call.
15. Tone toward an absent party is the writer's call.
16. Where a disclosure carries legal or professional exposure (severance terms, non-disparagement, active claims) flag it once, plainly, name the class of exposure, and stop. Do not advise around it, do not repeat the flag, and do not soften the underlying content to dodge it.

Surface each with a recommendation, then execute what the writer chooses.

**Sources.** `sources/standing-social.md`: Scott and Lyman item 19 (excuse versus
justification: rule 1), stealing thunder item 20 (rule 7, note the corrected journal),
McGuire item 21 (inoculation: rule 7's second half), Goffman item 22 (covering versus
passing: rule 9), BLUF item 26 (rule 4, note the corrected doctrinal home), Meisner item 35
(attention outward: rule 11), the Olivier anecdote item 27 (apocryphal as usually told, do
not cite the quip as documented). `sources/craft-structure.md`: Minto item 33 (SCQA:
rule 3).

---

# Axis conflicts

The primary axis wins. These are the recurring collisions:

- Instruction keeps its exhaustive failure modes; the argument around an instruction section does not inherit them.
- Orientation's answer-first beats Argument's context-first for any reader who has not committed yet. The first screen belongs to Orientation.
- Standing's pattern-before-chronology always overrides the writer's memory order.
- Argument wants a claim that could be wrong; Standing wants claims that survive forwarding. Standing wins, because a Standing document is the wrong place to be interestingly wrong.
- Instruction's one recommended path and Orientation's honest scope boundaries both fit, in sequence: recommend the path, then bound it. Never interleave.
