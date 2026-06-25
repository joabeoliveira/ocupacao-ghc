# Contexto do Projeto: Painel de Regulação e Censo (EGAA)

## 1. Visão Geral

Este MVP foi concebido para resolver a lentidão e a falta de padronização na geração de relatórios, painéis e análise de dados no cenário hospitalar.

Atualmente perdemos muito tempo com a extração manual de dados do sistema `esusreport`, que é feito diariamente, e com a manipulação de planilhas para gerar relatórios e painéis de controle. Isso resulta em atrasos na tomada de decisões e na identificação de problemas relacionados à ocupação hospitalar.

Exemplos:

- O controle do EGAA (Escritório de Gestão da Admissão e Alta) é feito via planilhas manuais atualizadas diariamente, dificultando o acompanhamento ágil de pacientes de longa permanência para atuar na desospitalização.

- A análise de ocupação hospitalar é feita com base em planilhas, o que não permite uma visão clara e rápida da situação atual, dificultando a tomada de decisões estratégicas.

- Não conseguimos responder com celeridade demandas judiciais, como a criação de relatórios para demonstrar os motivos da redução da disponibilidade de leitos, devido à falta de padronização e automação na geração de relatórios.

- Não conseguimos responder rapidamente a demandas internas, como a criação de relatórios para demonstrar os motivos da redução da disponibilidade de leitos, devido à falta de padronização e automação na geração de relatórios.

## 2. Fontes de Dados

* **Origem principal:** Exportações manuais em formato `.xls` do sistema `esusreport`.
* **Arquivo de referência para estrutura:** `relatório de internação - esusreport - censo hospitalar.csv` "relatório de internação - esusreport".

## 3. Infraestrutura & Stack

* **Ambiente:** VPS gerenciada via Easypanel com deploy automatizado via GitHub (CI/CD).
* **Banco de Dados:** MySQL (compartilhado em rede com outro MVP existente) `nir`.
* **Tabela Alvo:** `ocupacao_leitos_esusreport` (Isolada da tabela `historico_ocupacao_completo` para evitar colisão de regras).

## 4. Regras Críticas de Negócio para a IA (evolutiva)

* **Censo Ativo:** Se `DATA_ALTA` estiver em branco, o paciente está internado. O tempo de internação deve ser calculado dinamicamente em relação à data atual.
* **Limpeza de Dados:** A coluna `IDADE_ANOS` vem formatada como string (ex: "74a"). É mandatório extrair apenas os dígitos numéricos antes de persistir no banco de dados.
* **Filtros Obrigatórios:** O painel deve permitir filtrar por Especialidades (Garantir suporte à nomenclatura exata como "DERMATO", "MEDICINA INTENSIVA", etc.) e por Unidade/Enfermaria.

Repositório github: [https://github.com/joabeoliveira/ocupacao-ghc](https://github.com/joabeoliveira/ocupacao-ghc)

## 5. Estratégia de Ingestão de Dados

* **Carga Inicial Histórica:** Utiliza o arquivo `relatorio de internacao.csv` para popular o banco com dados retroativos de 1 ano (contém altas e internações ativas).

* **Atualização Diária (Censo):** Utiliza o arquivo `censo hospitalar.csv` para atualizar o estado dos leitos diariamente (foco em pacientes internados e gestão de giro de leito).