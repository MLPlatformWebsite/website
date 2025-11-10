#!/bin/bash
# shellcheck disable=SC2154
set -e
NEW_CHANGES="/*"

echo "======== CREATING INVALIDATION ========"
echo "--distribution-id \"$CF_DIST_ID_STATIC_LO\" --paths $NEW_CHANGES"
invID=$(aws cloudfront create-invalidation --distribution-id "$CF_DIST_ID_STATIC_LO" --paths "$NEW_CHANGES" --query Invalidation.Id --output text)
export invID

echo "======== INVALIDATION ID ========"
echo "${invID}"

echo "======== POLLING COMPLETED INVALIDATION ========"
# Increasingly, a single call to cloudfront wait invalidation-completed has been erroring
# out with "max attempts exceeded". We now run this in a do loop to ensure that we repeat
# the call until it is all finished.
until aws cloudfront wait invalidation-completed --distribution-id "$CF_DIST_ID_STATIC_LO" --id "${invID}" 2>/dev/null
do
    # Still waiting - output some progress
    echo "Still waiting ..."
    aws cloudfront get-invalidation --distribution-id "$CF_DIST_ID_STATIC_LO" --id "${invID}"
    sleep 10
done

# and final confirmation
aws cloudfront get-invalidation --distribution-id "$CF_DIST_ID_STATIC_LO" --id "${invID}"

echo "======== INVALIDATION COMPLETED ========"
