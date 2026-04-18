FROM dhi.io/python:3.12-alpine3.23-sfw-ent-dev AS builder

WORKDIR /app

# Install uv (explicit, don’t assume base image has it)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install deps
RUN uv sync --frozen

# Copy app code
COPY ./app ./app

# Runtime stage (clean)
FROM dhi.io/python:3.12-alpine3.23

WORKDIR /app

# bring uv into runtime
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy installed environment + app
COPY --from=builder /app /app

USER nonroot

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
