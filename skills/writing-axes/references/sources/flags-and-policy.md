# Sources: flags, corrections, and current policy

Open this file before citing any source by name in output. It carries the verification report's scope note, its full corrections summary, and the one time-sensitive policy item. Item numbering follows the verification report of 2026-08-04.

## Scope note (from the report, verbatim)

Every verbatim quotation in these source files is marked as such and is copied from the cited locator; wording labeled "summary" is a verified paraphrase, not a quote. Paywalled or secondhand cases are flagged explicitly. Where editions or dates conflict, the conflict is reported rather than silently resolved.

---

## 34. ACM Policy on Authorship — current (2026) generative-AI disclosure — VERIFIED (TIME-SENSITIVE)

The ACM Policy on Authorship was updated (effective **May 14, 2026**; publicly surfaced ~June 2026) and **supersedes the April 20, 2023 AI-disclosure provisions**. It replaces blanket mandatory disclosure with a **two-tier model plus an accountability regime**. **Verbatim** (current "Use of Artificial Intelligence" section): "Rather than attempt to limit the use of Artificial Intelligence (AI)… by placing expectations on authors to disclose all uses of large language models in their Works, this updated Policy attempts to set clear expectations for their responsible use."

- **Tier 1 — AI used in the *research itself*** ("design and methodology… creation and selection of data sources… designing experiments… coding, implementing models, running simulations, data analysis, testing, validating results…"): **Verbatim** — "the specific use(s) of AI tools must be described in detail in the **methods section** of the Work."
- **Tier 2 — AI used to *assist with writing*:** **Verbatim** — "ACM no longer requires the disclosure of information regarding the use of AI."
- **Accountability — Verbatim:** "All named authors on an ACM submission will be held responsible and accountable for any problematic content contained in the submission regardless of the source of that problematic content," with ACM reserving the right to **reject** (pre-publication) or **retract** (post-publication) works with AI-caused integrity problems (hallucinated references, plagiarism, fabricated/unverifiable artifacts, propagated bias).

**Differences from 2023:** (a) **Location:** disclosure moves from the **Acknowledgements** section (2023) to the **Methods** section — and only for *research* use; (b) **Scope:** writing-assistance disclosure changes from mandatory ("must be fully disclosed in the Work") to **not required**; (c) **Emphasis:** the policy pivots from *disclosure* to *author accountability* for AI-caused errors. Generative AI still **may not be listed as an author**.

**Caveats (important):** The ACM URL serves inconsistent versions depending on fetch method — a cached/bot-detection path still returns the **stale April 2023 text** ("must be fully disclosed in the Work"), while a clean extraction returns the May 14, 2026 text. The current wording was corroborated against the **April 2026 ACM "Blue Diamond" newsletter** (which stated the Board's aim was to stop AI-caused errors rather than enforce disclosure) and independent June 9, 2026 community summaries (SIGCHI's Medium guidance carries an "UPDATE JUNE 2026" banner; a RecSys community post summarizes the two-tier rule verbatim). Numerous ACM SIG venue pages (SIGCSE Virtual 2026, RESPECT 2026) and university libguides **still quote the old 2023 language and are lagging** — do not rely on them for the current state. This is a moving target: re-verify against acm.org before relying on it for a submission. Locator: acm.org/publications/policies/new-acm-policy-on-authorship (updated May 14, 2026); acm.org/articles/pubs-newsletter/2026/blue-diamond-april-2026.

---

## Summary of corrections / flags (from the report, verbatim)

- **#16** Toolsmith II is *CACM* **39(3)**, not 39(5).
- **#20** Stealing Thunder is in ***Law and Human Behavior*** 17(6):597–609, not *Basic and Applied Social Psychology*.
- **#24** The specific claim that *excessive hedging shifts reader attention to author confidence* is **NOT supported** in Hyland's work as located; do not attribute it to him.
- **#26** BLUF's doctrinal home is **AR 25-50 (2013)**, not FM 6-22.
- **#27** The Olivier/Hoffman "try acting" story is **apocryphal as usually told** and denied by Hoffman.
- **#29** Progressive disclosure originates with **Carroll/IBM (early 1980s)**, not "Nielsen and Wilson"; Nielsen popularized it.
- **#30** No canonical writing-craft source applies speech-act theory as a sentence-level revision technique — that heuristic is **folklore**.
- **#32** The per-paragraph "So what?" test is **unattributable folklore**; the documented cousin is Graff & Birkenstein's thesis-level "So what? Who cares?"
- **#33** Minto dates genuinely **conflict** (1978 vs. 1985 first edition; 1996 expanded) — reported, not resolved.
- **#34** The ACM policy **has changed** (effective May 14, 2026): two-tier model — Methods-section disclosure for research use, **no disclosure required for writing assistance** — with a shift to author accountability. The live ACM page and many SIG/library pages still cache the old 2023 text.
- Items where the core rests on a faithful **secondary** source rather than the primary (flagged in place): **#4** (Toulmin, paywalled primary) and portions of **#15/#19/#22** (definitions given as labeled summaries corroborated by reference works).

## Additional conversation-verified flags (outside the numbered report)

- **Orwell's checklist** is four questions plus two optional ones; "five questions" and mergers with the six rules are common garbles (full text in `craft-sentence.md`).
- **Mensh & Kording rule numbers** are frequently miscited: C-C-C is Rule 3, the abstract is Rule 5, the introduction gap-funnel is Rule 6; "roughly four sentences" for the abstract is not theirs. Their PLOS reference list misprints Gopen & Swan's first author as "George GD" (correct: George D. Gopen). Details in `craft-structure.md`.
- **Peyton Jones** quotes Brooks's Toolsmith line in his own slides; cite Brooks *CACM* 39(3) for it, not the slides. Details in `craft-structure.md` and `rhetoric.md`.
