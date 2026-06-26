# Backlog Técnico EGAA

Fonte: `ajustes.md` e `informacoes-iniciais/mvp-skill/SKILL.md`

## Objetivo

Transformar a área de longa permanência do EGAA em um fluxo operacional completo para acompanhar pacientes de risco, registrar intervenções, controlar pendências e apoiar decisões sobre alta, desospitalização e priorização assistencial.

## Princípios de priorização

- Prioridade 1: identificar rapidamente pacientes `>15 dias`, `>30 dias` e `>60 anos`.
- Prioridade 2: permitir registro de intervenções e pendências por paciente.
- Prioridade 3: entregar visão gerencial com KPIs e gráficos de evolução.
- Prioridade 4: habilitar exportação e parametrização do fluxo.

---

## Épico 1. Base de dados e modelo operacional

### BT-E1.1 - Criar tabela de tipos de intervenção
- Objetivo: permitir cadastro dos tipos de intervenção usados pelo EGAA.
- Tarefas:
  - criar migration da tabela `egaa_tipo_intervencao`;
  - incluir campos para nome, descrição, ativo/inativo e ordem de exibição;
  - criar seed inicial com:
    - `Evolução EGAA`
    - `Pendência para alta`
    - `Intervenção EGAA`
    - `Acompanhamento de paciente crônico`
    - `Risco de readmissão`
- Dependência: nenhuma.
- Critério de aceite:
  - tipos de intervenção podem ser cadastrados e listados;
  - ao menos os tipos iniciais existem após a migration.

### BT-E1.2 - Criar tabela de intervenções por paciente
- Objetivo: armazenar o histórico operacional por paciente.
- Tarefas:
  - criar migration da tabela `egaa_intervencao_paciente`;
  - vincular com paciente, tipo de intervenção, usuário, data/hora, observação e status;
  - permitir vínculo opcional com alta, óbito ou transferência;
  - indexar por paciente, data e tipo.
- Dependência: BT-E1.1.
- Critério de aceite:
  - uma intervenção pode ser registrada e consultada por paciente;
  - o histórico aparece em ordem cronológica.

### BT-E1.3 - Estruturar campos de pendência e acompanhamento
- Objetivo: suportar o acompanhamento de pendências para alta.
- Tarefas:
  - criar campos para status da pendência;
  - criar campos para data prevista, data de conclusão e observação;
  - padronizar valores de status.
- Dependência: BT-E1.2.
- Critério de aceite:
  - pendências podem ser abertas, concluídas e revisadas.

---

## Épico 2. Longa permanência

### BT-E2.1 - Tornar a página de longa permanência a área principal
- Objetivo: centralizar a operação do EGAA.
- Tarefas:
  - manter `dashboard` com resumo executivo;
  - criar navegação clara para `Pacientes`, `Longa Permanência` e `Configurações`;
  - destacar a página de longa permanência como foco operacional.
- Dependência: nenhuma.
- Critério de aceite:
  - o usuário identifica rapidamente a área principal do EGAA;
  - a navegação leva para as páginas operacionais corretas.

### BT-E2.2 - Implementar filtros operacionais prioritários
- Objetivo: localizar casos críticos rapidamente.
- Tarefas:
  - filtrar por `>15 dias`;
  - filtrar por `>30 dias`;
  - filtrar por `>60 anos`;
  - filtrar por `>30 dias e >60 anos`;
  - manter filtros por unidade, especialidade e período.
- Dependência: BT-E2.1.
- Critério de aceite:
  - filtros combinados retornam o recorte esperado;
  - a tela exibe o total encontrado e a paginação corretamente.

### BT-E2.3 - Criar visual de prioridade assistencial
- Objetivo: evidenciar pacientes que exigem atenção imediata.
- Tarefas:
  - destacar pacientes com mais tempo de permanência;
  - destacar pacientes acima de 60 anos;
  - priorizar pacientes com combinação de risco;
  - usar badges/status visuais.
- Dependência: BT-E2.2.
- Critério de aceite:
  - o usuário consegue bater o olho e identificar prioridades.

### BT-E2.4 - Exibir KPIs operacionais da longa permanência
- Objetivo: mostrar indicadores-chave do EGAA.
- KPIs mínimos:
  - total de internados;
  - longa permanência geral (`>30 dias`);
  - pacientes acima de 60 anos;
  - longa permanência acima de 60 anos;
  - tempo médio de permanência;
  - altas com intervenção EGAA;
  - óbitos;
  - transferências;
  - admitidos no dia.
- Dependência: BT-E1.2.
- Critério de aceite:
  - KPIs aparecem no painel e respondem aos filtros.

### BT-E2.5 - Gráficos de evolução mensal e trimestral
- Objetivo: acompanhar a evolução da gestão ao longo do tempo.
- Tarefas:
  - gráfico mensal dos principais indicadores;
  - gráfico trimestral dos principais indicadores;
  - séries de longa permanência, altas, óbitos e transferências;
  - visual por clínica/unidade.
