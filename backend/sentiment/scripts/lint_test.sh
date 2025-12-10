#!/usr/bin/env bash
set -euo pipefail
echo "No linters configured; running pytest if installed."
if command -v pytest >/dev/null 2>&1; then
  pytest -q
else
  echo "pytest not installed."
fi
