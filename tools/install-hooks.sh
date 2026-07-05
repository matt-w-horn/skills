#!/usr/bin/env bash
# Install this repo's git pre-commit hook — validation, tests, and a gitleaks
# scan on every commit, with no framework needed. (If you prefer the
# pre-commit framework, `pre-commit install` uses .pre-commit-config.yaml
# and runs the same checks; either one works, last install wins.)
set -euo pipefail
cd "$(dirname "$0")/.." || exit 1

hooks_dir="$(git rev-parse --git-path hooks)"
cat > "$hooks_dir/pre-commit" <<'HOOK'
#!/usr/bin/env bash
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1
status=0
python3 tools/validate_skills.py || status=1
tools/run_tests.sh || status=1
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks git --pre-commit --staged --no-banner || status=1
else
  echo "warn: gitleaks not installed; secret scan skipped (CI still runs it)" >&2
fi
exit "$status"
HOOK
chmod +x "$hooks_dir/pre-commit"
echo "pre-commit hook installed at $hooks_dir/pre-commit"
