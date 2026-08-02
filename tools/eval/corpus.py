#!/usr/bin/env python3
"""Load and validate the eval corpus.

Two families live side by side, one per question the suite answers:

  trigger    Does Claude reach for this skill when it should, and leave it
             alone when it shouldn't? One `evals/trigger.json` per skill, each
             query carrying expectations for *every* skill so the overlap
             between them is measured rather than assumed away.

  execution  Given the skill fires, is the deliverable worth having? One
             directory per eval under `evals/execution/`, holding the user's
             prompt, the files they "brought", a rubric of binary assertions,
             and reference artifacts that prove the rubric can tell good from
             bad.

This module only reads and shape-checks. Quality judgments (balance, blinding,
near-miss hardness) belong to lint_evals.py, which is the part CI gates.
"""
import json
import os

SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "skills",
)

SPLITS = ("train", "validation", "sealed")
SHAPES = ("seeded-defect", "finish-the-job")
EITHER = "either"


class CorpusError(Exception):
    """A corpus file is malformed. Distinct from a corpus that is merely poor."""


def _read_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        raise CorpusError(f"{path}: invalid JSON ({exc})") from exc
    except OSError as exc:
        raise CorpusError(f"{path}: cannot read ({exc})") from exc


def skill_names(skills_dir=SKILLS_DIR):
    """Every skill directory name, sorted. The universe `expect` maps cover."""
    if not os.path.isdir(skills_dir):
        return []
    return sorted(
        d for d in os.listdir(skills_dir)
        if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md"))
    )


def _require(cond, msg):
    if not cond:
        raise CorpusError(msg)


def load_trigger_file(path, known_skills):
    """Parse one `trigger.json`, returning its query list with `source` stamped.

    Every query is checked for the fields the runner and scorer depend on. A
    missing or misspelled key here would otherwise surface much later as a
    silently skipped query, which is the failure mode this suite exists to
    avoid elsewhere.
    """
    data = _read_json(path)
    _require(isinstance(data, dict), f"{path}: top level must be an object")
    _require(data.get("version") == 1, f"{path}: expected version 1")

    skill = data.get("skill")
    _require(skill in known_skills,
             f"{path}: `skill` is {skill!r}, not one of {known_skills}")

    queries = data.get("queries")
    _require(isinstance(queries, list) and queries,
             f"{path}: `queries` must be a non-empty list")

    out = []
    for i, q in enumerate(queries):
        where = f"{path}[{i}]"
        _require(isinstance(q, dict), f"{where}: must be an object")
        for key in ("id", "query", "expect", "why", "split"):
            _require(key in q, f"{where}: missing `{key}`")
        _require(isinstance(q["id"], str) and q["id"].strip(),
                 f"{where}: `id` must be a non-empty string")
        _require(isinstance(q["query"], str) and q["query"].strip(),
                 f"{q['id']}: `query` must be a non-empty string")
        _require(isinstance(q["why"], str) and q["why"].strip(),
                 f"{q['id']}: `why` must explain the label")
        _require(q["split"] in SPLITS,
                 f"{q['id']}: `split` is {q['split']!r}, expected one of {SPLITS}")

        expect = q["expect"]
        _require(isinstance(expect, dict), f"{q['id']}: `expect` must be an object")
        _require(set(expect) == set(known_skills),
                 f"{q['id']}: `expect` covers {sorted(expect)}, expected {known_skills}")
        for name, val in expect.items():
            _require(val is True or val is False or val == EITHER,
                     f"{q['id']}: expect[{name}] is {val!r}, expected true/false/'either'")

        out.append({**q, "source": path, "owner": skill})
    return out


def load_trigger_corpus(skills_dir=SKILLS_DIR):
    """Merge every skill's trigger file into one corpus, ids checked unique."""
    known = skill_names(skills_dir)
    _require(known, f"no skills found under {skills_dir}")

    queries, seen = [], {}
    for skill in known:
        path = os.path.join(skills_dir, skill, "evals", "trigger.json")
        if not os.path.exists(path):
            continue
        for q in load_trigger_file(path, known):
            if q["id"] in seen:
                raise CorpusError(
                    f"duplicate query id {q['id']!r} in {q['source']} "
                    f"and {seen[q['id']]}"
                )
            seen[q["id"]] = q["source"]
            queries.append(q)
    _require(queries, f"no trigger queries found under {skills_dir}/*/evals/")
    return queries


