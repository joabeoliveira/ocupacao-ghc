-- Script para limpar dados de censo de teste/acumulados
-- Antes de executar, verifique quais lotes existem:
-- SELECT DISTINCT data_snapshot, lote_importacao_id, COUNT(*) 
-- FROM ocupacao_leitos_ghc 
-- WHERE fonte_dado = 'censo_diario' 
-- GROUP BY data_snapshot, lote_importacao_id 
-- ORDER BY data_snapshot DESC;

-- 1. Remova APENAS os lotes com data_snapshot diferente do seu CSV atual
--    (substitua '2026-06-25' pela data do seu CSV)
DELETE FROM ocupacao_leitos_ghc
WHERE fonte_dado = 'censo_diario'
  AND data_snapshot != '2026-06-25';

-- 2. Confira se sobrou apenas 1 lote:
-- SELECT data_snapshot, COUNT(*) FROM ocupacao_leitos_ghc 
-- WHERE fonte_dado = 'censo_diario' 
-- GROUP BY data_snapshot;
