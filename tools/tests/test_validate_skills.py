"""Tests for tools/validate_skills.py. Run from the tools directory:
    python3 -m unittest discover tests

Each test builds a throwaway skill tree and validates it, pinning the
behaviors that once false-positived (multi-line YAML descriptions, example
links in fenced blocks) or false-negatived (fenced commands, nested skills).
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import validate_skills as vs  # noqa: E402


def make_skill(root, name, skill_md, files=()):
    sdir = os.path.join(root, name)
    for rel, content in (("SKILL.md", skill_md),) + tuple(files):
        path = os.path.join(sdir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return sdir


class ValidateTree(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def test_clean_skill_passes(self):
        make_skill(self.root, "good",
                   "---\nname: good\ndescription: A skill.\n---\n"
                   "See `references/guide.md` and [g](references/guide.md).\n",
                   files=(("references/guide.md", "hello"),))
        errors, warnings = vs.validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_multiline_description_is_read(self):
        make_skill(self.root, "multi",
                   "---\nname: multi\ndescription:\n"
                   "  Folded across two lines,\n  still one value.\n---\nBody.\n")
        errors, _ = vs.validate(self.root)
        self.assertEqual(errors, [])

    def test_block_scalar_alone_is_empty(self):
        make_skill(self.root, "hollow",
                   "---\nname: hollow\ndescription: >\n---\nBody.\n")
        errors, _ = vs.validate(self.root)
        self.assertTrue(any("missing `description`" in e for e in errors))

    def test_example_link_in_fence_is_ignored(self):
        make_skill(self.root, "fenced",
                   "---\nname: fenced\ndescription: A skill.\n---\n"
                   "Example output:\n```\n[config](config.json)\n```\n")
        errors, _ = vs.validate(self.root)
        self.assertEqual(errors, [])

    def test_fenced_command_path_is_checked(self):
        make_skill(self.root, "cmd",
                   "---\nname: cmd\ndescription: A skill.\n---\n"
                   "Run it:\n```\npython3 scripts/model.py --config out/x.json\n```\n",
                   files=(("scripts/other.py", "pass\n"),))
        errors, warnings = vs.validate(self.root)
        # scripts/ is real so scripts/model.py must exist; out/ is not a dir
        # in the skill, so out/x.json is ignored as a runtime artifact.
        self.assertTrue(any("scripts/model.py" in e for e in errors))
        self.assertFalse(any("out/x.json" in e for e in errors))
        self.assertTrue(any("scripts/other.py" in w for w in warnings))

    def test_broken_prose_reference_fails(self):
        make_skill(self.root, "broken",
                   "---\nname: broken\ndescription: A skill.\n---\n"
                   "See `references/gone.md`.\n",
                   files=(("references/present.md", "x"),))
        errors, warnings = vs.validate(self.root)
        self.assertTrue(any("references/gone.md" in e for e in errors))
        self.assertTrue(any("references/present.md" in w for w in warnings))

    def test_nested_skill_is_discovered(self):
        make_skill(self.root, os.path.join("category", "deep"),
                   "---\nname: wrongname\ndescription: A skill.\n---\nBody.\n")
        errors, _ = vs.validate(self.root)
        self.assertTrue(any("`wrongname` != directory `deep`" in e for e in errors))

    def test_name_mismatch_and_no_skills(self):
        errors, _ = vs.validate(self.root)
        self.assertTrue(any("no skills found" in e for e in errors))

    def test_trailing_sentence_period_not_part_of_path(self):
        make_skill(self.root, "punct",
                   "---\nname: punct\ndescription: A skill.\n---\n"
                   "Run scripts/run.py.\n",
                   files=(("scripts/run.py", "pass\n"),))
        errors, _ = vs.validate(self.root)
        self.assertEqual(errors, [])

    def test_urls_are_not_paths(self):
        make_skill(self.root, "urls",
                   "---\nname: urls\ndescription: A skill.\n---\n"
                   "See https://example.com/references/x and "
                   "[site](https://example.com/a/b).\n",
                   files=(("references/real.md", "cited: `references/real.md`"),))
        errors, _ = vs.validate(self.root)
        self.assertEqual(errors, [])


class RealRepo(unittest.TestCase):
    def test_this_repo_validates(self):
        errors, warnings = vs.validate(vs.ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
