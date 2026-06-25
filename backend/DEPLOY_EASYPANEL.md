# Deploy no Easypanel

## Objetivo

Publicar o backend FastAPI do MVP do EGAA usando o repositório GitHub como fonte.

Repositório:

- [https://github.com/joabeoliveira/ocupacao-ghc](https://github.com/joabeoliveira/ocupacao-ghc)

## Pré-requisitos

- O repositório precisa conter os arquivos de deploy já commitados.
- O banco MySQL `nir` precisa estar acessível a partir da VPS onde o Easypanel roda.
- A tabela `ocupacao_leitos_ghc` precisa existir antes do primeiro uso dos endpoints e upload.

## Arquitetura de deploy

- Tipo de serviço: App
- Fonte: GitHub
- Build: Dockerfile da raiz do repositório
- Porta interna: `8000`
- Healthcheck: `GET /health`

## Passo a passo no Easypanel

1. Criar um novo app do tipo `App`.
2. Selecionar `GitHub` como source.
3. Informar a URL do repositório `https://github.com/joabeoliveira/ocupacao-ghc`.
4. Selecionar o branch desejado.
5. Confirmar que o build será feito pelo `Dockerfile` da raiz.
6. Configurar a porta interna como `8000`.
7. Configurar a URL pública/domínio provisório.
8. Adicionar as variáveis de ambiente abaixo.
9. Fazer o primeiro deploy.

## Variáveis de ambiente

- `APP_NAME=EGAA API`
- `APP_ENV=production`
- `API_PREFIX=/api`
- `MYSQL_USER=...`
- `MYSQL_PASSWORD=...`
- `MYSQL_HOST=...`
- `MYSQL_PORT=3306`
- `MYSQL_DATABASE=nir`
- `CORS_ORIGINS=https://seu-frontend.exemplo.com,http://localhost:3000`
- `UPLOAD_TMP_DIR=/app/backend/tmp`
- `PORT=8000`

## Endpoints esperados após deploy

- `GET /health`
- `GET /api/censo/kpis`
- `GET /api/censo/pacientes`
- `POST /api/upload/censo`

## Verificações pós-deploy

1. Abrir `/health` e validar `{"status":"ok"}`.
2. Testar `GET /api/censo/kpis` com o banco acessível.
3. Testar `GET /api/censo/pacientes` sem filtro e com filtro por `especialidade=DERMATO`.
4. Testar `POST /api/upload/censo` com um arquivo real de censo.

## Observações operacionais

- O container sobe apenas o backend; o frontend Next.js pode ser publicado como outro app depois.
- O upload grava temporariamente em `/app/backend/tmp` e remove o arquivo ao final do processamento.
- O `PYTHONPATH` do container já inclui `/app` e `/app/backend`, então o FastAPI e o ETL compartilham o mesmo código sem depender do ambiente local.
