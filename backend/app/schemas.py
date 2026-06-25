from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class OcupacaoPorUnidade(BaseModel):
    unidade: str | None
    total_pacientes: int


class CensoKPIsResponse(BaseModel):
    total_internados: int
    longa_permanencia_15: int
    longa_permanencia_30: int
    ocupacao_por_unidade: list[OcupacaoPorUnidade]


class PacienteInternadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prontuario: str
    nome_paciente: str | None = None
    idade_anos: int | None = None
    idade_meses: int | None = None
    data_internacao: datetime | None = None
    dias_internacao: int | None = None
    especialidade: str
    unidade: str | None = None
    enfermaria: str | None = None
    leito: str | None = None
    cid_internacao_codigo: str | None = None
    cid_internacao_descricao: str | None = None
    data_snapshot: date | None = None


class PacientesInternadosPage(BaseModel):
    total: int
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    items: list[PacienteInternadoResponse]


class UploadCensoResponse(BaseModel):
    message: str
    nome_arquivo: str
    lote_importacao_id: str
    linhas_processadas: int