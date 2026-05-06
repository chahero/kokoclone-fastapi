from kokoclone_api.main import app


if __name__ == "__main__":
    import uvicorn

    from kokoclone_api.config import settings

    uvicorn.run(
        "kokoclone_api.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
