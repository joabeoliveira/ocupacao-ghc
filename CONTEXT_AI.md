# Contexto do Projeto: Painel de Regulação e Censo (EGAA)

Este documento é a fonte de verdade para qualquer agente (humanos ou LLMs) que precise compreender, desenvolver ou operar o MVP de ocupação hospitalar (EGAA). Contém visão de negócio, arquitetura, pontos de integração, convenções e passos práticos para reprodução local, deploy e troubleshooting.

## 1. Visão e Objetivo

Objetivo: fornecer ingestão automatizada e padronizada de relatórios do `esusreport` (histórico e censo diário), persistir em tabela única analítica e expor KPIs e listagens via API para suporte à regulação e gestão de leitos.

Resultados esperados:
- Carga histórica única e idempotente.
- Atualização diária (censo) sem duplicidade.
- Painel com filtros por especialidade, unidade, enfermaria e período.

## 2. Fontes de Dados

- Origem principal: exportações do `esusreport` em `.xls`, `.xlsx` e `.csv`.
- Arquivos conhecidos no repositório: [relatório de internação - esusreport - relatorio de internacao.csv](relatório de internação - esusreport - relatorio de internacao.csv) e [relatório de internação - esusreport - censo hospitalar.csv](relatório de internação - esusreport - censo hospitalar.csv).

## 3. Stack, Infra e Como Rodar

- Linguagem: Python 3.12+
- Web: FastAPI + Uvicorn
- DB: MySQL (driver: pymysql) via SQLAlchemy 2.x
- ETL: pandas, openpyxl, xlrd
- Deploy: Docker → Easypanel (deploy por GitHub push)

Requisitos locais mínimos:
1. Ter Python 3.12+ e venv ativado.
2. Instalar dependências: `pip install -r requirements.txt`.
3. Variáveis de ambiente (veja `.env.example`) — essenciais: `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_DATABASE`.

