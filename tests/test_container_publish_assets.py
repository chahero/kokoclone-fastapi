from pathlib import Path


def test_gpu_compose_has_operational_container_settings():
    compose = Path("docker/compose.gpu.yml").read_text(encoding="utf-8")

    assert "container_name: kokoclone-fastapi" in compose
    assert "restart: always" in compose
    assert "count: 1" in compose


def test_ghcr_image_compose_uses_published_image_name():
    compose = Path("docker/compose.gpu.image.yml").read_text(encoding="utf-8")

    assert "image: ghcr.io/chahero/kokoclone-fastapi-gpu:latest-arm64" in compose
    assert "build:" not in compose
    assert '"8890:8880"' in compose
    assert "container_name: kokoclone-fastapi" in compose


def test_publish_scripts_reference_expected_ghcr_image():
    for script_name in ["publish-gpu.sh", "publish-gpu.ps1"]:
        script = Path(script_name).read_text(encoding="utf-8")
        assert "ghcr.io/chahero/kokoclone-fastapi-gpu:latest-arm64" in script
        assert "docker push" in script
