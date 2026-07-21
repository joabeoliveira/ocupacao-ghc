# Contexto Tecnico para LLMs: MVP EGAA (Estrutura e Arquitetura)

Este documento complementa o CONTEXT_AI.md.
Objetivo: acelerar execucao de tarefas por qualquer LLM com foco em estrutura de codigo, arquitetura, pontos de entrada e padroes de alteracao com baixo risco.

## 0. Como usar este documento junto com CONTEXT_AI.md

Ordem recomendada para qualquer LLM antes de editar:
1. Ler CONTEXT_AI.md para regras de negocio e estado funcional validado.
2. Ler este arquivo para mapa tecnico do codigo e estrategia de mudanca.
3. Localizar o ponto exato de alteracao no arquivo certo.
4. Fazer mudanca minima e validar sintaxe/execucao local.

## 1. Visao arquitetural (alto nivel)

Camadas do MVP:
- Dados/ETL: leitura e normalizacao de arquivos esusreport, com persistencia idempotente no MySQL.
- API backend: FastAPI com routers separados por dominio (censo, EGAA, upload, UI).
- UI principal do MVP: HTML renderizado no backend (nao e o Next.js).
- UI Next.js: existe no repositorio, mas ainda nao e fonte principal para operacao do MVP.

Fluxo principal:
1. Upload de arquivos via UI/endpoint.
2. ETL normaliza e persiste na tabela analitica.
3. Endpoints /api/censo e /api/egaa expoem dados e indicadores.
4. UI HTML consome esses endpoints e renderiza dashboard/listas/acoes.

## 2. Mapa pratico de arquivos criticos

### 2.1 Backend API
- backend/app/main.py
  - Cria app FastAPI.
  - Registra CORS.
  - Inclui routers.
  - Endpoint /health.

- backend/app/routers/censo.py
  - KPIs e listagens de pacientes por snapshot de censo.
  - Endpoint-chave para dashboard e longa permanencia.

- backend/app/routers/egaa.py
  - CRUD de intervencoes, tipos, pendencias e desfechos.
  - Endpoint de indicadores EGAA consumido no dashboard.

- backend/app/routers/upload.py
  - Endpoints de upload (auto, censo, historico).

- backend/app/routers/ui.py
  - UI HTML principal do MVP (paginas e scripts inline).
  - Quase todas as mudancas de interface ficam aqui.

### 2.2 ETL e persistencia
- src/etl/etl_process.py
  - Pipeline principal de parsing, normalizacao e persistencia.
  - Funcoes importantes: prepare_dataframe, normalize_historico, normalize_censo, persist_dataframe.
  - Sanitizacao critica: NaT/NaN/NA para None antes de insert/upsert.

