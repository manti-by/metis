FROM python:3.13-slim

LABEL maintainer="Alex Chaika <manti.by@gmail.com>"

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/usr/local

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

WORKDIR /app

EXPOSE 8003

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
