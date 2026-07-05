#!/usr/bin/env bash
# Run every skill's unittest suite (any skill with a tests/ directory).
# Used by both the pre-commit hook and CI. Exits non-zero if any suite fails.
set -uo pipefail
cd "$(dirname "$0")/.."

status=0
ran=0
for testsdir in */tests; do
  [ -d "$testsdir" ] || continue          # no skills with tests -> glob stays literal
  skill="${testsdir%/tests}"
  ran=$((ran + 1))
  echo "== $skill =="
  if ! ( cd "$skill" && python3 -m unittest discover -s tests ); then
    status=1
  fi
done

if [ "$ran" -eq 0 ]; then
  echo "no skills with a tests/ directory"
fi
exit "$status"
