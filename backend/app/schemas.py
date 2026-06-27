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


class EgaaTipoIntervencaoBase(BaseModel):
    nome: str
    descricao: str | None = None
    ativo: bool = True
    ordem_exibicao: int = 0


class EgaaTipoIntervencaoCreate(EgaaTipoIntervencaoBase):
    pass


class EgaaTipoIntervencaoResponse(EgaaTipoIntervencaoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class EgaaIntervencaoPacienteCreate(BaseModel):
    ocupacao_leito_id: int | None = None
    prontuario: str
    tipo_intervencao_id: int
    titulo: str
    descricao: str | None = None
    status: str = "aberta"
    usuario_responsavel: str | None = None
    data_prevista: date | None = None
    data_conclusao: datetime | None = None
    observacao: str | None = None


class EgaaIntervencaoPacienteResponse(EgaaIntervencaoPacienteCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
