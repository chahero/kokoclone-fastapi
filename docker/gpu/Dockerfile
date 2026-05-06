FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    curl \
    espeak-ng \
    espeak-ng-data \
    ffmpeg \
    git \
    libsndfile1 \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
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

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .[gpu]

EXPOSE 8880

CMD ["python", "-m", "uvicorn", "kokoclone_api.main:app", "--host", "0.0.0.0", "--port", "8880"]
