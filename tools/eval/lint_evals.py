#!/usr/bin/env python3
"""Quality gate for the eval corpus. Runs in CI; needs no network and no CLI.

An eval corpus is bulk-generated content, and bulk-generated content fails in
classes rather than one-offs. So each rule below is a detector for one class of
defect, run across the whole corpus rather than spot-checked, and each one has a
test that feeds it a corpus built to trip it. A detector nobody has watched
fail cannot be told apart from one that returns green unconditionally.

The rules encode what the published methodology says makes a trigger set worth
running: balance between the classes, negatives that are near-misses rather than
obvious irrelevancies, queries substantive enough that consulting a skill is
plausible at all, and a train/validation/sealed partition that survives the
corpus being edited.

The leakage rule does work no reviewer reliably does: it checks that no query
or assertion echoes a phrase found in a skill body but not in its description.
It cannot prove an author never looked, since paraphrase evades it. What it
catches is the failure blinding exists to prevent, an eval written by restating
the skill's own wording, and that much is a property of the artifact rather
than of somebody's intentions.

    python3 tools/eval/lint_evals.py [--skills-dir DIR] [--strict]

Exits non-zero on any error. `--strict` promotes warnings to errors.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import corpus            # noqa: E402
import validate_skills   # noqa: E402  (reused, not reimplemented)

NGRAM = 5
DUPLICATE_JACCARD = 0.80
MIN_QUERY_WORDS = 12
MIN_PER_CLASS = 8
MAX_CLASS_SKEW = 3
MAX_EITHER = 8
MIN_NEAR_MISS_OVERLAP = 3

# Judgment words smuggled into an assertion make two careful readers disagree,
# which is the one property an assertion may not have.
VAGUE = {
    "good", "bad", "appropriate", "comprehensive", "thorough", "clear",
    "insightful", "reasonable", "proper", "adequate", "quality", "robust",
    "meaningful", "useful", "effective", "well-written", "sensible",
}

STOPWORDS = {
    "a", "the", "and", "or", "but", "if", "of", "to", "in", "on", "for",
    "with", "at", "by", "from", "is", "are", "was", "were", "be", "been", "it",
    "this", "that", "these", "those", "as", "an", "not", "no", "do", "does",
    "did", "so", "than", "then", "there", "their", "they", "them", "you",
    "your", "i", "me", "my", "we", "our", "he", "she", "his", "her", "what",
    "when", "which", "who", "how", "why", "can", "could", "would", "should",
    "will", "have", "has", "had", "s", "t", "m", "re", "ve", "ll", "d", "up",
    "out", "about", "into", "over", "more", "most", "some", "any", "all",
    "one", "two", "its", "also", "just", "like", "get", "got",
}

# A path or a filename is unambiguous: the model will go looking, find nothing,
# and ask a question instead of acting.
FILE_HINT = re.compile(
    r"(~/|\.{1,2}/|/Users/|/home/|[A-Za-z]:\\)"
    r"|\b[\w -]+\.(csv|xlsx?|json|md|txt|pdf|numbers|ods|tsv|ya?ml)\b"
    r"|\battach(ed|ment)\b",
    re.I,
)

# An artifact named without a path is a judgment call. "I have kept a
# spreadsheet for years" is background and fine; "check my spreadsheet" needs a
# file that will not be there. Only a person can tell those apart, so this
# warns rather than fails.
ARTIFACT_HINT = re.compile(
    r"\b(spreadsheet|workbook|export|screenshot|the document|the file)\b", re.I)
ARTIFACT_DEMAND = re.compile(
    r"\b(check|review|look at|open|read|fix|audit|see|use|attached to)\b", re.I)

SYNTHETIC = re.compile(r"synthetic|fictional|not a real (person|company)", re.I)


def normalize(text):
    return [w for w in re.findall(r"[a-z0-9']+", text.lower()) if w]


def ngrams(words, n=NGRAM):
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def distinctive(gram):
    """Enough non-stopword content to be a real echo rather than English."""
    return sum(1 for w in gram if w not in STOPWORDS) >= 3


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def skill_texts(skills_dir, skill):
    """(description, body) for one skill.

    `body` is everything an author was told not to read: the SKILL.md after its
    frontmatter, plus every reference file. `description` is what they were
    given. Anything echoed from body-but-not-description is leakage.
    """
    skill_md = os.path.join(skills_dir, skill, "SKILL.md")
    text = read(skill_md)
    description, body = "", text

    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm, body = text[3:end], text[end + 4:]
            match = re.search(r"^description:\s*(.*)$", fm, re.M)
            if match:
                description = match.group(1).strip()
                rest = fm[match.end():]
                for line in rest.splitlines():
                    if re.match(r"^[A-Za-z0-9_-]+:", line):
                        break
                    description += " " + line.strip()

    refs = os.path.join(skills_dir, skill, "references")
    if os.path.isdir(refs):
        for name in sorted(os.listdir(refs)):
            if name.endswith(".md"):
                body += "\n" + read(os.path.join(refs, name))
    return description.strip(), body


def eval_markdown_files(skills_dir):
    """Every Markdown file under any skill's evals/ tree."""
    out = []
    for skill in corpus.skill_names(skills_dir):
        root = os.path.join(skills_dir, skill, "evals")
        for dp, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in sorted(files):
                if f.endswith(".md"):
                    out.append((skill, os.path.join(dp, f)))
    return out


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, rule, msg):
        self.errors.append(f"[{rule}] {msg}")

    def warn(self, rule, msg):
        self.warnings.append(f"[{rule}] {msg}")


