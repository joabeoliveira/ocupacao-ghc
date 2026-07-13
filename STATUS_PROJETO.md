# STATUS DO PROJETO - Ocupação NIR / EGAA
Data: 2026-07-10

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

## Atualizações recentes (08/07)

- Implementado campo **Evolução do paciente** na página de detalhe (`/paciente/{prontuario}`):
  - Nova tabela `egaa_evolucao_paciente` (migration `006_create_egaa_evolucao_paciente.sql`).
  - Modelo `EgaaEvolucaoPaciente` em `backend/app/models.py`.
  - Schema `EvolucaoPacienteResponse` e `EvolucaoPacienteUpdate` em `backend/app/schemas.py`.
  - Endpoint `PUT /api/censo/paciente/{prontuario}/evolucao` em `backend/app/routers/censo.py`.
  - Card "Evolução do paciente" logo abaixo do "Resumo clínico" na UI, com textarea grande e botão "Salvar evolução".
  - Evolução carregada automaticamente ao abrir a página do paciente e salva via requisição PUT assíncrona.

## Atualizações recentes (30/06)

- Corrigido o `SyntaxWarning` em `backend/app/routers/ui.py` (escape de regex JavaScript). Commit aplicado no repositório.
- Adicionada uma barra de navegação simples na página de Upload para facilitar retorno às telas principais (`/dashboard`, `/pacientes`, `/configuracoes`).
- Criado o script de seed `scripts/seed_egaa_tipos.py` para popular a tabela `egaa_tipo_intervencao` com a lista padronizada de intervenções.
- Fornecido bloco SQL com `INSERT ... ON DUPLICATE KEY UPDATE` para uso direto no phpMyAdmin (opção recomendada quando o acesso ao MySQL pelo ambiente local não estiver disponível).
- Observação de execução: tentativa de rodar o seed localmente falhou devido a conexão MySQL não acessível no ambiente do agente (ConnectionRefused). Instruções para executar localmente:
   - No PowerShell:

      ```powershell
      $env:PYTHONPATH='backend'
      python scripts/seed_egaa_tipos.py
      ```

   - Ou cole o SQL na aba SQL do phpMyAdmin.

## Atualizações recentes (09-10/07)

### 1. Carga de dados EGAA (evoluções, pendências e intervenções)

- Gerados SQLs de carga a partir da planilha de controle `dados para bd egaa - dados_limpos.csv`:
  - **74 evoluções** → tabela `egaa_evolucao_paciente` (upsert por prontuário)
  - **73 pendências** → tabela `egaa_pendencia_alta` (split por vírgula, mapeamento para códigos padronizados, 30 pacientes)
  - **80 intervenções** → tabela `egaa_intervencao_paciente` (a partir de CSV estruturado com dados de atuação)
- Criados **17 novos tipos de intervenção** na `egaa_tipo_intervencao`:
  - **11 ativos** (aparecem no dropdown em ordem alfabética): Acompanhamento do quadro clínico, Articulação com a rede, Articulação com especialistas, Discussão em round, Encaixe de exame, Entrevista social, Orientação educativa, Planejamento da alta, Solic. acompanhamento da fisioterapia, Solic. acompanhamento da T.O., Solic. acompanhamento do Serviço Social
  - **6 inativos** (só histórico, não poluem o seletor): tipos muito específicos de agendamento/regulação
- SQLs executados no phpMyAdmin com sucesso.

### 2. Scripts auxiliares criados

- `scripts/gerar_pendencias_sql.py` — geração de SQL de pendências com split por vírgula e mapeamento de códigos
- `scripts/gerar_intervencoes_sql.py` — geração de SQL de intervenções a partir de CSV padronizado
- `src/etl/egaa_evolucao_import.py` — script adicional para importação de evoluções
- `src/etl/egaa_carga_atual.py` — estendido com funções `write_pendencias_sql`, `write_evolucoes_sql`, `write_all_sql` e dicionário `PENDENCIA_ROTULOS`

### 3. Limpeza e versionamento

- Commit e push realizados (`2b7f5e3` + `305a63d`)
- Artefatos temporários (`tmp/`) removidos
- `.vscode/` adicionado ao `.gitignore`

## Próximos passos específicos sugeridos

- Validar visualmente na página de detalhe do paciente se evoluções, pendências e intervenções estão sendo exibidas corretamente.
- Validar dropdown `Tipo de intervenção` na página do paciente e confirmar que as 11 opções ativas aparecem em ordem alfabética.
- Realizar deploy da versão mais recente no Easypanel para refletir os novos dados.

