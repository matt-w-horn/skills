#!/usr/bin/env python3
"""Run the execution benchmark: is the deliverable worth having?

Each eval runs twice over, once with the skill loaded and once without,
because a pass rate with no baseline is uninterpretable. If a competent model
produces the same thing unaided, the skill is costing tokens and latency to
change nothing, and only the comparison can tell you that.

Runs are long: the skills under test dispatch subagents, search the web, and
write and test code. So every run is cached the moment it lands and the sweep
resumes rather than restarts, and grading is a separate step you can repeat
without paying for the runs again.

    python3 tools/eval/run_exec.py --runs 2
    python3 tools/eval/run_exec.py --eval audit-flawed-model --grade-only
    python3 tools/eval/run_exec.py --eval write-the-plan,plan-career-break

`--eval` takes a comma-separated list, so a subset can be re-run after a
change without paying for the full benchmark. The summary is always built
from every valid cached run on disk, whichever subset this invocation
executed: evals whose cache is stale under the current fingerprints show up
as insufficient data rather than silently vanishing, and a subset run never
overwrites the record of the rest.

The useful output is the per-assertion cross-tab: which assertions pass with
the skill and fail without it. Those are the ones measuring something.
Assertions that pass either way inflate the score while telling you nothing,
and the report names them so they can be cut or sharpened.

On permissions. `financial-planning` writes its own model code and runs
`python3 -m unittest` as part of doing its job, so the runs need a shell.
Measured on Claude Code 2.1.220, asking for one `python3 -c` call:

    default                                          blocked
    --permission-mode acceptEdits                    blocked
    --allowedTools 'Bash(python3 *)' + acceptEdits   runs
    --permission-mode bypassPermissions              runs

The allowlist works but fails badly for a sweep: a Bash call outside the list
does not get denied, it waits for an approval that headless mode will never
deliver, so one stray `ls` costs that run its entire timeout and scores as a
failure of the skill. Hence bypassPermissions, deliberately, in per-run scratch
directories. That is a real grant of shell access on the machine running the
sweep, which is why it is written down here rather than left to a default.
"""
import argparse
import concurrent.futures
import glob
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import corpus      # noqa: E402
import grade       # noqa: E402
import harness     # noqa: E402

DEFAULT_RESULTS = os.path.join(harness.REPO_ROOT, "tools", "eval", "results")


def run_dir(results_dir, eval_id, configuration, index):
    return os.path.join(results_dir, eval_id, configuration, f"run-{index}")


def fingerprint(ev, args):
    """What a cached run was measured under.

    Without this, resuming after editing a prompt, a fixture, or a skill
    reuses the old measurement while the summary reports the new settings,
    and cached rows are indistinguishable from fresh ones in the log. That is
    the quietest way for this suite to report a number about something other
    than what it names.
    """
    h = hashlib.sha256()
    h.update(ev["prompt"].encode("utf-8"))
    for path in sorted(glob.glob(os.path.join(ev["dir"], "fixture", "**", "*"),
                                 recursive=True)):
        if os.path.isfile(path):
            h.update(os.path.relpath(path, ev["dir"]).encode("utf-8"))
            with open(path, "rb") as fh:
                h.update(fh.read())
    for skill in sorted(corpus.skill_names()):
        skill_md = os.path.join(corpus.SKILLS_DIR, skill, "SKILL.md")
        if os.path.isfile(skill_md):
            with open(skill_md, "rb") as fh:
                h.update(fh.read())
    for setting in (args.model, args.timeout, args.permission_mode):
        h.update(repr(setting).encode("utf-8"))
    return h.hexdigest()[:16]


def grading_fingerprint(ev, args):
    """What a cached grading was produced under: the rubric and the judge."""
    h = hashlib.sha256()
    for a in ev["assertions"]:
        h.update(f"{a['id']}\x00{a['text']}".encode("utf-8"))
    h.update(repr(args.judge_model).encode("utf-8"))
    return h.hexdigest()[:16]


