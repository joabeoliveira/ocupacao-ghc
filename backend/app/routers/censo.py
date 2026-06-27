from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import OcupacaoLeitoGHC
from app.schemas import CensoKPIsResponse, OcupacaoPorUnidade, PacienteInternadoResponse, PacientesInternadosPage


router = APIRouter(prefix="/censo", tags=["Censo"])


def _active_filter():
    return and_(OcupacaoLeitoGHC.data_alta.is_(None))


def _apply_date_filter(query, data_inicio: date | None, data_fim: date | None):
    if data_inicio is None and data_fim is None:
        return query

    query = query.where(_date_filter_expression(data_inicio, data_fim))
    return query


def _date_filter_expression(data_inicio: date | None, data_fim: date | None):
    reference_date = func.coalesce(OcupacaoLeitoGHC.data_snapshot, func.date(OcupacaoLeitoGHC.data_internacao))
    if data_inicio is not None and data_fim is not None:
        return reference_date.between(data_inicio, data_fim)
    if data_inicio is not None:
        return reference_date >= data_inicio
    if data_fim is not None:
        return reference_date <= data_fim
    return True


def _filtered_active_query(data_inicio: date | None = None, data_fim: date | None = None):
    query = select(OcupacaoLeitoGHC).where(_active_filter())
    return _apply_date_filter(query, data_inicio, data_fim)


@router.get("/kpis", response_model=CensoKPIsResponse)
def get_censo_kpis(
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> CensoKPIsResponse:
    base_query = _filtered_active_query(data_inicio, data_fim)
    base_subquery = base_query.subquery()

    total_internados = db.scalar(select(func.count()).select_from(base_subquery)) or 0
    longa_15 = db.scalar(
        select(func.count()).select_from(base_subquery).where(base_subquery.c.dias_internacao >= 15)
    ) or 0
    longa_30 = db.scalar(
        select(func.count()).select_from(base_subquery).where(base_subquery.c.dias_internacao >= 30)
    ) or 0
    longa_60_anos = db.scalar(
        select(func.count()).select_from(base_subquery).where(base_subquery.c.idade_anos >= 60)
    ) or 0

    unidades_query = (
        select(OcupacaoLeitoGHC.unidade, func.count().label("total_pacientes"))
        .select_from(OcupacaoLeitoGHC)
        .where(_active_filter())
        .where(_date_filter_expression(data_inicio, data_fim))
        .group_by(OcupacaoLeitoGHC.unidade)
        .order_by(desc("total_pacientes"), OcupacaoLeitoGHC.unidade)
    )
    unidades = db.execute(unidades_query).all()

    return CensoKPIsResponse(
        total_internados=total_internados,
        longa_permanencia_15=longa_15,
        longa_permanencia_30=longa_30,
        longa_permanencia_60_anos=longa_60_anos,
        ocupacao_por_unidade=[
            OcupacaoPorUnidade(unidade=row.unidade, total_pacientes=row.total_pacientes) for row in unidades
        ],
    )


@router.get("/pacientes", response_model=PacientesInternadosPage)
def get_pacientes_internados(
    especialidade: str | None = Query(default=None),
    unidade: str | None = Query(default=None),
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    min_dias: int | None = Query(default=None, ge=0),
    idade_minima: int | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PacientesInternadosPage:
    base_query = _filtered_active_query(data_inicio, data_fim)
    if especialidade:
        base_query = base_query.where(OcupacaoLeitoGHC.especialidade == especialidade)
    if unidade:
        base_query = base_query.where(OcupacaoLeitoGHC.unidade == unidade)
    if min_dias is not None:
        base_query = base_query.where(OcupacaoLeitoGHC.dias_internacao >= min_dias)
    if idade_minima is not None:
        base_query = base_query.where(OcupacaoLeitoGHC.idade_anos >= idade_minima)

    total = db.scalar(select(func.count()).select_from(base_query.subquery())) or 0

    rows = db.execute(
        base_query.order_by(desc(OcupacaoLeitoGHC.dias_internacao), OcupacaoLeitoGHC.nome_paciente)
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).scalars().all()

    return PacientesInternadosPage(
        total=total,
        page=page,
        page_size=page_size,
        items=[PacienteInternadoResponse.model_validate(row) for row in rows],
    )
