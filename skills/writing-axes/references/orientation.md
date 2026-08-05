# Orientation

**When:** the reader is deciding whether this thing is for them. READMEs, landing pages, project overviews, announcements, docs home pages, abstracts read in isolation.

**The reader's question:** what is this, and is it for me?

**Signature failure:** the reader cannot picture using it. They are not resisting a claim — they do not yet know what claim is on offer. Sharpening the argument does not fix this; answering their questions in order does.

## First contact

1. Trunk test: dropped onto this page cold, can the reader answer what this is and what they can do here, without effort? If not, nothing else in the document gets read.
2. One sentence, first, that tells them whether to keep reading. The best one-line description is often hiding in the Related Work or the closing section.
3. Answer first, then support. The reader may stop after paragraph one, and most do.
4. Lead with the concrete failure the thing prevents, not with the design rationale. Rationale answers a question the reader has not reached yet — a good argument in the wrong seat is still a failure of order.
5. Differentiation in the first ten seconds. A reader who already knows the alternatives needs to know how this differs before anything else; positioning parked in a final "related work" section arrives after they have stopped caring.

## Ordering

6. Match the document's order to the reader's question order: what is this → will it work for me → how do I try it → why is it built this way → how do I contribute. Write the question list first, then check the ordering against it. Documents default to the order of the author's discovery, which is nearly the reverse.
7. Front-load. Readers scan in an F-shape: the first two paragraphs and the left edge of each line carry disproportionate weight, so the load-bearing words go there.
8. Progressive disclosure: surface the minimum needed to decide, and defer the rest behind a marked path. Everything visible competes with everything else visible.
9. Trust-building material belongs where trust is still being decided, not in the last section anyone reads. "Extracted from the toolchain rather than recalled" is credibility; scattered across Installing, Sources, and Contributing it is invisible.

## Content

10. Cut happy talk — introductory, content-free text that welcomes the reader and says the thing is great. Readers hear "blah blah blah" and their trust drops with every line of it.
11. Vocabulary wall: the first scannable element must not read as an insider club. A dozen coined terms in the first table is where evaluators bounce, and the author cannot see it, because the curse of knowledge removes access to not-knowing.
12. Do not mix the four documentation modes — tutorial, how-to, reference, explanation — without marking them. Reference inside a tutorial and steps inside an explanation degrade both.
13. Say what it does not do. Scope boundaries are orienting information, not defensive hedging; the reader deciding fit needs the edges as much as the center.
14. The only reliable instrument for this axis is a real person who does not know the domain, watched for where they stop. Introspection cannot simulate them.

## Hand back to the writer

How much to sell versus describe is a stance about the project, not a writing decision. Surface it with a recommendation and take the writer's answer.

## Sources

Open before citing; quote only wording marked Verbatim there.

- `sources/reader-research.md` — Krug item 10 (trunk test, happy talk: rules 1, 10), Nielsen item 12 (scanning, F-pattern, inverted pyramid: rules 3, 7), Redish item 9 (content as conversation, question order: rule 6), Pinker item 11 (curse of knowledge and the real-reader remedy: rules 11, 14), Diátaxis item 8 (the four modes: rule 12), progressive disclosure item 29 (rule 8 — note the corrected attribution to Carroll at IBM).
- `sources/craft-structure.md` — Minto item 33 (answer-first pyramid: rule 3), Swales item 13 (discourse community: who the insiders actually are, rule 11's calibration).
