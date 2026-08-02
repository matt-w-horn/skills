"""Tests for tools/eval/corpus.py. Run from the tools/eval directory:
    python3 -m unittest discover tests

`classify` decides what each query counts as when the corpus is balanced and
scored, and it is derived from `expect` rather than stored, so a wrong
derivation would silently misreport balance rather than raise. These pin it.
"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import corpus  # noqa: E402

SKILLS = ["alpha-skill", "beta-skill"]


def q(owner, expect):
    return {"id": "x", "owner": owner, "expect": expect, "split": "train",
            "query": "text", "why": "because"}


class Classify(unittest.TestCase):
    def test_owner_fires_is_positive(self):
        self.assertEqual(
            corpus.classify(q("alpha-skill",
                              {"alpha-skill": True, "beta-skill": False}), SKILLS),
            "positive")

    def test_other_skill_fires_is_cross(self):
        self.assertEqual(
            corpus.classify(q("alpha-skill",
                              {"alpha-skill": False, "beta-skill": True}), SKILLS),
            "cross")

    def test_nothing_fires_is_near_miss(self):
        self.assertEqual(
            corpus.classify(q("alpha-skill",
                              {"alpha-skill": False, "beta-skill": False}), SKILLS),
            "near-miss")

    def test_either_wins_over_everything_else(self):
        self.assertEqual(
            corpus.classify(q("alpha-skill",
                              {"alpha-skill": corpus.EITHER,
                               "beta-skill": True}), SKILLS),
            "either")


class Loading(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        for name, desc in (("alpha-skill", "Alpha."), ("beta-skill", "Beta.")):
            os.makedirs(os.path.join(self.root, name), exist_ok=True)
            with open(os.path.join(self.root, name, "SKILL.md"), "w",
                      encoding="utf-8") as fh:
                fh.write(f"---\nname: {name}\ndescription: {desc}\n---\nBody.\n")

    def write(self, skill, queries, version=1):
        edir = os.path.join(self.root, skill, "evals")
        os.makedirs(edir, exist_ok=True)
        with open(os.path.join(edir, "trigger.json"), "w", encoding="utf-8") as fh:
            json.dump({"version": version, "skill": skill, "queries": queries}, fh)

    def good_query(self, qid="a-01"):
        return {"id": qid, "query": "a realistic question about the future",
                "expect": {"alpha-skill": True, "beta-skill": False},
                "why": "clearly this one", "split": "train"}

    def test_skill_names_finds_both(self):
        self.assertEqual(corpus.skill_names(self.root), SKILLS)

    def test_loads_a_valid_file(self):
        self.write("alpha-skill", [self.good_query()])
        loaded = corpus.load_trigger_corpus(self.root)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["owner"], "alpha-skill")

    def test_rejects_an_unknown_split(self):
        bad = self.good_query()
        bad["split"] = "holdout"
        self.write("alpha-skill", [bad])
        with self.assertRaises(corpus.CorpusError) as cm:
            corpus.load_trigger_corpus(self.root)
        self.assertIn("split", str(cm.exception))

    def test_rejects_expect_missing_a_skill(self):
        bad = self.good_query()
        bad["expect"] = {"alpha-skill": True}
        self.write("alpha-skill", [bad])
        with self.assertRaises(corpus.CorpusError):
            corpus.load_trigger_corpus(self.root)

    def test_rejects_a_non_boolean_expectation(self):
        bad = self.good_query()
        bad["expect"] = {"alpha-skill": "yes", "beta-skill": False}
        self.write("alpha-skill", [bad])
        with self.assertRaises(corpus.CorpusError):
            corpus.load_trigger_corpus(self.root)

    def test_accepts_either_as_an_expectation(self):
        ok = self.good_query()
        ok["expect"] = {"alpha-skill": corpus.EITHER, "beta-skill": corpus.EITHER}
        self.write("alpha-skill", [ok])
        self.assertEqual(len(corpus.load_trigger_corpus(self.root)), 1)

    def test_rejects_duplicate_ids_across_files(self):
        self.write("alpha-skill", [self.good_query("same-id")])
        beta = self.good_query("same-id")
        beta["expect"] = {"alpha-skill": False, "beta-skill": True}
        self.write("beta-skill", [beta])
        with self.assertRaises(corpus.CorpusError) as cm:
            corpus.load_trigger_corpus(self.root)
        self.assertIn("duplicate", str(cm.exception))

    def test_rejects_an_unexpected_version(self):
        self.write("alpha-skill", [self.good_query()], version=2)
        with self.assertRaises(corpus.CorpusError):
            corpus.load_trigger_corpus(self.root)

    def test_reports_which_file_failed(self):
        self.write("alpha-skill", [self.good_query()])
        path = os.path.join(self.root, "alpha-skill", "evals", "trigger.json")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("{oh no")
        with self.assertRaises(corpus.CorpusError) as cm:
            corpus.load_trigger_corpus(self.root)
        self.assertIn("trigger.json", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
