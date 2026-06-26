#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-localhost}
PORT=${2:-8000}
TEST_UPLOAD=${3:-}

usage() {
  cat <<EOF
Usage: $0 [host] [port] [optional: path-to-test-upload]

Examples:
  $0 localhost 8000
  $0 my.server.com 8000 /tmp/sample.csv   # executa upload de teste (ALTERA DADOS)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

TMPRESP="/tmp/prod_smoke_resp.$$"
failed=0

check_get() {
  local path="$1"
  local url="http://$HOST:$PORT$path"
  echo "GET $url"
  http_code=$(curl -sS -o "$TMPRESP" -w "%{http_code}" "$url" || true)
  if [[ "$http_code" -ge 200 && "$http_code" -lt 300 ]]; then
    echo "  OK ($http_code)"
    if command -v jq >/dev/null 2>&1; then jq . "$TMPRESP" || cat "$TMPRESP"; else cat "$TMPRESP"; fi
  else
    echo "  ERRO ($http_code)" >&2
    cat "$TMPRESP" >&2 || true
    failed=1
  fi
  rm -f "$TMPRESP"
}

do_upload() {
  local file="$1"
  local endpoint="/api/upload/arquivo"
  if [[ ! -f "$file" ]]; then
    echo "Arquivo nao encontrado: $file" >&2
    failed=1
    return 1
  fi
  local url="http://$HOST:$PORT$endpoint"
  echo "POST $url (file: $file)"
  http_code=$(curl -sS -o "$TMPRESP" -w "%{http_code}" -F "file=@${file}" "$url" || true)
  if [[ "$http_code" -ge 200 && "$http_code" -lt 300 ]]; then
    echo "  OK ($http_code)"
    if command -v jq >/dev/null 2>&1; then jq . "$TMPRESP" || cat "$TMPRESP"; else cat "$TMPRESP"; fi
  else
    echo "  ERRO ($http_code)" >&2
    cat "$TMPRESP" >&2 || true
    failed=1
  fi
  rm -f "$TMPRESP"
}

echo "Smoke checks para http://$HOST:$PORT"

check_get "/health" || true
check_get "/api/censo/kpis" || true
check_get "/api/censo/pacientes?page=1&page_size=1" || true
check_get "/upload" || true
check_get "/dashboard" || true

if [[ -n "$TEST_UPLOAD" ]]; then
  echo "Executando upload de teste (opcional) - ATENCAO: altera dados no banco"
  do_upload "$TEST_UPLOAD" || true
fi

if [[ "$failed" -eq 0 ]]; then
  echo "Todos os checks OK"
  exit 0
else
  echo "Alguns checks falharam" >&2
  exit 2
fi
#!/usr/bin/env bash
# Smoke checks para execução em container (bash). Não altera dados por padrão.
# Uso:
#   ./scripts/prod_smoke.sh [host] [port] [test_upload_path]
# Exemplo:
#   ./scripts/prod_smoke.sh localhost 8000 /tmp/sample-small.csv

set -o pipefail

HOST=${1:-localhost}
PORT=${2:-8000}
TEST_UPLOAD_PATH=${3:-}

BASE_URL="http://$HOST:$PORT"
ALL_OK=0

echo "Smoke checks para $BASE_URL"

check_get() {
  local path="$1"
  local label="$2"
  url="$BASE_URL$path"
  printf "GET %s ... " "$url"
  if curl -sS --fail "$url" -o /tmp/prod_smoke_resp.$$; then
    echo "OK"
    # printa um trecho do corpo (útil para KPIs)
    head -n 12 /tmp/prod_smoke_resp.$$ | sed -n '1,12p'
    return 0
  else
    echo "ERRO"
    ALL_OK=2
    return 1
  fi
}

check_upload() {
  local file_path="$1"
  url="$BASE_URL/api/upload/arquivo"
  if [ ! -f "$file_path" ]; then
    echo "Arquivo de teste nao encontrado: $file_path" >&2
    ALL_OK=2
    return 1
  fi
  printf "POST %s (arquivo: %s) ... " "$url" "$file_path"
  if curl -sS -F "file=@${file_path}" "$url" -o /tmp/prod_smoke_upload_resp.$$; then
    echo "OK"
    head -n 20 /tmp/prod_smoke_upload_resp.$$ | sed -n '1,20p'
    return 0
  else
    echo "ERRO"
    ALL_OK=2
    return 1
  fi
}

check_get "/health" "health"
check_get "/api/censo/kpis" "kpis"
check_get "/api/censo/pacientes?page=1&page_size=1" "pacientes"
check_get "/upload" "upload_ui"
check_get "/dashboard" "dashboard_ui"

if [ -n "$TEST_UPLOAD_PATH" ]; then
  echo "Executando upload de teste (opcional) - cuidado: isso processa dados"
  check_upload "$TEST_UPLOAD_PATH"
fi

if [ "$ALL_OK" -eq 0 ]; then
  echo "Todos os checks OK"
  exit 0
else
  echo "Alguns checks falharam"
  exit 2
fi
