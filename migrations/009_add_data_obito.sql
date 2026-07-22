-- Migration 009: Adiciona coluna data_obito na tabela principal
-- O CSV do relatório de internação possui coluna DATA_OBITO separada da DATA_ALTA.
-- Necessário para distinguir corretamente óbitos de altas na geração automática de desfechos.

ALTER TABLE ocupacao_leitos_ghc
  ADD COLUMN data_obito DATETIME NULL AFTER data_alta;
