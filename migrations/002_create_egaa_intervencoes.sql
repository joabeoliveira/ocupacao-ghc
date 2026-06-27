CREATE TABLE IF NOT EXISTS egaa_tipo_intervencao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    descricao TEXT NULL,
    ativo TINYINT(1) NOT NULL DEFAULT 1,
    ordem_exibicao INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_egaa_tipo_intervencao_nome UNIQUE (nome),
    INDEX idx_egaa_tipo_intervencao_ativo_ordem (ativo, ordem_exibicao, nome)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS egaa_intervencao_paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ocupacao_leito_id INT NULL,
    prontuario VARCHAR(50) NOT NULL,
    tipo_intervencao_id INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT NULL,
    status ENUM('aberta', 'em_andamento', 'concluida', 'cancelada') NOT NULL DEFAULT 'aberta',
    usuario_responsavel VARCHAR(100) NULL,
    data_prevista DATE NULL,
    data_conclusao DATETIME NULL,
    observacao TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_egaa_intervencao_paciente_ocupacao
        FOREIGN KEY (ocupacao_leito_id) REFERENCES ocupacao_leitos_ghc(id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_egaa_intervencao_paciente_tipo
        FOREIGN KEY (tipo_intervencao_id) REFERENCES egaa_tipo_intervencao(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_egaa_intervencao_paciente_prontuario (prontuario, created_at),
    INDEX idx_egaa_intervencao_paciente_tipo_status (tipo_intervencao_id, status, created_at),
    INDEX idx_egaa_intervencao_paciente_ocupacao (ocupacao_leito_id, created_at),
    INDEX idx_egaa_intervencao_paciente_datas (data_prevista, data_conclusao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao) VALUES
('Evolução EGAA', 'Registro de evolução do paciente e conduta do dia', 1, 1),
('Pendência para alta', 'Pendência que precisa ser resolvida antes da alta', 1, 2),
('Intervenção EGAA', 'Intervenção realizada pela equipe do EGAA', 1, 3),
('Acompanhamento de paciente crônico', 'Acompanhamento de condição crônica e desospitalização', 1, 4),
('Risco de readmissão', 'Paciente com risco aumentado de retorno', 1, 5);
