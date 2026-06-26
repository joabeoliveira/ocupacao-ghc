# Backend EGAA

## Estrutura

- `app/main.py`: inicializacao do FastAPI
- `app/config.py`: configuracoes por variavel de ambiente
- `app/database.py`: engine e sessao SQLAlchemy
- `app/models.py`: modelo ORM de `ocupacao_leitos_ghc`
- `app/schemas.py`: contratos Pydantic da API
- `app/routers/censo.py`: endpoints de KPIs e listagem do censo vivo
- `app/routers/upload.py`: upload do censo diario
- `app/routers/ui.py`: interface web para upload via navegador (`/upload`)
- `etl_process.py`: integracao com o ETL existente em `src/etl/etl_process.py`

## Variaveis de ambiente

- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `CORS_ORIGINS`
- `API_PREFIX`
- `UPLOAD_TMP_DIR`

## Execucao local

```bash
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

## Deploy

O repositório já inclui um `Dockerfile` na raiz para deploy no Easypanel.

Veja o guia em `backend/DEPLOY_EASYPANEL.md`.

## Upload sem curl

Depois de subir a API, abra:

- `/upload`

Essa tela envia arquivos para os endpoints de upload sem depender de comandos no terminal.
