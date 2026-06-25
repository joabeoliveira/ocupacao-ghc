from __future__ import annotations

from sqlalchemy import and_, desc, func, select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.models import OcupacaoLeitoGHC
from app.schemas import CensoKPIsResponse, OcupacaoPorUnidade, PacienteInternadoResponse, PacientesInternadosPage


router = APIRouter(prefix="/censo", tags=["Censo"])


def _active_filter():
    return and_(OcupacaoLeitoGHC.data_alta.is_(None))


@router.get("/kpis", response_model=CensoKPIsResponse)
def get_censo_kpis(db: Session = Depends(get_db)) -> CensoKPIsResponse:
    active_condition = _active_filter()

    total_internados = db.scalar(select(func.count()).select_from(OcupacaoLeitoGHC).where(active_condition)) or 0
    longa_15 = (
        db.scalar(
            select(func.count()).select_from(OcupacaoLeitoGHC).where(active_condition, OcupacaoLeitoGHC.dias_internacao >= 15)
        )
        or 0
    )
    longa_30 = (
        db.scalar(
            select(func.count()).select_from(OcupacaoLeitoGHC).where(active_condition, OcupacaoLeitoGHC.dias_internacao >= 30)
        )
        or 0
    )

    unidades = db.execute(
        select(OcupacaoLeitoGHC.unidade, func.count().label("total_pacientes"))
        .where(active_condition)
        .group_by(OcupacaoLeitoGHC.unidade)
        .order_by(desc("total_pacientes"), OcupacaoLeitoGHC.unidade)
    ).all()

    return CensoKPIsResponse(
        total_internados=total_internados,
        longa_permanencia_15=longa_15,
        longa_permanencia_30=longa_30,
        ocupacao_por_unidade=[
            OcupacaoPorUnidade(unidade=row.unidade, total_pacientes=row.total_pacientes) for row in unidades
        ],
    )


@router.get("/pacientes", response_model=PacientesInternadosPage)
def get_pacientes_internados(
    especialidade: str | None = Query(default=None),
    unidade: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PacientesInternadosPage:
    filters = [_active_filter()]

    if especialidade:
        filters.append(OcupacaoLeitoGHC.especialidade == especialidade)
    if unidade:
        filters.append(OcupacaoLeitoGHC.unidade == unidade)

    base_query = select(OcupacaoLeitoGHC).where(*filters)
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