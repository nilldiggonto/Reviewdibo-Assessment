#!/bin/bash
set -e

echo "Running database seed..."
uv run python -m app.seed

echo "Starting server..."
exec uv run fastapi run --port "${PORT:-8000}"