# STATUS DO PROJETO - Ocupação NIR / EGAA
Data: 2026-06-28

## Situação atual

O MVP evoluiu para cobrir:
- painel de pacientes internados;
- longa permanência;
- página de detalhe do paciente;
- registro de atuações EGAA em lote;
- catálogo técnico de listas padronizadas;
- exportações e indicadores básicos.

O projeto retomou o foco na carga inicial/atualização do banco com a planilha de controle do EGAA.

## O que já está pronto

- UI com dashboard, pacientes, longa permanência, configurações e detalhe do paciente.
- Registro de múltiplas atuações por paciente.
- Campo `data_atuacao` para permitir lançamento retroativo correto.
- Linha do tempo do paciente exibindo a atuação e a data correspondente.
- Resumo EGAA na longa permanência com destaque para pacientes com atuações.
- Catálogo técnico de listas padronizadas em `informacoes-iniciais/listas-padronizadas-egaa.md`.
- Migration nova para `data_atuacao` em `migrations/003_add_data_atuacao_egaa_intervencao.sql`.

## O que ainda depende de decisão

- Como transformar a planilha atual em carga confiável para o banco.
- Como tratar campos mistos da planilha, especialmente:
  - evoluções EGAA;
  - pendências para alta;
  - intervenções EGAA;
  - procedimentos e informações textuais que não devem ir direto para ocupação.

## Próximos passos recomendados

1. Executar a carga assistida gerada pela planilha atual.
   - separar ocupação/censo de atuações EGAA;
   - gerar arquivos limpos para importação segura.

2. Validar o resultado da carga.
   - conferir páginas `dashboard`, `pacientes` e `longa-permanencia`;
   - confirmar se os vínculos 1 paciente -> N atuações ficaram corretos.

3. Aplicar a migration `003_add_data_atuacao_egaa_intervencao.sql` se ainda não estiver ativa em produção.
   - garantir lançamento retroativo correto das atuações.

4. Evoluir a importação assistida, se necessário.
   - carregar atuações como eventos independentes;
   - manter a rastreabilidade dos textos da planilha original.

## Ponto de atenção

A planilha atual mistura:
- ocupação assistencial;
- evoluções;
- pendências;
- intervenções;
- textos livres de acompanhamento.

Por isso, a carga direta sem saneamento tende a gerar inconsistência. O melhor caminho é usar a carga assistida antes de importar.

## Próxima ação sugerida

Próximo passo imediato:
- gerar os arquivos de carga assistida com a planilha atual;
- revisar a separação entre ocupação e atuações EGAA;
- importar primeiro a ocupação e depois as atuações.
