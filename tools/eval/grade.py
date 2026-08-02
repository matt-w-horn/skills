#!/usr/bin/env python3
"""Grade produced artifacts against a rubric, one assertion at a time.

Each assertion gets its own judge call. Handing a judge ten criteria at once
invites it to form an overall impression and then distribute verdicts to match
it, so the rubric collapses into one overall impression. One criterion per call
costs more and answers the question that was asked.

The judge never learns which configuration produced an artifact. It cannot
prefer the skill's output if it cannot tell which output is the skill's.

    python3 tools/eval/grade.py --calibrate        # test the judge itself
    python3 tools/eval/grade.py --artifact FILE --eval audit-flawed-model

`--calibrate` is the gate. Every eval ships two reference artifacts: one that
should pass its rubric and one built to fail specific assertions. If the judge
cannot separate those, its verdicts on real runs mean nothing, and the sweep is
measuring the judge rather than the skill. So calibration runs first and its
failure is a stop, not a warning.
"""
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import corpus      # noqa: E402

JUDGE_TIMEOUT = 180

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
        "evidence": {"type": "string"},
    },
    "required": ["verdict", "evidence"],
}

JUDGE_PROMPT = """\
You are grading one document against one criterion. Answer only for this \
criterion; ignore every other quality the document may or may not have.

<criterion>
{assertion}
</criterion>
{sources}
<document>
{artifact}
</document>

Rules for your verdict:

- Pass only on concrete evidence you can point to in the document. Quote the \
part that satisfies the criterion.
- A label without the substance behind it is a fail. If the criterion asks for \
a range and the document has a heading called "Range" containing one number, \
that is a fail.
- The burden of proof is on the criterion. If you are unsure whether it is \
satisfied, it is not.
- Do not reward the document for being well written, confident, or thorough \
about something else. Those are not this criterion.
- Do not speculate about how the document was produced or by what.

Reply with your verdict and, in `evidence`, the quotation or the specific \
absence that decided it. Keep evidence under 300 characters.
"""


DOCUMENT_SUFFIXES = (".md", ".markdown", ".txt", ".rst")
WORKING_SUFFIXES = (".py", ".ipynb", ".html", ".json", ".csv", ".tsv", ".log")


def _artifact_rank(name):
    """Documents first, working files last, so truncation drops the right end.

    A skill that builds a workspace can leave 50KB of its own model code beside
    the deliverable. That code is how the answer was reached, not the answer,
    and the rubric grades outcomes; letting it consume the budget pushes the
    document the assertions are about past the truncation point.
    """
    lower = name.lower()
    if lower.endswith(DOCUMENT_SUFFIXES):
        return (0, name)
    if lower.endswith(WORKING_SUFFIXES):
        return (2, name)
    return (1, name)


def build_artifact(final_text, produced_files=None, limit=120_000):
    """The gradeable surface: what the user would have read, plus files made."""
    parts = []
    if final_text and final_text.strip():
        parts.append(f"=== response ===\n{final_text.strip()}")
    for name in sorted((produced_files or {}), key=_artifact_rank):
        body = produced_files[name]
        if body and body.strip():
            parts.append(f"=== file: {name} ===\n{body.strip()}")
    artifact = "\n\n".join(parts)
    if len(artifact) > limit:
        artifact = artifact[:limit] + "\n\n[truncated]"
    return artifact


def build_sources(fixture_dir, limit=60_000):
    """The material the person supplied, for assertions that check against it.

    Several assertions ask whether the document's figures match the person's
    own records, or whether it engages with a specific fact they provided. A
    judge holding only the document cannot answer those, and will fail them for
    lack of evidence, which reports a fact about the harness as though it were a
    fact about the skill.
    """
    if not fixture_dir or not os.path.isdir(fixture_dir):
        return ""
    parts = []
    for dirpath, dirs, files in os.walk(fixture_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in sorted(files):
            if name.startswith("."):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, fixture_dir)
            try:
                with open(path, encoding="utf-8") as fh:
                    body = fh.read().strip()
            except (OSError, UnicodeDecodeError):
                continue
            if body:
                parts.append(f"--- {rel} ---\n{body}")
    if not parts:
        return ""
    joined = "\n\n".join(parts)
    if len(joined) > limit:
        joined = joined[:limit] + "\n\n[truncated]"
    return ("\n<source_material>\nThe person supplied these files. They are "
            "context for judging the document, not part of it.\n\n"
            f"{joined}\n</source_material>\n")


