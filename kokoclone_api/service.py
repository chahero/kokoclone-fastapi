import threading
from functools import lru_cache

from .config import Settings, settings


class CloneService:
    def __init__(self, app_settings: Settings = settings):
        from core.cloner import KokoClone

        self._lock = threading.Semaphore(app_settings.max_concurrent_jobs)
        self._cloner = KokoClone(
            kanade_model=app_settings.kanade_model,
            hf_repo=app_settings.hf_repo,
        )

    def clone_text(
        self,
        *,
        text: str,
        lang: str,
        reference_audio: str,
        output_path: str,
    ) -> None:
        with self._lock:
            self._cloner.generate(
                text=text,
                lang=lang,
                reference_audio=reference_audio,
                output_path=output_path,
            )

    def convert_audio(
        self,
        *,
        source_audio: str,
        reference_audio: str,
        output_path: str,
    ) -> None:
        with self._lock:
            self._cloner.convert(
                source_audio=source_audio,
                reference_audio=reference_audio,
                output_path=output_path,
            )


@lru_cache(maxsize=1)
def get_clone_service() -> CloneService:
    return CloneService()

