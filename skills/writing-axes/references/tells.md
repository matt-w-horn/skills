# Hunting the tells: a reading procedure

The tells that make prose read as machine-made are mostly syntactic shapes with open lexical slots. "The proof is technically correct. The statement is technically correct. But the docstring lies." shares no reusable surface string with "safety at a high load certifies every lower one" — the shape lives in the matched frame and the polarity flip, and no regex or contiguous n-gram catches a shape. So the scanner computes only format-robust measures and frequency tables, and this procedure does the finding. Perplexity — word-level predictability — needs a language model and is out of the scanner's scope entirely; the frame census below is the manual stand-in.

Run the steps in order on the whole document. Each takes minutes, not passes of machinery.

## Step 0 — read the scanner output

Run `scripts/style_scan.py` first, then take four things from it:

- **The one flag.** Flat sentence rhythm (low length CV) is the only tell that is a well-defined statistic, so it is the only thing the scanner flags. Everything below is judgment.
- **The n-gram tables, read selectively.** Skip pure-syntax noise ("of the", "in the", "and the"). Circle anything carrying contrast or negation ("rather than", ", not the", "instead of", "not merely") — those are frame instances, and a count of 5+ in a short document usually means one construction is carrying the emphatic moments. Circle any repeated trigram that is an authorial phrase rather than a topic phrase ("verdict goes stale" is topic; ", and only" is authorial). High counts on clause connectives (", and", ", so", ", because") are sentence-shape monotony data: many sentences built as *clause, connective, clause*.
- **The repeated-words line.** Frame anchors (rather, than, not, no, never, only, instead, merely) are deliberately kept out of the stoplist because discontinuous frames — "would rather X than Y", "no A, no B, just C" — never form a repeated n-gram. Their only trace is the anchor words running hot. An anchor at 3+ in a short document is a search target: find each instance and classify it in Step 1.
- **Contraction rate and grade level** feed Step 4 (register). If FKGL and Coleman-Liau disagree by several grades, distrust the extraction before the prose.

## Step 1 — frame census of the emphatic moments

Mark every emphatic moment: paragraph enders, thesis sentences, the lines that carry the point. For each, name the construction doing the work:

- substitution contrast: "X rather than Y", "X instead of Y", "X, not Y"
- balanced antithesis couplet: two adjacent clauses, matched syntax, flipped polarity
- aphorism ender: a short symmetrical declarative closing a paragraph
- asyndetic list: three or four items, no conjunction
- em-dash interruption
- plain assertion (no frame)

One construction carrying most of the emphasis is the tic, whatever the construction is. The measured line: more than about one contrast frame per 300 words of prose reads as templated. The fix is never global search-and-replace; recast instance by instance into different grammatical moves — an assertion pair, a negation followed by the mechanism it protects, an agent-first sentence, a concession. Drill source for range: Le Guin's syntax exercises (`sources/craft-sentence.md`, item 18).

## Step 2 — negative parallelism specifically

The slipperiest shape, and the one that survives every mechanical net. Recognizers, applied by reading:

- two adjacent sentences or clauses with matching syntax and opposite polarity
- "not / never / no" inside the second leg of a matched pair
- a definitional sentence whose second half only excludes: "X is A, not B"

Then the test that decides keep or cut: does the negative leg tell the reader something they did not have, or does it restate the positive leg by exclusion? "The kernel isn't wrong, but it doesn't check intent" carries information in both legs — keep. "It is a certificate, not a posture" restates one claim twice — recast or cut. A document where every emphatic pair passes through this shape needs Step 1's per-instance recasting even when each individual pair survives the test.

## Step 3 — cadence pass

Read the paragraph endings and openings in sequence, aloud or subvocalized:

- aphorism-ender density: how many paragraphs close on a short symmetrical punch line; a few land, a rhythm of them reads as performance
- question stacks: two or more consecutive rhetorical questions performing seriousness without paying for it — answer or cut
- announced enumeration: "There are three things…" where the list would do the work (fine in Instruction, a tell elsewhere)
- symmetric bookends: the same deference or reassurance at open and close; said twice it reads as anxiety about the thing being reassured

## Step 4 — narration and register

- **Cognition-narration.** Search the phrase family — "I've been thinking", "I keep wondering", "I should say", "I have since noticed", "all of this has me thinking" — but treat the list as open. The real test for any first-person sentence: does it narrate the act of thinking or writing rather than the subject? The document is the evidence that thinking happened.
- **Register.** Read the opening two sentences and name the register they promise, then check the body against it. The scanner's contraction rate is the fastest instrument: a greeting-and-exclamation opening followed by zero contractions and a run of "do not / is not / I would" is style transfer, and readers hear it before they can name it.

## Step 5 — prefab sweep

Orwell's test, sentence by sentence over the suspect stretches: could this phrase have assembled itself without a decision? Stock catastrophe lists, stock stakes paragraphs, stock transitions ("in today's rapidly evolving…"), and any image the writer has seen in print more than twice. The full checklist and its exact wording: `sources/craft-sentence.md`, Orwell entry — check `sources/flags-and-policy.md` before quoting it, since the checklist is commonly garbled.

## Sources

`sources/craft-sentence.md` — Le Guin item 18 (syntax range drills), Gopen & Swan item 1 (stress position: why frame monotony lands on the emphatic moments), Orwell (prefab phrases; verified wording). `sources/rhetoric.md` — item 30: the "what does each sentence do" heuristic is craft folklore, not speech-act theory; do not dress it in Austin/Searle citations. Open `sources/flags-and-policy.md` before citing any of these by name.
