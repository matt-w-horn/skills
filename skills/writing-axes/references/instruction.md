# Instruction

**When:** the reader is executing. Runbooks, procedures, install guides, migration steps, API how-tos, recipes.

**The reader's question:** what do I do next, and how do I know it worked?

**Signature failure:** the reader gets stuck at a choice the text left open. They cannot disagree with instructions — they can only fail — so every unresolved decision, missing precondition, and silent failure mode lands on them.

## Executability

1. Condition before command: "if X, do Y", never the reverse. A reader who executes the command before reaching the condition has already done the wrong thing.
2. One worked path, end to end. A concrete example — real values, real output — beats any volume of accurate description, because the reader can diff their situation against it.
3. Resolve every decision the reader lacks information to make. Options belong to the second reading; the first reading needs one recommended path with the reasoning stated in a clause, not a menu.
4. Name the entry point. Seven choices and "pick whichever" hands the reader a decision they cannot yet make. Name a starting one or two, say why, and note that the rest exist for later.
5. Name failure modes alongside the happy path. Happy-path-only instructions fail silently, and the reader assumes the failure is theirs.
6. Give the reader a way to verify each step succeeded. A step with no observable outcome cannot be followed with confidence, and errors compound invisibly until something distant breaks.

## Sequence and reference

7. Numbered lists for sequences, bullets for unordered items, parallel in form throughout. Broken parallelism reads as a change in meaning.
8. Name things rather than pointing: "the setup step", not "the section above". Pointers break when the document is excerpted, reordered, or read out of order — which is how instructions are actually read.
9. Special case first, generalize after. Introduce the concrete instance, get it working, then spiral back to widen it. Generality before the reader has anything running is load without payoff.
10. Never start a sentence with a symbol; the reader cannot tell where the sentence begins.
11. Code elements in code font, qualified with a noun: "the `config.yaml` file". The noun tells the reader what kind of thing they are looking at before they parse the name.
12. Visible placeholders (PROJECT_ID), each with a note on what replaces it.

## Language

13. Write for a second-language reader: short sentences, simple words, active voice with an explicit actor. The actor matters — "the installer writes the file" and "write the file" assign the work to different parties.
14. Put the action in the verb, not a nominalization. State things affirmatively; a negated instruction forces the reader to compute the complement.
15. Ban "simply", "easy", "just", and "quickly" from procedures. They convert a stuck reader's confusion into shame, and they carry no information.
16. Unambiguous dates (2026-08-04 or August 4, 2026), timezone when it matters.
17. Carry meaning in the text itself, never in color or layout alone.
18. Do not mix explanation into procedure. When the reader needs the why, mark it and set it aside — a reader mid-execution who hits a paragraph of rationale loses their place.

## Hand back to the writer

How much to assume about the reader's environment and prior knowledge is the writer's scoping call. Assuming too much strands beginners; assuming too little buries experts. Surface the choice with a recommendation and take their answer.

## Sources

Open before citing; quote only wording marked Verbatim there.

- `sources/craft-structure.md` — Halmos item 23 (symbol rules and the spiral method behind rules 9–10), Zinsser item 17 (the step-by-step ladder for technical material, rule 9's pacing).
- `sources/reader-research.md` — Diátaxis item 8 (rule 18: how-to and explanation are different modes and degrade when mixed), progressive disclosure item 29 (rule 3's defer-the-options logic).
- `scripts/style_scan.py` reports "simply/just/easy/quickly" counts for rule 15.
