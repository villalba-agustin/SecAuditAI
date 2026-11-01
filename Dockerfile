# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a dedicated prefix
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/       ./app/
COPY .agents/   ./.agents/
COPY agents/    ./agents/

# Create writable data directories
RUN mkdir -p data/uploads data/db \
 && chown -R appuser:appuser /app

USER appuser

# Runtime environment (overrideable via docker-compose / .env)
ENV APP_NAME=SecAuditAI \
    APP_ENV=production \
    DEBUG=False \
    HOST=0.0.0.0 \
    PORT=8080 \
    DATABASE_URL=sqlite:////app/data/db/secauditai.db \
    UPLOAD_DIR=/app/data/uploads \
    OLLAMA_BASE_URL=http://ollama:11434 \
    OLLAMA_MODEL=qwen3.5:4b \
    OLLAMA_TIMEOUT_SECONDS=180

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

CMD ["python", "-m", "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "8080", \
     "--workers", "1", "--log-level", "info"]
