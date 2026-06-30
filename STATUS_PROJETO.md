# STATUS DO PROJETO - Ocupação NIR / EGAA
Data: 2026-06-30

## Situação atual

A correção do censo diário foi implementada e validada no ambiente provisório, com foco em:
- importação integral do snapshot de leitos (ocupados, livres e bloqueados);
- KPIs consistentes por snapshot de censo diário;
- ajuste de longa permanência usando exclusivamente `dias_internacao` do relatório;
- eliminação de acúmulo indevido no dashboard.

## Entregas concluídas hoje

### 1. Dashboard / KPIs de ocupação

- Inclusão de KPIs no dashboard:
   - leitos ocupados;
   - leitos livres;
   - leitos bloqueados;
   - taxa de ocupação geral;
   - taxa de ocupação operacional;
   - taxa de ocupação ajustada (sem emergência).
- Ajuste solicitado de layout do dashboard:
   - removido KPI `Internados` do painel principal;
   - removido KPI `Taxa de ocupação ajustada (sem emergência)` do painel principal.
- Correção da regra de exclusão de emergência na taxa ajustada:
   - passou a considerar variações no `leito` com sufixo, por exemplo `111.01`, `113.05`, `114.01`.

### 2. Longa permanência

- Página de longa permanência atualizada para exibir exclusivamente os KPIs:
   - total de pacientes internados;
   - permanência >= 15 dias;
   - permanência >= 30 dias;
   - pacientes >= 60 anos;
   - pacientes >= 60 anos com permanência >= 15 dias;
   - pacientes >= 60 anos com permanência >= 30 dias.
- KPIs consumidos do endpoint `/api/censo/kpis` com filtro por data da própria tela.

### 3. Filtros de pesquisa de pacientes

- API `/api/censo/pacientes` com novos filtros:
   - `nome` (busca parcial);
   - `prontuario` (busca parcial).
- API `/api/censo/export/xlsx` alinhada com os mesmos filtros.
- UI (`dashboard`, `pacientes` e `longa-permanencia`) com campos de busca por nome/prontuário.

## Entregas acumuladas desta frente (29/06 -> 30/06)

- Schema:
   - `status_leito` adicionado via migration `004_add_status_leito.sql`;
   - `prontuario` permitido como `NULL` para censo diário via `005_allow_null_prontuario_for_censo.sql`.
- ETL do censo:
   - importação de todas as linhas (ocupado/livre/bloqueado);
   - `status_leito` normalizado e persistido;
   - hash revisado para contexto de leito/snapshot;
   - `dias_internacao` vindo somente de `DIAS INTER.`.
- API de censo:
   - usa `fonte_dado = 'censo_diario'`;
   - usa snapshot mais recente quando data não é informada;
   - KPIs de paciente apenas com `status_leito = 'Ocupado'`.

## Validações já confirmadas

- Snapshot `2026-06-29`:
   - total: `642`;
   - ocupados: `412`;
   - livres: `165`;
   - bloqueados: `65`.
- Longa permanência (ocupados):
   - `>=15`: `152`;
   - `>=30`: `84`;
   - `>=40`: `53`.

## Próximos passos recomendados

1. Realizar deploy da versão mais recente no Easypanel.
2. Validar visualmente dashboard e longa permanência com hard refresh.
3. Conferir resposta do endpoint `/api/censo/kpis` para o snapshot atual.
4. Registrar no documento de operação os KPIs ativos do dashboard e os removidos por decisão funcional.

## Ponto de atenção

- Permanece um `SyntaxWarning` antigo em `backend/app/routers/ui.py` relacionado a escape de regex JavaScript embutida em string Python.
- Não bloqueia execução, mas recomenda-se ajuste posterior de higiene de código.
