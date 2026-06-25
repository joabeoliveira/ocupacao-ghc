CREATE TABLE IF NOT EXISTS ocupacao_leitos_ghc (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Identificação do Paciente e Prontuário
    prontuario VARCHAR(50) NOT NULL,
    nome_paciente VARCHAR(255) NULL,
    
    -- Dados Demográficos Tratados
    idade_anos INT NULL,
    idade_meses INT NULL,
    
    -- Fluxo Clínico e Datas
    data_internacao DATETIME NULL,
    data_alta DATETIME NULL,
    dias_internacao INT NULL, -- Calculado no ETL para agilizar os KPIs de longa permanência
    internado_ativo TINYINT(1) AS (CASE WHEN data_alta IS NULL THEN 1 ELSE 0 END) STORED,
    
    -- Localização e Especialidade (Onde entra o filtro 'DERMATO')
    especialidade VARCHAR(150) NOT NULL,
    unidade VARCHAR(150) NULL,
    enfermaria VARCHAR(150) NULL,
    leito VARCHAR(50) NULL,
    
    -- Diagnóstico
    cid_internacao_codigo VARCHAR(20) NULL,
    cid_internacao_descricao VARCHAR(255) NULL,
    tipo_alta VARCHAR(100) NULL,
    
    -- Metadados de Controle de Lote (Essencial para conviver Censo + Histórico)
    fonte_dado ENUM('historico_internacao', 'censo_diario') NOT NULL,
    lote_importacao_id CHAR(36) NOT NULL,
    nome_arquivo VARCHAR(255) NOT NULL,
    hash_registro CHAR(64) NOT NULL,
    data_snapshot DATE NULL, -- Preenchida para censo_diario; representa a fotografia do dia
    periodo_referencia_inicio DATE NULL, -- Faixa lógica do arquivo histórico, quando aplicável
    periodo_referencia_fim DATE NULL,
    data_impressao_arquivo DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_ocupacao_fonte_hash UNIQUE (fonte_dado, hash_registro),
    CONSTRAINT chk_contexto_referencia CHECK (
        (fonte_dado = 'censo_diario' AND data_snapshot IS NOT NULL)
        OR (fonte_dado = 'historico_internacao')
    ),

    -- Índices Estratégicos para o Painel do EGAA
    INDEX idx_painel_censo_ativo (internado_ativo, data_snapshot, especialidade, unidade, enfermaria),
    INDEX idx_painel_especialidade (especialidade, internado_ativo, data_snapshot),
    INDEX idx_painel_unidade (unidade, enfermaria, internado_ativo, data_snapshot),
    INDEX idx_prontuario_datas (prontuario, data_internacao, data_alta),
    INDEX idx_longa_permanencia (internado_ativo, dias_internacao),
    INDEX idx_fonte_snapshot (fonte_dado, data_snapshot),
    INDEX idx_lote_importacao (lote_importacao_id),
    INDEX idx_nome_arquivo (nome_arquivo),
    INDEX idx_cid_codigo (cid_internacao_codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;