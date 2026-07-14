-- 008_create_egaa_desfecho.sql
-- Tabela para registrar desfechos (alta/obito) com apoio do EGAA,
-- permitindo demonstrar resultados da deshospitalizacao ao longo do tempo.

CREATE TABLE IF NOT EXISTS `egaa_desfecho` (
    `id`                INT          NOT NULL AUTO_INCREMENT,
    `prontuario`        VARCHAR(50)  NOT NULL,
    `tipo`              ENUM('alta', 'obito') NOT NULL COMMENT 'Tipo de desfecho: alta ou obito',
    `data_desfecho`     DATE         NOT NULL COMMENT 'Data em que ocorreu o desfecho',
    `descricao`         TEXT         NULL     COMMENT 'Descricao ou observacao sobre o desfecho',
    `usuario_responsavel` VARCHAR(100) NULL   COMMENT 'Nome do membro do EGAA que registrou',
    `intervencao_id`    INT          NULL     COMMENT 'Vinculo opcional com intervencao do EGAA',
    `created_at`        DATETIME     NULL,
    `updated_at`        DATETIME     NULL,
    PRIMARY KEY (`id`),
    INDEX `idx_desfecho_prontuario` (`prontuario`),
    INDEX `idx_desfecho_tipo` (`tipo`),
    INDEX `idx_desfecho_data` (`data_desfecho`),
    INDEX `idx_desfecho_responsavel` (`usuario_responsavel`),
    INDEX `idx_desfecho_intervencao` (`intervencao_id`),
    CONSTRAINT `fk_desfecho_intervencao`
        FOREIGN KEY (`intervencao_id`) REFERENCES `egaa_intervencao_paciente`(`id`)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
