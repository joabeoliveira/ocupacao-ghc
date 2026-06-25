# SKILL: Desenvolvimento do MVP de Ocupação de Leitos (EGAA)

## Objetivo

Criar uma skill orientada e reutilizável para guiar o desenvolvimento do MVP de ocupação de leitos com base nos documentos: [CONTEXT_AI.md](CONTEXT_AI.md), [informacoes-iniciais/stack.md](informacoes-iniciais/stack.md) e [informacoes-iniciais/design-system.md](informacoes-iniciais/design-system.md). Antes de iniciar qualquer implementação, todas as dúvidas sobre fluxo e requisitos devem ser saneadas para evitar retrabalho e uso excessivo de tokens.

## Escopo

- Escopo: workspace (orientada ao repositório do projeto)
- Saída: checklist inicial, backlog mínimo viável, tarefas técnicas e artefatos (esquemas, endpoints, componentes)

## Pré-requisitos

- Arquivos de referência: [CONTEXT_AI.md](CONTEXT_AI.md), [informacoes-iniciais/stack.md](informacoes-iniciais/stack.md), [informacoes-iniciais/design-system.md](informacoes-iniciais/design-system.md)
- Acesso ao repositório e permissões de deploy/CI quando for necessário

## Resultado esperado

- Backlog inicial priorizado para o MVP
- Rotinas ETL/ingest mínimas e validadas
- Endpoints FastAPI para consumo frontend
- Páginas/Componentes Next.js seguindo o design-system
- Critérios de aceitação e checklist de QA

## Processo passo-a-passo

1. Saneamento de dúvidas (obrigatório) — responder todas as perguntas da seção "Perguntas essenciais" abaixo.
2. Inventário de dados — inspecionar amostras de exportações (`.xls`/`.csv`) e mapear colunas.
3. Regras de limpeza e validação — implementar transformações críticas (ex.: `IDADE_ANOS` → extrair dígitos; `DATA_ALTA` em branco → paciente internado; cálculo de tempo de internação relativo à data atual).
4. Modelagem & DB — definir esquema `ocupacao_leitos_esusreport` e scripts de migração.
5. Implementar ETL — script Python (Pandas) para normalizar e inserir no MySQL com logs e rollback parcial.
6. Backend — endpoints FastAPI: ingestão, listagem com filtros (especialidade, unidade/enfermaria), métricas, healthcheck.
7. Frontend — páginas Next.js: `Dashboard`, `Leitos`, `Pacientes`, `Relatórios`, utilizando componentes do design-system.
8. Testes & QA — testes unitários e integração para regras críticas; verificação de acessibilidade (WCAG AA) e responsividade.
9. Deploy & CI — pipeline para rodar ETL programado/manual, migrar DB e publicar frontend/backend.
10. Iterar com base em feedback e monitoramento (logs e métricas de uso).

## Pontos de decisão / branching

- Ingestão: batch diário vs. upload manual ad-hoc
- Persistir dados brutos + transformados vs. apenas transformados
- Normalização de nomenclaturas (ex.: especialidades) automatizada por lookup ou manual
- Armazenar histórico completo de mudanças ou apenas snapshot diário

## Critérios de aceitação (QA)

- Filtros Obrigatórios: por período, filtros por Especialidade e Unidade funcionais e com nomenclatura exata.
- Censo Ativo: registros com `DATA_ALTA` em branco aparecem como internados e tempo de internação calculado corretamente.
- Idade: `IDADE_ANOS` normalizada para inteiro (ex.: "74a" → 74).
- Testes: cobertura mínima nos módulos críticos (ingestão/limpeza/filtragem).
- Acessibilidade e responsividade conforme design-system.

## Perguntas essenciais (saneamento de dúvidas)

Responda essas perguntas antes de solicitar geração de backlog ou início de implementação.

- Com que frequência receberemos os arquivos exportados do `esusreport`? (diária, semanal, ad-hoc) 
No primeiro momento serão injetados no banco de dados os dados do arquvivo que será importado com um período de um ano ou mais que normalmente vem com o nome
`HFB.internacao.relatorio-internacao.13.d9pou7sjnefkcqc3k6cb50fnh7 (1)` no formato xls. Depois o banco será atualizado com informações do arquivo de censo hospitala diariamente ou quando for necessário normalmente com o nome  `HFB.internacao.relatorio-censo-hospitalar.33.d9pou7sjnefkcqc3k6cb50fnh7`.

Obs: O nome é definido na hora que é importado.