- Dependência: BT-E2.4.
- Critério de aceite:
  - gráficos refletem o recorte selecionado;
  - a leitura gerencial fica clara.

---

## Épico 3. Registro de intervenções

### BT-E3.1 - Formulário de registro de intervenção
- Objetivo: permitir inclusão de intervenções no paciente.
- Tarefas:
  - criar formulário na página do paciente;
  - selecionar tipo de intervenção;
  - informar observação livre;
  - salvar data/hora automática e usuário responsável.
- Dependência: BT-E1.1 e BT-E1.2.
- Critério de aceite:
  - uma intervenção pode ser salva e aparece no histórico do paciente.

### BT-E3.2 - Linha do tempo do paciente
- Objetivo: mostrar histórico de ações do EGAA.
- Tarefas:
  - exibir evoluções, pendências e intervenções em ordem temporal;
  - diferenciar os tipos com badges;
  - permitir consulta rápida do histórico.
- Dependência: BT-E3.1.
- Critério de aceite:
  - o histórico é legível e ajuda na tomada de decisão.

### BT-E3.3 - Atualização de status das pendências
- Objetivo: controlar ciclo de vida das pendências.
- Tarefas:
  - abrir pendência;
  - marcar em andamento;
  - marcar concluída;
  - registrar justificativa da conclusão.
- Dependência: BT-E3.1.
- Critério de aceite:
  - o time consegue rastrear pendências abertas e encerradas.

---

## Épico 4. Configurações EGAA

### BT-E4.1 - Criar página de configurações
- Objetivo: permitir parametrização do sistema pelo EGAA.
- Tarefas:
  - criar rota `/configuracoes`;
  - listar tipos de intervenção;
  - permitir ativar/desativar tipos;
  - permitir reorganizar a ordem de exibição.
- Dependência: BT-E1.1.
- Critério de aceite:
  - tipos de intervenção podem ser administrados sem mexer no código.

### BT-E4.2 - Parametrizar categorias adicionais
- Objetivo: permitir extensão do fluxo operacional.
- Tarefas:
  - cadastrar categorias como acompanhamento crônico e risco de readmissão;
  - permitir novos rótulos futuros;
  - manter compatibilidade com o histórico já salvo.
- Dependência: BT-E4.1.
- Critério de aceite:
  - o EGAA consegue adaptar o sistema ao fluxo local.

---

## Épico 5. Exportação e relatórios

### BT-E5.1 - Exportar relatório em Excel
- Objetivo: permitir compartilhamento operacional dos dados.
- Tarefas:
  - exportar lista filtrada;
  - exportar KPIs e recortes;
  - exportar histórico de intervenções por paciente.
- Dependência: BT-E2.2 e BT-E3.2.
- Critério de aceite:
  - o arquivo Excel abre com os dados esperados.

### BT-E5.2 - Exportar relatório em PDF
- Objetivo: gerar material para gestão e repasse.
- Tarefas:
  - exportar dashboards/resumos;
  - exportar gráficos principais;
  - exportar visão da longa permanência.
- Dependência: BT-E2.5.
- Critério de aceite:
  - o PDF apresenta os indicadores legíveis e organizados.

---

## Épico 6. Qualidade, testes e validação

### BT-E6.1 - Testes de regras de permanência
- Objetivo: evitar regressão nas classificações.
- Tarefas:
  - testar `>15 dias`;
  - testar `>30 dias`;
  - testar `>60 anos`;
  - testar combinações de filtros.
- Dependência: nenhuma.
- Critério de aceite:
  - os testes passam e protegem a regra de negócio.

### BT-E6.2 - Testes do registro de intervenções
- Objetivo: validar o fluxo operacional.
- Tarefas:
  - testar criação de intervenção;
  - testar listagem do histórico;
  - testar alteração de status de pendência.
- Dependência: BT-E3.1.
- Critério de aceite:
  - a API responde corretamente e os dados são persistidos.

### BT-E6.3 - Validação pós-deploy
- Objetivo: garantir operação em produção.
- Tarefas:
  - checar `GET /health`;
  - checar `GET /api/censo/kpis`;
  - checar `GET /pacientes`;
  - checar `GET /longa-permanencia`;
  - checar `GET /configuracoes`.
- Dependência: BT-E2.1, BT-E4.1.
- Critério de aceite:
  - os endpoints principais sobem e carregam dados.

---

## Ordem recomendada de implementação

1. BT-E1.1, BT-E1.2 e BT-E1.3
2. BT-E2.1, BT-E2.2 e BT-E2.3
3. BT-E3.1, BT-E3.2 e BT-E3.3
4. BT-E4.1 e BT-E4.2
5. BT-E2.4 e BT-E2.5
6. BT-E5.1 e BT-E5.2
7. BT-E6.1, BT-E6.2 e BT-E6.3

## Observação

Este backlog assume que a linha de cuidado do EGAA vai ser construída incrementalmente, começando pela longa permanência e evoluindo para intervenções, configurações e exportações.
