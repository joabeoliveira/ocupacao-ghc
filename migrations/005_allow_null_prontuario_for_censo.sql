-- Migration: Permite prontuario nulo para suportar censo diário com leitos livres/bloqueados
-- Mantém compatibilidade com histórico de internação (prontuário continua preenchido no fluxo histórico).

ALTER TABLE ocupacao_leitos_ghc
MODIFY COLUMN prontuario VARCHAR(50) NULL;
