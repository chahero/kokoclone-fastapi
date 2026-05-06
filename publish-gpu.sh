#!/usr/bin/env sh
set -eu

IMAGE_NAME="${IMAGE_NAME:-ghcr.io/chahero/kokoclone-fastapi-gpu:latest-arm64}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker CLI was not found. Install Docker, then run this script again." >&2
  exit 1
fi

docker build -f docker/gpu/Dockerfile -t "$IMAGE_NAME" .
docker push "$IMAGE_NAME"
