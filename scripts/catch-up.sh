#!/usr/bin/env bash
# Put your code exactly where it should be at the END of a lab.
#
#   scripts/catch-up.sh 1      # reviewer/ and tests/ = end of lab 1 → ready for lab 2
#   scripts/catch-up.sh 0      # back to the start
#
# It REPLACES reviewer/ and tests/ with the reference copies in solutions/.
# Nothing else is touched: not the prepared PRs, not your Azure resources.
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-}" in
  0) SRC=solutions/start ;;
  1|2) SRC="solutions/end-of-lab-0$1" ;;
  *) echo "usage: scripts/catch-up.sh <0, 1 or 2>"; exit 2 ;;
esac
rm -rf reviewer tests
cp -R "$SRC/reviewer" "$SRC/tests" .
echo "✅ reviewer/ and tests/ are now at $SRC."