# --------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------

def rule_balance(queries, skills, rep):
    """Both classes present in force. One-sided evals drive one-sided fixes."""
    either_total = 0
    for skill in skills:
        owned = [q for q in queries if q["owner"] == skill]
        if not owned:
            rep.error("balance", f"{skill}: no trigger queries at all")
            continue
        graded = [q for q in owned if q["split"] != "sealed"]
        pos = [q for q in graded if corpus.classify(q, skills) == "positive"]
        neg = [q for q in graded
               if corpus.classify(q, skills) in ("near-miss", "cross")]
        either_total += sum(
            1 for q in owned if corpus.classify(q, skills) == "either")

        if len(pos) < MIN_PER_CLASS:
            rep.error("balance",
                      f"{skill}: {len(pos)} should-trigger queries, need >= {MIN_PER_CLASS}")
        if len(neg) < MIN_PER_CLASS:
            rep.error("balance",
                      f"{skill}: {len(neg)} should-not-trigger queries, need >= {MIN_PER_CLASS}")
        if abs(len(pos) - len(neg)) > MAX_CLASS_SKEW:
            rep.error("balance",
                      f"{skill}: {len(pos)} positive vs {len(neg)} negative; "
                      f"skew above {MAX_CLASS_SKEW}")
        if not any(corpus.classify(q, skills) == "cross" for q in owned):
            rep.warn("balance",
                     f"{skill}: no cross-skill disambiguation queries; the "
                     f"overlap between skills goes unmeasured")

    if either_total > MAX_EITHER:
        rep.error("balance",
                  f"{either_total} 'either' queries, cap is {MAX_EITHER}; "
                  f"ambiguity is being used to avoid hard calls")


def rule_splits(queries, skills, rep):
    """A partition that survives editing, and a sealed set that stays sealed."""
    for skill in skills:
        owned = [q for q in queries if q["owner"] == skill]
        if not owned:
            continue
        counts = {s: sum(1 for q in owned if q["split"] == s)
                  for s in corpus.SPLITS}
        if counts["train"] == 0 or counts["validation"] == 0:
            rep.error("splits",
                      f"{skill}: needs both train and validation ({counts})")
            continue
        if counts["sealed"] == 0:
            rep.warn("splits",
                     f"{skill}: no sealed queries; nothing is held back for a "
                     f"final generalization check")
        for split in ("train", "validation"):
            in_split = [q for q in owned if q["split"] == split]
            pos = sum(1 for q in in_split
                      if corpus.classify(q, skills) == "positive")
            if in_split and (pos == 0 or pos == len(in_split)):
                rep.error("splits",
                          f"{skill}/{split}: all {len(in_split)} queries are the "
                          f"same class; the split is not stratified")


def rule_duplicates(queries, rep):
    """Near-identical queries inflate a score without adding coverage."""
    grams = {q["id"]: set(normalize(q["query"])) for q in queries}
    ids = sorted(grams)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            score = jaccard(grams[a], grams[b])
            if score >= DUPLICATE_JACCARD:
                rep.error("duplicates",
                          f"{a} and {b} overlap {score:.0%}, near-duplicates")


def rule_substance(queries, rep):
    """Trivial requests never trigger a skill, so they measure nothing."""
    for q in queries:
        words = normalize(q["query"])
        if len(words) < MIN_QUERY_WORDS:
            rep.error("substance",
                      f"{q['id']}: {len(words)} words, too slight to require a "
                      f"skill, so a no-trigger tells you nothing")


