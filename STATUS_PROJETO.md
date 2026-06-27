# STATUS DO PROJETO - Ocupação NIR / EGAA
Data: 2026-06-27

## Situação atual

O MVP evoluiu para cobrir:
- painel de pacientes internados;
- longa permanência;
- página de detalhe do paciente;
- registro de atuações EGAA em lote;
- catálogo técnico de listas padronizadas;
- exportações e indicadores básicos.

O projeto está em pausa aguardando uma decisão sobre a melhor estratégia de carga inicial/atualização do banco com a planilha de controle do EGAA.

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
- Se a importação será feita:
  - em um CSV único saneado;
  - em dois CSVs separados;
  - ou via carga assistida por etapas.
- Como tratar campos mistos da planilha, especialmente:
  - evoluções EGAA;
  - pendências para alta;
  - intervenções EGAA;
  - procedimentos e informações textuais que não devem ir direto para ocupação.

## Próximos passos recomendados

1. Definir o formato final da carga.
   - separar ocupação/censo de atuações EGAA;
   - validar quais colunas entram e quais ficam fora.

2. Saneamento da planilha.
   - transformar campos textuais de EGAA em linhas de atuação;
   - remover colunas que são apenas referência diária;
   - padronizar cabeçalhos.

3. Aplicar a migration `003_add_data_atuacao_egaa_intervencao.sql`.
   - só depois da decisão sobre a carga final.

4. Revalidar produção.
   - conferir páginas `dashboard`, `pacientes`, `longa-permanencia` e `configuracoes`;
   - confirmar se a carga escolhida mantém o histórico consistente.

5. Se necessário, criar importador específico para EGAA.
   - carregar atuações como eventos independentes;
   - manter `1 paciente -> N atuações`.

## Ponto de atenção

A planilha atual mistura:
- ocupação assistencial;
- evoluções;
- pendências;
- intervenções;
- textos livres de acompanhamento.

Por isso, a carga direta sem saneamento tende a gerar inconsistência. O melhor caminho é validar a estrutura final antes de importar.

## Próxima ação sugerida

Quando o projeto voltar:
- revisar o CSV final;
- fechar o mapeamento de colunas;
- executar a carga com segurança;
- aplicar a migration pendente se fizer sentido no cenário escolhido.
