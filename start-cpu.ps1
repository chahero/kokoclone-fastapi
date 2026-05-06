$ErrorActionPreference = "Stop"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker CLI was not found. Install Docker, then run this script again."
}

docker compose -f docker/compose.cpu.yml up --build

