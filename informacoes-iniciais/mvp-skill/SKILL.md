# Skill: Desenvolvimento de MVP — Ocupação de Leitos (esusreport)

## Objetivo

Fornecer um fluxo repetível e verificável para desenvolver o MVP de ocupação de leitos baseado nos documentos: `CONTEXT_AI.md`, `stack.md` e `design-system.md`. A skill exige saneamento de dúvidas antes de iniciar qualquer trabalho prático, evitando retrabalho e uso excessivo de tokens.

## Quando usar

- Ao iniciar o projeto ou uma nova iteração do MVP.
- Antes de aceitar demandas de implementação que dependam de suposições sobre dados, infraestrutura ou requisitos UX.

## Entradas obrigatórias

- [CONTEXT_AI.md](CONTEXT_AI.md) — contexto, regras de negócio e fontes de dados.
- [stack.md](stack.md) — stack técnica proposta.
- [design-system.md](design-system.md) — identidade visual e componentes.

## Saídas esperadas

- Checklist saneamento preenchido e aprovado pelo responsável.
- Plano de trabalho com passos claros (prioridades, subtarefas, responsáveis, critérios de aceite).
- Artefatos iniciais: API spec mínima, esquema de tabela `ocupacao_leitos_esusreport` (esboço), protótipo de telas (wireframes simples) e roteiro de testes básicos.

## Regras da skill (obrigatórias)

1. Antes de qualquer implementação, disparar a etapa de "Saneamento" — listar dúvidas e obter confirmação do usuário/responsável.
2. Todas as decisões técnicas que alterem a stack proposta devem ser anotadas e justificadas.
3. Priorizar entrega incremental: mínimo útil que responde às perguntas de negócio definidas no design system.
4. Validar limpeza e transformação de dados conforme as regras em `CONTEXT_AI.md` (ex.: extrair dígitos de `IDADE_ANOS`, internado se `DATA_ALTA` vazia).

## Perguntas de saneamento (sempre executar)

- Quem é o stakeholder responsável pela validação do MVP? (nome, contato)
  Eu mesmo Joabe Oliveira, responsável pelo projeto, farei a revisão de UX/Design e acessibilidade, garantindo que o design-system seja seguido e que as melhores práticas de acessibilidade sejam aplicadas.

- Qual é o critério mínimo de sucesso do MVP? (ex.: dashboard com ocupação diária por unidade)

  Não definido 

- Com que frequência os arquivos `.xls/.csv` serão entregues e por quem?
Diariamente ou quando necessário, pelo setor responsável do GHC.

- Já existe acesso ao banco MySQL e credenciais para o schema `nir`? Quem fornece?
  Sim eu mesmo tenho acesso ao banco MySQL e credenciais para o schema `nir`. 

- Há limites de privacidade ou anonimização necessários nos dados de pacientes?
  Não, os dados são internos e não serão expostos externamente. No entanto, devem ser tratados com confidencialidade.

- Quais filtros são mandatórios na v1 (Especialidade, Unidade/Enfermaria, intervalo de datas)?
  Especialidade, Unidade/Enfermaria, intervalo de datas

- Confirmação das regras de negócio críticas (ex.: cálculo de tempo de internação, tratamento de idades e status de alta).
  Devem ser definidas conforme o MVP é desenvolvido, mas as regras básicas são: se `DATA_ALTA` estiver em branco, o paciente está internado; `IDADE_ANOS` deve ser convertido para inteiro; tempo de internação calculado em relação à data atual.


- Preferência por testes automatizados (unit/integration) e quais ambientes de deploy devem ser cobertos pela CI?
  
  Sim, testes unitários e de integração são obrigatórios. A CI deve cobrir ambientes de teste e produção, mas vale ressaltar que o ambiente local que estou atualmente há limitação por se tratar de ambiente corporativo e cheio de restrições. Sendo assim os testes devem priorizar o ambiente de produção no easypanel, que é o ambiente de deploy real do MVP.
  
- Existe um prazo alvo para entrega do MVP ou milestones importantes?
  Não definido, mas o MVP deve ser entregue em etapas incrementais, com entregas funcionais a cada iteração.

O fluxo só avança após a aprovação explícita das respostas.

## Fluxo passo a passo (alto nível)

1. Saneamento: aplicar as perguntas acima e anotar decisões.
2. Definir escopo da primeira entrega (ex.: API + página dashboard com três métricas e tabela filtrável).
3. Criar especificação mínima da API (endpoints, contratos, exemplos de payloads) e esquema inicial da tabela `ocupacao_leitos_esusreport`.
4. Implementar pipeline de ingestão: parser robusto para `.xls/.csv` com validações e testes de limpeza (ex.: IDADE_ANOS → inteiro).
5. Backend mínimo: FastAPI com endpoints para obter métricas e lista de leitos/pacientes filtrável.
6. Frontend mínimo: Next.js + Tailwind — página Dashboard + componente DataTable (usando tokens do design-system).
7. Testes e validação de dados: conjunto de testes que cobrem transformações críticas e endpoints.
8. Deploy em ambiente de teste via CI (Easypanel/GitHub Actions) e validação manual com stakeholder.

## Pontos de decisão e alternativas

- Dados inconsistentes frequentes → criar etapa de preview e aprovação manual antes de persistir.
- Falta de acesso ao DB → usar uma camada de armazenamento temporário (SQLite ou arquivos JSON) para prototipação.
- Importação diária com volume alto → adicionar fila de processamento (RabbitMQ/Redis) e jobs assíncronos.

## Critérios de aceite (mínimos)

- Dashboard mostra ocupação global e por unidade com dados do último arquivo processado.
- Filtros por Especialidade e Unidade funcionando e refletidos nas consultas.
- Regras de limpeza aplicadas e logs de erros visíveis para registros rejeitados.
- Endpoints documentados com exemplos (OpenAPI/Swagger).

## Exemplos de prompts para usar esta skill

- "Inicie a skill: saneamento com stakeholder X, prazo 2 semanas, acesso DB sim." 
- "Gerar API spec mínima e esquema da tabela com base nas respostas aprovadas." 
- "Criar parser para CSV seguindo regras de `CONTEXT_AI.md` e testes unitários." 

## Iteração e melhoria

- Após cada entrega, rodar uma sessão de feedback com o stakeholder e atualizar o checklist de saneamento se necessário.
- Registre decisões importantes no repositório (CHANGELOG ou documento `decisions.md`).

## Onde salvar e como invocar

Salvar este arquivo como `informacoes-iniciais/mvp-skill/SKILL.md`. Para executar a skill manualmente, siga as seções "Perguntas de saneamento" e "Fluxo passo a passo".

---
Versão: 1.0 — criado para o repositório `ocupacao-nir`.
