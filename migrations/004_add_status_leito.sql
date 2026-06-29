-- Migration: Adiciona coluna status_leito na tabela ocupacao_leitos_ghc
-- Execute este script no banco de dados de produção ou ambiente de testes apropriado.

ALTER TABLE ocupacao_leitos_ghc
ADD COLUMN status_leito VARCHAR(100) NULL AFTER leito;

-- Atualiza registros do censo de 2026-06-29 para marcar como 'Ocupado' quando ausente
UPDATE ocupacao_leitos_ghc
SET status_leito = 'Ocupado'
WHERE fonte_dado = 'censo_diario'
  AND data_snapshot = '2026-06-29'
  AND status_leito IS NULL;