- Haverá um naming convention fixo para os arquivos? Qual o padrão?

No primeiro momento serão injetados no banco de dados os dados do arquvivo que será importado com um período de um ano ou mais que normalmente vem com o nome
`HFB.internacao.relatorio-internacao.13.d9pou7sjnefkcqc3k6cb50fnh7 (1)` no formato xls. Depois o banco será atualizado com informações do arquivo de censo hospitala diariamente ou quando for necessário normalmente com o nome  `HFB.internacao.relatorio-censo-hospitalar.33.d9pou7sjnefkcqc3k6cb50fnh7`.

- Quem é responsável por fazer uploads/validações manuais (usuário final) vs. automatizar via SFTP/integração?
Usuário final fará o upload manualmente, mas a skill deve permitir que seja automatizado via SFTP/integração no futuro.

- Qual o ambiente alvo do deploy (credenciais, host do MySQL, secrets)?
easypanel puxando diretamente do github a versão mais recente do repositório. 

# Configuração de conexão com o banco de dados MySQL
DATABASE_URL=mysql://joabeoliveira:114211Jo@site_nir:3306/nir
# Chave secreta Flask
SECRET_KEY=114211Jo

- Precisamos manter os arquivos brutos no repositório/armazenamento? Por quanto tempo (retention)?
Não é preciso manter os arquivos brutos no repositório/armazenamento, mas é importante manter um histórico de pelo menos 30 dias para auditoria e rastreabilidade.

- Há uma lista mestra de especialidades/unidades ou precisamos construir um mapeamento?
Precisamos mapear todas as colunas dos arquivos antes de prosseguir com a implementação. A lista mestra de especialidades/unidades deve ser construída com base nos dados existentes e validada com o stakeholder.

- Regras de confidencialidade / anonimização necessárias antes do armazenamento?
Não é necessário anonimizar os dados, mas é importante garantir que o acesso ao banco de dados seja restrito a usuários autorizados e que haja logs de acesso para auditoria.

- Métricas/indicadores essenciais no MVP (ex.: taxa de ocupação, leitos livres por unidade)?

Os KPIs e gráficos essenciais para o MVP incluem:

- Taxa de ocupação geral
- Taxa de ocupação operacional
- Taxa de ocupação ajustada
- Leitos ocupados
- Leitos livres
- Leitos bloqueados
- Leitos impedidos
- Leitos em manutenção
- Leitos por unidade/enfermaria
- Leitos por especialidade

Módulo EGAA (escritório de gestão da admissão e alta):

- Total de pacientes internados:
  - Longa permanência geral (acima de 30 dias)
  - Pacientes acima de 60 anos
  - Pacientes de Longa permanência paciente com mais de 60 anos

- Tempo médio de permanência
  - Pacientes acima de 60 anos
  - Pacientes de longa permanência
  - Pacientes de longa permanência acima de 60 anos

- Giro de leitos
  - Tempo médio de permanência

- Altas c/ intervenção do EGAA
  - Total de altas c/ intervenção do EGAA
  - Total de altas c/ intervenção do EGAA acima de 60 anos
  - Total de altas c/ intervenção do EGAA de longa permanência
  - Total de altas c/ intervenção do EGAA por periodo (mensal, trimestral, anual)

- Total de Pacientes prontos para operar
- Total de pacientes com pendências para operar


- Responsável pela revisão de UX/Design (confirmação do design-system) e acessibilidade?
Eu mesmo Joabe Oliveira, responsável pelo projeto, farei a revisão de UX/Design e acessibilidade, garantindo que o design-system seja seguido e que as melhores práticas de acessibilidade sejam aplicadas.


## Como usar esta skill (exemplos de prompts)

- "Saneie dúvidas" — pede para o agente listar e anotar respostas das Perguntas essenciais.
- "Gerar backlog inicial para MVP" — após responder às perguntas essenciais, gera tarefas com prioridade.
- "Criar endpoint de ingestão" — gera código exemplar FastAPI + teste unitário para ingestão.
- "Gerar script ETL para arquivo X" — cria script Pandas baseado na amostra de arquivo enviada.

## Iteração e manutenção

- Após cada iteração, revisar: dados ingeridos, tickets abertos, falhas de ETL e feedback do usuário.
- Atualizar a skill com novos padrões de arquivo ou mapeamentos quando necessários.

## Local deste arquivo

Salvo em: [informacoes-iniciais/SKILL.md](informacoes-iniciais/SKILL.md)

---
