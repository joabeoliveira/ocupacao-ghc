from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import CHAR, Date, DateTime, Integer, String, Text
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OcupacaoLeitoGHC(Base):
    __tablename__ = "ocupacao_leitos_ghc"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prontuario: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    nome_paciente: Mapped[str | None] = mapped_column(String(255), nullable=True)
    idade_anos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    idade_meses: Mapped[int | None] = mapped_column(Integer, nullable=True)
    data_internacao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    data_alta: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    dias_internacao: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    internado_ativo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    especialidade: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    unidade: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    enfermaria: Mapped[str | None] = mapped_column(String(150), nullable=True)
    leito: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cid_internacao_codigo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cid_internacao_descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    tipo_alta: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fonte_dado: Mapped[str] = mapped_column(ENUM("historico_internacao", "censo_diario"), nullable=False, index=True)
    lote_importacao_id: Mapped[str] = mapped_column(CHAR(36), nullable=False, index=True)
    nome_arquivo: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hash_registro: Mapped[str] = mapped_column(CHAR(64), nullable=False, unique=True)
    data_snapshot: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    periodo_referencia_inicio: Mapped[date | None] = mapped_column(Date, nullable=True)
    periodo_referencia_fim: Mapped[date | None] = mapped_column(Date, nullable=True)
    data_impressao_arquivo: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)