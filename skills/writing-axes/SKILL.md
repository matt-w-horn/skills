---
name: writing-axes
description: Audience-and-goal-first drafting and review for human-facing prose. Use whenever the user asks to write, rewrite, draft, critique, review, or edit any document — blog posts, READMEs, papers, emails, docs, announcements, forum posts — or asks for a title, headline, or subject line, or asks to check something before posting or publishing it to a public venue, or asks why text sounds like AI, cringe, amateurish, or unconvincing, or who a piece is for, or whether a document is worth writing at all. Also use before drafting anything longer than a few paragraphs, even when the request is just "write X".
---

# Writing axes

Every document serves one reader making one decision. Route any writing or review task through four gates — reader, goal, axis, and whether to write at all — then apply the rules for the axis in play. Axis rules live in `references/`; the verified source library behind them lives in `references/sources/`. Cite sources from those files, never from memory.

## The four gates

Run them in order. Each answer constrains the next.

### Gate 1 — Who is the reader?

One person, at one moment. Resolve five things:

- What they already know — sets vocabulary and what can go unexplained.
- What they are about to do — sets what the text must equip them for.
- What they are deciding — this produces the axis (Gate 3).
- Who else will see it. Email gets forwarded, papers get excerpted into review notes, READMEs get skimmed by people the author never pictured. Design for the furthest plausible reader.
- Their relationship to the writer, and whether this text changes it.

"Developers", "the community", "readers" are categories, not readers. If the conversation does not pin a person, infer the most likely one, state the assumption in one line, and proceed. Ask only when two plausible readers would produce two different documents.

**Published venues: the title selects the reader.** When the document goes to a public venue, the reader is not given in advance; the title determines which population arrives, and that population determines which axis the responses run on. A title that advertises the output recruits readers who judge outputs; one that advertises the mechanism recruits readers who judge mechanisms. Draft the title last, from the finished body, and test it with two questions: who does this recruit, and what will they argue about? If the recruited argument is not the one the writer wants, the title is wrong even when it is accurate. The same holds for subject lines, repository descriptions, and any other text that decides whether the body gets opened. Title drafting and the pre-publication check in `references/reception.md` run at the same moment and constrain each other.

### Gate 2 — What is the goal?

State the goal as a change in the reader, never as a property of the text. "Explain the gate system" is a property. "Get one maintainer to fork the template and report which gate fires first" is a goal. The test: if the goal is met, what does the reader do or believe that they otherwise would not? No answer means no drafting yet.

### Gate 3 — Which axis?

| Axis | The reader is deciding | Signature failure | Open |
|---|---|---|---|
| Argument | whether to believe or act on a claim | nothing in it could be wrong | references/argument.md |
| Instruction | nothing — they are executing | stuck at a choice the text left open | references/instruction.md |
| Orientation | whether this thing is for them | they cannot picture using it | references/orientation.md |
| Standing | something about the writer | the writer reads as excusing themself | references/standing.md |

Open the reference file for the governing axis before drafting or judging. On mixed documents, open every axis present.

Diagnose as well as accept. When handed a draft, infer its actual axis from what the text is doing and compare with what it was meant to be. "This was asked for as Orientation but it is doing Argument work" is often the single highest-value finding, and it is invisible if the axis is only ever taken as declared.

### Gate 4 — Mix, split, or don't write

**Mix** when one axis is primary and the others appear as marked sections following their own rules locally. Conflicts resolve to the primary (table below).

**Split** into separate documents when two axes need different readers or different orderings. Signals: no first sentence serves both; the ordering that suits one buries the other; the draft explains why a thing is built before saying what it is.

**Don't write** — a legitimate outcome; say it plainly — when:

- Something that already exists meets the goal. Write a pointer instead.
- The decision the text depends on has not been made. Text hardens ambiguity; it cannot resolve it.
- The axis is Argument and no claim exists yet that a knowledgeable reader could reject.
- The axis is Standing and the content needs tone, follow-up questions, or deniability. That is a conversation, not a document.
- The axis is Standing and the content carries legal or professional exposure the writer has not decided about. Flag the exposure once, name its class, and stop.

