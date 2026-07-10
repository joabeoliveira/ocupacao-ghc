-- Intervenções EGAA geradas a partir do CSV padronizado.
-- Resolve tipo_intervencao_id via JOIN com egaa_tipo_intervencao.

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8399062', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e definição de condutas clínicas.', 'concluida',
  'ENF EDUARDO', '2026-02-25',
  '2026-02-25', '2026-02-25', 'Round multidisciplinar realizado.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8399062', t.id, 'SOLICITADO ACOMPANHAMENTO DA T.O.',
  'Solicitação de avaliação e acompanhamento pela Terapia Ocupacional.', 'em_andamento',
  'ENF EDUARDO', '2026-04-16',
  '2026-04-20', '2026-04-24', 'TO Lúcia avaliou a paciente.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DA T.O.';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '163119', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica do paciente.', 'em_andamento',
  'ENF EDUARDO', '2026-06-19',
  '2026-06-19', NULL, 'Paciente em VM, sem previsão de alta.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '163119', t.id, 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL',
  'Solicitação de intervenção do Serviço Social para aspectos biopsicossociais.', 'em_andamento',
  'ENF EDUARDO', '2026-06-19',
  '2026-06-22', '2026-06-22', 'Acompanhamento social iniciado.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '2231704', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-06-15',
  '2026-06-15', '2026-06-15', 'Definido encaminhamento para CM.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '2231704', t.id, 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS',
  'Contato e alinhamento com equipes especializadas para suporte ao caso.', 'em_andamento',
  'ENF EDUARDO', '2026-06-15',
  '2026-06-15', '2026-06-15', 'Contato com NIR e gastro realizado.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '2231704', t.id, 'SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR',
  'Solicitação de transferência/movimentação de leito via NIR.', 'em_andamento',
  'ENF EDUARDO', '2026-06-15',
  '2026-06-16', '2026-06-16', 'Movimentação autorizada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8429434', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-07-09',
  '2026-07-09', NULL, 'Paciente em CTI pós-amputação.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8417830', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-07-09',
  '2026-07-09', NULL, 'Pós-operatório de cistectomia.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8380681', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-07-10',
  '2026-07-10', NULL, 'Desmame ventilatório em progresso.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8422810', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-07-09',
  '2026-07-09', NULL, 'Desmame de VM, sem intercorrências.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8425031', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-07-01',
  '2026-07-01', NULL, 'Dados clínicos não detalhados na evolução.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8421512', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-05-28',
  '2026-05-28', '2026-05-28', 'Definição de transferência para CM.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8421512', t.id, 'SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR',
  'Solicitação de movimentação de leito via NIR.', 'em_andamento',
  'ENF EDUARDO', '2026-05-28',
  '2026-05-29', '2026-05-29', 'Transferência solicitada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8421512', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-05-28',
  '2026-05-28', NULL, 'Aguardando RNM e evolução.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '2054019', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-06-18',
  '2026-06-18', NULL, 'Pós-transplante renal com DGF.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8243725', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-07-03',
  '2026-07-03', '2026-07-03', 'Round com definição de condutas.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8243725', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-07-03',
  '2026-07-03', NULL, 'Aguardando biópsia e endoscopia.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8243725', t.id, 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS',
  'Solicitação de celeridade na liberação de resultados laboratoriais.', 'em_andamento',
  'ENF EDUARDO', '2026-07-03',
  '2026-07-03', '2026-07-03', 'Aguardando resultados para definição.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8336103', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-06-16',
  '2026-06-16', NULL, 'Pós-transplantectomia, em uso de NPT.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8336103', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano para alta segura do paciente.', 'em_andamento',
  'ENF EDUARDO', '2026-06-16',
  '2026-07-30', NULL, 'Aguardando melhora clínica para alta.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8390556', t.id, 'SOLICITADO AGILIDADE NA RESPOSTA DO PARECER',
  'Solicitação de priorização na emissão de parecer técnico.', 'em_andamento',
  'ENF EDUARDO', '2026-05-04',
  '2026-05-04', '2026-05-04', 'Parecer da pneumologia obtido.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO AGILIDADE NA RESPOSTA DO PARECER';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8390556', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-05-04',
  '2026-05-04', '2026-05-04', 'Definição de cirurgia e vaga em CTI.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8390556', t.id, 'SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR',
  'Solicitação de movimentação de leito via NIR.', 'em_andamento',
  'ENF EDUARDO', '2026-05-22',
  '2026-05-22', '2026-05-22', 'Vaga de CTI reservada para PO.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8382864', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-05-19',
  '2026-05-19', '2026-05-19', 'Discussão sobre febre e exames.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8382864', t.id, 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS',
  'Alinhamento com equipes especializadas para condução do caso.', 'em_andamento',
  'ENF EDUARDO', '2026-05-19',
  '2026-05-19', '2026-05-19', 'Contato com laboratório e especialistas.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8382864', t.id, 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS',
  'Solicitação de agilidade em exames laboratoriais.', 'em_andamento',
  'ENF EDUARDO', '2026-05-19',
  '2026-05-19', '2026-05-20', 'Exame de urina agilizado.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8382864', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-05-19',
  '2026-05-19', NULL, 'Aguardando RNM e transferência para INC.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8382864', t.id, 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL',
  'Solicitação de intervenção do Serviço Social.', 'em_andamento',
  'ENF EDUARDO', '2026-06-09',
  '2026-06-10', '2026-06-10', 'Avaliação social iniciada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8413091', t.id, 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL',
  'Solicitação de intervenção do Serviço Social.', 'em_andamento',
  'ENF EDUARDO', '2026-04-16',
  '2026-04-17', '2026-04-17', 'Acompanhamento para judicialização.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8413091', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-04-16',
  '2026-04-16', NULL, 'Aguardando CPRE e pareceres.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8413091', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-04-16',
  '2026-04-16', '2026-04-16', 'Definição de condutas diagnósticas.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8413091', t.id, 'SOLICITADO AGILIDADE NA RESPOSTA DO PARECER',
  'Solicitação de priorização na emissão de parecer.', 'em_andamento',
  'ENF EDUARDO', '2026-05-26',
  '2026-05-26', '2026-05-27', 'Parecer para judicialização.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO AGILIDADE NA RESPOSTA DO PARECER';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8401430', t.id, 'SOLICITADO ACOMPANHAMENTO DA T.O.',
  'Solicitação de acompanhamento pela Terapia Ocupacional.', 'em_andamento',
  'ENF EDUARDO', '2026-04-09',
  '2026-04-10', '2026-04-10', 'TO Lúcia atendeu o paciente.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DA T.O.';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8401430', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-04-09',
  '2026-04-09', NULL, 'Aguardando treinamento para diálise peritoneal.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8401430', t.id, 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL',
  'Solicitação de intervenção do Serviço Social.', 'em_andamento',
  'ENF EDUARDO', '2026-04-09',
  '2026-04-10', '2026-04-10', 'Acompanhamento para orientação familiar.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8401430', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-04-09',
  '2026-04-09', '2026-04-09', 'Decisão sobre diálise peritoneal.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8422196', t.id, 'ENCAIXE DE EXAME',
  'Inserção de exame complementar na agenda/rotina do paciente.', 'em_andamento',
  'ENF EDUARDO', '2026-06-09',
  '2026-06-09', '2026-06-09', 'Cistoscopia realizada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ENCAIXE DE EXAME';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8422196', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano para alta hospitalar.', 'em_andamento',
  'ENF EDUARDO', '2026-06-09',
  '2026-07-16', NULL, 'Alta condicionada ao resultado do exame.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1387163', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-04-07',
  '2026-04-07', NULL, 'Aguardando regulação e TC.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1387163', t.id, 'ACOMPANHAMENTO DE AGENDAMENTO DE EXAMES/PROCEDIMENTOS EXTERNOS/REGULAÇÃO NIR',
  'Monitoramento de agendamentos externos e regulação via NIR.', 'em_andamento',
  'ENF EDUARDO', '2026-04-07',
  '2026-04-07', NULL, 'Regulação para transferência.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ACOMPANHAMENTO DE AGENDAMENTO DE EXAMES/PROCEDIMENTOS EXTERNOS/REGULAÇÃO NIR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8301440', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-06-29',
  '2026-06-29', '2026-06-29', 'Definição de exames pendentes.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8301440', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-07-08',
  '2026-07-08', NULL, 'Aguardando USG e EDA.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8301440', t.id, 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS',
  'Alinhamento com equipes especializadas.', 'em_andamento',
  'ENF EDUARDO', '2026-07-08',
  '2026-07-08', '2026-07-08', 'Fisioterapia acionada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8423357', t.id, 'ENTREVISTA SOCIAL',
  'Realização de entrevista com paciente/família para avaliação social.', 'em_andamento',
  'ENF EDUARDO', '2026-06-15',
  '2026-06-15', '2026-06-15', 'Entrevista com familiar realizada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ENTREVISTA SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8423357', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-06-15',
  '2026-06-15', NULL, 'Em tratamento de ITU.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1250960', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-06-29',
  '2026-06-29', '2026-06-29', 'Definição de suporte para alta.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1250960', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano de alta.', 'em_andamento',
  'ENF EDUARDO', '2026-06-29',
  '2026-07-15', NULL, 'Aguardando holter e reabilitação.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1250960', t.id, 'SOLICITADO ACOMPANHAMENTO DA FISIOTERAPIA',
  'Solicitação de avaliação e acompanhamento fisioterapêutico.', 'em_andamento',
  'ENF EDUARDO', '2026-07-07',
  '2026-07-08', '2026-07-08', 'Fisioterapia acionada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DA FISIOTERAPIA';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1250960', t.id, 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL',
  'Solicitação de intervenção do Serviço Social.', 'em_andamento',
  'ENF EDUARDO', '2026-06-29',
  '2026-06-30', '2026-06-30', 'Acompanhamento social para alta.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8421778', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-06-16',
  '2026-06-16', NULL, 'Aguardando estabilidade glicêmica.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8421778', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano de alta.', 'em_andamento',
  'ENF EDUARDO', '2026-06-16',
  '2026-07-30', NULL, 'Depende da regulação de HD.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8422486', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-06-10',
  '2026-06-10', '2026-06-10', 'Discussão sobre exames e condutas.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8422486', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-06-10',
  '2026-06-10', NULL, 'Eletroneuromiografia agendada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8422486', t.id, 'ACOMPANHAR EXAMES/CONSULTAS/PROCEDIMENTOS REGULADOS VIA NIR',
  'Monitoramento de exames e procedimentos regulados pelo NIR.', 'em_andamento',
  'ENF EDUARDO', '2026-06-10',
  '2026-06-10', '2026-06-10', 'Exame externo agendado.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ACOMPANHAR EXAMES/CONSULTAS/PROCEDIMENTOS REGULADOS VIA NIR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8422486', t.id, 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS',
  'Solicitação de agilidade em exames laboratoriais.', 'em_andamento',
  'ENF EDUARDO', '2026-07-08',
  '2026-07-08', '2026-07-08', 'Coleta e resultado agilizados.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8110761', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-06-18',
  '2026-06-18', '2026-06-18', 'Decisão sobre GTT e cuidados paliativos.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8110761', t.id, 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS',
  'Alinhamento com equipes especializadas.', 'em_andamento',
  'ENF EDUARDO', '2026-06-18',
  '2026-06-18', '2026-06-18', 'CG e regulação oncológica acionadas.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8110761', t.id, 'ACOMPANHAR EXAMES/CONSULTAS/PROCEDIMENTOS REGULADOS VIA NIR',
  'Monitoramento de exames e procedimentos regulados via NIR.', 'em_andamento',
  'ENF EDUARDO', '2026-06-18',
  '2026-06-18', NULL, 'Aguardando consulta oncológica.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ACOMPANHAR EXAMES/CONSULTAS/PROCEDIMENTOS REGULADOS VIA NIR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8110761', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano de alta.', 'em_andamento',
  'ENF EDUARDO', '2026-07-08',
  '2026-07-20', NULL, 'Aguardando adaptação ao GTT e treino familiar.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8416248', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-05-11',
  '2026-05-11', '2026-05-11', 'Discussão sobre HD e regulação.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8416248', t.id, 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL',
  'Solicitação de intervenção do Serviço Social.', 'em_andamento',
  'ENF EDUARDO', '2026-05-13',
  '2026-05-14', '2026-05-14', 'Avaliação social para alta.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8416248', t.id, 'Acompanhamento de regulação de HD',
  'Acompanhamento de regulação de alta hospitalar (HD).', 'em_andamento',
  'ENF EDUARDO', '2026-05-11',
  '2026-05-11', NULL, 'Dificuldade de regulação para clínica satélite.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento de regulação de HD';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8416248', t.id, 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS',
  'Solicitação de agilidade em exames laboratoriais.', 'em_andamento',
  'ENF EDUARDO', '2026-05-11',
  '2026-05-11', '2026-05-11', 'Resultado de PCR liberado.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8416248', t.id, 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS',
  'Alinhamento com equipes especializadas.', 'em_andamento',
  'ENF EDUARDO', '2026-05-25',
  '2026-05-25', '2026-05-25', 'Contato com urologia para procedimento.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8416248', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano de alta.', 'em_andamento',
  'ENF EDUARDO', '2026-05-11',
  '2026-07-30', NULL, 'Depende de regulação de HD e cirurgia.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1373852', t.id, 'ENCAIXE DE EXAME',
  'Inserção de exame complementar na rotina do paciente.', 'em_andamento',
  'ENF EDUARDO', '2026-06-05',
  '2026-06-05', '2026-06-05', 'Doppler reagendado e realizado.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ENCAIXE DE EXAME';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1373852', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-06-05',
  '2026-06-05', NULL, 'Aguardando reavaliação médica.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '1373852', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano de alta.', 'em_andamento',
  'ENF EDUARDO', '2026-06-05',
  '2026-07-20', NULL, 'Depende de resultado de exames.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8083480', t.id, 'Acompanhamento do quadro clínico de paciente',
  'Monitoramento contínuo da evolução clínica.', 'em_andamento',
  'ENF EDUARDO', '2026-06-16',
  '2026-06-16', NULL, 'Aguardando cirurgia cardíaca.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento do quadro clínico de paciente';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8429429', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-06-29',
  '2026-06-29', '2026-06-29', 'Definição de alta e suporte familiar.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8429429', t.id, 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS',
  'Alinhamento com equipes especializadas.', 'em_andamento',
  'ENF EDUARDO', '2026-06-29',
  '2026-06-29', '2026-06-29', 'Contato com hematologia e ginecologia.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8429429', t.id, 'SOLICITADO AGILIDADE NA RESPOSTA DO PARECER',
  'Solicitação de priorização na emissão de parecer.', 'em_andamento',
  'ENF EDUARDO', '2026-06-29',
  '2026-06-29', '2026-06-30', 'Parecer da ginecologia obtido.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO AGILIDADE NA RESPOSTA DO PARECER';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8429429', t.id, 'ORIENTAÇÃO EDUCATIVA',
  'Orientação educativa ao paciente/família sobre cuidados e condutas.', 'em_andamento',
  'ENF EDUARDO', '2026-06-30',
  '2026-06-30', '2026-07-10', 'Treinamento familiar para curativos.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ORIENTAÇÃO EDUCATIVA';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8429429', t.id, 'PLANEJAMENTO DA ALTA HOSPITALAR',
  'Estruturação do plano de alta.', 'em_andamento',
  'ENF EDUARDO', '2026-06-29',
  '2026-07-16', NULL, 'Alta planejada para após consulta ambulatorial.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'PLANEJAMENTO DA ALTA HOSPITALAR';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8377747', t.id, 'ARTICULAÇÃO COM A REDE',
  'Contato e alinhamento com a rede de atenção à saúde (ex.: UBS, CAPS, etc.).', 'em_andamento',
  'ENF EDUARDO', '2025-11-27',
  '2025-11-27', NULL, 'Aguardando PADI/PMEC e judicialização.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM A REDE';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8410268', t.id, 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND',
  'Discussão em equipe sobre pendências e condutas.', 'concluida',
  'ENF EDUARDO', '2026-05-11',
  '2026-05-11', '2026-05-11', 'Discussão sobre HD peritoneal e suporte social.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8410268', t.id, 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL',
  'Solicitação de intervenção do Serviço Social.', 'em_andamento',
  'ENF EDUARDO', '2026-05-05',
  '2026-05-06', '2026-05-06', 'Entrevista familiar realizada.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8410268', t.id, 'Acompanhamento de regulação de HD',
  'Acompanhamento de regulação de alta hospitalar.', 'em_andamento',
  'ENF EDUARDO', '2026-05-11',
  '2026-05-11', NULL, 'Aguardando definição de HD peritoneal.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'Acompanhamento de regulação de HD';

INSERT INTO egaa_intervencao_paciente (
  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,
  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao
)
SELECT
  NULL, '8388949', t.id, 'ARTICULAÇÃO COM A REDE',
  'Contato e alinhamento com a rede de atenção à saúde.', 'em_andamento',
  'ENF EDUARDO', '2026-02-13',
  '2026-02-13', NULL, 'Aguardando PADI/PMEC de Itaboraí.'
FROM egaa_tipo_intervencao t
WHERE t.nome = 'ARTICULAÇÃO COM A REDE';
