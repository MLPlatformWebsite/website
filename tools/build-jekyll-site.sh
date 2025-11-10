#!/bin/bash
# shellcheck disable=SC2154
#
# Note: do NOT use "set -e" in this script because we need the "if" statement to execute and it won't
# if we use "set -e"

function setup_vars(){
    # The following vars are set from .github-env
    # AWS_STATIC_SITE_URL
    # JEKYLL_ENV
    # SITE_URL
    PR_NUMBER=$(jq -r ".pull_request.number" $GITHUB_EVENT_PATH)
    STATUSES_URL=$(jq -r ".pull_request.statuses_url // empty" $GITHUB_EVENT_PATH)
}

function make_dirs(){
  if [ ! -d "$SITE_URL" ]; then
    echo "Making output directory \"$SITE_URL\""
    mkdir "$SITE_URL"
  else
    echo "Using output directory \"$SITE_URL\""
  fi
}

function post_build_cleanup(){
  if [ -d "generated" ]; then
    echo "'generated' folder found in repository directory"
    if [ -d "$SITE_URL/generated" ]; then
      echo "'generated' folder found in $SITE_URL - merging"
      cp -R generated/* "$SITE_URL/generated/"
      echo "Removing 'generated' folder to clean up"
      rm -rf generated
    else
      echo "No 'generated' folder in $SITE_URL - moving"
      mv "generated" "$SITE_URL"
    fi
  else
    echo "No 'generated' folder in repository directory"
  fi
}

function check_for_generated() {
  # If the folder for the last build incarnation contains a
  # "generated" folder, move that up into the repo directory
  # in order to shorten the time to rebuild the image assets.
  if [ -d "$SITE_URL/generated" ]; then
    # Make sure there isn't a pre-existing folder there already
    # as that will cause the move to fail
    if [ -d "generated" ]; then
      echo "Removing pre-existing 'generated' folder"
      rm -rf generated || exit 1
    fi
    echo "Moving 'generated' folder up a level"
    mv "$SITE_URL/generated" . || exit 1
  else
    echo "No 'generated' folder found in $SITE_URL"
  fi
}

function docker_build_site() {
  echo "Building the site ..."
  echo "docker run -e JEKYLL_ENV=$JEKYLL_ENV ${DOCKER_MOUNTS[@]} -u $(id -u):$(id -g) -v $GITHUB_WORKSPACE/website:/srv/source linaroits/jekyllsitebuild:latest"
  docker run --rm \
    -t \
    --cap-drop ALL \
    -e JEKYLL_ENV="$JEKYLL_ENV" \
    -e SKIP_JEKYLL_DOCTOR="$SKIP_JEKYLL_DOCTOR" \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    "${DOCKER_MOUNTS[@]}" \
    -u "$(id -u)":"$(id -g)" \
    -v "$GITHUB_WORKSPACE/website":/srv/source \
    linaroits/jekyllsitebuild:latest
}

cd "$GITHUB_WORKSPACE/website" || exit 1
setup_vars
make_dirs || exit 1
check_for_generated
docker_build_site
result=$?
post_build_cleanup
exit $result
