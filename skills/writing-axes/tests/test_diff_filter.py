import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import diff_filter  # noqa: E402

DIFF = "\n".join(
    [
        "diff --git a/paper/main.tex b/paper/main.tex",
        "index 1111111..2222222 100644",
        "--- a/paper/main.tex",
        "+++ b/paper/main.tex",
        "@@ -10,4 +10,5 @@ a section heading",
        " unchanged one",
        "-removed line",
        "+added line A",
        "+added line B",
        " unchanged two",
        "@@ -30 +31 @@",
        "-old",
        "+new",
        "diff --git a/gone.tex b/gone.tex",
        "--- a/gone.tex",
        "+++ /dev/null",
        "@@ -1,2 +0,0 @@",
        "-bye",
        "-bye",
    ]
)


class ChangedLinesTests(unittest.TestCase):
    def test_new_side_numbering_with_context_and_deletions(self):
        changed = diff_filter.changed_lines(DIFF)
        # hunk 1 starts at 10: context(10), two additions(11, 12), context(13)
        self.assertEqual(changed["paper/main.tex"], {11, 12, 31})

    def test_deleted_file_contributes_nothing(self):
        self.assertNotIn("gone.tex", diff_filter.changed_lines(DIFF))

    def test_empty_diff_changes_nothing(self):
        self.assertEqual(diff_filter.changed_lines(""), {})

    def test_plain_diff_u_timestamp_headers_are_handled(self):
        diff = "\n".join(
            [
                "--- a/main.tex\t2026-08-07 16:00:00.000000000 -0700",
                "+++ b/main.tex\t2026-08-07 16:01:00.000000000 -0700",
                "@@ -174 +174 @@",
                "-old",
                "+new",
            ]
        )
        self.assertEqual(diff_filter.changed_lines(diff), {"main.tex": {174}})


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.changed = diff_filter.changed_lines(DIFF)

    def test_finding_on_changed_line_survives(self):
        findings = ["main.tex:11:5:Core.Hedges:msg"]
        self.assertEqual(
            diff_filter.filter_findings(findings, self.changed), findings
        )

    def test_finding_on_unchanged_line_is_dropped(self):
        findings = ["main.tex:10:5:Core.Hedges:msg", "main.tex:13: [rule] x"]
        self.assertEqual(diff_filter.filter_findings(findings, self.changed), [])

    def test_path_matches_by_trailing_components(self):
        keep = ["/abs/repo/paper/main.tex:31:1:Check:msg"]
        drop = ["other/main.tex:31:1:Check:msg", "notes.tex:31:1:Check:msg"]
        self.assertEqual(
            diff_filter.filter_findings(keep + drop, self.changed), keep
        )

    def test_check_tex_output_format_is_accepted(self):
        findings = ["paper/main.tex:12: [crossref-case] 'rule~4'"]
        self.assertEqual(
            diff_filter.filter_findings(findings, self.changed), findings
        )

    def test_non_finding_lines_are_dropped(self):
        self.assertEqual(
            diff_filter.filter_findings(["just some text"], self.changed), []
        )


class MainTests(unittest.TestCase):
    def test_wrong_usage_raises_valueerror(self):
        with self.assertRaises(ValueError):
            diff_filter.main([])

    def test_missing_diff_file_raises_valueerror(self):
        with self.assertRaises(ValueError):
            diff_filter.main(["/nonexistent/changes.diff"])


if __name__ == "__main__":
    unittest.main()
