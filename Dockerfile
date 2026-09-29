FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# OS deps for PDF/DOCX/XLSX/PPTX extraction
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY config /app/config
COPY docs /app/docs
COPY schemas /app/schemas

RUN pip install -e ".[all]"

EXPOSE 8088

# Dashboard
CMD ["uvicorn", "epe.dashboard.app:app", "--host", "0.0.0.0", "--port", "8088"]
