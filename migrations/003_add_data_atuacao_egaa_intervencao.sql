ALTER TABLE egaa_intervencao_paciente
    ADD COLUMN data_atuacao DATE NULL AFTER usuario_responsavel;

CREATE INDEX idx_egaa_intervencao_paciente_data_atuacao
    ON egaa_intervencao_paciente (data_atuacao, created_at);
