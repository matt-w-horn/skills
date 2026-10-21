# Academic-journal register and copy-editing

**When:** on the Argument axis for formal academic papers and LaTeX or Markdown manuscripts, when asked to copy-edit or "journal-ready" a paper, apply or check a house style, fold in a copy-editor's pass, or normalize dialect (US/UK spelling, dashes, hyphenation). It is the academic-register counterpart to `references/plain-language.md`.

Convert compressed, author-voiced academic prose into standard formal journal English, or detect where a manuscript deviates from that register, without ever changing what a sentence claims. **Edits that cannot be certified meaning-preserving become flags, not edits.**

## The four-layer model

Style rules come in layers with different detection physics. Keeping them separate is what makes the work auditable:

1. **Syntax** (judgment lens, dialect-neutral):
   - No reduced relative clauses ("the bound *the algorithm computes*" becomes "the bound *that* the algorithm computes").
   - Participles become finite clauses ("a cache holding stale entries, causing misses" becomes "a cache that holds stale entries and therefore causes misses").
   - One claim per sentence ("The cache fills, eviction begins, and latency rises, which the client misreads as failure." is split into two or three sentences).
   - Explicit connectives ("The queue drains. The alarm clears." becomes "The queue drains. Consequently, the alarm clears.").
   - No sentence-initial "And/But/So" ("And the second case is worse." becomes "In addition, the second case is worse."; Vale: `Core.SentenceStart`).
   - No elliptical colon intros ("Three causes:" becomes "The three causes are as follows:").
   - Direct questions marked as questions ("the question of who pays the cost." becomes "the question, 'who pays the cost?'").
   - Inanimate subjects lose cognitive verbs ("The table knows the answer." becomes "The table contains the answer."). Conventional metonymy stays ("this paper presents", "Section 2 describes"); judge, do not pattern-match.
   - Contrastive "while" becomes "whereas" ("while the second fails" becomes "whereas the second fails"; keep "while" temporal).

2. **Lexicon** (Vale + judgment lens, dialect-neutral):
   - Hedges (Vale: `Core.Hedges`): "as far as we know" to "to our knowledge"; "at this writing" to "at the time of writing"; "we know of no" to "we are unaware of any".
   - Informal idioms (Vale: `Core.InformalIdioms`, plus lens): "goes back to" to "traces to"; "rides on" to "is based on"; "blows up" to "diverges"; "deletes/destroys (an equilibrium)" to "eliminates/removes"; "buys" to "provides"; "prices" to "accounts for"; "the cartoon" to "the stylized approximation"; "cheap" to "low-cost/low-latency".
   - Deliberate aphorisms survive: a standalone slogan sentence an author clearly built ("Cheap rejection is the amplifier.") is voice, not noise. The same word inside an ordinary clause gets formalized.
   - Dialect-specific participle choice: US style prefers attributive "proven" ("a proven method"); traditional British style prefers "proved" as the participle. Do not enforce either without a target.

3. **Orthography** (deterministic, *canon-specific*; Vale `USScientific` overlay, which **inverts** by guide):

   | Rule | US scientific | Typical British journal |
   |---|---|---|
   | Dashes (`USScientific.EmDashSpacing`) | closed `---`, no space or newline either side | spaced en-dash `word -- word` |
   | Prefixes (`USScientific.PrefixHyphens`) | closed: multisite, nonzero, subunit, rearmed | often hyphenated |
   | Serial comma (`USScientific.SerialComma`) | required | omitted unless ambiguous (Oxford requires) |
   | Latin phrases (`USScientific.LatinPhrases`) | open, roman: post hoc, ad hoc | same, but check the journal |
   | Slash spacing (`USScientific.SpacedSlash`) | closed: safe/congested | same |
   | Heading articles (`USScientific.HeadingArticle`, `scripts/check_tex.py`) | dropped: "Model Hierarchy" | same |
   | Cross-reference case (`scripts/check_tex.py`) | Rule~4, Figure~2 | journal-dependent |
   | Spelling | -ize, -or, modeling | -ise (except Oxford), -our, modelling |

   Prefix-closure exceptions: meaning-bearing hyphens (re-form vs. reform, re-cover vs. recover), prefix before a capital or numeral (non-Gaussian, pre-1990), and awkward doublings the dictionary keeps hyphenated. When no target guide is named, `Core.DialectConsistency` flags mixed varieties; report the dominant one and normalize toward it only if asked.

4. **Protocol** (universal):
   - Mask before linting; never touch math, code, identifiers, citation keys, or URLs.
   - Attributed quotations (text reproduced from a source) are verbatim even when they violate the house style; imagined or illustrative quotes are the author's own prose and editable. When unsure which kind a quote is, flag rather than edit.
   - Ventilated prose (one sentence per source line) so diffs sentence-align.
   - Flag comments for uncertain edits and all structural suggestions (`% copyedit-flag:` in TeX, `<!-- copyedit-flag: ... -->` in Markdown).
   - Meaning gate after any bulk edit: run `references/meaning-gate.md` over every changed pair old-against-new.

## Mechanical sweep and diff-scoped runs

Requires [Vale](https://vale.sh) (`brew install vale`), using this skill's `vale.ini` and `styles/` directory (`styles/Core` and `styles/USScientific`), plus `scripts/check_tex.py` for TeX structure rules that Vale cannot see:

```bash
vale --config vale.ini paper.tex
python3 scripts/check_tex.py paper.tex
```

To copy-edit or lint only what changed in a revision pass or PR, keep the lint whole-file (so sentence segmentation, masks, and dialect consistency have full context) and intersect the `path:line:...` output with the unified diff's added or modified lines via `scripts/diff_filter.py`:

```bash
vale --config vale.ini --output=line paper.tex | python3 scripts/diff_filter.py <(git diff -U0 HEAD~1 -- paper.tex)
python3 scripts/check_tex.py paper.tex | python3 scripts/diff_filter.py <(git diff -U0 HEAD~1 -- paper.tex)
```
