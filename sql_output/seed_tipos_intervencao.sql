-- Seed de tipos de intervenção extraídos do CSV de intervenções.
-- Usa INSERT ... ON DUPLICATE KEY UPDATE para:
--   - Inserir novos tipos se não existirem
--   - Atualizar ativo e ordem_exibicao se já existirem
--
-- ATIVOS (aparecem no dropdown, ordem alfabética):
--   ordem_exibicao = 50 (agrupamento único, ordena por nome)
-- INATIVOS (só histórico, não poluem o seletor):
--   ativo = 0, ordem_exibicao = 99

-- ▸ ATIVOS ──────────────────────────────────────────

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('Acompanhamento do quadro clínico de paciente', 'Monitoramento contínuo da evolução clínica do paciente', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('ARTICULAÇÃO COM A REDE', 'Contato e alinhamento com a rede de atenção à saúde (UBS, CAPS, etc.)', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS', 'Alinhamento com equipes especializadas para condução do caso', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND', 'Discussão em equipe sobre pendências e definição de condutas', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('ENCAIXE DE EXAME', 'Inserção de exame complementar na agenda/rotina do paciente', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('ENTREVISTA SOCIAL', 'Realização de entrevista com paciente/família para avaliação social', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('ORIENTAÇÃO EDUCATIVA', 'Orientação educativa ao paciente/família sobre cuidados e condutas', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('PLANEJAMENTO DA ALTA HOSPITALAR', 'Estruturação do plano para alta segura do paciente', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('SOLICITADO ACOMPANHAMENTO DA FISIOTERAPIA', 'Solicitação de avaliação e acompanhamento fisioterapêutico', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('SOLICITADO ACOMPANHAMENTO DA T.O.', 'Solicitação de avaliação e acompanhamento pela Terapia Ocupacional', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL', 'Solicitação de intervenção do Serviço Social', 1, 50, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=1, ordem_exibicao=50, updated_at=NOW();

-- ▸ INATIVOS (só histórico, não aparecem no dropdown) ──

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('ACOMPANHAMENTO DE AGENDAMENTO DE EXAMES/PROCEDIMENTOS EXTERNOS/REGULAÇÃO NIR', '', 0, 99, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=0, ordem_exibicao=99, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('ACOMPANHAR EXAMES/CONSULTAS/PROCEDIMENTOS REGULADOS VIA NIR', '', 0, 99, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=0, ordem_exibicao=99, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('Acompanhamento de regulação de HD', '', 0, 99, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=0, ordem_exibicao=99, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('SOLICITADO AGILIDADE NA RESPOSTA DO PARECER', '', 0, 99, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=0, ordem_exibicao=99, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS', '', 0, 99, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=0, ordem_exibicao=99, updated_at=NOW();

INSERT INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)
VALUES ('SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR', '', 0, 99, NOW(), NOW())
ON DUPLICATE KEY UPDATE ativo=0, ordem_exibicao=99, updated_at=NOW();
