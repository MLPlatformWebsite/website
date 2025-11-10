#!/bin/bash
# shellcheck disable=SC2154
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
if [ -n "$1" ]; then
    PARM1="$1"
    # Some push workflows provide a / at the end so check and remove
    # if present
    LAST="${PARM1: -1}"
    if [ "$LAST" == "/" ]; then
        PARM1="${PARM1%?}"
    fi
    if [ ! -d "$PARM1" ]; then
        echo "$PARM1 is not a directory"
        exit 1
    else
        echo "Checking $PARM1 for routing rules"
    fi
    if [ -d "$PARM1/_data" ] && [ -f "$PARM1/_data/routingrules.json" ]; then
        cd $DIR
        echo "Processing $PARM1/_data/routingrules.json"
        pipenv run python lambda_redirect.py -r "$PARM1/_data/routingrules.json"
    else
        echo "No routing rules - skipping"
    fi
else
    echo "No parameters provided - skipping"
fi
