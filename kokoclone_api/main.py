from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import router


def create_app(*, mount_webui: bool = settings.enable_webui) -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version,
    )

    if settings.cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    app.include_router(router)

    if mount_webui:
        import gradio as gr

        from .webui import create_gradio_app

        app = gr.mount_gradio_app(app, create_gradio_app(), path="/web")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "kokoclone_api.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
