from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KOKOCLONE_")

    api_title: str = "KokoClone API"
    api_description: str = "FastAPI service for KokoClone voice cloning"
    api_version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8880
    temp_dir: Path = Path("tmp/kokoclone")
    kanade_model: str = "frothywater/kanade-12.5hz"
    hf_repo: str = "PatnaikAshish/kokoclone"
    max_concurrent_jobs: int = 1
    cors_enabled: bool = True
    cors_origins: list[str] = ["*"]
    enable_webui: bool = True


settings = Settings()

