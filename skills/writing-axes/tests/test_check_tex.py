import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_tex  # noqa: E402

BAD = "\n".join(
    [
        r"\section{The Model Hierarchy}",  # heading-article, line 1
        r"Retries act on demand.",
        r"Compare the caps against rule~4 and figure~\ref{fig:phase}.",  # 2x
        r"\subsection{A Worked Example}",  # heading-article, line 4
    ]
)

GOOD = "\n".join(
    [
        r"\section{Model Hierarchy}",
        r"\paragraph{A worked example.}",  # articles allowed in \paragraph
        r"Compare the caps against Rule~4 and Figure~\ref{fig:phase}.",
        r"The rule applies broadly.",  # 'rule' without ~ref is prose
        r"50\% of runs pass.",  # escaped percent is not a comment
    ]
)

MASKED = "\n".join(
    [
        r"\begin{verbatim}",
        r"see rule~4 in \section{The Manual}",  # masked, must not fire
        r"\end{verbatim}",
        r"% comment only: rule~4",  # comments stripped, must not fire
        r"But see rule~4.",  # line 5: the one real finding
    ]
)


def _tmp(content: str) -> Path:
    f = tempfile.NamedTemporaryFile(
        "w", suffix=".tex", delete=False, encoding="utf-8"
    )
    f.write(content)
    f.close()
    return Path(f.name)


class CheckTexTests(unittest.TestCase):
    def test_fires_on_constructed_bad_input(self):
        findings = check_tex.check(_tmp(BAD))
        rules = [(lineno, rule) for lineno, rule, _ in findings]
        self.assertIn((1, "heading-article"), rules)
        self.assertIn((4, "heading-article"), rules)
        self.assertEqual(
            [lineno for lineno, rule in rules if rule == "crossref-case"],
            [3, 3],
        )

    def test_silent_on_good_input(self):
        self.assertEqual(check_tex.check(_tmp(GOOD)), [])

    def test_masks_verbatim_and_comments_preserving_lines(self):
        findings = check_tex.check(_tmp(MASKED))
        self.assertEqual(findings, [(5, "crossref-case", "rule~4")])

    def test_missing_file_raises_valueerror(self):
        with self.assertRaises(ValueError):
            check_tex.check(Path("/nonexistent/nope.tex"))

    def test_no_args_raises_valueerror(self):
        with self.assertRaises(ValueError):
            check_tex.main([])


if __name__ == "__main__":
    unittest.main()
