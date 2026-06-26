-- Auditoria operacional da tabela ocupacao_leitos_ghc após carga histórica/censo.
-- Execute no MySQL conectado ao banco configurado para o EGAA.

-- 1. Resumo geral por fonte de dado.
SELECT
  fonte_dado,
  COUNT(*) AS total_registros,
  COUNT(DISTINCT hash_registro) AS hashes_distintos,
  COUNT(DISTINCT lote_importacao_id) AS lotes_distintos,
  MIN(data_internacao) AS primeira_internacao,
  MAX(data_internacao) AS ultima_internacao,
  MAX(data_snapshot) AS ultimo_snapshot
FROM ocupacao_leitos_ghc
GROUP BY fonte_dado
ORDER BY fonte_dado;

-- 2. Registros por lote para reconciliar linhas processadas versus linhas persistidas/upserts.
SELECT
  lote_importacao_id,
  fonte_dado,
  nome_arquivo,
  COUNT(*) AS total_registros,
  MIN(created_at) AS primeira_linha_criada,
  MAX(created_at) AS ultima_linha_criada
FROM ocupacao_leitos_ghc
GROUP BY lote_importacao_id, fonte_dado, nome_arquivo
ORDER BY ultima_linha_criada DESC, lote_importacao_id;

-- 3. Verificação de campos obrigatórios ou críticos ausentes.
SELECT
  SUM(CASE WHEN prontuario IS NULL OR TRIM(prontuario) = '' THEN 1 ELSE 0 END) AS sem_prontuario,
  SUM(CASE WHEN especialidade IS NULL OR TRIM(especialidade) = '' THEN 1 ELSE 0 END) AS sem_especialidade,
  SUM(CASE WHEN hash_registro IS NULL OR TRIM(hash_registro) = '' THEN 1 ELSE 0 END) AS sem_hash,
  SUM(CASE WHEN lote_importacao_id IS NULL OR TRIM(lote_importacao_id) = '' THEN 1 ELSE 0 END) AS sem_lote,
  SUM(CASE WHEN data_internacao IS NULL THEN 1 ELSE 0 END) AS sem_data_internacao
FROM ocupacao_leitos_ghc;

-- 4. Datas incoerentes que precisam ser revisadas antes da homologação.
SELECT
  id,
  prontuario,
  nome_paciente,
  data_internacao,
  data_alta,
  fonte_dado,
  lote_importacao_id
FROM ocupacao_leitos_ghc
WHERE data_alta IS NOT NULL
  AND data_internacao IS NOT NULL
  AND data_alta < data_internacao
ORDER BY data_alta DESC
LIMIT 100;

-- 5. Garantia lógica do censo: todo censo_diario deve ter data_snapshot.
SELECT COUNT(*) AS censo_sem_snapshot
FROM ocupacao_leitos_ghc
WHERE fonte_dado = 'censo_diario'
  AND data_snapshot IS NULL;

-- 6. Duplicidades lógicas por hash, útil caso a UNIQUE constraint não esteja aplicada no ambiente.
SELECT
  fonte_dado,
  hash_registro,
  COUNT(*) AS ocorrencias
FROM ocupacao_leitos_ghc
GROUP BY fonte_dado, hash_registro
HAVING COUNT(*) > 1
ORDER BY ocorrencias DESC
LIMIT 100;

-- 7. KPIs-base para comparar com GET /api/censo/kpis.
SELECT
  COUNT(*) AS total_internados,
  SUM(CASE WHEN dias_internacao >= 15 THEN 1 ELSE 0 END) AS longa_permanencia_15,
  SUM(CASE WHEN dias_internacao >= 30 THEN 1 ELSE 0 END) AS longa_permanencia_30
FROM ocupacao_leitos_ghc
WHERE data_alta IS NULL;

-- 8. Distribuição de internados ativos por unidade/especialidade.
SELECT
  unidade,
  especialidade,
  COUNT(*) AS total_internados
FROM ocupacao_leitos_ghc
WHERE data_alta IS NULL
GROUP BY unidade, especialidade
ORDER BY total_internados DESC, unidade, especialidade;
