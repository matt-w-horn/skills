# The source check

**When:** any document that states facts a reader can check: dates, numbers, quotes,
attributions, causal claims, citations. Run it on every review of such a document, before
the persona or reception passes. It is not needed for pure opinion or for instructions
whose only check is running them.

**Why it is separate from every other check:** the scanner and the tells procedure read only
the document. A claim the source contradicts reads exactly like a claim the source supports,
so no amount of reading the document finds it. Only reading the source does. This is rule 9
(every checkable number gets a source) and rule 10 (never present reconstructed wording as a
quote) carried out against the sources instead of assumed.

## How to run it

1. **Inventory the claims.** List every checkable statement with its location: each date
   and time, each number, each quotation, each "X said", each causal "because", each
   figure label and caption, each citation's title, author, venue, place, year and pages.
   Captions and diagram labels count; they are where unsourced detail accumulates.
2. **Get the source text, not a description of it.** Fetch the raw page or file and search
   it directly (`curl` and `grep`, `pdftotext`, OCR for scans). A fetch tool that
   summarizes the page paraphrases quotes, and checking a quote against a paraphrase
   confirms nothing. When a site blocks fetching, try an archived copy before giving up.
3. **Test the extraction before trusting it.** Confirm it returns one sentence you already
   know the source contains. An HTML-to-text step that drops a paragraph reports "not
   found" for text that is there.
4. **Read each source whole.** The sentence next to the one that matched is the one that
   qualifies it, contradicts it, or dates it.
5. **Check citation metadata against a registry,** not against memory or the document's own
   footnote: Crossref or the DOI record for papers, the publisher's page for books, the
   document's own title page for reports.
6. **Record both sides verbatim** for every claim: the document's words and the source's
   words, with page or paragraph. "Checked, matches" with nothing quoted is not a check.
7. **Give each claim one verdict:**
   - **supported**: the source says it, with the same strength and scope;
   - **contradicted**: the source says something incompatible;
   - **not in source**: the cited source does not say it (the claim may still be true,
     but its citation does not carry it);
   - **unverifiable**: the source could not be read. Name which source and why. Never
     promote an unverifiable claim to supported.

Report contradicted claims first, then not-in-source, then unverifiable, as a table:
`| Location | Document says | Source says (verbatim, page) | Verdict |`. Changes to what the
document claims go back to the writer (rule 22).

## Defect classes

These all survive a careful reading of the document alone. All examples are constructed.

### 1. Dateline read as event date

A newspaper dated the 12th reporting what an official "said yesterday" dates the
statement to the 11th. Wire copy, weeklies, and digests lag differently. Check the
weekday against the calendar for that year.

### 2. Truncated quotation

The quoted words are exact, but the sentence continues past the closing mark and narrows
them. "We accept responsibility." quoted from "We accept responsibility for the delay in
notifying customers" is a different statement. Check what follows every quotation.

### 3. Plan reported as done

The source says a fix "will be installed" or "is scheduled for completion by year end",
and the document says it was installed. A later claim built on the fix (that it prevented
a repeat) then rests on nothing. Keep tense and modality as the source has them.

### 4. Inference presented as finding

The document explains why something happened with a mechanism the source never mentions:
a plausible engineering or human-factors story that bridges a gap in the record. It may
be right. It is still the writer's inference, and it is labeled as one or cut.

### 5. Relabeled figure

A number moves from the quantity the source measured to a neighboring one: "40% of call
traffic restored" becomes "40% of capacity restored"; "canceled or delayed" becomes
"grounded"; "affected" becomes "stranded". Check the noun and the verb attached to every
number, not only the digits.

### 6. Added qualifier

The source says "more than 2 million calls" and the document says "more than 2 million
long-distance and data calls". The added words claim a breakdown the source never gave.

### 7. Blame relocated, not removed

An organization's correction that clears one group often names another: "the operators
were not at fault; the supervisor should have followed procedure." A document that reports
only the first half says the blame moved to the design when the source says it moved to a
person. Quote the correction whole.

### 8. Rule or standard read at the wrong date

The current text of a regulation, standard, or policy is checked against a claim about an
earlier year. Thresholds and deadlines change between versions, so find the version in
force on the date the document describes, and say which version you read.

### 9. Headline presented as speech

A headline or subhead ("Firm Says Staff Ignored Warnings") is quoted as if a person said
it. Headlines are the publication's words. Quote the article body, or attribute the
headline to the publication.

### 10. Source conflict hidden

Two sources disagree on a count, a time, or a sequence, and the document silently picks
one. Pick deliberately and note the disagreement where the reader can find it.

### 11. Citation metadata drift

A wrong report title, a wrong conference city, a wrong year, a title invented to fit what
the writer remembered. A reader who follows the citation and finds a different document
stops trusting the rest. The registry check in step 5 catches these.

### 12. Co-authored work described as solo

A multi-author publication, specification, or joint project is described with single-author
ownership. Check the byline on the source document and match the attribution to it ("a paper
co-authored with...", "our joint report").

### 13. Unverified diagram labels and part numbers

A schematic, architecture figure, or technical diagram carries model numbers, terminal
labels, or component names reconstructed from memory rather than read off the source manual
or datasheet. Check every label inside a figure against the primary document the same way
you check numbers in body prose.