def _parse(stdout):
    """Pull a verdict out of the CLI response, tolerating shape drift."""
    try:
        payload = json.loads(stdout)
    except (json.JSONDecodeError, ValueError):
        payload = None

    candidate = payload
    if isinstance(payload, dict):
        if isinstance(payload.get("result"), (dict, str)):
            candidate = payload["result"]
        if isinstance(candidate, str):
            try:
                candidate = json.loads(candidate)
            except (json.JSONDecodeError, ValueError):
                pass

    if isinstance(candidate, dict) and "verdict" in candidate:
        verdict = str(candidate["verdict"]).strip().lower()
        if verdict in ("pass", "fail"):
            return verdict == "pass", str(candidate.get("evidence", ""))[:400]

    # Last resort: find an embedded JSON object and parse it whole. Scraping a
    # bare `"verdict": "..."` with a regex would happily take one quoted inside
    # the evidence text and pair it with an unrelated evidence string, which
    # returns a confident wrong verdict rather than an honest failure to read.
    for start in (m.start() for m in re.finditer(r"\{", stdout)):
        for end in range(len(stdout), start, -1):
            if stdout[end - 1] != "}":
                continue
            try:
                obj = json.loads(stdout[start:end])
            except (json.JSONDecodeError, ValueError):
                continue
            if isinstance(obj, dict) and str(obj.get("verdict", "")).lower() in (
                    "pass", "fail"):
                return (str(obj["verdict"]).lower() == "pass",
                        str(obj.get("evidence", ""))[:400])
            break
    return None, f"unparseable judge response: {stdout[:200]}"


def judge(assertion_text, artifact, model=None, timeout=JUDGE_TIMEOUT, sources=""):
    """One verdict. Returns (passed_or_None, evidence)."""
    cmd = ["claude", "-p", "--output-format", "json",
           "--strict-mcp-config", "--no-session-persistence",
           "--setting-sources", "project",
           "--json-schema", json.dumps(VERDICT_SCHEMA)]
    if model:
        cmd += ["--model", model]

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    prompt = JUDGE_PROMPT.format(assertion=assertion_text, artifact=artifact,
                                 sources=sources)
    # On stdin, not argv. Artifact plus fixture can reach ~180KB, and Linux
    # caps a single argument at 128KiB, so passing it positionally fails with
    # E2BIG on exactly the machines a long sweep would be moved to.
    try:
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True,
            timeout=timeout, env=env, cwd=os.path.dirname(os.path.abspath(__file__)),
        )
    except subprocess.TimeoutExpired:
        return None, "judge timed out"
    except OSError as exc:
        return None, f"judge could not run: {exc}"
    if proc.returncode != 0:
        return None, f"judge exited {proc.returncode}: {proc.stderr[:200]}"
    return _parse(proc.stdout)


def grade_artifact(artifact, assertions, model=None, workers=4, sources=""):
    """Every assertion judged independently, in parallel."""
    results = [None] * len(assertions)

    def one(i):
        a = assertions[i]
        passed, evidence = judge(a["text"], artifact, model=model, sources=sources)
        return i, {"id": a["id"], "text": a["text"],
                   "passed": passed, "evidence": evidence}

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for i, res in pool.map(one, range(len(assertions))):
            results[i] = res

    decided = [r for r in results if r["passed"] is not None]
    return {
        "assertions": results,
        "passed": sum(1 for r in decided if r["passed"]),
        "failed": sum(1 for r in decided if not r["passed"]),
        "undecided": len(results) - len(decided),
        "pass_rate": (sum(1 for r in decided if r["passed"]) / len(decided)
                      if decided else None),
    }


