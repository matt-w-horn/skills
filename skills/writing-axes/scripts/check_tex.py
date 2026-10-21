#!/usr/bin/env python3
"""TeX structure checks the Vale layer cannot express.

Rules (US scientific canon):
  heading-article   \\section{The ...}: sectioning headings should not open
                    with an article. Applies to chapter/section/subsection/
                    subsubsection only; \\paragraph headings legitimately
                    keep articles.
  crossref-case     rule~4, figure~\\ref{...}: named cross-references are
                    capitalized (Rule~4, Figure~\\ref{...}).

Verbatim-like environments and TeX comments are masked before scanning, with
line numbers preserved.

Usage: check_tex.py FILE [FILE...]
Exits 1 if any finding was reported, 0 otherwise.
"""
import re
import sys
from pathlib import Path

MASK_ENVS = ("verbatim", "alltt", "lstlisting", "tikzpicture")

HEADING = re.compile(
    r"\\(?:chapter|section|subsection|subsubsection)\*?\{\s*(?:The|An|A)\b"
)
CROSSREF = re.compile(
    r"\b(?:rule|section|figure|table|theorem|lemma|corollary|appendix)s?"
    r"~(?:\d|\\ref\b)"
)
COMMENT = re.compile(r"(?<!\\)%.*")


def _blank_preserving_lines(match: "re.Match[str]") -> str:
    return "\n" * match.group(0).count("\n")


def mask(text: str) -> str:
    """Blank out masked environments, keeping line numbers stable."""
    for env in MASK_ENVS:
        pattern = r"\\begin\{%s\*?\}.*?\\end\{%s\*?\}" % (env, env)
        text = re.sub(pattern, _blank_preserving_lines, text, flags=re.S)
    return text


def check(path: Path) -> list:
    """Return (lineno, rule, excerpt) findings for one TeX file."""
    if not path.is_file():
        raise ValueError(f"not a readable file: {path}")
    findings = []
    for lineno, line in enumerate(mask(path.read_text()).splitlines(), 1):
        line = COMMENT.sub("", line)
        for m in HEADING.finditer(line):
            findings.append((lineno, "heading-article", m.group(0)))
        for m in CROSSREF.finditer(line):
            findings.append((lineno, "crossref-case", m.group(0)))
    return findings


def main(argv: list) -> int:
    if not argv:
        raise ValueError("usage: check_tex.py FILE [FILE...]")
    status = 0
    for name in argv:
        for lineno, rule, excerpt in check(Path(name)):
            print(f"{name}:{lineno}: [{rule}] {excerpt!r}")
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
