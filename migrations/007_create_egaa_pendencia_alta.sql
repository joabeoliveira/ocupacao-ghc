-- 007_create_egaa_pendencia_alta.sql
-- Tabela para gerenciar pendencias para alta do paciente,
-- desacoplada das atuacoes EGAA. Cada linha e uma pendencia
-- que pode ser marcada como resolvida quando sanada.

CREATE TABLE IF NOT EXISTS `egaa_pendencia_alta` (
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `prontuario`  VARCHAR(50)  NOT NULL,
    `codigo`      VARCHAR(80)  NOT NULL COMMENT 'Codigo da pendencia (ex: regulacao, ajuste_inr)',
    `resolvida`   TINYINT(1)   NOT NULL DEFAULT 0 COMMENT '0 = pendente, 1 = resolvida',
    `created_at`  DATETIME     NULL,
    `updated_at`  DATETIME     NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_pendencia_prontuario` (`prontuario`),
    UNIQUE INDEX `uq_pendencia_paciente_codigo` (`prontuario`, `codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
