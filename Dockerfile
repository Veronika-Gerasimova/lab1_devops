FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV APP_PORT=8000 \
    DATABASE_URL="postgresql+psycopg2://postgres:postgres@db:5432/appdb"

EXPOSE 8000

# Gunicorn as WSGI server
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "app:app"]
