# Instruções para Agentes de IA — Projeto Ocupação NIR / EGAA

> **Sempre começar lendo:** [`CONTEXT_AI.md`](CONTEXT_AI.md) (negócio/regras) e [`CONTEXT_LLM_MVP.md`](CONTEXT_LLM_MVP.md) (arquitetura/mapa técnico).
> Estes dois arquivos são a fonte de verdade e devem ser consultados **antes de qualquer alteração**.

---

## 📋 Visão Geral do Projeto

Painel de regulação e censo hospitalar (EGAA/GHC). Ingestão automatizada de relatórios do **esusreport**, persistência em MySQL e exposição de KPIs via API FastAPI + UI HTML server-side.

**Stack:** Python 3.12+, FastAPI, MySQL (pymysql/SQLAlchemy 2.x), pandas, Docker
**UI Principal:** HTML inline no backend (`backend/app/routers/ui.py`)
**UI Futura:** Next.js 14 + React + Tailwind (`frontend-next/`) — **não é a UI principal do MVP**

---

## 🚀 Comandos Essenciais

```powershell
# Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Rodar API local
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Rodar testes
pytest -q

# Compilar (verificar sintaxe) arquivo alterado
python -m py_compile backend/app/routers/ui.py

# Aplicar migrations pendentes
python scripts/apply_migrations.py

# Seed de tipos de intervenção EGAA
$env:PYTHONPATH='backend'; python scripts/seed_egaa_tipos.py
```

---

## 🏗️ Arquitetura (Camadas)

| Camada | Localização | Responsabilidade |
|--------|-------------|------------------|
| **ETL** | `src/etl/etl_process.py` | Parsing, normalização e persistência de arquivos esusreport |
| **API** | `backend/app/routers/` | Endpoints FastAPI (censo, EGAA, upload) |
| **UI HTML** | `backend/app/routers/ui.py` | ~3300+ linhas de HTML/CSS/JS inline — **interface MVP atual** |
| **Frontend Next** | `frontend-next/` | Nova UI em desenvolvimento, **não é produção** |
| **Migrations** | `migrations/*.sql` | Evolução do schema MySQL, aplicadas em ordem numérica |
| **Testes** | `tests/` | Testes pytest do ETL e carga EGAA |

---

## 🔌 Endpoints da API (mais usados pela UI)

- `GET  /api/censo/kpis` — KPIs de ocupação
- `GET  /api/censo/pacientes` — Lista de pacientes (filtros: nome, prontuário, especialidade, unidade, data)
- `GET  /api/censo/paciente/{prontuario}` — Detalhe do paciente + evolução EGAA
- `PUT  /api/censo/paciente/{prontuario}/evolucao` — Salvar evolução textual
- `GET  /api/egaa/indicadores` — Indicadores agregados EGAA
- `GET  /api/egaa/intervencoes` — Listar intervenções
- `POST /api/egaa/intervencoes/lote` — Criar intervenções em lote
- `GET  /api/egaa/pendencia/{prontuario}` — Pendências do paciente
- `GET  /api/egaa/tipos-intervencao` — Tipos de intervenção disponíveis
- `GET  /api/egaa/desfechos` — Listar desfechos (filtros: prontuario, tipo, data)
- `POST /api/egaa/desfechos` — Criar desfecho (alta/óbito)
- `GET  /api/egaa/indicadores/desfechos` — Indicadores de desfechos
- `POST /api/upload/arquivo` — Upload auto-detect (censo ou histórico) + geração automática de desfechos
- `POST /api/upload/historico` — Upload de histórico + geração automática de desfechos

---

## 📐 Convenções de Código

- `from __future__ import annotations` em **todos** os arquivos Python
- Type hints com `| None` (PEP 604) em vez de `Optional`
- Nomes em **PT-BR** para endpoints e funções (`criar_desfecho`, `listar_pendencias`)
- `snake_case` no backend Python, `camelCase` no frontend TypeScript
- Constantes em `MAIÚSCULAS`
- Logging com `logging.getLogger(__name__)`
- Dataclass `Settings` com `slots=True` para configuração

---

## ⚠️ Riscos e Pitfalls Comuns