**Axis conflicts** — the primary axis wins; these are the recurring collisions:

- Instruction keeps its exhaustive failure modes; the argument around an instruction section does not inherit them.
- Orientation's answer-first beats Argument's context-first for any reader who has not committed yet. The first screen belongs to Orientation.
- Standing's pattern-before-chronology always overrides the writer's memory order.
- Argument wants a claim that could be wrong; Standing wants claims that survive forwarding. Standing wins — a Standing document is the wrong place to be interestingly wrong.
- Instruction's one recommended path and Orientation's honest scope boundaries both fit, in sequence: recommend the path, then bound it. Never interleave.

## Universal rules

These apply on every axis, on top of the axis file.

### Reader modeling

1. Hold the one reader from Gate 1 through every sentence. Every fork left open — two audiences, two venues, the recipient versus whoever they forward to — costs more than any sentence-level defect.
2. Given-new: open each sentence with what the reader already holds; end it with the new thing to emphasize. The end of a sentence carries stress whether or not it was planned.
3. Every sentence performs an act — assert, concede, request, orient, hedge. A sentence performing no act gets cut. Two sentences performing the same act: one gets cut.
4. The curse of knowledge is not introspectable. When stakes justify it, the fix is a real reader who does not know the material, watched for where they stop.

### Placement

5. Placement is a claim about importance. The strongest, most-the-writer's-own material sitting at 80% of a document says it does not matter, and readers hear that claim. In venues where readers reply, the opening does more: it sets the subject of the replies, not only the emphasis. An opening about motivation gets a thread about motivation; an opening about mechanism gets a thread about mechanism. Open on what the writer wants discussed.
6. Distribute payoffs; do not save them. Readers abandon dry stretches before reaching a hoarded reward.
7. The ends of units — sentences, paragraphs, sections, documents — carry the emphasis. Put the strongest material there.

### Precision

8. One term, one concept, for the whole document set. Prose vocabulary, coined terms, symbols, and the names a thing goes by. A second word for the same concept sends readers hunting for a second meaning.
9. Every checkable number gets a source or gets cut. A number a reader can verify is an invitation; failing that check costs more than omitting the number.
10. Never present reconstructed wording as a quote. Paraphrase is labeled as paraphrase — including paraphrases of the writer's own earlier drafts.
11. State requirements, deadlines, and consequences literally, with the number and the name attached.

### Self-monitoring — the through-line failure class

12. Cut cognition-narration: "I've been thinking", "I keep wondering", "I should say". The document is the evidence that thinking happened.
13. Cut pre-emptive concession and disclaimed qualifications. Ethos is built by demonstrated judgment inside the text, not imported from credentials or subtracted by disclaimers.
14. Hedges are a budget, not a courtesy. Attach the qualifier and the rebuttal condition to the specific claim that needs them, then stop hedging the surrounding prose. Ambient uncertainty makes the reader evaluate the writer's confidence instead of the claim.
15. Reassurance said twice is anxiety about the thing being reassured, and readers hear the anxiety before the content. Once is information.

### Sound

16. Vary construction, not just length. When one syntactic frame carries most of the emphatic moments, the prose reads as machine-made regardless of word choice. Frames to count: "X rather than Y", "X, not Y", balanced antithesis couplets, short aphorisms as paragraph-enders, three- and four-item lists without conjunctions, em-dash interruptions. This is a late-revision check, because revision is what introduces the tic; the hunting procedure is `references/tells.md`.
17. Register consistency. A casual opening plus uniformly formal negation reads as style transfer. Contraction rate should match the register and stay stable within it.
18. Answer rhetorical questions or cut them. A stack of questions performs seriousness without paying for it.
19. Do not announce enumeration where the list itself would do the work.
20. Hunt prefabricated phrases — the ready-made sequence that assembles itself without thought: stock catastrophe lists, stock stakes paragraphs, stock transitions.

### Ownership — hard rules