def execute(ev, configuration, index, skills, results_dir, args):
    """One run of one eval in one configuration, cached on disk."""
    base = run_dir(results_dir, ev["id"], configuration, index)
    record_path = os.path.join(base, "run.json")
    if os.path.exists(record_path) and not args.overwrite:
        cached = harness.read_json(record_path)
        if cached is not None and cached.get("fingerprint") == fingerprint(ev, args):
            return cached
        # Either corrupt, or measured under different inputs. Re-run.

    os.makedirs(base, exist_ok=True)
    cwd = os.path.join(base, "workspace")
    harness.prepare_cwd(cwd, ev["fixture_dir"])
    stream = os.path.join(base, "stream.jsonl")

    record = harness.run_once(
        prompt=ev["prompt"],
        configuration=configuration,
        skills=skills,
        cwd=cwd,
        stream_path=stream,
        timeout=args.timeout,
        model=args.model,
        permission_mode=args.permission_mode,
        run_to_completion=True,
    )
    record.update({"eval_id": ev["id"], "index": index, "skill": ev["skill"],
                   "fingerprint": fingerprint(ev, args)})
    record["void"] = harness.void_reason(record, skills)
    record["final_text"] = harness.final_text(stream)
    record["produced"] = sorted(
        harness.collect_outputs(cwd, ev["fixture_dir"]).keys())

    harness.write_json(record_path, record)
    return record


def grade_run(ev, configuration, index, results_dir, args):
    """Grade one completed run, cached separately from the run itself."""
    base = run_dir(results_dir, ev["id"], configuration, index)
    record_path = os.path.join(base, "run.json")
    grading_path = os.path.join(base, "grading.json")
    if not os.path.exists(record_path):
        return None
    if os.path.exists(grading_path) and not args.regrade:
        cached = harness.read_json(grading_path)
        if cached is not None and cached.get("fingerprint") == grading_fingerprint(ev, args):
            return cached

    with open(record_path, encoding="utf-8") as fh:
        record = json.load(fh)
    if record.get("fingerprint") != fingerprint(ev, args):
        # The run was produced under different inputs (an edited prompt,
        # fixture, or skill body). Its artifact answers an old question, and
        # grading it spends judge calls on a result the summary would have to
        # exclude anyway.
        return None
    if record.get("void"):
        return None
    if (record.get("outcome") in (harness.TIMEOUT, harness.ERROR)
            or record.get("timed_out")
            or record.get("completed") is False):
        # The artifact is whatever existed when the run was cut off. Grading a
        # truncated deliverable as though it were finished reports a quality
        # verdict on an interrupted run. Each condition catches a different
        # way that happens: an outright failure, a watchdog kill, or a stream
        # that never carried the CLI's end-of-turn event. A run killed after
        # it invoked the skill still reports `triggered`, so `outcome` alone
        # would miss it.
        return None

    produced = harness.collect_outputs(
        os.path.join(base, "workspace"), ev["fixture_dir"])
    artifact = grade.build_artifact(record.get("final_text", ""), produced)
    if not artifact.strip():
        # A real result: the run finished and delivered nothing. Every
        # assertion fails, which is what "produced no deliverable" means.
        graded = {"assertions": [{"id": a["id"], "text": a["text"],
                                  "passed": False,
                                  "evidence": "the run produced no text to grade"}
                                 for a in ev["assertions"]],
                  "passed": 0, "failed": len(ev["assertions"]),
                  "undecided": 0, "pass_rate": 0.0}
    else:
        graded = grade.grade_artifact(artifact, ev["assertions"],
                                      model=args.judge_model,
                                      workers=args.judge_workers,
                                      sources=grade.build_sources(ev["fixture_dir"]))
        if graded["undecided"] == len(ev["assertions"]):
            # Every verdict undecided means the judge never answered, not that
            # the run was bad. Leaving it uncached keeps a transient judge
            # outage from freezing into a permanent result.
            print(f"    judge returned nothing for {ev['id']} {configuration} "
                  f"#{index}; not caching", flush=True)
            return None

    graded.update({"eval_id": ev["id"], "configuration": configuration,
                   "index": index, "fingerprint": grading_fingerprint(ev, args)})
    harness.write_json(grading_path, graded)
    return graded


def load_cached(ev, configuration, index, results_dir, args):
    """Valid cached (run, grading) for one run slot, or Nones.

    Validity means the fingerprints match the current inputs. A stale run is
    returned as nothing at all rather than as data, because a number measured
    against an old skill body answers a question nobody is asking now.
    """
    base = run_dir(results_dir, ev["id"], configuration, index)
    record = harness.read_json(os.path.join(base, "run.json"))
    if record is None or record.get("fingerprint") != fingerprint(ev, args):
        return None, None
    grading = harness.read_json(os.path.join(base, "grading.json"))
    if grading is not None and grading.get("fingerprint") != grading_fingerprint(ev, args):
        grading = None
    return record, grading