def rule_self_contained(queries, rep):
    """Runs happen in an empty directory; a query needing a file will misfire.

    The failure is nasty because it is invisible: the model hunts for a file
    that was never there, asks a question instead of acting, and the row reads
    as a description problem.
    """
    for q in queries:
        hit = FILE_HINT.search(q["query"])
        if hit:
            rep.error("self-contained",
                      f"{q['id']}: refers to a file ({hit.group(0)!r}) that will "
                      f"not exist in the scratch directory")
            continue
        named = ARTIFACT_HINT.search(q["query"])
        if named and ARTIFACT_DEMAND.search(q["query"]):
            rep.warn("self-contained",
                     f"{q['id']}: mentions a {named.group(0)!r} the run cannot "
                     f"open; check the request still stands without it")


def rule_near_miss(queries, skills, descriptions, rep):
    """Negatives must be near-misses; an unrelated negative tests nothing."""
    for q in queries:
        if corpus.classify(q, skills) != "near-miss":
            continue
        desc = set(normalize(descriptions.get(q["owner"], "")))
        words = set(normalize(q["query"]))
        shared = {w for w in words & desc if w not in STOPWORDS}
        if len(shared) < MIN_NEAR_MISS_OVERLAP:
            rep.warn("near-miss",
                     f"{q['id']}: shares only {len(shared)} content words with "
                     f"the {q['owner']} description; likely too easy a negative")


def rule_leakage(items, descriptions, bodies, rep):
    """Authored blind, or paraphrased from the skill? This is the check.

    `items` are (label, owner, text) triples covering both queries and
    assertions. A phrase present in the skill body but absent from the
    description could not have come from the material a blind author was given.
    """
    body_grams, desc_grams = {}, {}
    for skill, body in bodies.items():
        body_grams[skill] = ngrams(normalize(body))
        desc_grams[skill] = ngrams(normalize(descriptions.get(skill, "")))

    # Authors were given every skill's description, so a phrase from any of
    # them is fair. They were given no skill's body, so a phrase from any body
    # is a problem regardless of which skill the item belongs to. Checking only
    # the owner's body left cross-skill queries unchecked, and those are exactly
    # the ones an author would write with the other skill in view.
    allowed = set().union(*desc_grams.values()) if desc_grams else set()

    for label, _owner, text in items:
        suspect = ngrams(normalize(text))
        for skill, grams in body_grams.items():
            for gram in sorted(suspect & grams):
                if gram in allowed or not distinctive(gram):
                    continue
                rep.error("leakage",
                          f"{label}: echoes the {skill} skill body: "
                          f"{' '.join(gram)!r}")


def rule_assertions(evals, rep):
    """Binary, single-criterion, and free of words that invite disagreement."""
    for ev in evals:
        for a in ev["assertions"]:
            tag = f"{ev['id']}/{a['id']}"
            words = set(normalize(a["text"]))
            for bad in sorted(words & VAGUE):
                rep.error("assertions",
                          f"{tag}: contains judgment word {bad!r}; two readers "
                          f"will not agree")
            if len(normalize(a["text"])) > 45:
                rep.warn("assertions", f"{tag}: long enough to hide a second criterion")
            if re.search(r"\band\b", a["text"], re.I) and re.search(
                    r"\band\b.*\b(includes?|states?|shows?|names?|reports?|"
                    r"identifies|gives?|lists?)\b", a["text"], re.I):
                rep.warn("assertions",
                         f"{tag}: reads as two checkable claims joined by 'and'; "
                         f"split it so a half-pass cannot score as a pass")


def rule_calibration(evals, rep):
    """A rubric nobody has tried to fail is not an instrument."""
    for ev in evals:
        if not any(a["bad_expect"] is False for a in ev["assertions"]):
            rep.error("calibration",
                      f"{ev['id']}: no assertion is expected to fail on the bad "
                      f"reference, so the rubric has never been falsified")
        if not any(a["good_expect"] is True for a in ev["assertions"]):
            rep.error("calibration",
                      f"{ev['id']}: no assertion is expected to pass on the good "
                      f"reference")
        ref = ev["reference_dir"]
        for name in ("good.md", "bad.md"):
            if not ref or not os.path.isfile(os.path.join(ref, name)):
                rep.error("calibration", f"{ev['id']}: missing reference/{name}")

        caught = {d["assertion"] for d in ev["planted_defects"]}
        for d in ev["planted_defects"]:
            match = next(a for a in ev["assertions"] if a["id"] == d["assertion"])
            if match["bad_expect"] is not False:
                rep.warn("calibration",
                         f"{ev['id']}/{d['id']}: the assertion meant to catch this "
                         f"defect is not expected to fail on the bad reference")
        if ev["shape"] == "seeded-defect" and not caught:
            rep.error("calibration",
                      f"{ev['id']}: shape is seeded-defect but nothing is planted")


