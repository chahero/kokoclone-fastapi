from pathlib import Path


def test_start_scripts_exist():
    for script_name in [
        "start-cpu.ps1",
        "start-gpu.ps1",
        "start-cpu.sh",
        "start-gpu.sh",
    ]:
        assert Path(script_name).exists()


def test_shell_scripts_use_expected_compose_files():
    cpu_script = Path("start-cpu.sh").read_text(encoding="utf-8")
    gpu_script = Path("start-gpu.sh").read_text(encoding="utf-8")

    assert "docker compose -f docker/compose.cpu.yml up --build" in cpu_script
    assert "docker compose -f docker/compose.gpu.yml up --build" in gpu_script


def test_shell_scripts_are_sh_compatible():
    for script_name in ["start-cpu.sh", "start-gpu.sh"]:
        script = Path(script_name).read_text(encoding="utf-8")
        assert script.startswith("#!/usr/bin/env sh")
        assert "pipefail" not in script


def test_powershell_scripts_use_expected_compose_files():
    cpu_script = Path("start-cpu.ps1").read_text(encoding="utf-8")
    gpu_script = Path("start-gpu.ps1").read_text(encoding="utf-8")

    assert "docker compose -f docker/compose.cpu.yml up --build" in cpu_script
    assert "docker compose -f docker/compose.gpu.yml up --build" in gpu_script


def test_compose_files_publish_to_non_conflicting_host_port():
    for compose_file in ["docker/compose.cpu.yml", "docker/compose.gpu.yml"]:
        compose = Path(compose_file).read_text(encoding="utf-8")
        assert '"8890:8880"' in compose
        assert '"8880:8880"' not in compose
