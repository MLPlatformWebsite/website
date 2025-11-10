#!/bin/bash
# shellcheck disable=SC2154
#
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BUILDDIR="$1"
shift

cd $DIR
echo "check-links-3.py -d $BUILDDIR $@"
pipenv run python check_links_3.py -d "$BUILDDIR" "$@"
