$ErrorActionPreference = "Stop"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker CLI was not found. Install Docker and NVIDIA Container Toolkit, then run this script again."
}

docker compose -f docker/compose.gpu.yml up --build

