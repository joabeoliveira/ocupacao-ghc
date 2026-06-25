# Saneamento — Checklist validado e Backlog mínimo do MVP

## Resumo das respostas (extraídas de `informacoes-iniciais/mvp-skill/SKILL.md`)

- **Stakeholder / Validação:** Joabe Oliveira — OK
- **Frequência dos arquivos:** Diária ou quando necessário — OK
- **Acesso ao DB (`nir`):** Joabe informou que já possui credenciais — OK
- **Privacidade/Anonimização:** Dados internos; tratados com confidencialidade — OK (sem anonimização exigida)
- **Filtros mandatórios (v1):** Especialidade, Unidade/Enfermaria, intervalo de datas — OK
- **Regras críticas básicas:** `DATA_ALTA` vazio → internado; `IDADE_ANOS` → extrair inteiro; tempo de internação calculado em relação à data atual — Parcial (regras básicas definidas, faltam exceções e validações)
- **Testes:** Unitários e de integração obrigatórios; CI deve priorizar deploy em Easypanel/produção — OK
- **Prazo / milestones:** Não definido — MISSING
- **Critério mínimo de sucesso (MVP):** Não definido — MISSING (recomendo: Dashboard com ocupação por unidade + tabela filtrável)
- **Naming convention para arquivos:** MISSING
- **Retention / armazenamento dos arquivos brutos:** MISSING
- **Lista mestra de especialidades/unidades:** MISSING (necessário para normalização)

## Itens a decidir antes de implementar (prioridade: alta)

1. Definir o critério mínimo de sucesso do MVP (aceitação).  
2. Definir prazo / milestones (sprints ou entregas incrementais).  
3. Confirmar naming convention dos arquivos e método de ingestão (upload manual vs SFTP).  
4. Decidir retenção de arquivos brutos e política de logs/erros.  
5. Fornecer ou autorizar criação de lista mestra de especialidades/unidades para normalização.

## Backlog mínimo priorizado (primeira iteração)

1. Definir Critério de Sucesso e Milestones — Prazo: 1 dia (Joabe) — Prioridade: Alta  
   - Critério sugerido: Dashboard com taxa de ocupação global e por unidade + tabela filtrável com filtros obrigatórios.  
   - Critério de aceite: stakeholder aprova layout e métricas.

2. Especificação API mínima & esquema DB (`ocupacao_leitos_esusreport`) — Prazo: 1-2 dias — Prioridade: Alta  
   - Entregável: OpenAPI parcial + SQL de criação de tabela (colunas mínimas: id, paciente_id, data_internacao, data_alta, idade_anos_int, especialidade, unidade, status, origem_arquivo, import_ts).
   - Aceite: endpoints documentados no Swagger.

3. Script ETL (Pandas) para ingestão e limpeza básica — Prazo: 2-3 dias — Prioridade: Alta  
   - Funções: parse `.xls/.csv`, extrair dígitos de `IDADE_ANOS`, marcar internado se `DATA_ALTA` vazio, validações de campos obrigatórios, log de registros rejeitados.
   - Aceite: testes unitários cobrindo transformações críticas e conjunto de amostras processadas com sucesso.

4. Backend FastAPI mínimo — endpoints: ingestão (trigger), listagem filtrável, métricas — Prazo: 3 dias — Prioridade: Alta  
   - Aceite: endpoints funcionais, retornando dados compatíveis com a API spec.

5. Frontend Next.js — Dashboard simples + DataTable filtrável (Tailwind) — Prazo: 3-5 dias — Prioridade: Alta  
   - Aceite: filtros funcionais e visual coerente com design-system, acessibilidade básica.

6. Testes & CI — Cobertura para ETL e endpoints; pipeline GitHub Actions com deploy em Easypanel — Prazo: 2-4 dias — Prioridade: Média-Alta  
   - Aceite: pipeline executa testes e realiza deploy de teste; healthcheck verde.

7. Data preview / approval UI (opcional inicial) — Prazo: 3 dias — Prioridade: Média  
   - Aceite: permitir revisão manual de registros rejeitados/ambíguos antes de persistir.

8. Observabilidade: logs de ingestão, métricas básicas, painel de erros — Prazo: 2 dias — Prioridade: Média

## Tasks rápidas que eu posso gerar agora

- Gerar OpenAPI parcial + SQL de criação da tabela.  
- Gerar script ETL base em Python (Pandas) com testes unitários.  
- Gerar scaffold inicial FastAPI com endpoints mínimos.  
- Gerar scaffold Next.js com página `Dashboard` e DataTable.

## Próximo passo recomendado

1. Você confirma o critério de sucesso sugerido (Dashboard com ocupação por unidade + tabela filtrável) ou fornece outro?  
2. Confirma prazo/milestones mínimos (ex.: 2 sprints de 2 semanas) ou prefere trabalhar sem prazo fixo?  

Responda 1-2 para eu gerar automaticamente o backlog detalhado e os artefatos iniciais (API spec, SQL e ETL base).