def load_execution_eval(eval_dir, known_skills):
    """Parse one execution eval directory into a dict the runner can drive."""
    meta = _read_json(os.path.join(eval_dir, "eval.json"))
    name = os.path.basename(eval_dir)
    _require(meta.get("version") == 1, f"{name}: expected version 1")
    _require(meta.get("id") == name,
             f"{name}: `id` is {meta.get('id')!r}, must match the directory name")
    _require(meta.get("skill") in known_skills,
             f"{name}: `skill` is {meta.get('skill')!r}, not one of {known_skills}")
    _require(meta.get("shape") in SHAPES,
             f"{name}: `shape` is {meta.get('shape')!r}, expected one of {SHAPES}")

    prompt_path = os.path.join(eval_dir, meta.get("prompt_file", "prompt.md"))
    _require(os.path.isfile(prompt_path), f"{name}: missing {meta.get('prompt_file')}")
    with open(prompt_path, encoding="utf-8") as fh:
        prompt = fh.read().strip()
    _require(prompt, f"{name}: prompt file is empty")

    rubric = _read_json(os.path.join(eval_dir, "rubric.json"))
    _require(rubric.get("version") == 1, f"{name}/rubric.json: expected version 1")
    assertions = rubric.get("assertions")
    _require(isinstance(assertions, list) and assertions,
             f"{name}/rubric.json: `assertions` must be a non-empty list")

    ids = set()
    for i, a in enumerate(assertions):
        where = f"{name}/rubric.json[{i}]"
        _require(isinstance(a, dict), f"{where}: must be an object")
        for key in ("id", "text", "good_expect", "bad_expect"):
            _require(key in a, f"{where}: missing `{key}`")
        _require(a["id"] not in ids, f"{where}: duplicate assertion id {a['id']!r}")
        ids.add(a["id"])
        _require(isinstance(a["text"], str) and a["text"].strip(),
                 f"{where}: `text` must be a non-empty string")
        for key in ("good_expect", "bad_expect"):
            _require(isinstance(a[key], bool), f"{where}: `{key}` must be true or false")

    defects = meta.get("planted_defects", [])
    _require(isinstance(defects, list), f"{name}: `planted_defects` must be a list")
    for i, d in enumerate(defects):
        where = f"{name}.planted_defects[{i}]"
        _require(isinstance(d, dict), f"{where}: must be an object")
        for key in ("id", "summary", "assertion"):
            _require(key in d, f"{where}: missing `{key}`")
        _require(d["assertion"] in ids,
                 f"{where}: assertion {d['assertion']!r} is not in the rubric")

    fixture_dir = os.path.join(eval_dir, meta.get("fixture_dir", "fixture"))
    reference_dir = os.path.join(eval_dir, "reference")

    return {
        "id": name,
        "dir": eval_dir,
        "skill": meta["skill"],
        "shape": meta["shape"],
        "prompt": prompt,
        "fixture_dir": fixture_dir if os.path.isdir(fixture_dir) else None,
        "reference_dir": reference_dir if os.path.isdir(reference_dir) else None,
        "assertions": assertions,
        "planted_defects": defects,
    }


def load_execution_evals(skills_dir=SKILLS_DIR):
    """Every execution eval across every skill, sorted by id."""
    known = skill_names(skills_dir)
    _require(known, f"no skills found under {skills_dir}")

    evals, seen = [], {}
    for skill in known:
        root = os.path.join(skills_dir, skill, "evals", "execution")
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            eval_dir = os.path.join(root, name)
            if not os.path.isfile(os.path.join(eval_dir, "eval.json")):
                continue
            ev = load_execution_eval(eval_dir, known)
            if ev["id"] in seen:
                raise CorpusError(
                    f"duplicate execution eval id {ev['id']!r} in {eval_dir} "
                    f"and {seen[ev['id']]}"
                )
            seen[ev["id"]] = eval_dir
            evals.append(ev)
    return sorted(evals, key=lambda e: e["id"])


def classify(query, skills):
    """The role a query plays, derived from `expect` rather than declared.

    Deriving it keeps one fact in one place: an author who edits `expect` can't
    leave a stale label behind, because there is no label to go stale.
    """
    expect = query["expect"]
    if any(v == EITHER for v in expect.values()):
        return "either"
    owner = query["owner"]
    if expect.get(owner) is True:
        return "positive"
    if any(expect.get(s) is True for s in skills if s != owner):
        return "cross"
    return "near-miss"