def cross_tab(evals, gradings):
    """Per-assertion pass rate in each configuration, and what that means.

    The verdicts here decide which assertions stay in the suite, so they are
    stated plainly rather than as a score: an assertion that behaves the same
    with and without the skill is not measuring the skill.
    """
    out = []
    for ev in evals:
        rows = []
        for a in ev["assertions"]:
            cell = {}
            for cfg in harness.CONFIGURATIONS:
                verdicts = [
                    r["passed"]
                    for g in gradings
                    if g and g.get("eval_id") == ev["id"]
                    and g.get("configuration") == cfg
                    for r in g.get("assertions", [])
                    if r["id"] == a["id"] and r["passed"] is not None
                ]
                cell[cfg] = {
                    "n": len(verdicts),
                    "passed": sum(1 for v in verdicts if v),
                    "rate": (sum(1 for v in verdicts if v) / len(verdicts)
                             if verdicts else None),
                }
            with_rate = cell[harness.WITH_SKILL]["rate"]
            without_rate = cell[harness.WITHOUT_SKILL]["rate"]

            if with_rate is None or without_rate is None:
                verdict = "insufficient data"
            elif with_rate == without_rate == 1.0:
                verdict = ("non-discriminating: passes without the skill too, "
                           "so it inflates the score without measuring it")
            elif with_rate == without_rate == 0.0:
                verdict = ("never passes either way: the assertion or the task "
                           "is broken, not the skill")
            elif with_rate == without_rate:
                # Equal but not at a boundary measures the skill exactly as
                # little as equal-at-1.0 does; it just looks less obvious.
                verdict = (f"non-discriminating: same rate ({with_rate:.0%}) in "
                           f"both configurations")
            elif with_rate > without_rate:
                verdict = "discriminating: the skill helps here"
            elif with_rate < without_rate:
                verdict = "inverted: the skill does worse than the baseline"
            else:
                verdict = "no difference between configurations"

            rows.append({"id": a["id"], "text": a["text"],
                         "with_skill": cell[harness.WITH_SKILL],
                         "without_skill": cell[harness.WITHOUT_SKILL],
                         "delta": (None if with_rate is None or without_rate is None
                                   else round(with_rate - without_rate, 3)),
                         "verdict": verdict})
        out.append({"eval": ev["id"], "skill": ev["skill"], "assertions": rows})
    return out


