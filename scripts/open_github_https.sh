#!/bin/zsh

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <https://github.com/...>" >&2
  exit 64
fi

url="$1"

case "$url" in
  https://github.com/*)
    open "$url"
    ;;
  *)
    echo "blocked: only https://github.com/... URLs are allowed" >&2
    exit 65
    ;;
esac