- migrations/*.sql
  - Evolucao de schema e regras de armazenamento.
  - Base da consistencia de dados e compatibilidade de API.

### 2.3 Frontend Next (contexto)
- frontend-next/
  - Estrutura existe e pode evoluir no futuro.
  - Nao assumir como UI principal do MVP sem validacao funcional de importacao.

## 3. Estado atual da UI principal (HTML no backend)

Decisoes consolidadas no MVP:
- Interface principal: backend/app/routers/ui.py.
- Dashboard simplificado para foco operacional.

Mudancas de simplificacao ja aplicadas:
- Removido bloco "Longa permanencia em foco" do dashboard.
- No card "Resultados do EGAA":
  - "Intervencoes por status" convertido para visualizacao em pizza.
  - "Intervencoes por tipo" removido.
- No card "Unidades com mais pacientes":
  - visualizacao convertida para pizza.
- Tabela "Pacientes internados" removida do dashboard.
- Pagina /pacientes retirada do fluxo principal:
  - rota /pacientes mantida apenas com redirect para /dashboard.
  - links de navegacao para /pacientes removidos.
- Na pagina Longa Permanencia:
  - card "Historico EGAA por prontuario" removido do rodape.

## 4. Onde alterar cada tipo de demanda

### 4.1 Alteracao de layout/componente da UI HTML
Arquivo alvo prioritario:
- backend/app/routers/ui.py

Estrutura interna relevante:
- Funcoes de pagina retornam HTML como string multilinha.
- CSS e JavaScript estao inline dentro de cada pagina.
- Alteracoes devem ser pequenas e localizadas para evitar regressao.

### 4.2 Alteracao de dados exibidos na UI
Checar primeiro:
1. endpoint em backend/app/routers/censo.py ou backend/app/routers/egaa.py;
2. consumo do endpoint em script da pagina dentro de backend/app/routers/ui.py.

### 4.3 Alteracao em importacao e consistencia de dados
Arquivo alvo:
- src/etl/etl_process.py

Sempre preservar:
- idempotencia por hash_registro + fonte_dado;
- sanitizacao de nulos para banco;
- regra de snapshot para censo.

## 5. Contratos e pontos de integracao

Endpoints utilizados com mais frequencia pela UI HTML:
- /api/censo/kpis
- /api/censo/pacientes
- /api/censo/paciente/{prontuario}
- /api/egaa/indicadores
- /api/egaa/intervencoes
- /api/egaa/intervencoes/lote
- /api/egaa/tipos-intervencao
- /api/egaa/pendencia/*
- /api/upload/*

Sempre que alterar payload/resposta de endpoint:
1. atualizar consumo no JavaScript da pagina afetada;
2. validar telas que dependem do mesmo endpoint;
3. validar exportacoes quando aplicavel.

## 6. Padrao de trabalho recomendado para LLMs

Checklist antes de editar:
1. Confirmar qual camada sera alterada (UI, API, ETL, migration).
2. Localizar arquivo correto e trecho exato.
3. Evitar refatoracao ampla sem necessidade.

Checklist apos editar:
1. Rodar validacao de sintaxe do arquivo alterado.
2. Se alterou backend Python: compilar arquivo (py_compile) e, quando possivel, rodar testes relacionados.
3. Verificar ausencia de links/rotas obsoletas na UI.
4. Confirmar que mudanca nao quebrou filtros, carregamento inicial e botoes principais.

## 7. Comandos uteis (local)

- Compilar arquivo de UI backend:
  - python -m py_compile backend/app/routers/ui.py

- Rodar API local:
  - uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

- Rodar testes:
  - pytest -q

## 8. Riscos comuns e como evitar

Riscos recorrentes:
- Editar frontend-next achando que e a UI principal do MVP atual.
- Alterar endpoint sem ajustar o JS que consome os campos.
- Remover elemento HTML e esquecer listeners/variaveis associadas.
- Quebrar string multilinha HTML/JS dentro de ui.py por aspas/chaves.

Mitigacoes:
- Sempre validar sintaxe apos mudancas em ui.py.
- Buscar por IDs/nomes removidos para limpar referencias.
- Fazer mudanca minima, em pequenos blocos, com revisao de diff.

## 9. Guia rapido por cenario de tarefa

### Cenario A: "ajustar card/grafico no dashboard"
- Arquivo: backend/app/routers/ui.py (funcao de dashboard).
- Revisar HTML da secao + JS de renderizacao + CSS correspondente.

### Cenario B: "filtro nao retorna dados esperados"
- Verificar query params montados no JS.
- Verificar assinatura e filtros no endpoint correspondente (censo.py/egaa.py).
- Verificar tipo/normalizacao de dados no ETL se erro vier da origem.

### Cenario C: "importacao funciona local e falha em prod"
- Verificar variaveis de ambiente e logs do container.
- Validar rota /health e dependencias de upload.
- Conferir sanitizacao de nulos e formato de datas no ETL.

## 10. Politica de compatibilidade do MVP

Principio geral:
- Preservar comportamento validado em producao provisoria.
- Priorizar estabilidade operacional da UI HTML principal.
- Tratar frontend-next como trilha futura, nao substituta imediata.

## 11. Sugestao de prompt para qualquer LLM neste repositorio

"Leia primeiro CONTEXT_AI.md e CONTEXT_LLM_MVP.md. Em seguida, identifique a camada correta (UI HTML em backend/app/routers/ui.py, API em routers, ETL em src/etl/etl_process.py), proponha mudanca minima sem regressao, aplique e valide sintaxe/testes relevantes."

---
Ultima atualizacao: 2026-07-21
Escopo: MVP EGAA em operacao com UI HTML principal
