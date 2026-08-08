# The meaning gate

**When:** any bulk edit. A batch rewrite, a register conversion, a style pass applied across
files, a de-AI sweep, an agent-applied copy-edit. Not needed for a single sentence written
by hand and read back.

**Why it is separate from every other check:** a fluent rewrite and a faithful rewrite are
different properties, and the defects below all look locally correct. Nothing in `tells.md`
or `plain-language.md` catches them, because the output reads better than the input. Both
professional copy-editors and language models produce every class here.

**How to run it:** read each changed sentence as a pair, old against new, and ask per class,
"did this happen here?" A sweep that only reads the new text cannot see any of it. Anything
caught goes back to the original wording, or into a flagged comment for the writer. Never
silently keep a fluent-but-unfaithful rewrite: rule 22 in `SKILL.md` says changes to what a
text claims are kicked back to the writer, and this is where that rule is actually load
bearing.

All examples below are constructed.

## 1. Attachment flip

A modifier or genitive reattaches to the wrong head.

- Before: "the setting disabling automatic upload" (the setting does the disabling)
- After: "the setting for automatic disabling of upload" (now the disabling is automatic)

## 2. Negation or subject inversion

Restructuring inverts who does what, or what is negated.

- Before: "A job that exceeds the disk quota cannot be resumed."
- After: "Failure to exceed the disk quota means the job cannot be resumed." (the condition inverted)

## 3. Hyphen-manufactured compounds

A hyphenation rule creates a different concept.

- Before: "one user account" (a single account)
- After: "one-user account" (an account limited to one user)

Prefix closure has the same failure: "re-form the committee" is not "reform the committee",
and "read-only" is not "read only".

## 4. Broken expansions and names

Punctuation "fixes" inside acronym expansions, proper names, or terms of art destroy them.

- Before: "RAID (redundant array of independent disks)"
- After: "RAID (redundant array; independent disks)"

Terms of art misread as typos belong here too. Closing "half-open interval" to "half open
interval" changes a defined term into a description. Check how the field writes it before
touching it.

## 5. Coordination damage

Splitting or joining clauses drops a conjunct, strands a modifier, or produces a double
negative.

- Before: "no missing fields, no duplicate rows"
- After: "with no missing fields or no duplicate rows" (ungrammatical, and the second negation now misscopes)

## 6. Quantifier and scope drift

A rewrite silently widens or narrows a claim.

- Before: "the share of the two teams' tickets"
- After: "the share of total tickets" (different denominator)
- Before: "holds for every release on the branch"
- After: "holds for the release branch" (collective rather than universal)

## 7. Tampering with attributed quotations

Edits inside a quotation that reproduces a source, including "fixing" the quoted text's own
style to match the house style. Reproduced text is verbatim, and a style rule stops at its
quotation mark.

Imagined or illustrative quotes (invented speech, an aphorism the author coined) are the
author's own prose; editing them is legitimate and is judged by the other classes, not this
one. The hazard here is misclassification: check for a source before treating a quote as
editable, and flag when unsure.

## 8. Strength drift in claim verbs

"Proves" against "shows" against "suggests"; "is" against "approximates"; "certifies"
against "indicates". Swapping these is not register, it is a different claim. Flag rather
than judge when unsure which strength the author can support.
