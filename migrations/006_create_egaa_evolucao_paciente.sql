-- 006_create_egaa_evolucao_paciente.sql
-- Tabela para armazenar a evolucao textual do paciente (diario do EGAA),
-- desacoplada dos snapshots de censo hospitalar.
-- 1 paciente -> 1 registro de evolucao (upsert por prontuario).

CREATE TABLE IF NOT EXISTS `egaa_evolucao_paciente` (
    `id`          INT          NOT NULL AUTO_INCREMENT,
    `prontuario`  VARCHAR(50)  NOT NULL,
    `evolucao`    TEXT         NULL COMMENT 'Texto livre de evolucao do paciente (diario do EGAA)',
    `created_at`  DATETIME     NULL,
    `updated_at`  DATETIME     NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `uq_evolucao_prontuario` (`prontuario`),
    INDEX `idx_evolucao_prontuario` (`prontuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
