#!/usr/bin/env bash
# Build the site image from ./dist and tag it.
# Usage: ./docker-build.sh [tag]
#   tag  optional; defaults to gfl-simulator-<yyyyMMddHHmmss>
set -euo pipefail

if [[ $# -gt 1 ]]; then
  echo "Usage: $0 [tag]" >&2
  exit 1
fi

tag=${1:-gfl-simulator-$(date +%Y%m%d%H%M%S)}

if [[ ! -f dist/index.html ]]; then
  echo "dist/ does not exist or is not built (run ./build.sh first)" >&2
  exit 1
fi

docker build -t "$tag" .
echo "Built image '$tag'; run it with: docker run --rm -p 8000:8000 $tag"
