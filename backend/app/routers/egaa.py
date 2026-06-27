from __future__ import annotations

from datetime import date
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app.database import get_db
from app.models import EgaaIntervencaoPaciente, EgaaTipoIntervencao
from app.schemas import (
    EgaaIntervencaoPacienteBatchCreate,
    EgaaIntervencaoPacienteCreate,
    EgaaIntervencaoPacienteResponse,
    EgaaIndicadoresResponse,
    EgaaIntervencaoPorMes,
    EgaaIntervencaoPorStatus,
    EgaaIntervencaoPorTipo,
    EgaaTipoIntervencaoCreate,
    EgaaTipoIntervencaoResponse,
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
