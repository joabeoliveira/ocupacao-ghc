#!/bin/sh
set -eu

PORT_VALUE="${PORT:-8000}"

exec uvicorn app.main:app \
  --app-dir /app/backend \
  --host 0.0.0.0 \
  --port "$PORT_VALUE"