from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool

from .config import settings
from .service import get_clone_service


SUPPORTED_LANGUAGES = ["en", "hi", "fr", "ja", "zh", "it", "es", "pt"]

router = APIRouter()


def _cleanup_paths(paths: list[str]) -> None:
    for path in paths:
        try:
            Path(path).unlink(missing_ok=True)
        except OSError:
            pass


def _new_temp_path(suffix: str) -> str:
    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=settings.temp_dir, suffix=suffix, delete=False) as fp:
        return fp.name


async def _save_upload(upload: UploadFile, suffix: str) -> str:
    path = _new_temp_path(suffix)
    Path(path).write_bytes(await upload.read())
    return path


@router.get("/api/languages")
async def list_languages():
    return {"languages": SUPPORTED_LANGUAGES}


@router.post("/api/tts/clone")
async def clone_text_to_speech(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    lang: str = Form("en"),
    reference_audio: UploadFile = Form(...),
):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is required.")
    if lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {lang}")

    ref_path = await _save_upload(reference_audio, ".wav")
    output_path = _new_temp_path(".wav")
    cleanup = [ref_path, output_path]

    try:
        service = get_clone_service()
        await run_in_threadpool(
            service.clone_text,
            text=text,
            lang=lang,
            reference_audio=ref_path,
            output_path=output_path,
        )
    except Exception as exc:
        _cleanup_paths(cleanup)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    background_tasks.add_task(_cleanup_paths, cleanup)
    return FileResponse(
        output_path,
        media_type="audio/wav",
        filename="kokoclone-output.wav",
        background=background_tasks,
    )


@router.post("/api/audio/convert")
async def convert_audio(
    background_tasks: BackgroundTasks,
    source_audio: UploadFile = Form(...),
    reference_audio: UploadFile = Form(...),
):
    source_path = await _save_upload(source_audio, ".wav")
    ref_path = await _save_upload(reference_audio, ".wav")
    output_path = _new_temp_path(".wav")
    cleanup = [source_path, ref_path, output_path]

    try:
        service = get_clone_service()
        await run_in_threadpool(
            service.convert_audio,
            source_audio=source_path,
            reference_audio=ref_path,
            output_path=output_path,
        )
    except Exception as exc:
        _cleanup_paths(cleanup)
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    background_tasks.add_task(_cleanup_paths, cleanup)
    return FileResponse(
        output_path,
        media_type="audio/wav",
        filename="kokoclone-converted.wav",
        background=background_tasks,
    )

