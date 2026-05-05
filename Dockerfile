FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application source
COPY app.py config.py memm.py index.html ./
COPY models/ models/
COPY static/ static/

EXPOSE 8000

CMD ["uv", "run", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