def summarize(evals, records, gradings):
    per_config = {}
    for cfg in harness.CONFIGURATIONS:
        rates = [g["pass_rate"] for g in gradings
                 if g and g.get("configuration") == cfg
                 and g.get("pass_rate") is not None]
        per_config[cfg] = {
            "runs": len(rates),
            "mean_pass_rate": round(sum(rates) / len(rates), 3) if rates else None,
            "min": round(min(rates), 3) if rates else None,
            "max": round(max(rates), 3) if rates else None,
        }
    voided = [{"eval": r["eval_id"], "configuration": r["configuration"],
               "index": r["index"], "reason": r["void"]}
              for r in records if r and r.get("void")]
    return {"per_configuration": per_config, "voided_runs": voided,
            "cross_tab": cross_tab(evals, gradings)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--eval", default=None,
                    help="comma-separated eval ids to run (default: all)")
    ap.add_argument("--runs", type=int, default=2,
                    help="runs per configuration; 2 is a tripwire, not a benchmark")
    ap.add_argument("--workers", type=int, default=3,
                    help="concurrent runs; these are heavy")
    ap.add_argument("--timeout", type=int, default=2400)
    ap.add_argument("--permission-mode", default="bypassPermissions",
                    help="these runs execute model-written code unattended in "
                         "their own scratch directories; see the note in this "
                         "file on why the tighter modes were rejected")
    ap.add_argument("--model", default=None)
    ap.add_argument("--judge-model", default=None)
    ap.add_argument("--judge-workers", type=int, default=4)
    ap.add_argument("--grade-only", action="store_true",
                    help="skip running; grade whatever is already on disk")
    ap.add_argument("--regrade", action="store_true")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--results-dir", default=DEFAULT_RESULTS)
    ap.add_argument("--skills-dir", default=corpus.SKILLS_DIR)
    args = ap.parse_args(argv)

    skills = corpus.skill_names(args.skills_dir)
    evals = corpus.load_execution_evals(args.skills_dir)
    selected = evals
    if args.eval:
        wanted = [w.strip() for w in args.eval.split(",") if w.strip()]
        by_id = {e["id"]: e for e in evals}
        missing = [w for w in wanted if w not in by_id]
        if missing:
            sys.exit(f"no execution eval named {missing[0]!r} "
                     f"(known: {', '.join(sorted(by_id))})")
        selected = [by_id[w] for w in wanted]

    results_dir = os.path.join(args.results_dir, "execution")
    os.makedirs(results_dir, exist_ok=True)

    jobs = [(ev, cfg, i) for ev in selected
            for cfg in harness.CONFIGURATIONS for i in range(args.runs)]
    started = time.time()

    if not args.grade_only:
        print(f"{len(selected)} evals x {len(harness.CONFIGURATIONS)} configs x "
              f"{args.runs} runs = {len(jobs)} runs ({args.workers} at a time). "
              f"These are long.", flush=True)
        done = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {
                pool.submit(execute, ev, cfg, i, skills, results_dir, args):
                    (ev, cfg, i) for ev, cfg, i in jobs
            }
            for fut in concurrent.futures.as_completed(futures):
                ev, cfg, i = futures[fut]
                done += 1
                try:
                    rec = fut.result()
                except Exception as exc:                 # noqa: BLE001
                    rec = {"eval_id": ev["id"], "configuration": cfg, "index": i,
                           "outcome": harness.ERROR, "skills_invoked": [],
                           "void": f"{type(exc).__name__}: {exc}"}
                flag = f"  VOID: {rec['void']}" if rec.get("void") else ""
                print(f"  [{done}/{len(jobs)}] {ev['id']} {cfg} #{i} "
                      f"{rec['outcome']} {rec.get('seconds', '?')}s{flag}",
                      flush=True)

    print("\ngrading...", flush=True)
    for ev, cfg, i in jobs:
        g = grade_run(ev, cfg, i, results_dir, args)
        if g:
            rate = g.get("pass_rate")
            shown = "n/a" if rate is None else f"{rate:.0%}"
            print(f"  {ev['id']} {cfg} #{i}: {shown}", flush=True)

    # The summary is rebuilt from disk over every eval, not just this
    # invocation's subset, so `--eval` refreshes a slice of the record instead
    # of replacing the whole record with the slice. Stale caches fail their
    # fingerprint check and drop out, which the cross-tab reports as
    # insufficient data rather than as a number.
    records, gradings = [], []
    for ev in evals:
        for cfg in harness.CONFIGURATIONS:
            for i in range(args.runs):
                rec, g = load_cached(ev, cfg, i, results_dir, args)
                if rec is not None:
                    records.append(rec)
                if g is not None:
                    gradings.append(g)
    # `--runs` decides which run indices get enumerated, so summarising with a
    # smaller value than the sweep used silently drops runs. Say so rather
    # than reporting a partial result as a whole one.
    on_disk = len(glob.glob(os.path.join(results_dir, "*", "*", "run-*",
                                         "run.json")))
    if on_disk > len(records):
        print(f"note: {on_disk} runs on disk but only {len(records)} are "
              f"enumerated by --runs {args.runs} and valid under the current "
              f"fingerprints; the rest are stale or out of range", flush=True)

    summary = summarize(evals, records, gradings)
    summary["meta"] = {
        "ran_evals": sorted(e["id"] for e in selected),
        "runs_per_configuration": args.runs,
        "permission_mode": args.permission_mode,
        "model": args.model or "(session default)",
        "judge_model": args.judge_model or "(session default)",
        "elapsed_seconds": round(time.time() - started, 1),
        "caveat": ("Two runs per configuration is a regression tripwire, not a "
                   "benchmark. Read the transcripts before believing any number."),
    }
    out = os.path.join(results_dir, "summary.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print("\npass rate by configuration:")
    for cfg, stats in summary["per_configuration"].items():
        mean = stats["mean_pass_rate"]
        print(f"  {cfg:<14} {'n/a' if mean is None else f'{mean:.0%}'} "
              f"over {stats['runs']} graded run(s)")
    flagged = [r for ev in summary["cross_tab"] for r in ev["assertions"]
               if r["verdict"].startswith(("non-discriminating", "never passes",
                                           "inverted"))]
    if flagged:
        print(f"\n{len(flagged)} assertion(s) need attention:")
        for r in flagged:
            print(f"  {r['id']}: {r['verdict']}")
    if summary["voided_runs"]:
        print(f"\n{len(summary['voided_runs'])} run(s) voided; see {out}")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
