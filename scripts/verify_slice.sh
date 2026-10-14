#!/usr/bin/env bash
# Compatibility name used by older campus lessons. Runs the current checker.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/verify_campus.py "$@"
