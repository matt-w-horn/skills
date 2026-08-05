"""Tests for the Claude Code plugin manifests. Run from the tools directory:
    python3 -m unittest discover tests

These encode distribution rules that are invisible locally: everything here
passes on a machine that never installs the plugin, and fails only for someone
downstream. The one that earned its place is the version pin. Claude Code
resolves a plugin's version from plugin.json, then the marketplace entry, then
the source commit SHA, and skips the update when the resolved version matches
what a user already has. A literal `"version": "1.0.0"` that nobody remembers
to bump therefore freezes every existing install, silently, no matter how many
commits land. Omitting the field entirely makes each commit its own version,
which is what an actively-developed repo wants.

    https://code.claude.com/docs/en/plugin-marketplaces#version-resolution-and-release-channels
"""

import json
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import validate_skills as vs  # noqa: E402

MARKETPLACE = os.path.join(vs.ROOT, ".claude-plugin", "marketplace.json")
PLUGIN = os.path.join(vs.ROOT, ".claude-plugin", "plugin.json")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Names reserved for Anthropic. A marketplace using one stops loading and is
# reported as registered from an untrusted source.
RESERVED = {
    "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official",
    "claude-plugins-community", "claude-community", "anthropic-marketplace",
    "anthropic-plugins", "agent-skills", "anthropic-agent-skills",
    "knowledge-work-plugins", "life-sciences", "claude-for-legal",
    "claude-for-financial-services", "financial-services-plugins",
    "first-party-plugins", "healthcare",
}

UNPINNED = (
    "pins the plugin: Claude Code compares the resolved version against what a "
    "user already has and skips the update when they match, so pushing commits "
    "without bumping this string reaches nobody. Omit it and each commit "
    "becomes its own version."
)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


class Marketplace(unittest.TestCase):
    def setUp(self):
        self.data = load(MARKETPLACE)
        self.entries = self.data.get("plugins", [])

    def test_required_fields(self):
        self.assertTrue(self.data.get("name"), "marketplace needs a `name`")
        self.assertTrue(self.data.get("owner", {}).get("name"), "owner needs a `name`")
        self.assertTrue(self.entries, "marketplace needs at least one plugin entry")

    def test_name_is_kebab_case_and_unreserved(self):
        name = self.data["name"]
        self.assertRegex(name, KEBAB, f"marketplace name `{name}` must be kebab-case")
        self.assertNotIn(name, RESERVED, f"`{name}` is reserved for Anthropic")

    def test_entries_are_well_formed(self):
        for entry in self.entries:
            name = entry.get("name", "")
            self.assertRegex(name, KEBAB, f"plugin name `{name}` must be kebab-case")
            source = entry.get("source")
            self.assertTrue(source, f"{name}: needs a `source`")
            if isinstance(source, str):
                self.assertTrue(
                    source.startswith("./"), f"{name}: relative source must start with ./"
                )
                self.assertTrue(
                    os.path.isdir(os.path.join(vs.ROOT, source)),
                    f"{name}: source `{source}` does not resolve",
                )

    def test_no_entry_pins_a_version(self):
        for entry in self.entries:
            self.assertNotIn("version", entry, f"{entry.get('name')}: `version` {UNPINNED}")

    def test_metadata_holds_only_documented_keys(self):
        # `description` and `version` are top-level fields; only `pluginRoot`
        # is documented under `metadata`, so anything else there is ignored.
        for key in self.data.get("metadata", {}):
            self.assertEqual(key, "pluginRoot", f"metadata.{key} is not a documented field")


class Plugin(unittest.TestCase):
    def setUp(self):
        self.data = load(PLUGIN)

    def test_name_matches_the_marketplace_entry(self):
        names = [e.get("name") for e in load(MARKETPLACE).get("plugins", [])]
        self.assertIn(
            self.data.get("name"),
            names,
            "plugin.json `name` must match a marketplace entry; users install by that name",
        )

    def test_does_not_pin_a_version(self):
        # plugin.json wins over the marketplace entry without warning, so a
        # stale value here masks anything set there.
        self.assertNotIn("version", self.data, f"plugin.json `version` {UNPINNED}")

    def test_license_is_backed_by_a_license_file(self):
        if self.data.get("license"):
            self.assertTrue(os.path.exists(os.path.join(vs.ROOT, "LICENSE")))

    def test_skills_are_auto_discovered(self):
        # No `skills` path is declared, so Claude Code discovers skills/ in the
        # plugin root. That only works if the skills actually live there.
        self.assertNotIn("skills", self.data)
        self.assertTrue(os.path.isdir(os.path.join(vs.ROOT, "skills")))


if __name__ == "__main__":
    unittest.main()
