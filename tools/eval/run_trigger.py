#!/usr/bin/env python3
"""Run the trigger sweep: does the right skill fire for each query?

Every query runs with both skills loaded, several times, because model
behaviour is not deterministic and a single sample can't tell a marginal case
from a broken one. The score for a query is its *trigger rate*, the fraction
of runs in which a given skill fired, and a query passes when that rate lands
on the right side of a threshold.

Results are written per run, so an interrupted sweep resumes instead of
restarting, and so the raw evidence for any number survives the number.

    python3 tools/eval/run_trigger.py --split train
    python3 tools/eval/run_trigger.py --split validation --runs 3
    python3 tools/eval/run_trigger.py --split sealed        # once, deliberately

The sealed split is guarded. It exists to answer one question honestly: does
the description generalize beyond what it was tuned against? That answer is
only worth having the first time it is asked. Running it again after a
change turns it into another training set, so a second run needs --force and
says so in the record.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import corpus      # noqa: E402
import harness     # noqa: E402

DEFAULT_RESULTS = os.path.join(harness.REPO_ROOT, "tools", "eval", "results")
THRESHOLD = 0.5
SEALED_MARKER = "sealed-runs.json"


def result_path(results_dir, query_id, index):
    return os.path.join(results_dir, "runs", f"{query_id}__{index}.json")


def fingerprint(query, args):
    """What a cached run was measured under.

    The whole point of this tool is to tell you whether a description change
    helped. Without a fingerprint, re-running after such a change replays the
    old descriptions' results while the summary reports the new settings, and
    a cached row looks exactly like a fresh one in the log.
    """
    h = hashlib.sha256()
    h.update(query["query"].encode("utf-8"))
    h.update(repr(sorted(query["expect"].items())).encode("utf-8"))
    for skill in sorted(corpus.skill_names()):
        skill_md = os.path.join(corpus.SKILLS_DIR, skill, "SKILL.md")
        if os.path.isfile(skill_md):
            with open(skill_md, "rb") as fh:
                h.update(fh.read())
    for setting in (args.model, args.timeout, args.max_tool_calls,
                    args.run_to_completion):
        h.update(repr(setting).encode("utf-8"))
    return h.hexdigest()[:16]


def execute(query, index, skills, results_dir, args):
    """One run of one query, cached on disk so a resumed sweep skips it."""
    path = result_path(results_dir, query["id"], index)
    if os.path.exists(path) and not args.overwrite:
        cached = harness.read_json(path)
        if cached is not None and cached.get("fingerprint") == fingerprint(query, args):
            return cached
        # Either corrupt, or measured against different inputs. Re-run.

    cwd = os.path.join(results_dir, "scratch", f"{query['id']}__{index}")
    harness.prepare_cwd(cwd)
    stream = os.path.join(results_dir, "streams", f"{query['id']}__{index}.jsonl")
    os.makedirs(os.path.dirname(stream), exist_ok=True)

    record = harness.run_once(
        prompt=query["query"],
        configuration=harness.WITH_SKILL,
        skills=skills,
        cwd=cwd,
        stream_path=stream,
        timeout=args.timeout,
        max_tool_calls=args.max_tool_calls,
        model=args.model,
        run_to_completion=args.run_to_completion,
    )
    record.update({"query_id": query["id"], "index": index,
                   "split": query["split"], "owner": query["owner"],
                   "fingerprint": fingerprint(query, args)})
    record["void"] = harness.void_reason(record, skills)

    harness.write_json(path, record)
    return record


def score(queries, records, skills, threshold=THRESHOLD):
    """Per-query trigger rates and pass/fail, plus a routing confusion matrix.

    Runs that errored are excluded from the denominator rather than counted as
    non-triggers, for the reason given on the outcome constants in harness.py.
    """
    by_query = {}
    for rec in records:
        by_query.setdefault(rec["query_id"], []).append(rec)

    rows, matrix = [], {}
    for q in queries:
        runs = by_query.get(q["id"], [])
        usable = [r for r in runs if not r["void"]]
        excluded = [r for r in runs if r["void"]]

        rates, verdicts = {}, {}
        for skill in skills:
            fired = sum(1 for r in usable if skill in r["skills_invoked"])
            rate = fired / len(usable) if usable else None
            rates[skill] = rate
            want = q["expect"][skill]
            if rate is None:
                verdicts[skill] = None
            elif want == corpus.EITHER:
                verdicts[skill] = None          # no constraint; see below
            elif rate == threshold:
                # Exactly on the line decides nothing, and voiding a run makes
                # even denominators routine, so this is reachable. Treating it
                # as a pass for positives and a fail for negatives would let
                # the same evidence mean opposite things depending on the
                # label. One firing in two says only that the row needs more
                # runs.
                verdicts[skill] = None
            elif want is True:
                verdicts[skill] = rate > threshold
            else:
                verdicts[skill] = rate < threshold

        # `either` marks a skill whose firing is defensible but not required,
        # so it constrains nothing on its own. Every definite expectation still
        # has to hold. When a query is `either` all the way down there is no
        # definite expectation left, and the rule becomes "something sensible
        # must fire", which stops the label from excusing a total miss.
        required = [s for s in skills if q["expect"][s] != corpus.EITHER]
        permitted = [s for s in skills if q["expect"][s] == corpus.EITHER]

        if required and any(verdicts[s] is None for s in required):
            # A definite expectation that could not be decided leaves the query
            # undecided. Dropping it and scoring on the others would let a row
            # pass on its incidental expectation while the one it was written
            # to test never got an answer.
            passed = None
        elif required:
            passed = all(verdicts[s] for s in required)
        elif permitted:
            passed = any((rates[s] or 0) > threshold for s in permitted)
        else:
            passed = False

        # Normally the scanner stops at the first skill it sees, so this is a
        # matrix over which skill routed first: the decision worth measuring,
        # since the user gets the winner rather than a ranking. Under
        # --run-to-completion the scan continues, so a "both" cell can appear.
        for rec in usable:
            fired = tuple(sorted(s for s in skills if s in rec["skills_invoked"]))
            key = (",".join(fired) or "none",
                   ",".join(f"{s}={q['expect'][s]}" for s in skills))
            matrix[key] = matrix.get(key, 0) + 1

        rows.append({
            "id": q["id"], "owner": q["owner"], "split": q["split"],
            "class": corpus.classify(q, skills), "expect": q["expect"],
            "rates": rates, "passed": passed if usable else None,
            "runs": len(usable), "excluded": len(excluded),
            "void_reasons": sorted({r["void"] for r in excluded if r["void"]}),
            "query": q["query"],
        })

    graded = [r for r in rows if r["passed"] is not None]
    return {
        "threshold": threshold,
        "queries": len(rows),
        "graded": len(graded),
        "passed": sum(1 for r in graded if r["passed"]),
        "failed": sum(1 for r in graded if not r["passed"]),
        "ungraded": len(rows) - len(graded),
        "rows": rows,
        "confusion": [{"fired": k[0], "expected": k[1], "count": v}
                      for k, v in sorted(matrix.items())],
    }


def check_sealed(results_dir, args):
    """Refuse to spend the one-shot split twice, wherever it is about to run.

    Guarding only `--split sealed` would leave `--split all` free to spend the
    holdout without recording it, which is the same loss by a different route.
    """
    marker = os.path.join(results_dir, SEALED_MARKER)
    prior = []
    if os.path.exists(marker):
        prior = harness.read_json(marker) or []
    if prior and not args.force:
        when = prior[-1].get("finished", "previously")
        sys.exit(
            f"The sealed split was already run ({when}). Running it again after "
            f"a change makes it a training set, and the generalization check it "
            f"exists for is gone. Pass --force if you mean to, and know that the "
            f"second number is worth less than the first."
        )
    return marker, prior


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--split", default="train",
                    choices=[*corpus.SPLITS, "graded", "all"],
                    help="'graded' means train+validation")
    ap.add_argument("--runs", type=int, default=3,
                    help="runs per query; the trigger rate needs more than one")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=150)
    ap.add_argument("--max-tool-calls", type=int, default=6,
                    help="tool calls before a run with no skill call is called a "
                         "no-trigger; audit this with --run-to-completion")
    ap.add_argument("--run-to-completion", action="store_true",
                    help="disable early stopping, to check the cheap rule is "
                         "not hiding late skill invocations")
    ap.add_argument("--model", default=None)
    ap.add_argument("--results-dir", default=DEFAULT_RESULTS)
    ap.add_argument("--overwrite", action="store_true",
                    help="ignore cached runs and re-measure")
    ap.add_argument("--force", action="store_true",
                    help="permit a repeat run of the sealed split")
    ap.add_argument("--skills-dir", default=corpus.SKILLS_DIR)
    args = ap.parse_args(argv)

    skills = corpus.skill_names(args.skills_dir)
    queries = corpus.load_trigger_corpus(args.skills_dir)
    if args.split == "graded":
        queries = [q for q in queries if q["split"] in ("train", "validation")]
    elif args.split != "all":
        queries = [q for q in queries if q["split"] == args.split]
    if not queries:
        sys.exit(f"no queries in split {args.split!r}")

    results_dir = os.path.join(args.results_dir, "trigger", args.split)
    os.makedirs(results_dir, exist_ok=True)
    spends_sealed = any(q["split"] == "sealed" for q in queries)
    marker, prior = (check_sealed(results_dir, args)
                     if spends_sealed else (None, None))
    if spends_sealed and args.split != "sealed":
        print(f"note: --split {args.split} includes sealed queries; this spends "
              f"the one-shot holdout", flush=True)

    jobs = [(q, i) for q in queries for i in range(args.runs)]
    print(f"{len(queries)} queries x {args.runs} runs = {len(jobs)} runs "
          f"({args.workers} at a time)", flush=True)

    started, records, done = time.time(), [], 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(execute, q, i, skills, results_dir, args): (q, i)
                   for q, i in jobs}
        for fut in concurrent.futures.as_completed(futures):
            q, i = futures[fut]
            done += 1
            try:
                rec = fut.result()
            except Exception as exc:                     # noqa: BLE001
                rec = {"query_id": q["id"], "index": i, "outcome": harness.ERROR,
                       "skills_invoked": [], "void": f"{type(exc).__name__}: {exc}",
                       "split": q["split"], "owner": q["owner"]}
            records.append(rec)
            fired = ",".join(rec["skills_invoked"]) or "-"
            print(f"  [{done}/{len(jobs)}] {q['id']}#{i} {rec['outcome']:<11} "
                  f"{fired}", flush=True)

    summary = score(queries, records, skills, THRESHOLD)
    summary["meta"] = {
        "split": args.split, "runs_per_query": args.runs,
        "skills": skills, "model": args.model or "(session default)",
        "elapsed_seconds": round(time.time() - started, 1),
        "early_stop_tool_calls": None if args.run_to_completion
        else args.max_tool_calls,
        "timeout_seconds": args.timeout,
    }
    out = os.path.join(results_dir, "summary.json")
    harness.write_json(out, summary)

    if marker is not None:
        prior.append({"finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
                      "split": args.split,
                      "passed": summary["passed"], "graded": summary["graded"]})
        harness.write_json(marker, prior)

    voided = sum(r["excluded"] for r in summary["rows"])
    print(f"\n{summary['passed']}/{summary['graded']} queries passed")
    if summary["ungraded"]:
        print(f"{summary['ungraded']} ungraded: every run errored")
    if voided:
        print(f"{voided} run(s) excluded; see void_reasons in {out}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
