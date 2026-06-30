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
    longa_permanencia_40: int
    longa_permanencia_60_anos: int
    longa_permanencia_60_15: int
    longa_permanencia_60_30: int
    leitos_ocupados: int
    leitos_livres: int
    leitos_bloqueados: int
    taxa_ocupacao_geral_percentual: float
    taxa_ocupacao_operacional_percentual: float
    taxa_ocupacao_ajustada_sem_emergencia_percentual: float
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
    egaa_total_atuacoes: int = 0
    egaa_ultima_atuacao: date | None = None


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
    data_atuacao: date | None = None
    data_prevista: date | None = None
    data_conclusao: datetime | None = None
    observacao: str | None = None


class EgaaIntervencaoPacienteResponse(EgaaIntervencaoPacienteCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class EgaaIntervencaoPacienteBatchCreate(BaseModel):
    items: list[EgaaIntervencaoPacienteCreate] = Field(min_length=1)


class EgaaIntervencaoPorTipo(BaseModel):
    tipo_intervencao_id: int
    tipo_intervencao_nome: str
    total: int


class EgaaIntervencaoPorStatus(BaseModel):
    status: str
    total: int


class EgaaIntervencaoPorMes(BaseModel):
    mes: str
    total: int


class EgaaIndicadoresResponse(BaseModel):
    total_intervencoes: int
    pacientes_com_intervencao: int
    abertas: int
    em_andamento: int
    concluidas: int
    canceladas: int
    por_status: list[EgaaIntervencaoPorStatus]
    por_tipo: list[EgaaIntervencaoPorTipo]
    por_mes: list[EgaaIntervencaoPorMes]
