#!/bin/bash
# shellcheck disable=SC2154
#
# Note: do NOT use "set -e" in this script because we need the "if" statement to execute and it won't
# if we use "set -e"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$GITHUB_WORKSPACE/website" || exit 1
if [ -d _data ] && [ -f _data/routingrules.json ]; then
  $DIR/test-routing-rules.py
else
  echo "No routing rules file - skipping test"
fi