Comandos úteis:
```powershell
# testar sintaxe do ETL
python -m py_compile src\etl\etl_process.py

# executar ETL localmente sem persistir
python -m src.etl.etl_process --historico data/samples/relatorio-internacao.xls

# executar API local
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## 4. Estrutura do Repositório (resumo rápido)

- `src/etl/etl_process.py`: pipeline ETL principal (parsing, normalização, persistência). Veja funções: `prepare_dataframe`, `normalize_historico`, `normalize_censo`, `persist_dataframe`.
- `migrations/001_create_ocupacao_leitos_esusreport.sql`: DDL da tabela única (idempotência, índices, coluna gerada `internado_ativo`).
- `backend/app/`: API FastAPI com routers para upload, KPIs e UI de upload.
- `tests/`: testes automatizados do ETL.
- `Dockerfile`, `backend/start.sh`, `.env.example`: deploy/execução.

## 5. Esquema e Regras Operacionais da Tabela

Tabela alvo: `ocupacao_leitos_ghc` (nome usado no DDL/migrations). Pilares:
- Temporalidade: `data_snapshot`, `periodo_referencia_inicio/fim` e `data_impressao_arquivo`.
- Idempotência: `hash_registro` + `fonte_dado` com UNIQUE constraint.
- Coluna gerada: `internado_ativo` definida por `data_alta IS NULL`.

Campos críticos: `prontuario`, `especialidade`, `hash_registro`, `lote_importacao_id`, `data_internacao`, `data_alta`.

Regras de negócio implementadas no ETL:
- Extrair apenas dígitos de `idade` e normalizar para `Int64` quando aplicável.
- Converter datas no formato brasileiro para `datetime`/`date` compatíveis com MySQL.
- Para evitar regressão: sanitizar valores pandas nulos (`NaT`, `NaN`, `<NA>`) para `NULL` do banco antes do insert.

## 6. ETL — pontos relevantes para desenvolvedores/LLMs

- Entrada: arquivos `.xls/.xlsx/.csv` com possíveis metadados no topo; detector automático de tipo (`historico_internacao` vs `censo_diario`).
- Normalização: unificar cabeçalhos via alias, remover colunas duplicadas, tipar colunas numéricas (`idade`, `dias_internacao`) e datetimes.
- Persistência: batching (variável `ETL_BATCH_SIZE`, default `1000`) usando `INSERT ... ON DUPLICATE KEY UPDATE` para upsert.
- Sanitização final: `_sanitize_record_for_sql(record)` converte `pd.NaT/pd.NA/NaN` para `None` e `pd.Timestamp` para `datetime` nativo.

Pontos de atenção já detectados e corrigidos:
- Erro clássico: `Incorrect datetime value: 'NaT'` — resolvido com sanitização por registro antes do upsert.
- Arquivos CSV com metadados no topo: parser robusto detecta e extrai a tabela real.

Para adicionar transformações:
1. Abrir `src/etl/etl_process.py` e localizar `normalize_historico` / `normalize_censo`.
2. Inserir transformações antes de `prepare_dataframe` retornar o DataFrame final.

## 7. API — endpoints relevantes

- `GET /health` — health check.
- `POST /api/upload/arquivo` — upload automático (detecta tipo de arquivo e chama ETL).
- `POST /api/upload/historico` e `POST /api/upload/censo` — uploads específicos.
- `GET /api/censo/kpis` — KPIs de ocupação.
- `GET /api/censo/pacientes` — listagem filtrável de pacientes.

Logs e monitoramento: rota de upload escreve logs detalhados; em produção verifique os logs do contêiner e o endpoint `/health`.

## 8. Deploy (Easypanel via Docker)

Fluxo resumido:
1. Commit + push para `main` no GitHub.
2. Easypanel faz pull e build do Dockerfile.
3. Ajuste de variáveis de ambiente no painel (MYQL_* etc.).

Checks pós-deploy:
- `GET /health` = 200
- Verificar que a migration foi aplicada (tabela existe)
- Testar upload via UI `/upload`

## 9. Testes e validações automatizadas

- `tests/test_etl_process.py`: casos para parsing e normalização.
- Recomenda-se adicionar teste que injeta um `pd.NaT` em `data_alta` e valida que `_sanitize_record_for_sql` retorna `None` no payload.

Comando para rodar testes:
```powershell
pytest -q
```

## 10. Troubleshooting rápido (FAQ)

- Sintoma: `Incorrect datetime value: 'NaT'` → ação: garantir que `_sanitize_record_for_sql` está presente e é chamado antes do insert (arquivo `src/etl/etl_process.py`).
- Sintoma: diferenças entre `linhas_processadas` do uploader e `COUNT(*)` no banco → ação: checar `COUNT(DISTINCT hash_registro)` e duplicates por `hash_registro` (upserts explicam redução).
- Sintoma: upload falha em produção mas funciona local → ação: verificar variáveis de ambiente no Easypanel e logs do contêiner.

## 11. Convenções de código e PR

- Preferir mudanças mínimas e manter compatibilidade.
- Escrever testes para qualquer alteração que toque parsing ou persistência.
- Mensagens de commit: `feat:`, `fix:`, `chore:` e incluir referência ao lote ou issue quando aplicável.

## 12. Checklist de revisão para cargas

Antes de marcar um lote como aprovado:
- Rodar queries de auditoria (COUNT por lote, campos obrigatórios nulos, datas incoerentes, duplicidades por hash).
- Conferir que `linhas_processadas - COUNT(*)` é explicado por upserts (ver `hash_registro`).
- Validar KPIs no painel.

## 13. Próximos passos recomendados

1. Criar teste end-to-end que simula upload do CSV real usado em produção.
2. Adicionar métricas/alerts para falhas no ETL (Sentry/alerts simples por logs).
3. Documentar formato de hash (`build_hash_registro`) e contrato de campos esperados no README técnico.

---
Arquivo principal do ETL: [src/etl/etl_process.py](src/etl/etl_process.py)
DDL importante: [migrations/001_create_ocupacao_leitos_esusreport.sql](migrations/001_create_ocupacao_leitos_esusreport.sql)
API principal: [backend/app/main.py](backend/app/main.py)

Se quiser, eu já atualizo o `README.md` com estes passos e crio o teste que valida `NaT -> NULL` automaticamente.