def rule_fixtures(skills_dir, evals, rep):
    """Fixtures must not trip the repo validator or masquerade as real data."""
    for skill in corpus.skill_names(skills_dir):
        root = os.path.join(skills_dir, skill, "evals")
        for dp, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            if "SKILL.md" in files:
                rep.error("fixtures",
                          f"{os.path.relpath(dp, skills_dir)}: contains SKILL.md; "
                          f"the repo validator would treat this fixture as a skill")

    # Ask the repo validator itself what it would claim about these files,
    # rather than reimplementing its rules here. It also checks Markdown links,
    # gates on any real subdirectory rather than a fixed list, strips a
    # sentence-ending dot, and resolves relative to the file as well as the
    # skill root. Every one of those was a way for a mirror to disagree with
    # the thing it mirrors, and a linter that passes what CI fails is worse
    # than no linter.
    for skill, path in eval_markdown_files(skills_dir):
        rel = os.path.relpath(path, skills_dir)
        skill_root = os.path.join(skills_dir, skill)
        subdirs = {d for d in os.listdir(skill_root)
                   if os.path.isdir(os.path.join(skill_root, d))}
        for token in validate_skills.referenced_paths(path, subdirs):
            candidates = [
                os.path.normpath(os.path.join(skill_root, token)),
                os.path.normpath(os.path.join(os.path.dirname(path), token)),
            ]
            if not any(os.path.exists(c) for c in candidates):
                rep.error("fixtures",
                          f"{rel}: writes {token!r}, which the repo validator "
                          f"reads as a claim that the file exists and will "
                          f"report as a broken reference")

    for ev in evals:
        if not ev["fixture_dir"]:
            continue
        for dp, _dirs, files in os.walk(ev["fixture_dir"]):
            for f in sorted(files):
                path = os.path.join(dp, f)
                try:
                    text = read(path)
                except (OSError, UnicodeDecodeError):
                    continue
                if not SYNTHETIC.search(text):
                    rep.error("fixtures",
                              f"{ev['id']}/{f}: no marker saying this is synthetic "
                              f"data; invented personal records should say so")


# --------------------------------------------------------------------------

def lint(skills_dir=corpus.SKILLS_DIR):
    rep = Report()
    skills = corpus.skill_names(skills_dir)
    if not skills:
        rep.error("schema", f"no skills found under {skills_dir}")
        return rep

    descriptions, bodies = {}, {}
    for skill in skills:
        try:
            descriptions[skill], bodies[skill] = skill_texts(skills_dir, skill)
        except OSError as exc:
            rep.error("schema", f"{skill}: cannot read SKILL.md ({exc})")

    try:
        queries = corpus.load_trigger_corpus(skills_dir)
    except corpus.CorpusError as exc:
        rep.error("schema", str(exc))
        queries = []

    try:
        evals = corpus.load_execution_evals(skills_dir)
    except corpus.CorpusError as exc:
        rep.error("schema", str(exc))
        evals = []

    if queries:
        rule_balance(queries, skills, rep)
        rule_splits(queries, skills, rep)
        rule_duplicates(queries, rep)
        rule_substance(queries, rep)
        rule_self_contained(queries, rep)
        rule_near_miss(queries, skills, descriptions, rep)

    if evals:
        rule_assertions(evals, rep)
        rule_calibration(evals, rep)
    rule_fixtures(skills_dir, evals, rep)

    items = [(q["id"], q["owner"], q["query"]) for q in queries]
    items += [(f"{ev['id']}/{a['id']}", ev["skill"], a["text"])
              for ev in evals for a in ev["assertions"]]
    if items and bodies:
        rule_leakage(items, descriptions, bodies, rep)

    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--skills-dir", default=corpus.SKILLS_DIR)
    ap.add_argument("--strict", action="store_true",
                    help="treat warnings as errors")
    args = ap.parse_args(argv)

    rep = lint(args.skills_dir)
    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"ERROR {e}")

    failed = len(rep.errors) + (len(rep.warnings) if args.strict else 0)
    print(f"\neval corpus: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
