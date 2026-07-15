-- Script para limpar dados de censo de teste/acumulados
--
-- Lotes identificados no banco em 15/07/2026:
--   Correto:   9cf6f025-36cd-4256-9814-f748f17c28b9  (641 registros, 441 ocupados)
--   Incorreto: 82b14f34-54e6-4413-8359-683dc2c93909  (88 registros, 61 ocupados)
--   Antigos:   8 lotes de 29/06 a 14/07 (641-642 registros cada)

-- 1. Delete APENAS o lote incorreto de hoje (88 registros)
DELETE FROM ocupacao_leitos_ghc
WHERE lote_importacao_id = '82b14f34-54e6-4413-8359-683dc2c93909';

-- 2. Delete TODOS os lotes antigos (anteriores a 15/07)
DELETE FROM ocupacao_leitos_ghc
WHERE fonte_dado = 'censo_diario'
  AND data_snapshot < '2026-07-15';

-- 3. Confira se sobrou apenas 1 lote (o correto):
-- SELECT lote_importacao_id, data_snapshot, COUNT(*) as total,
--   SUM(CASE WHEN status_leito = 'Ocupado' THEN 1 ELSE 0 END) as ocupados
-- FROM ocupacao_leitos_ghc
-- WHERE fonte_dado = 'censo_diario'
-- GROUP BY lote_importacao_id, data_snapshot;