def calibrate(evals, model=None, workers=4):
    """Does the judge distinguish the good reference from the bad one?

    Reports per-assertion agreement with the expectations the eval author
    committed to in advance. Disagreement means one of three things, and the
    report says which is which so the next step isn't a guess: the judge is
    unreliable, the reference artifact doesn't do what its author thought, or
    the assertion is not checkable as written.
    """
    report = []
    for ev in evals:
        entry = {"eval": ev["id"], "skill": ev["skill"], "references": {}}
        sources = build_sources(ev["fixture_dir"])
        for ref, key in (("good.md", "good_expect"), ("bad.md", "bad_expect")):
            path = os.path.join(ev["reference_dir"] or "", ref)
            if not os.path.isfile(path):
                entry["references"][ref] = {"error": "missing"}
                continue
            with open(path, encoding="utf-8") as fh:
                artifact = build_artifact(fh.read())

            graded = grade_artifact(artifact, ev["assertions"], model=model,
                                    workers=workers, sources=sources)
            rows, agree = [], 0
            for a, got in zip(ev["assertions"], graded["assertions"]):
                expected = a[key]
                matched = got["passed"] is not None and got["passed"] == expected
                agree += 1 if matched else 0
                rows.append({"id": a["id"], "expected": expected,
                             "got": got["passed"], "agrees": matched,
                             "evidence": got["evidence"]})
            entry["references"][ref] = {
                "agreement": f"{agree}/{len(ev['assertions'])}",
                "agreed": agree, "total": len(ev["assertions"]),
                "rows": rows,
            }
        report.append(entry)
    return report


def _print_calibration(report):
    ok = True
    for entry in report:
        print(f"\n{entry['eval']}  ({entry['skill']})")
        for ref, data in entry["references"].items():
            if "error" in data:
                print(f"  {ref}: {data['error']}")
                ok = False
                continue
            print(f"  {ref}: {data['agreement']} assertions agreed with expectation")
            for row in data["rows"]:
                if row["agrees"]:
                    continue
                ok = False
                got = {True: "pass", False: "fail", None: "undecided"}[row["got"]]
                want = "pass" if row["expected"] else "fail"
                print(f"    {row['id']}: expected {want}, judge said {got}")
                print(f"      {row['evidence'][:180]}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--calibrate", action="store_true",
                    help="grade the reference artifacts and check the judge")
    ap.add_argument("--eval", default=None, help="limit to one eval id")
    ap.add_argument("--artifact", default=None,
                    help="grade this file against --eval's rubric")
    ap.add_argument("--model", default=None, help="judge model")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=None, help="write JSON here")
    ap.add_argument("--skills-dir", default=corpus.SKILLS_DIR)
    args = ap.parse_args(argv)

    evals = corpus.load_execution_evals(args.skills_dir)
    if args.eval:
        evals = [e for e in evals if e["id"] == args.eval]
        if not evals:
            sys.exit(f"no execution eval named {args.eval!r}")

    if args.calibrate:
        report = calibrate(evals, model=args.model, workers=args.workers)
        ok = _print_calibration(report)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                json.dump(report, fh, indent=2)
            print(f"\nwrote {args.out}")
        print("\ncalibration: " + ("judge separates good from bad" if ok else
              "MISMATCHES ABOVE: do not trust grades until these are resolved"))
        return 0 if ok else 1

    if not args.artifact:
        sys.exit("give --artifact FILE (with --eval) or --calibrate")
    if len(evals) != 1:
        sys.exit("--artifact needs exactly one --eval")

    with open(args.artifact, encoding="utf-8") as fh:
        artifact = build_artifact(fh.read())
    graded = grade_artifact(artifact, evals[0]["assertions"],
                            model=args.model, workers=args.workers,
                            sources=build_sources(evals[0]["fixture_dir"]))
    print(json.dumps(graded, indent=2))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(graded, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
