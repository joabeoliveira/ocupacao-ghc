from __future__ import annotations

from datetime import date
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from datetime import datetime as dt_datetime

from app.database import get_db
from app.models import EgaaDesfecho, EgaaIntervencaoPaciente, EgaaPendenciaAlta, EgaaTipoIntervencao
from app.schemas import (
    EgaaDesfechoCreate,
    EgaaDesfechoResponse,
    EgaaIndicadoresDesfechoResponse,
    EgaaDesfechoPorMes,
    EgaaDesfechoPorTipo,
    EgaaIntervencaoPacienteBatchCreate,
    EgaaIntervencaoPacienteCreate,
    EgaaIntervencaoPacienteResponse,
    EgaaIndicadoresResponse,
    EgaaIntervencaoPorMes,
    EgaaIntervencaoPorStatus,
    EgaaIntervencaoPorTipo,
    EgaaTipoIntervencaoCreate,
    EgaaTipoIntervencaoResponse,
    PendenciaAltaCreate,
    PendenciaAltaResolve,
    PendenciaAltaResponse,
)


router = APIRouter(prefix="/egaa", tags=["EGAA"])


def _atuacao_date_expr():
    return func.coalesce(EgaaIntervencaoPaciente.data_atuacao, func.date(EgaaIntervencaoPaciente.created_at))


@router.get("/tipos-intervencao", response_model=list[EgaaTipoIntervencaoResponse])
def list_tipos_intervencao(db: Session = Depends(get_db)) -> list[EgaaTipoIntervencaoResponse]:
    rows = db.execute(
        select(EgaaTipoIntervencao).order_by(
            desc(EgaaTipoIntervencao.ativo),
            EgaaTipoIntervencao.ordem_exibicao,
            EgaaTipoIntervencao.nome,
        )
    ).scalars().all()
    return [EgaaTipoIntervencaoResponse.model_validate(row) for row in rows]


