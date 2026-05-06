import tomllib


def test_kanade_dependency_is_pip_installable_direct_reference():
    with open("pyproject.toml", "rb") as fp:
        project = tomllib.load(fp)["project"]

    dependencies = project["dependencies"]

    assert (
        "kanade-tokenizer @ git+https://github.com/frothywater/kanade-tokenizer"
        in dependencies
    )


def test_gpu_dockerfile_installs_python_headers_for_source_builds():
    with open("docker/gpu/Dockerfile", encoding="utf-8") as fp:
        dockerfile = fp.read()

    assert "python3-dev" in dockerfile


def test_readme_documents_verified_ghcr_arm64_deployment():
    with open("README.md", encoding="utf-8") as fp:
        readme = fp.read()

    assert "ghcr.io/chahero/kokoclone-fastapi-gpu:latest-arm64" in readme
    assert "http://localhost:8890/health" in readme
    assert "DGX Spark" in readme
