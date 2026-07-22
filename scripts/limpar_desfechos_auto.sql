-- Limpa todos os desfechos importados automaticamente do histórico.
-- Desfechos registrados manualmente pelo EGAA têm usuario_responsavel preenchido.
-- Esta query mantém apenas os que foram cadastrados manualmente.
DELETE FROM egaa_desfecho WHERE usuario_responsavel IS NULL;
