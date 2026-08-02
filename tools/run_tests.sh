#!/usr/bin/env bash
# Run every unittest suite in the repo: any tests/ directory, at any depth
# (skills and tools alike), executed from its parent so imports resolve.
# Used by both the pre-commit hook and CI. Exits non-zero if any suite
# fails — or if no suites ran at all, so a wrong working directory can
# never pass silently.
#
# Eval sweep output is excluded deliberately. Those runs hand a working
# directory to a model that writes and tests its own Python, and the
# financial-planning skill is told to put that code under tests/. Discovering
# it here would make this script, and the pre-commit hook that calls it,
# execute unreviewed model output.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

status=0
ran=0
while IFS= read -r testsdir; do
  parent="${testsdir%/tests}"
  ran=$((ran + 1))
  echo "== $parent =="
  if ! ( cd "$parent" && python3 -m unittest discover -s tests ); then
    status=1
  fi
done < <(find . -type d -name tests -not -path '*/.*' \
           -not -path './tools/eval/results/*' | sort)

if [ "$ran" -eq 0 ]; then
  echo "ERROR: no tests/ directories found — wrong working directory?" >&2
  exit 1
fi
exit "$status"
