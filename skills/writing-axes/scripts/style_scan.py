#!/usr/bin/env python3
"""Prose metrics scanner: standard, format-robust measures only.

Computes readability (Flesch Reading Ease, Flesch-Kincaid Grade,
Coleman-Liau), sentence-length statistics, and token/n-gram frequency
tables over markdown, HTML, or LaTeX input. FKGL is syllable-based and
Coleman-Liau is character-based; if the two disagree wildly, suspect
the text extraction before the prose.

The single flag is flat sentence rhythm (low length variance), the one
tell that is a well-defined statistic. Everything else is data for the
reading procedure in references/tells.md — the tells that matter most
are syntactic shapes with open lexical slots, and no pattern matcher
catches those.

Usage:
    python3 style_scan.py FILE [FILE ...] [--format auto|markdown|html|latex]
    python3 style_scan.py --self-test
"""

import argparse
import html
import html.parser
import re
import statistics
import sys
from collections import Counter

# ---------- extraction ------------------------------------------------------


class _HTMLText(html.parser.HTMLParser):
    SKIP = {"script", "style", "head", "code", "pre", "svg"}
    BREAK = {"p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BREAK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def extract_html(text):
    p = _HTMLText()
    p.feed(text)
    return "".join(p.parts)


LATEX_DROP_ENVS = ("equation", "align", "alignat", "gather", "eqnarray",
                   "figure", "table", "tabular", "tikzpicture", "verbatim",
                   "lstlisting", "minted", "alltt", "thebibliography", "axis")
LATEX_DROP_ARG = ("cite", "citep", "citet", "ref", "eqref", "autoref",
                  "label", "url", "input", "include", "includegraphics",
                  "bibliography", "bibliographystyle", "usepackage",
                  "documentclass", "begin", "end", "texttt", "lean",
                  "newcommand", "renewcommand", "hypersetup", "pagestyle")


def extract_latex(text):
    text = re.sub(r"(?<!\\)%.*", " ", text)
    for env in LATEX_DROP_ENVS:
        text = re.sub(r"\\begin\{" + env + r"\*?\}.*?\\end\{" + env + r"\*?\}",
                      " ", text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", " ", text, flags=re.S)
    text = re.sub(r"(?<!\\)\$[^$]*\$", " ", text)
    text = text.replace(r"\\", " ")
    drop = "|".join(LATEX_DROP_ARG)
    for _ in range(6):  # unwrap nested commands innermost-first
        text = re.sub(r"\\(" + drop + r")\*?(\[[^\]]*\])?\{[^{}]*\}", " ",
                      text)
        text = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = text.replace("~", " ").replace("{", " ").replace("}", " ")
    return text.replace("``", '"').replace("''", '"')


def extract_markdown(text):
    text = re.sub(r"\A(---|\+\+\+)\n.*?\n\1\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```|~~~.*?~~~", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", " ", text)
    text = "\n".join(ln for ln in text.splitlines()
                     if not ln.lstrip().startswith("|"))
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", text, flags=re.M)
    text = re.sub(r"[*_]{1,3}([^*_\n]+)[*_]{1,3}", r"\1", text)
    return text


def detect_format(path, text):
    ext = path.lower().rsplit(".", 1)[-1] if "." in path else ""
    if ext in ("tex", "ltx", "latex"):
        return "latex"
    if ext in ("html", "htm", "xhtml"):
        return "html"
    if ext in ("md", "markdown", "mdx", "txt", "rst"):
        return "markdown"
    if "\\documentclass" in text[:2000] or "\\begin{document}" in text:
        return "latex"
    if re.search(r"<(html|body|p|div|h1)\b", text[:2000], re.I):
        return "html"
    return "markdown"


def extract(text, fmt):
    text = {"html": extract_html, "latex": extract_latex,
            "markdown": extract_markdown}[fmt](text)
    text = re.sub(r"https?://\S+", " ", text)
    text = text.replace("\u2019", "'").replace("---", "\u2014")
    for abbr, safe in (("e.g.", "eg"), ("i.e.", "ie"), ("etc.", "etc"),
                       ("vs.", "vs")):
        text = text.replace(abbr, safe)
    return text


# ---------- metrics ---------------------------------------------------------

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")
CONTRACTION_RE = re.compile(r"\b\w+'(t|s|re|ve|ll|d|m)\b", re.I)
PROCEDURE_RE = re.compile(r"\b(simply|easy|easily|just|quickly)\b", re.I)
NGRAM_TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?|[,;:\u2014\u2013]")

# Common-word stoplist for the repeated-words table. Contrast and negation
# anchors (not, no, never, rather, instead, than, only, merely) are kept OUT
# of this list on purpose: a high count on one of them is exactly the signal
# the tells procedure wants, including for discontinuous frames like
# "rather X than Y" that no contiguous n-gram can see.
STOPWORDS = set("""a an and are as at be but by can could did do does for from
had has have he her his i if in into is it its me my of on one or our she so
that the their them there they this to was we were what when where which who
will with would you your""".split())


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")) and n > 1:
        n -= 1
    return max(1, n)


def split_sentences(prose):
    parts = re.split(r"(?<=[.!?])\s+", prose)
    out = []
    for p in parts:
        n = len(WORD_RE.findall(p))
        if n >= 2:
            out.append((p.strip(), n))
    return out


def top_ngrams(tokens, n, min_count, k):
    counts = Counter(tuple(tokens[i:i + n])
                     for i in range(len(tokens) - n + 1))
    items = [(g, c) for g, c in counts.items()
             if c >= min_count and any(t[0].isalpha() for t in g)]
    items.sort(key=lambda x: (-x[1], x[0]))
    return items[:k]


def pretty(gram):
    return " ".join(gram).replace(" ,", ",").replace(" ;", ";") \
                         .replace(" :", ":")


def analyze(prose):
    words = WORD_RE.findall(prose)
    nw = len(words)
    letters = sum(1 for w in words for ch in w if ch.isalpha())
    syl = sum(syllables(w) for w in words)
    sents = split_sentences(prose)
    ns = len(sents)
    lens = [n for _, n in sents]
    m = {"words": nw, "sentences": ns, "letters": letters}
    if nw and ns:
        asl, asw = nw / ns, syl / nw
        m["fre"] = round(206.835 - 1.015 * asl - 84.6 * asw, 1)
        m["fkgl"] = round(0.39 * asl + 11.8 * asw - 15.59, 2)
        m["cli"] = round(0.0588 * (letters / nw * 100)
                         - 0.296 * (ns / nw * 100) - 15.8, 2)
        m["sent_mean"] = round(statistics.mean(lens), 1)
        m["sent_min"], m["sent_max"] = min(lens), max(lens)
        m["sent_cv"] = (round(statistics.stdev(lens)
                              / statistics.mean(lens), 2)
                        if ns >= 2 else None)
    toks = NGRAM_TOKEN_RE.findall(prose.lower())
    m["bigrams"] = top_ngrams(toks, 2, min_count=3, k=12)
    m["trigrams"] = top_ngrams(toks, 3, min_count=2, k=8)
    reps = Counter(t for t in toks if t.isalpha() and t not in STOPWORDS)
    m["repeated_words"] = sorted(
        ((w, c) for w, c in reps.items() if c >= 3),
        key=lambda x: (-x[1], x[0]))[:12]
    m["contractions"] = len(CONTRACTION_RE.findall(prose))
    m["procedure_words"] = len(PROCEDURE_RE.findall(prose))
    m["exclamations"] = prose.count("!")

    m["flags"] = []
    if (m.get("sent_cv") is not None and ns >= 15
            and m["sent_cv"] < 0.30):
        m["flags"].append(("variance",
                           f"sentence-length CV {m['sent_cv']} over {ns} "
                           "sentences; rhythm is flat (low burstiness)"))
    return m


# ---------- report ----------------------------------------------------------


def per_k(m, n):
    return round(n * 1000.0 / m["words"], 1) if m["words"] else 0.0


def report(name, fmt, m):
    print(f"\n== {name} ({fmt}) ==")
    print(f"  words {m['words']}  sentences {m['sentences']}  "
          f"mean len {m.get('sent_mean')}  "
          f"range {m.get('sent_min')}-{m.get('sent_max')}  "
          f"length CV {m.get('sent_cv')}")
    print(f"  Flesch Reading Ease {m.get('fre')}   FK Grade "
          f"{m.get('fkgl')}   Coleman-Liau {m.get('cli')}   "
          "(FKGL vs CLI far apart = suspect extraction)")
    print(f"  contractions {m['contractions']} "
          f"({per_k(m, m['contractions'])}/1000)   "
          f"simply/just/easy/quickly {m['procedure_words']} "
          "(matters on the Instruction axis)   "
          f"exclamations {m['exclamations']}")
    if m["bigrams"]:
        row = "   ".join(f"{pretty(g)} x{c}" for g, c in m["bigrams"])
        print(f"  repeated bigrams: {row}")
    if m["trigrams"]:
        row = "   ".join(f"{pretty(g)} x{c}" for g, c in m["trigrams"])
        print(f"  repeated trigrams: {row}")
    if m["repeated_words"]:
        row = "   ".join(f"{w} x{c}" for w, c in m["repeated_words"])
        print(f"  repeated words (frame anchors kept in): {row}")
    for key, msg in m["flags"]:
        print(f"  FLAG [{key}] {msg}")
    if not m["flags"]:
        print("  no flags (the scanner's only flag is flat rhythm; "
              "run the tells.md procedure regardless)")


# ---------- self-test -------------------------------------------------------
# A new check must first fail on constructed input with a known answer, and
# behave identically across formats, before its numbers count for anything.

HAND = "The cat sat on the mat. It was warm. The dog slept by the door."
# By hand: 15 words, 3 sentences, 15 syllables, 46 letters.
# FRE = 206.835 - 1.015*5 - 84.6*1 = 117.16
# FKGL = 0.39*5 + 11.8*1 - 15.59 = -1.84
# CLI = 0.0588*(46/15*100) - 0.296*(3/15*100) - 15.8 = -3.69

PARA = ("The build failed on Tuesday. I didn't notice until the pager went "
        "off, and by then two deploys had shipped on top of the broken "
        "artifact. Rollback took nine minutes. The fix itself was one line: "
        "the cache key omitted the compiler version, so a stale object "
        "survived the upgrade. I added the version to the key and rebuilt "
        "from scratch. We lost about an hour of capacity in one region. "
        "Nothing customer-visible broke, which was luck, and the postmortem "
        "should say so. Next week I'll add a canary that compiles a known "
        "file and diffs the object hash. That check would have caught this "
        "in seconds. It's cheap. Long term, the cache needs an owner, "
        "because nobody has looked at its eviction policy since it shipped, "
        "and this is the second surprise it has produced this year.")

MD_WRAP = "## Notes\n\n```\nignore this junk block entirely\n```\n\n" + \
    PARA.replace("canary", "*canary*")
HTML_WRAP = ("<html><body><h2>Notes</h2><script>ignore this junk block "
             "entirely</script><p>" + PARA.replace("canary",
                                                   "<em>canary</em>")
             + "</p></body></html>")
LATEX_WRAP = ("\\documentclass{article}\n\\begin{document}\n"
              "\\section{Notes}\n\\begin{verbatim}\nignore this junk block "
              "entirely\n\\end{verbatim}\n"
              + PARA.replace("canary", "\\emph{canary}")
              + "\n\\end{document}\n")

MONO = " ".join(
    "The nightly job copies every table into the backup region at "
    "midnight." for _ in range(16))

FRAMES = ("We chose steel rather than iron. We test rather than assume. "
          "It runs nightly rather than weekly. We patch rather than "
          "rewrite the module.")


def self_test():
    ok = True

    def check(cond, label):
        nonlocal ok
        print(("  pass  " if cond else "  FAIL  ") + label)
        ok = ok and cond

    print("hand-checked values:")
    m = analyze(extract(HAND, "markdown"))
    check(m["words"] == 15 and m["sentences"] == 3,
          f"words/sentences = {m['words']}/{m['sentences']} (want 15/3)")
    check(abs(m["fre"] - 117.16) < 0.5, f"FRE {m['fre']} (want ~117.16)")
    check(abs(m["fkgl"] - (-1.84)) < 0.1, f"FKGL {m['fkgl']} (want ~-1.84)")
    check(abs(m["cli"] - (-3.69)) < 0.3, f"CLI {m['cli']} (want ~-3.69)")

    print("format invariance (same prose as md, html, latex):")
    res = {f: analyze(extract(t, f)) for f, t in
           (("markdown", MD_WRAP), ("html", HTML_WRAP),
            ("latex", LATEX_WRAP))}
    w = {r["words"] for r in res.values()}
    s = {r["sentences"] for r in res.values()}
    g = [r["fkgl"] for r in res.values()]
    c = [r["cli"] for r in res.values()]
    check(len(w) == 1, f"word counts equal across formats: {sorted(w)}")
    check(len(s) == 1, f"sentence counts equal across formats: {sorted(s)}")
    check(max(g) - min(g) < 0.05, f"FKGL spread {max(g) - min(g):.3f}")
    check(max(c) - min(c) < 0.05, f"CLI spread {max(c) - min(c):.3f}")

    print("variance flag:")
    clean = analyze(extract(PARA, "markdown"))
    check(clean["sent_cv"] is not None and clean["sent_cv"] > 0.4
          and not clean["flags"],
          f"varied prose: CV {clean['sent_cv']}, no flags")
    mono = analyze(extract(MONO, "markdown"))
    check(any(k == "variance" for k, _ in mono["flags"]),
          f"uniform prose: CV {mono['sent_cv']}, variance flag fired")

    print("n-gram surfacing:")
    fr = analyze(extract(FRAMES, "markdown"))
    hit = next((c for g, c in fr["bigrams"] if g == ("rather", "than")), 0)
    check(hit >= 4, f"'rather than' surfaced x{hit} in bigram table")

    print("SELF-TEST " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--format", default="auto",
                    choices=["auto", "markdown", "html", "latex"])
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())
    if not args.files:
        ap.error("no files given (or use --self-test)")
    for path in args.files:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        fmt = args.format if args.format != "auto" \
            else detect_format(path, raw)
        report(path, fmt, analyze(extract(raw, fmt)))


if __name__ == "__main__":
    main()
