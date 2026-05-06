FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    espeak-ng \
    espeak-ng-data \
    ffmpeg \
    git \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    KOKOCLONE_HOST=0.0.0.0 \
    KOKOCLONE_PORT=8880 \
    KOKOCLONE_TEMP_DIR=/tmp/kokoclone \
    KOKOCLONE_ENABLE_WEBUI=true

COPY pyproject.toml requirements.txt README.md LICENSE ./
COPY core ./core
COPY kokoclone_api ./kokoclone_api
COPY app.py cli.py inference.py ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir .

EXPOSE 8880

CMD ["python", "-m", "uvicorn", "kokoclone_api.main:app", "--host", "0.0.0.0", "--port", "8880"]
