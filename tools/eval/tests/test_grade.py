"""Tests for the pure parts of tools/eval/grade.py. Run from tools/eval:
    python3 -m unittest discover tests

`_parse` reads the judge's answer out of whatever the CLI returned. When it
fails it returns None, which the scorer treats as undecided rather than as a
fail, so a parsing regression shows up as a suite that quietly grades nothing.
These pin the shapes it has to survive.

`build_sources` exists because of a bug this suite caught: assertions that ask
whether a document's figures match the person's records were being failed for
lack of evidence, because the judge only ever saw the document.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import grade  # noqa: E402


class ParseVerdict(unittest.TestCase):
    def test_reads_a_nested_result_object(self):
        raw = json.dumps({"result": {"verdict": "pass", "evidence": "quoted bit"}})
        self.assertEqual(grade._parse(raw), (True, "quoted bit"))

    def test_reads_a_result_holding_json_as_a_string(self):
        raw = json.dumps({"result": json.dumps({"verdict": "fail",
                                                "evidence": "absent"})})
        self.assertEqual(grade._parse(raw), (False, "absent"))

    def test_reads_a_bare_verdict_object(self):
        raw = json.dumps({"verdict": "fail", "evidence": "no range given"})
        self.assertEqual(grade._parse(raw), (False, "no range given"))

    def test_falls_back_to_finding_the_verdict_in_prose(self):
        raw = 'Some preamble {"verdict": "pass", "evidence": "found it"} trailing'
        passed, evidence = grade._parse(raw)
        self.assertTrue(passed)
        self.assertEqual(evidence, "found it")

    def test_unparseable_output_is_undecided_not_a_fail(self):
        passed, evidence = grade._parse("the model said something else entirely")
        self.assertIsNone(passed, "a broken judge must not read as a failed assertion")
        self.assertIn("unparseable", evidence)

    def test_an_unexpected_verdict_word_is_undecided(self):
        raw = json.dumps({"verdict": "maybe", "evidence": "hedged"})
        self.assertIsNone(grade._parse(raw)[0])

    def test_evidence_is_capped(self):
        raw = json.dumps({"verdict": "pass", "evidence": "x" * 5000})
        self.assertLessEqual(len(grade._parse(raw)[1]), 400)


class BuildArtifact(unittest.TestCase):
    def test_response_and_files_are_both_included(self):
        art = grade.build_artifact("the reply", {"PLAN.md": "the document"})
        self.assertIn("the reply", art)
        self.assertIn("the document", art)
        self.assertIn("PLAN.md", art)

    def test_empty_files_are_dropped(self):
        art = grade.build_artifact("reply", {"empty.md": "   ", "real.md": "x"})
        self.assertNotIn("empty.md", art)
        self.assertIn("real.md", art)

    def test_oversized_artifacts_are_truncated(self):
        art = grade.build_artifact("y" * 500, limit=100)
        self.assertLess(len(art), 300)
        self.assertIn("[truncated]", art)

    def test_documents_survive_truncation_ahead_of_code(self):
        """A workspace's own model code must not displace the deliverable.

        Observed on a real run: ~50KB of the skill's Python sat beside a 25KB
        plan document, and alphabetical order let it eat the budget.
        """
        files = {
            "workspace/model/run_analysis.py": "A" * 40_000,
            "workspace/model/test_plan.py": "B" * 40_000,
            "workspace/data/series.csv": "C" * 40_000,
            "workspace/PLAN.md": "the deliverable",
            "workspace/facts.md": "the sourced figures",
        }
        art = grade.build_artifact("the response", files, limit=60_000)
        self.assertIn("the deliverable", art)
        self.assertIn("the sourced figures", art)
        self.assertIn("[truncated]", art)

    def test_code_is_still_included_when_there_is_room(self):
        art = grade.build_artifact("", {"PLAN.md": "doc", "model.py": "code"})
        self.assertIn("doc", art)
        self.assertIn("code", art)
        self.assertLess(art.index("doc"), art.index("code"))

    def test_nothing_in_nothing_out(self):
        self.assertEqual(grade.build_artifact("", {}), "")


class BuildSources(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def write(self, name, body):
        path = os.path.join(self.root, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)

    def test_fixture_files_are_included_and_labelled(self):
        self.write("accounts.txt", "ISA 86,300")
        self.write("notes.md", "we agreed age 97")
        sources = grade.build_sources(self.root)
        self.assertIn("86,300", sources)
        self.assertIn("age 97", sources)
        self.assertIn("accounts.txt", sources)
        self.assertIn("source_material", sources)

    def test_sources_say_they_are_not_part_of_the_document(self):
        """Otherwise the judge can credit the document for the fixture's content."""
        self.write("notes.md", "content")
        self.assertIn("not part of it", grade.build_sources(self.root))

    def test_no_fixture_yields_nothing(self):
        self.assertEqual(grade.build_sources(None), "")
        self.assertEqual(grade.build_sources("/nonexistent/path"), "")

    def test_empty_fixture_directory_yields_nothing(self):
        self.assertEqual(grade.build_sources(self.root), "")

    def test_hidden_files_are_skipped(self):
        self.write(".DS_Store", "junk")
        self.assertEqual(grade.build_sources(self.root), "")

    def test_oversized_fixtures_are_truncated(self):
        self.write("big.csv", "z" * 5000)
        sources = grade.build_sources(self.root, limit=200)
        self.assertIn("[truncated]", sources)


class Prompt(unittest.TestCase):
    def test_prompt_formats_with_and_without_sources(self):
        bare = grade.JUDGE_PROMPT.format(assertion="A", artifact="B", sources="")
        self.assertIn("<criterion>", bare)
        self.assertNotIn("source_material", bare)
        withsrc = grade.JUDGE_PROMPT.format(assertion="A", artifact="B",
                                            sources="\n<source_material>x</source_material>\n")
        self.assertIn("source_material", withsrc)

    def test_prompt_puts_the_burden_of_proof_on_the_criterion(self):
        self.assertIn("burden of proof", grade.JUDGE_PROMPT)

    def test_prompt_does_not_reveal_provenance(self):
        """A judge that knows which run made the document can prefer it."""
        lowered = grade.JUDGE_PROMPT.lower()
        for leak in ("with_skill", "without_skill", "baseline", "the skill"):
            self.assertNotIn(leak, lowered)


if __name__ == "__main__":
    unittest.main()
