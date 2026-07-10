-- Pendências para alta geradas a partir da planilha de controle do EGAA.
-- Cada pendência é um registro separado (split por vírgula).
-- Não duplica registros existentes (usa WHERE NOT EXISTS).

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8399062', 'regulacao', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8399062' AND codigo='regulacao');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8399062', 'manejo_clinico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8399062' AND codigo='manejo_clinico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8399062', 'transporte_sanitario_eletivo', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8399062' AND codigo='transporte_sanitario_eletivo');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '163119', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='163119' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '163119', 'descompensacao_clinica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='163119' AND codigo='descompensacao_clinica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '2231704', 'definicao_diagnostica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='2231704' AND codigo='definicao_diagnostica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '2231704', 'manejo_clinico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='2231704' AND codigo='manejo_clinico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429434', 'cuidados_pos_operatorios', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429434' AND codigo='cuidados_pos_operatorios');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429434', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429434' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429434', 'descompensacao_clinica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429434' AND codigo='descompensacao_clinica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8417830', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8417830' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8417830', 'cuidados_pos_operatorios', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8417830' AND codigo='cuidados_pos_operatorios');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8417830', 'descompensacao_clinica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8417830' AND codigo='descompensacao_clinica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8380681', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8380681' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8380681', 'descompensacao_clinica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8380681' AND codigo='descompensacao_clinica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8422810', 'manejo_clinico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8422810' AND codigo='manejo_clinico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8421512', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8421512' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8421512', 'descompensacao_clinica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8421512' AND codigo='descompensacao_clinica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '2054019', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='2054019' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '2054019', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='2054019' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8243725', 'biopsia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8243725' AND codigo='biopsia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8243725', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8243725' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8336103', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8336103' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8336103', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8336103' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8336103', 'manejo_sintomatico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8336103' AND codigo='manejo_sintomatico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8390556', 'procedimento_cirurgico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8390556' AND codigo='procedimento_cirurgico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8382864', 'exame_pendente', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8382864' AND codigo='exame_pendente');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8382864', 'definicao_terapeutica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8382864' AND codigo='definicao_terapeutica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8413091', 'ajuste_medicamento', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8413091' AND codigo='ajuste_medicamento');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8413091', 'definicao_diagnostica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8413091' AND codigo='definicao_diagnostica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8413091', 'definicao_terapeutica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8413091' AND codigo='definicao_terapeutica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8413091', 'resultado_exame_pendente', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8413091' AND codigo='resultado_exame_pendente');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8401430', 'manejo_clinico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8401430' AND codigo='manejo_clinico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8401430', 'definicao_terapeutica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8401430' AND codigo='definicao_terapeutica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8422196', 'exame_pendente', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8422196' AND codigo='exame_pendente');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1387163', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1387163' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1387163', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1387163' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1387163', 'regulacao', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1387163' AND codigo='regulacao');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8301440', 'definicao_diagnostica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8301440' AND codigo='definicao_diagnostica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8301440', 'manejo_sintomatico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8301440' AND codigo='manejo_sintomatico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8301440', 'exame_pendente', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8301440' AND codigo='exame_pendente');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8423357', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8423357' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8423357', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8423357' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1250960', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1250960' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1250960', 'fragilidade_familiar', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1250960' AND codigo='fragilidade_familiar');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1250960', 'aguardando_documentacao', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1250960' AND codigo='aguardando_documentacao');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8421778', 'manejo_sintomatico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8421778' AND codigo='manejo_sintomatico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8421778', 'definicao_terapeutica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8421778' AND codigo='definicao_terapeutica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8422486', 'realizando_tratamento_terapeutico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8422486' AND codigo='realizando_tratamento_terapeutico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8422486', 'exame_pendente', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8422486' AND codigo='exame_pendente');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8110761', 'procedimento_cirurgico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8110761' AND codigo='procedimento_cirurgico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8110761', 'cuidados_paliativos', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8110761' AND codigo='cuidados_paliativos');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8110761', 'tratamento_oncologico_regulacao', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8110761' AND codigo='tratamento_oncologico_regulacao');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8416248', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8416248' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8416248', 'regulacao_clinica_satelite_hd', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8416248' AND codigo='regulacao_clinica_satelite_hd');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8416248', 'resultado_exame_pendente', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8416248' AND codigo='resultado_exame_pendente');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8416248', 'procedimento_cirurgico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8416248' AND codigo='procedimento_cirurgico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1373852', 'tratamento_lesoes', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1373852' AND codigo='tratamento_lesoes');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1373852', 'exame_pendente', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1373852' AND codigo='exame_pendente');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '1373852', 'reavaliacao_medica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='1373852' AND codigo='reavaliacao_medica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8083480', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8083480' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8083480', 'descompensacao_clinica', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8083480' AND codigo='descompensacao_clinica');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8083480', 'procedimento_cirurgico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8083480' AND codigo='procedimento_cirurgico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429429', 'tratamento_lesoes', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429429' AND codigo='tratamento_lesoes');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429429', 'aguarda_parecer_especialista', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429429' AND codigo='aguarda_parecer_especialista');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429429', 'manejo_clinico', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429429' AND codigo='manejo_clinico');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429429', 'fragilidade_familiar', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429429' AND codigo='fragilidade_familiar');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8429429', 'orientacao_educativa', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8429429' AND codigo='orientacao_educativa');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8377747', 'aguarda_padi_pmec', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8377747' AND codigo='aguarda_padi_pmec');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8410268', 'antibioticoterapia', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8410268' AND codigo='antibioticoterapia');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8410268', 'regulacao_clinica_satelite_hd', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8410268' AND codigo='regulacao_clinica_satelite_hd');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8410268', 'transporte_sanitario_eletivo', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8410268' AND codigo='transporte_sanitario_eletivo');

INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)
SELECT '8388949', 'aguarda_padi_pmec', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS
  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='8388949' AND codigo='aguarda_padi_pmec');
