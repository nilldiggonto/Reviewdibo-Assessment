FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY app/ app/
COPY start.sh ./

RUN mkdir -p /app/data

ENV DATABASE_URL=sqlite+aiosqlite:///./data/reviewdibo.db

EXPOSE 8000

CMD ["./start.sh"]