1. **`SyntaxWarning` em `ui.py`** — Escape de regex JS dentro de string Python. Validar com `py_compile`.
2. **`Incorrect datetime value: 'NaT'`** — A sanitização `_sanitize_record_for_sql` deve estar presente antes de inserts.
3. **Editar `frontend-next` achando que é UI principal** — A UI principal do MVP está em `backend/app/routers/ui.py`.
4. **Alterar endpoint sem ajustar JS que consome** — Sempre validar consumo no JavaScript da página afetada em `ui.py`.
5. **Strings multilinha HTML/JS em `ui.py`** — Quebram facilmente por aspas/chaves mal fechadas. Validar sintaxe sempre.
6. **Upload falha em prod mas funciona local** — Verificar variáveis de ambiente no Easypanel e logs do container.
7. **Desfechos automáticos no upload** — Ao importar relatório de internação com `data_alta`, desfechos são criados automaticamente. Para forçar recriação, usar `scripts/gerar_desfechos_do_historico.py`.
8. **Migration 009** — Adiciona coluna `data_obito` na tabela `ocupacao_leitos_ghc`. Necessário aplicar antes de importar novos históricos.

---

## 🏢 Restrições do Ambiente de Trabalho (HFB)

Este projeto é desenvolvido no **Hospital Federal de Bonsucesso**, órgão público com rígidas restrições de rede e bloqueios institucionais que **impedem**:
- Executar a API localmente (`uvicorn`, `pip install`, etc.)
- Instalar bibliotecas Python via pip (bloqueado pelo firewall)
- Rodar testes localmente (`pytest`)
- Acessar repositórios Git ou MySQL de dentro da rede

**Consequência:** todo o desenvolvimento, teste e validação é feito **diretamente no ambiente de produção (Easypanel)**. Não há ambiente local funcional. Comandos de execução local listados neste documento servem apenas para referência ou para uso fora do hospital.

---

## 📚 Documentação de Referência

- [`CONTEXT_AI.md`](CONTEXT_AI.md) — Regras de negócio, estado validado, KPI references
- [`CONTEXT_LLM_MVP.md`](CONTEXT_LLM_MVP.md) — Mapa técnico, onde alterar cada coisa, riscos
- [`STATUS_PROJETO.md`](STATUS_PROJETO.md) — Histórico de entregas e validações
- [`docs/OPERACAO.md`](docs/OPERACAO.md) — Guia de operação e fechamento
- [`informacoes-iniciais/design-system.md`](informacoes-iniciais/design-system.md) — Design system (cores GHC, componentes)
- [`informacoes-iniciais/stack.md`](informacoes-iniciais/stack.md) — Stack tecnológica detalhada
- [`informacoes-iniciais/listas-padronizadas-egaa.md`](informacoes-iniciais/listas-padronizadas-egaa.md) — Listas padronizadas EGAA
- [`backend/DEPLOY_EASYPANEL.md`](backend/DEPLOY_EASYPANEL.md) — Instruções de deploy

---

## 🗺️ Guia Rápido por Tipo de Demanda

| Se precisar... | Vá para... |
|---------------|-----------|
| Alterar layout/gráfico do dashboard | `backend/app/routers/ui.py` (HTML + JS + CSS inline) |
| Adicionar/modificar KPI | `backend/app/routers/censo.py` (endpoint) + `ui.py` (consumo JS) |
| Alterar importação de dados | `src/etl/etl_process.py` (normalize_historico/normalize_censo) |
| Nova migration SQL | Criar em `migrations/` e aplicar com `scripts/apply_migrations.py` |
| Modificar modelo de dados | `backend/app/models.py` + `schemas.py` + migration |
| Trabalhar no frontend Next.js | `frontend-next/src/` (consome API via proxy em `src/app/api/`) |
| Depurar falha de produção | Verificar `/health`, logs do container, variáveis de ambiente |
| Rodar auditoria de dados | `scripts/auditoria_ocupacao_leitos.sql` no MySQL |

---

> 💡 **Dica:** Use `/chronicle improve` para refinar estas instruções iterativamente com base em sessões passadas.
