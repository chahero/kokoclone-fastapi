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


def test_powershell_scripts_use_expected_compose_files():
    cpu_script = Path("start-cpu.ps1").read_text(encoding="utf-8")
    gpu_script = Path("start-gpu.ps1").read_text(encoding="utf-8")

    assert "docker compose -f docker/compose.cpu.yml up --build" in cpu_script
    assert "docker compose -f docker/compose.gpu.yml up --build" in gpu_script