21. The voice belongs to the author. Operating on someone's draft is translation, not rewriting.
22. Changes to what a text claims are kicked back to the writer, never made silently.
23. On the Standing axis, three calls are always the writer's: what to disclose, what characterization to accept about anyone not in the room, and what tone to take toward them. Surface the call with a recommendation, then execute what they choose.

## Workflow

**Drafting:** run the gates, open the axis file, draft, then run the review path below on the draft before delivering it.

**Reviewing** (a user's draft or a fresh one):

1. Run `scripts/style_scan.py` on the prose. It handles markdown, HTML, and LaTeX, and computes only standard, format-robust measures: readability grades (Flesch, FK, Coleman-Liau), sentence-length variance, contraction rate, and repeated word, bigram, and trigram tables. Its one flag is flat sentence rhythm. Then open `references/tells.md` and run the reading procedure on the scanner's output — the tells that matter most (negative parallelism, frame repetition, aphorism cadence, register breaks) are syntactic shapes with open lexical slots, and no pattern matcher catches them.
2. One holistic pass with the whole document in context: the axis check, claim-exists, a placement map of where the best material sits, the hedge budget, question order, the forward test. These findings cannot be produced any other way and outrank everything the scan returns — several are precisely the findings that vanish if the document is read in slices.
3. Optional, for high-stakes documents: fan out reader lenses as parallel subagents — the named reader from Gate 1, a naive reader, a hostile expert. Each receives the whole document and returns three things: where they stopped, what they would reject, what they needed that was not there. Consolidate in a single pass; several findings are often one pattern.
4. Report by severity, whole-document findings before span findings. End with what to keep. A review that lists only defects miscalibrates the writer; the strongest lines are load-bearing information about the writer's range.

**Publishing** (before anything goes to a public venue where readers respond):

Run `references/reception.md`. The review pass stress-tests the claims; the reception check forecasts the responses that are not about the claims — the topic's inherited debates, externalities, contested vocabulary, genre, the writer, and open basic questions — and in open venues that is most of the thread. Its output is a list of predicted readings, each tagged fold, prepare, or accept, with any folds executed under the hedge budget. It runs together with title drafting (Gate 1).

## Sources

The rules above compress a verified source library. Item numbers refer to the verification report of 2026-08-04; numbering is therefore non-sequential within a file. Entries marked "verified in conversation" were confirmed by direct search the same day and sit outside the numbered report.

| Open | For |
|---|---|
| references/sources/craft-sentence.md | sentence mechanics: given-new, rhythm exercises, sentence-length variance, knowing what a sentence says, Orwell's checklist (items 1, 2, 3, 18, 31) |
| references/sources/craft-structure.md | leads, structure from material, one ping, C-C-C, gold coins, the spiral method, notation discipline, OCAR, SCQA (items 7, 13, 14, 17, 23, 25, 32, 33) |
| references/sources/rhetoric.md | stance, ethos, argument anatomy, perspective by incongruity, value-to-readers, credibility devices, hedging research, stasis, speech acts (items 4, 5, 6, 15, 16, 24, 28, 30, 36) |
| references/sources/reader-research.md | curse of knowledge, scanning patterns, trunk test, content-as-conversation, documentation modes, progressive disclosure (items 8, 9, 10, 11, 12, 29) |
| references/sources/standing-social.md | excuses vs. justifications, stealing thunder, inoculation, covering, BLUF, attention-outward acting technique (items 19, 20, 21, 22, 26, 27, 35) |
| references/sources/flags-and-policy.md | the report's scope note and corrections summary, plus the current ACM AI-disclosure policy (item 34) |

Citation discipline:

- Before naming any source in output, open `references/sources/flags-and-policy.md`. Several common attributions are wrong, apocryphal, or superseded, and its corrections list is the fastest check.
- Quote only wording a sources file marks **Verbatim**. Everything else is presented as a summary and labeled as one.
- When a rule leans on a specific source, the axis file's Sources section says which file and item to open. Follow the pointer before asserting what the source says.
