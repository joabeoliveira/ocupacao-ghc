from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import CHAR, Boolean, Date, DateTime, ForeignKey, Integer, String, Text
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


class EgaaTipoIntervencao(Base):
    __tablename__ = "egaa_tipo_intervencao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    ordem_exibicao: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class EgaaIntervencaoPaciente(Base):
    __tablename__ = "egaa_intervencao_paciente"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ocupacao_leito_id: Mapped[int | None] = mapped_column(
        ForeignKey("ocupacao_leitos_ghc.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    prontuario: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    tipo_intervencao_id: Mapped[int] = mapped_column(
        ForeignKey("egaa_tipo_intervencao.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        ENUM("aberta", "em_andamento", "concluida", "cancelada"),
        nullable=False,
        default="aberta",
        index=True,
    )
    usuario_responsavel: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    data_atuacao: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    data_prevista: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    data_conclusao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
