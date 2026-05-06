from pathlib import Path
import os

os.environ.setdefault("KOKOCLONE_ENABLE_WEBUI", "false")

from fastapi.testclient import TestClient

from kokoclone_api.main import create_app
from kokoclone_api import routes


class FakeCloneService:
    def __init__(self):
        self.clone_calls = []
        self.convert_calls = []

    def clone_text(self, *, text, lang, reference_audio, output_path):
        self.clone_calls.append(
            {
                "text": text,
                "lang": lang,
                "reference_audio": Path(reference_audio).read_bytes(),
            }
        )
        Path(output_path).write_bytes(b"fake cloned wav")

    def convert_audio(self, *, source_audio, reference_audio, output_path):
        self.convert_calls.append(
            {
                "source_audio": Path(source_audio).read_bytes(),
                "reference_audio": Path(reference_audio).read_bytes(),
            }
        )
        Path(output_path).write_bytes(b"fake converted wav")


def test_health_reports_ready_without_loading_model():
    app = create_app(mount_webui=False)
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_languages_lists_supported_kokoclone_languages():
    app = create_app(mount_webui=False)
    client = TestClient(app)

    response = client.get("/api/languages")

    assert response.status_code == 200
    assert response.json() == {
        "languages": ["en", "hi", "fr", "ja", "zh", "it", "es", "pt"]
    }


def test_clone_endpoint_returns_generated_wav(monkeypatch):
    fake_service = FakeCloneService()
    monkeypatch.setattr(routes, "get_clone_service", lambda: fake_service)
    app = create_app(mount_webui=False)
    client = TestClient(app)

    response = client.post(
        "/api/tts/clone",
        data={"text": "Hello", "lang": "en"},
        files={"reference_audio": ("reference.wav", b"reference bytes", "audio/wav")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("audio/wav")
    assert response.content == b"fake cloned wav"
    assert fake_service.clone_calls == [
        {"text": "Hello", "lang": "en", "reference_audio": b"reference bytes"}
    ]


def test_convert_endpoint_returns_converted_wav(monkeypatch):
    fake_service = FakeCloneService()
    monkeypatch.setattr(routes, "get_clone_service", lambda: fake_service)
    app = create_app(mount_webui=False)
    client = TestClient(app)

    response = client.post(
        "/api/audio/convert",
        files={
            "source_audio": ("source.wav", b"source bytes", "audio/wav"),
            "reference_audio": ("reference.wav", b"reference bytes", "audio/wav"),
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("audio/wav")
    assert response.content == b"fake converted wav"
    assert fake_service.convert_calls == [
        {
            "source_audio": b"source bytes",
            "reference_audio": b"reference bytes",
        }
    ]
