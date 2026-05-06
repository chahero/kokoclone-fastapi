#!/usr/bin/env sh
set -eu

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker CLI was not found. Install Docker, then run this script again." >&2
  exit 1
fi

docker compose -f docker/compose.cpu.yml up --build
