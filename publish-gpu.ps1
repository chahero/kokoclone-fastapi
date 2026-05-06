$ErrorActionPreference = "Stop"

$ImageName = if ($env:IMAGE_NAME) {
    $env:IMAGE_NAME
} else {
    "ghcr.io/chahero/kokoclone-fastapi-gpu:latest-arm64"
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker CLI was not found. Install Docker, then run this script again."
}

docker build -f docker/gpu/Dockerfile -t $ImageName .
docker push $ImageName