@router.post("/tipos-intervencao", response_model=EgaaTipoIntervencaoResponse, status_code=201)
def create_tipo_intervencao(
    payload: EgaaTipoIntervencaoCreate,
    db: Session = Depends(get_db),
) -> EgaaTipoIntervencaoResponse:
    existing = db.scalar(select(EgaaTipoIntervencao).where(EgaaTipoIntervencao.nome == payload.nome))
    if existing is not None:
        raise HTTPException(status_code=409, detail="Tipo de intervenção já cadastrado.")

    row = EgaaTipoIntervencao(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return EgaaTipoIntervencaoResponse.model_validate(row)


@router.get("/intervencoes", response_model=list[EgaaIntervencaoPacienteResponse])
def list_intervencoes(
    prontuario: str | None = Query(default=None),
    ocupacao_leito_id: int | None = Query(default=None),
    tipo_intervencao_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[EgaaIntervencaoPacienteResponse]:
    query = select(EgaaIntervencaoPaciente)
    if prontuario:
        query = query.where(EgaaIntervencaoPaciente.prontuario == prontuario)
    if ocupacao_leito_id is not None:
        query = query.where(EgaaIntervencaoPaciente.ocupacao_leito_id == ocupacao_leito_id)
    if tipo_intervencao_id is not None:
        query = query.where(EgaaIntervencaoPaciente.tipo_intervencao_id == tipo_intervencao_id)

    rows = db.execute(
        query.order_by(
            desc(_atuacao_date_expr()),
            desc(EgaaIntervencaoPaciente.created_at),
            desc(EgaaIntervencaoPaciente.id),
        )
    ).scalars().all()
    return [EgaaIntervencaoPacienteResponse.model_validate(row) for row in rows]


@router.post("/intervencoes", response_model=EgaaIntervencaoPacienteResponse, status_code=201)
def create_intervencao(
    payload: EgaaIntervencaoPacienteCreate,
    db: Session = Depends(get_db),
) -> EgaaIntervencaoPacienteResponse:
    tipo = db.scalar(select(EgaaTipoIntervencao).where(EgaaTipoIntervencao.id == payload.tipo_intervencao_id))
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de intervenção não encontrado.")

    row = EgaaIntervencaoPaciente(**payload.model_dump(exclude_none=True))
    if row.data_atuacao is None:
        row.data_atuacao = date.today()
    db.add(row)
    db.commit()
    db.refresh(row)
    return EgaaIntervencaoPacienteResponse.model_validate(row)


@router.get("/intervencoes/{intervencao_id}", response_model=EgaaIntervencaoPacienteResponse)
def get_intervencao(
    intervencao_id: int,
    db: Session = Depends(get_db),
) -> EgaaIntervencaoPacienteResponse:
    row = db.scalar(select(EgaaIntervencaoPaciente).where(EgaaIntervencaoPaciente.id == intervencao_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Intervenção não encontrada.")
    return EgaaIntervencaoPacienteResponse.model_validate(row)


@router.put("/intervencoes/{intervencao_id}", response_model=EgaaIntervencaoPacienteResponse)
def update_intervencao(
    intervencao_id: int,
    payload: EgaaIntervencaoPacienteCreate,
    db: Session = Depends(get_db),
) -> EgaaIntervencaoPacienteResponse:
    row = db.scalar(select(EgaaIntervencaoPaciente).where(EgaaIntervencaoPaciente.id == intervencao_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Intervenção não encontrada.")

    tipo = db.scalar(select(EgaaTipoIntervencao).where(EgaaTipoIntervencao.id == payload.tipo_intervencao_id))
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de intervenção não encontrado.")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(row, field, value)
    if row.data_atuacao is None:
        row.data_atuacao = date.today()
    row.updated_at = dt_datetime.utcnow()
    db.commit()
    db.refresh(row)
    return EgaaIntervencaoPacienteResponse.model_validate(row)


@router.delete("/intervencoes/{intervencao_id}", status_code=204)
def delete_intervencao(
    intervencao_id: int,
    db: Session = Depends(get_db),
) -> None:
    row = db.scalar(select(EgaaIntervencaoPaciente).where(EgaaIntervencaoPaciente.id == intervencao_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Intervenção não encontrada.")
    db.delete(row)
    db.commit()


@router.post("/intervencoes/lote", response_model=list[EgaaIntervencaoPacienteResponse], status_code=201)
def create_intervencoes_lote(
    payload: EgaaIntervencaoPacienteBatchCreate,
    db: Session = Depends(get_db),
) -> list[EgaaIntervencaoPacienteResponse]:
    if not payload.items:
        raise HTTPException(status_code=400, detail="Informe ao menos uma atuação.")

    tipos_cache: dict[int, EgaaTipoIntervencao | None] = {}
    rows: list[EgaaIntervencaoPaciente] = []

    try:
        for item in payload.items:
            tipo = tipos_cache.get(item.tipo_intervencao_id)
            if item.tipo_intervencao_id not in tipos_cache:
                tipo = db.scalar(
                    select(EgaaTipoIntervencao).where(EgaaTipoIntervencao.id == item.tipo_intervencao_id)
                )
                tipos_cache[item.tipo_intervencao_id] = tipo
            if tipo is None:
                raise HTTPException(status_code=404, detail="Tipo de intervenção não encontrado.")

            row = EgaaIntervencaoPaciente(**item.model_dump(exclude_none=True))
            if row.data_atuacao is None:
                row.data_atuacao = date.today()
            db.add(row)
            rows.append(row)

        db.commit()
        for row in rows:
            db.refresh(row)
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:  # pragma: no cover - defensive guard for production
        db.rollback()
        raise HTTPException(status_code=500, detail="Não foi possível salvar as atuações em lote.") from exc

    return [EgaaIntervencaoPacienteResponse.model_validate(row) for row in rows]


@router.get("/indicadores", response_model=EgaaIndicadoresResponse)
def get_indicadores(db: Session = Depends(get_db)) -> EgaaIndicadoresResponse:
    try:
        total_intervencoes = db.scalar(select(func.count()).select_from(EgaaIntervencaoPaciente)) or 0
        pacientes_com_intervencao = db.scalar(
            select(func.count(func.distinct(EgaaIntervencaoPaciente.prontuario)))
        ) or 0

        status_rows = db.execute(
            select(EgaaIntervencaoPaciente.status, func.count().label("total"))
            .group_by(EgaaIntervencaoPaciente.status)
            .order_by(EgaaIntervencaoPaciente.status)
        ).all()
        status_map = {row.status: row.total for row in status_rows}

        tipo_rows = db.execute(
            select(
                EgaaIntervencaoPaciente.tipo_intervencao_id,
                EgaaTipoIntervencao.nome.label("tipo_intervencao_nome"),
                func.count().label("total"),
            )
            .join(EgaaTipoIntervencao, EgaaTipoIntervencao.id == EgaaIntervencaoPaciente.tipo_intervencao_id)
            .group_by(EgaaIntervencaoPaciente.tipo_intervencao_id, EgaaTipoIntervencao.nome)
            .order_by(desc("total"), EgaaTipoIntervencao.nome)
        ).all()

        atuacao_data_expr = _atuacao_date_expr()

        mes_rows = db.execute(
            select(
                func.date_format(atuacao_data_expr, "%Y-%m").label("mes"),
                func.count().label("total"),
            )
            .where(atuacao_data_expr.is_not(None))
            .group_by("mes")
            .order_by("mes")
        ).all()
    except Exception:
        return EgaaIndicadoresResponse(
            total_intervencoes=0,
            pacientes_com_intervencao=0,
            abertas=0,
            em_andamento=0,
            concluidas=0,
            canceladas=0,
            por_status=[],
            por_tipo=[],
            por_mes=[],
        )

    return EgaaIndicadoresResponse(
        total_intervencoes=total_intervencoes,
        pacientes_com_intervencao=pacientes_com_intervencao,
        abertas=int(status_map.get("aberta", 0) or 0),
        em_andamento=int(status_map.get("em_andamento", 0) or 0),
        concluidas=int(status_map.get("concluida", 0) or 0),
        canceladas=int(status_map.get("cancelada", 0) or 0),
        por_status=[
            EgaaIntervencaoPorStatus(status=row.status, total=row.total)
            for row in status_rows
        ],
        por_tipo=[
            EgaaIntervencaoPorTipo(
                tipo_intervencao_id=row.tipo_intervencao_id,
                tipo_intervencao_nome=row.tipo_intervencao_nome,
                total=row.total,
            )
            for row in tipo_rows
        ],
        por_mes=[EgaaIntervencaoPorMes(mes=row.mes, total=row.total) for row in mes_rows],
    )


@router.get("/export/xlsx")
def export_egaa_xlsx(db: Session = Depends(get_db)) -> StreamingResponse:
    tipos = db.execute(
        select(EgaaTipoIntervencao).order_by(
            desc(EgaaTipoIntervencao.ativo),
            EgaaTipoIntervencao.ordem_exibicao,
            EgaaTipoIntervencao.nome,
        )
    ).scalars().all()
    intervencoes = db.execute(
        select(EgaaIntervencaoPaciente, EgaaTipoIntervencao.nome.label("tipo_intervencao_nome"))
        .join(EgaaTipoIntervencao, EgaaTipoIntervencao.id == EgaaIntervencaoPaciente.tipo_intervencao_id)
        .order_by(desc(_atuacao_date_expr()), desc(EgaaIntervencaoPaciente.created_at), desc(EgaaIntervencaoPaciente.id))
    ).all()

    df_tipos = pd.DataFrame([{
        "id": item.id,
        "nome": item.nome,
        "descricao": item.descricao,
        "ativo": item.ativo,
        "ordem_exibicao": item.ordem_exibicao,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    } for item in tipos])
    df_intervencoes = pd.DataFrame([{
        "id": row.EgaaIntervencaoPaciente.id,
        "prontuario": row.EgaaIntervencaoPaciente.prontuario,
        "ocupacao_leito_id": row.EgaaIntervencaoPaciente.ocupacao_leito_id,
        "tipo_intervencao_id": row.EgaaIntervencaoPaciente.tipo_intervencao_id,
        "tipo_intervencao_nome": row.tipo_intervencao_nome,
        "titulo": row.EgaaIntervencaoPaciente.titulo,
        "descricao": row.EgaaIntervencaoPaciente.descricao,
        "status": row.EgaaIntervencaoPaciente.status,
        "usuario_responsavel": row.EgaaIntervencaoPaciente.usuario_responsavel,
        "data_atuacao": row.EgaaIntervencaoPaciente.data_atuacao,
        "data_prevista": row.EgaaIntervencaoPaciente.data_prevista,
        "data_conclusao": row.EgaaIntervencaoPaciente.data_conclusao,
        "observacao": row.EgaaIntervencaoPaciente.observacao,
        "created_at": row.EgaaIntervencaoPaciente.created_at,
        "updated_at": row.EgaaIntervencaoPaciente.updated_at,
    } for row in intervencoes])

    indicadores = get_indicadores(db)
    df_status = pd.DataFrame([item.model_dump() for item in indicadores.por_status])
    df_tipo = pd.DataFrame([item.model_dump() for item in indicadores.por_tipo])
    df_mes = pd.DataFrame([item.model_dump() for item in indicadores.por_mes])
    df_resumo = pd.DataFrame([{
        "total_intervencoes": indicadores.total_intervencoes,
        "pacientes_com_intervencao": indicadores.pacientes_com_intervencao,
        "abertas": indicadores.abertas,
        "em_andamento": indicadores.em_andamento,
        "concluidas": indicadores.concluidas,
        "canceladas": indicadores.canceladas,
    }])

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_resumo.to_excel(writer, index=False, sheet_name="resumo")
        df_status.to_excel(writer, index=False, sheet_name="por_status")
        df_tipo.to_excel(writer, index=False, sheet_name="por_tipo")
        df_mes.to_excel(writer, index=False, sheet_name="por_mes")
        df_tipos.to_excel(writer, index=False, sheet_name="tipos")
        df_intervencoes.to_excel(writer, index=False, sheet_name="intervencoes")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="egaa_resultados.xlsx"'},
    )


# --- Pendencias para alta ---

PENDENCIA_CODIGOS: set[str] = {
    "regulacao", "ajuste_inr", "ajuste_medicamento", "tratamento_lesoes",
    "antibioticoterapia", "definicao_diagnostica", "ajuste_laboratorial",
    "exame_pendente", "aguarda_parecer_especialista", "definicao_terapeutica",
    "reavaliacao_medica", "descompensacao_clinica", "procedimento_cirurgico",
    "aguarda_gtt_por_eda", "aguarda_cirurgia_cardiaca", "manejo_clinico",
    "manejo_sintomatico", "cuidados_paliativos", "cuidados_pos_operatorios",
    "cuidados_fim_vida", "fragilidade_familiar", "vulnerabilidade_social",
    "vulnerabilidade_socioeconomica", "vulnerabilidade_emocional",
    "documento_identidade", "familia_nao_cooperativa", "aguarda_padi_pmec",
    "aguarda_home_care", "aguarda_vaga_abrigo", "aguardando_documentacao",
    "transporte_sanitario_eletivo", "familiar_acompanhante_alta",
    "aguarda_leito_cuidados_prolongados", "aguarda_regulacao_transferencia",
    "aguarda_regulacao_marcapasso",
}

PENDENCIA_ROTULOS: dict[str, str] = {
    "regulacao": "Regulação",
    "ajuste_inr": "Ajuste INR",
    "ajuste_medicamento": "Ajuste de medicação",
    "tratamento_lesoes": "Tratamento de lesões",
    "antibioticoterapia": "Antibioticoterapia",
    "definicao_diagnostica": "Definição diagnóstica",
    "ajuste_laboratorial": "Ajuste laboratorial",
    "exame_pendente": "Exame pendente",
    "aguarda_parecer_especialista": "Aguarda parecer especialista",
    "definicao_terapeutica": "Definição terapêutica",
    "reavaliacao_medica": "Reavaliação médica",
    "descompensacao_clinica": "Descompensação clínica",
    "procedimento_cirurgico": "Procedimento cirúrgico",
    "aguarda_gtt_por_eda": "Aguarda GTT por EDA",
    "aguarda_cirurgia_cardiaca": "Aguarda cirurgia cardíaca",
    "manejo_clinico": "Manejo clínico",
    "manejo_sintomatico": "Manejo sintomático",
    "cuidados_paliativos": "Cuidados paliativos",
    "cuidados_pos_operatorios": "Cuidados pós-operatórios",
    "cuidados_fim_vida": "Cuidados de fim de vida",
    "fragilidade_familiar": "Fragilidade familiar",
    "vulnerabilidade_social": "Vulnerabilidade social",
    "vulnerabilidade_socioeconomica": "Vulnerabilidade socioeconômica",
    "vulnerabilidade_emocional": "Vulnerabilidade emocional",
    "documento_identidade": "Documento de identidade",
    "familia_nao_cooperativa": "Família não cooperativa",
    "aguarda_padi_pmec": "Aguarda PADI/PMEC",
    "aguarda_home_care": "Aguarda home care",
    "aguarda_vaga_abrigo": "Aguarda vaga em abrigo",
    "aguardando_documentacao": "Aguardando documentação",
    "transporte_sanitario_eletivo": "Transporte sanitário eletivo",
    "familiar_acompanhante_alta": "Familiar acompanhante para alta",
    "aguarda_leito_cuidados_prolongados": "Aguarda leito cuidados prolongados",
    "aguarda_regulacao_transferencia": "Aguarda regulação transferência",
    "aguarda_regulacao_marcapasso": "Aguarda regulação marcapasso",
}


@router.get("/pendencia/codigos")
def listar_codigos_pendencia() -> list[dict[str, str]]:
    return [
        {"codigo": codigo, "rotulo": PENDENCIA_ROTULOS.get(codigo, codigo)}
        for codigo in sorted(PENDENCIA_CODIGOS)
    ]


@router.get("/pendencia/{prontuario}", response_model=list[PendenciaAltaResponse])
def listar_pendencias(
    prontuario: str,
    db: Session = Depends(get_db),
) -> list[PendenciaAltaResponse]:
    rows = db.execute(
        select(EgaaPendenciaAlta)
        .where(EgaaPendenciaAlta.prontuario == prontuario)
        .order_by(EgaaPendenciaAlta.resolvida, EgaaPendenciaAlta.codigo)
    ).scalars().all()
    return [PendenciaAltaResponse.model_validate(row) for row in rows]


@router.post("/pendencia/{prontuario}", response_model=PendenciaAltaResponse, status_code=201)
def adicionar_pendencia(
    prontuario: str,
    payload: PendenciaAltaCreate,
    db: Session = Depends(get_db),
) -> PendenciaAltaResponse:
    if payload.codigo not in PENDENCIA_CODIGOS:
        raise HTTPException(status_code=400, detail=f"Código de pendência inválido: {payload.codigo}")

    existing = db.scalar(
        select(EgaaPendenciaAlta).where(
            EgaaPendenciaAlta.prontuario == prontuario,
            EgaaPendenciaAlta.codigo == payload.codigo,
        )
    )
    if existing is not None:
        if existing.resolvida:
            existing.resolvida = False
            existing.updated_at = dt_datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return PendenciaAltaResponse.model_validate(existing)
        raise HTTPException(status_code=409, detail="Pendência já cadastrada para este paciente.")

    now = dt_datetime.utcnow()
    row = EgaaPendenciaAlta(
        prontuario=prontuario,
        codigo=payload.codigo,
        resolvida=False,
        created_at=now,
        updated_at=now,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return PendenciaAltaResponse.model_validate(row)


@router.put("/pendencia/{prontuario}/{pendencia_id}", response_model=PendenciaAltaResponse)
def atualizar_pendencia(
    prontuario: str,
    pendencia_id: int,
    payload: PendenciaAltaResolve,
    db: Session = Depends(get_db),
) -> PendenciaAltaResponse:
    row = db.scalar(
        select(EgaaPendenciaAlta).where(
            EgaaPendenciaAlta.id == pendencia_id,
            EgaaPendenciaAlta.prontuario == prontuario,
        )
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Pendência não encontrada.")
    row.resolvida = payload.resolvida
    row.updated_at = dt_datetime.utcnow()
    db.commit()
    db.refresh(row)
    return PendenciaAltaResponse.model_validate(row)


@router.delete("/pendencia/{prontuario}/{pendencia_id}", status_code=204)
def remover_pendencia(
    prontuario: str,
    pendencia_id: int,
    db: Session = Depends(get_db),
) -> None:
    row = db.scalar(
        select(EgaaPendenciaAlta).where(
            EgaaPendenciaAlta.id == pendencia_id,
            EgaaPendenciaAlta.prontuario == prontuario,
        )
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Pendência não encontrada.")
    db.delete(row)
    db.commit()


# ─── Desfechos EGAA ──────────────────────────────────────────────


@router.get("/desfechos", response_model=list[EgaaDesfechoResponse])
def listar_desfechos(
    prontuario: str | None = Query(default=None),
    tipo: str | None = Query(default=None),
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    apenas_egaa: bool = Query(default=True, description="Se True, mostra apenas desfechos registrados manualmente pelo EGAA (com responsável)"),
    db: Session = Depends(get_db),
) -> list[EgaaDesfechoResponse]:
    query = select(EgaaDesfecho)
    if prontuario:
        query = query.where(EgaaDesfecho.prontuario == prontuario)
    if tipo:
        query = query.where(EgaaDesfecho.tipo == tipo)
    if data_inicio:
        query = query.where(EgaaDesfecho.data_desfecho >= data_inicio)
    if data_fim:
        query = query.where(EgaaDesfecho.data_desfecho <= data_fim)
    if apenas_egaa:
        # Desfechos registrados manualmente têm usuário responsável preenchido
        query = query.where(EgaaDesfecho.usuario_responsavel.isnot(None))

    rows = db.execute(
        query.order_by(
            desc(EgaaDesfecho.data_desfecho),
            desc(EgaaDesfecho.created_at),
            desc(EgaaDesfecho.id),
        )
    ).scalars().all()
    return [EgaaDesfechoResponse.model_validate(row) for row in rows]


@router.post("/desfechos", response_model=EgaaDesfechoResponse, status_code=201)
def criar_desfecho(
    payload: EgaaDesfechoCreate,
    db: Session = Depends(get_db),
) -> EgaaDesfechoResponse:
    if payload.tipo not in ("alta", "obito"):
        raise HTTPException(status_code=400, detail="Tipo deve ser 'alta' ou 'obito'.")

    if payload.intervencao_id is not None:
        intervencao = db.scalar(
            select(EgaaIntervencaoPaciente).where(EgaaIntervencaoPaciente.id == payload.intervencao_id)
        )
        if intervencao is None:
            raise HTTPException(status_code=404, detail="Intervenção vinculada não encontrada.")

    now = dt_datetime.utcnow()
    row = EgaaDesfecho(
        prontuario=payload.prontuario,
        tipo=payload.tipo,
        data_desfecho=payload.data_desfecho,
        descricao=payload.descricao,
        usuario_responsavel=payload.usuario_responsavel,
        intervencao_id=payload.intervencao_id,
        created_at=now,
        updated_at=now,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return EgaaDesfechoResponse.model_validate(row)


@router.get("/desfechos/{desfecho_id}", response_model=EgaaDesfechoResponse)
def get_desfecho(
    desfecho_id: int,
    db: Session = Depends(get_db),
) -> EgaaDesfechoResponse:
    row = db.scalar(select(EgaaDesfecho).where(EgaaDesfecho.id == desfecho_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Desfecho não encontrado.")
    return EgaaDesfechoResponse.model_validate(row)


@router.put("/desfechos/{desfecho_id}", response_model=EgaaDesfechoResponse)
def update_desfecho(
    desfecho_id: int,
    payload: EgaaDesfechoCreate,
    db: Session = Depends(get_db),
) -> EgaaDesfechoResponse:
    row = db.scalar(select(EgaaDesfecho).where(EgaaDesfecho.id == desfecho_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Desfecho não encontrado.")

    if payload.tipo not in ("alta", "obito"):
        raise HTTPException(status_code=400, detail="Tipo deve ser 'alta' ou 'obito'.")

    if payload.intervencao_id is not None:
        intervencao = db.scalar(
            select(EgaaIntervencaoPaciente).where(EgaaIntervencaoPaciente.id == payload.intervencao_id)
        )
        if intervencao is None:
            raise HTTPException(status_code=404, detail="Intervenção vinculada não encontrada.")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(row, field, value)
    row.updated_at = dt_datetime.utcnow()
    db.commit()
    db.refresh(row)
    return EgaaDesfechoResponse.model_validate(row)


@router.delete("/desfechos/{desfecho_id}", status_code=204)
def delete_desfecho(
    desfecho_id: int,
    db: Session = Depends(get_db),
) -> None:
    row = db.scalar(select(EgaaDesfecho).where(EgaaDesfecho.id == desfecho_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Desfecho não encontrado.")
    db.delete(row)
    db.commit()


def _desfecho_base_filter(apenas_egaa: bool = True):
    """Retorna o filtro base para consultas de desfecho."""
    if apenas_egaa:
        return EgaaDesfecho.usuario_responsavel.isnot(None)
    return True  # sem filtro


@router.get("/indicadores/desfechos", response_model=EgaaIndicadoresDesfechoResponse)
def get_indicadores_desfecho(
    apenas_egaa: bool = Query(default=True, description="Se True, mostra apenas desfechos registrados manualmente pelo EGAA"),
    db: Session = Depends(get_db),
) -> EgaaIndicadoresDesfechoResponse:
    try:
        base_filter = _desfecho_base_filter(apenas_egaa)
        total_desfechos = db.scalar(
            select(func.count()).select_from(EgaaDesfecho).where(base_filter)
        ) or 0
        total_altas = db.scalar(
            select(func.count()).select_from(EgaaDesfecho).where(EgaaDesfecho.tipo == "alta", base_filter)
        ) or 0
        total_obitos = db.scalar(
            select(func.count()).select_from(EgaaDesfecho).where(EgaaDesfecho.tipo == "obito", base_filter)
        ) or 0
        pacientes_com_desfecho = db.scalar(
            select(func.count(func.distinct(EgaaDesfecho.prontuario))).where(base_filter)
        ) or 0

        tipo_rows = db.execute(
            select(EgaaDesfecho.tipo, func.count().label("total"))
            .where(base_filter)
            .group_by(EgaaDesfecho.tipo)
            .order_by(EgaaDesfecho.tipo)
        ).all()

        mes_rows = db.execute(
            select(
                func.date_format(EgaaDesfecho.data_desfecho, "%Y-%m").label("mes"),
                func.count().label("total"),
            )
            .where(EgaaDesfecho.data_desfecho.is_not(None), base_filter)
            .group_by("mes")
            .order_by("mes")
        ).all()
    except Exception:
        return EgaaIndicadoresDesfechoResponse(
            total_desfechos=0,
            total_altas=0,
            total_obitos=0,
            pacientes_com_desfecho=0,
            por_tipo=[],
            por_mes=[],
        )

    return EgaaIndicadoresDesfechoResponse(
        total_desfechos=total_desfechos,
        total_altas=total_altas,
        total_obitos=total_obitos,
        pacientes_com_desfecho=pacientes_com_desfecho,
        por_tipo=[EgaaDesfechoPorTipo(tipo=row.tipo, total=row.total) for row in tipo_rows],
        por_mes=[EgaaDesfechoPorMes(mes=row.mes, total=row.total) for row in mes_rows],
    )
