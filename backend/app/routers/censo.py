from __future__ import annotations

from datetime import date
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, case, desc, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EgaaIntervencaoPaciente, OcupacaoLeitoGHC
from app.schemas import CensoKPIsResponse, OcupacaoPorUnidade, PacienteInternadoResponse, PacientesInternadosPage


router = APIRouter(prefix="/censo", tags=["Censo"])
EMERGENCIA_LEITOS = {"111", "113", "114", "115", "116", "117"}


def _resolve_snapshot_bounds(
    db: Session,
    data_inicio: date | None,
    data_fim: date | None,
) -> tuple[date | None, date | None]:
    if data_inicio is not None or data_fim is not None:
        return data_inicio, data_fim

    latest_snapshot = db.scalar(
        select(func.max(OcupacaoLeitoGHC.data_snapshot)).where(OcupacaoLeitoGHC.fonte_dado == "censo_diario")
    )
    if latest_snapshot is None:
        return None, None
    return latest_snapshot, latest_snapshot


def _active_filter():
    return and_(
        OcupacaoLeitoGHC.fonte_dado == "censo_diario",
        OcupacaoLeitoGHC.status_leito == "Ocupado",
    )


def _apply_date_filter(query, data_inicio: date | None, data_fim: date | None):
    if data_inicio is None and data_fim is None:
        return query

    query = query.where(_date_filter_expression(data_inicio, data_fim))
    return query


def _date_filter_expression(data_inicio: date | None, data_fim: date | None):
    reference_date = OcupacaoLeitoGHC.data_snapshot
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


def _egaa_summary_map(db: Session, prontuarios: list[str]) -> dict[str, dict[str, object]]:
    if not prontuarios:
        return {}

    atuacao_date_expr = func.coalesce(EgaaIntervencaoPaciente.data_atuacao, func.date(EgaaIntervencaoPaciente.created_at))
    rows = db.execute(
        select(
            EgaaIntervencaoPaciente.prontuario,
            func.count().label("egaa_total_atuacoes"),
            func.max(atuacao_date_expr).label("egaa_ultima_atuacao"),
        )
        .where(EgaaIntervencaoPaciente.prontuario.in_(prontuarios))
        .group_by(EgaaIntervencaoPaciente.prontuario)
    ).all()
    return {
        row.prontuario: {
            "egaa_total_atuacoes": int(row.egaa_total_atuacoes or 0),
            "egaa_ultima_atuacao": row.egaa_ultima_atuacao,
        }
        for row in rows
    }


@router.get("/kpis", response_model=CensoKPIsResponse)
def get_censo_kpis(
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> CensoKPIsResponse:
    try:
        data_inicio, data_fim = _resolve_snapshot_bounds(db, data_inicio, data_fim)
        if data_inicio is None and data_fim is None:
            return CensoKPIsResponse(
                total_internados=0,
                longa_permanencia_15=0,
                longa_permanencia_30=0,
                longa_permanencia_40=0,
                longa_permanencia_60_anos=0,
                longa_permanencia_60_15=0,
                longa_permanencia_60_30=0,
                leitos_ocupados=0,
                leitos_livres=0,
                leitos_bloqueados=0,
                taxa_ocupacao_geral_percentual=0.0,
                taxa_ocupacao_operacional_percentual=0.0,
                taxa_ocupacao_ajustada_sem_emergencia_percentual=0.0,
                ocupacao_por_unidade=[],
            )

        base_query = _filtered_active_query(data_inicio, data_fim)
        base_subquery = base_query.subquery()

        total_internados = db.scalar(select(func.count()).select_from(base_subquery)) or 0
        longa_15 = db.scalar(
            select(func.count()).select_from(base_subquery).where(base_subquery.c.dias_internacao >= 15)
        ) or 0
        longa_30 = db.scalar(
            select(func.count()).select_from(base_subquery).where(base_subquery.c.dias_internacao >= 30)
        ) or 0
        longa_40 = db.scalar(
            select(func.count()).select_from(base_subquery).where(base_subquery.c.dias_internacao >= 40)
        ) or 0
        longa_60_anos = db.scalar(
            select(func.count()).select_from(base_subquery).where(base_subquery.c.idade_anos >= 60)
        ) or 0
        longa_60_15 = db.scalar(
            select(func.count()).select_from(base_subquery).where(
                and_(base_subquery.c.idade_anos >= 60, base_subquery.c.dias_internacao >= 15)
            )
        ) or 0
        longa_60_30 = db.scalar(
            select(func.count()).select_from(base_subquery).where(
                and_(base_subquery.c.idade_anos >= 60, base_subquery.c.dias_internacao >= 30)
            )
        ) or 0

        leito_normalizado = func.trim(func.coalesce(OcupacaoLeitoGHC.leito, ""))
        base_leitos = db.execute(
            select(
                func.count().label("total_leitos"),
                func.sum(case((OcupacaoLeitoGHC.status_leito == "Ocupado", 1), else_=0)).label("leitos_ocupados"),
                func.sum(case((OcupacaoLeitoGHC.status_leito == "Livre", 1), else_=0)).label("leitos_livres"),
                func.sum(case((OcupacaoLeitoGHC.status_leito == "Bloqueado", 1), else_=0)).label("leitos_bloqueados"),
                func.sum(case((OcupacaoLeitoGHC.status_leito != "Bloqueado", 1), else_=0)).label("leitos_operacionais"),
                func.sum(
                    case(
                        (
                            and_(
                                OcupacaoLeitoGHC.status_leito == "Ocupado",
                                ~leito_normalizado.in_(EMERGENCIA_LEITOS),
                            ),
                            1,
                        ),
                        else_=0,
                    )
                ).label("ocupados_sem_emergencia"),
                func.sum(
                    case(
                        (
                            and_(
                                OcupacaoLeitoGHC.status_leito != "Bloqueado",
                                ~leito_normalizado.in_(EMERGENCIA_LEITOS),
                            ),
                            1,
                        ),
                        else_=0,
                    )
                ).label("operacionais_sem_emergencia"),
            )
            .where(OcupacaoLeitoGHC.fonte_dado == "censo_diario")
            .where(_date_filter_expression(data_inicio, data_fim))
        ).one()

        total_leitos = int(base_leitos.total_leitos or 0)
        leitos_ocupados = int(base_leitos.leitos_ocupados or 0)
        leitos_livres = int(base_leitos.leitos_livres or 0)
        leitos_bloqueados = int(base_leitos.leitos_bloqueados or 0)
        leitos_operacionais = int(base_leitos.leitos_operacionais or 0)
        ocupados_sem_emergencia = int(base_leitos.ocupados_sem_emergencia or 0)
        operacionais_sem_emergencia = int(base_leitos.operacionais_sem_emergencia or 0)

        taxa_ocupacao_geral = round((leitos_ocupados / total_leitos) * 100, 2) if total_leitos else 0.0
        taxa_ocupacao_operacional = (
            round((leitos_ocupados / leitos_operacionais) * 100, 2) if leitos_operacionais else 0.0
        )
        taxa_ocupacao_ajustada_sem_emergencia = (
            round((ocupados_sem_emergencia / operacionais_sem_emergencia) * 100, 2)
            if operacionais_sem_emergencia
            else 0.0
        )

        unidades_query = (
            select(OcupacaoLeitoGHC.unidade, func.count().label("total_pacientes"))
            .select_from(OcupacaoLeitoGHC)
            .where(_active_filter())
            .where(_date_filter_expression(data_inicio, data_fim))
            .group_by(OcupacaoLeitoGHC.unidade)
            .order_by(desc("total_pacientes"), OcupacaoLeitoGHC.unidade)
        )
        unidades = db.execute(unidades_query).all()
    except Exception:
        return CensoKPIsResponse(
            total_internados=0,
            longa_permanencia_15=0,
            longa_permanencia_30=0,
            longa_permanencia_40=0,
            longa_permanencia_60_anos=0,
            longa_permanencia_60_15=0,
            longa_permanencia_60_30=0,
            leitos_ocupados=0,
            leitos_livres=0,
            leitos_bloqueados=0,
            taxa_ocupacao_geral_percentual=0.0,
            taxa_ocupacao_operacional_percentual=0.0,
            taxa_ocupacao_ajustada_sem_emergencia_percentual=0.0,
            ocupacao_por_unidade=[],
        )

    return CensoKPIsResponse(
        total_internados=total_internados,
        longa_permanencia_15=longa_15,
        longa_permanencia_30=longa_30,
        longa_permanencia_40=longa_40,
        longa_permanencia_60_anos=longa_60_anos,
        longa_permanencia_60_15=longa_60_15,
        longa_permanencia_60_30=longa_60_30,
        leitos_ocupados=leitos_ocupados,
        leitos_livres=leitos_livres,
        leitos_bloqueados=leitos_bloqueados,
        taxa_ocupacao_geral_percentual=taxa_ocupacao_geral,
        taxa_ocupacao_operacional_percentual=taxa_ocupacao_operacional,
        taxa_ocupacao_ajustada_sem_emergencia_percentual=taxa_ocupacao_ajustada_sem_emergencia,
        ocupacao_por_unidade=[
            OcupacaoPorUnidade(unidade=row.unidade, total_pacientes=row.total_pacientes) for row in unidades
        ],
    )


@router.get("/pacientes", response_model=PacientesInternadosPage)
def get_pacientes_internados(
    prontuario: str | None = Query(default=None),
    nome: str | None = Query(default=None),
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
    try:
        data_inicio, data_fim = _resolve_snapshot_bounds(db, data_inicio, data_fim)
        if data_inicio is None and data_fim is None:
            return PacientesInternadosPage(total=0, page=page, page_size=page_size, items=[])

        base_query = _filtered_active_query(data_inicio, data_fim)
        if especialidade:
            base_query = base_query.where(OcupacaoLeitoGHC.especialidade == especialidade)
        if unidade:
            base_query = base_query.where(OcupacaoLeitoGHC.unidade == unidade)
        if prontuario:
            base_query = base_query.where(OcupacaoLeitoGHC.prontuario.like(f"%{prontuario}%"))
        if nome:
            base_query = base_query.where(OcupacaoLeitoGHC.nome_paciente.like(f"%{nome}%"))
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

        egas_map = _egaa_summary_map(db, [row.prontuario for row in rows if row.prontuario])
        items = [
            PacienteInternadoResponse.model_validate(row).model_copy(
                update=egas_map.get(
                    row.prontuario,
                    {"egaa_total_atuacoes": 0, "egaa_ultima_atuacao": None},
                )
            )
            for row in rows
        ]
    except Exception:
        return PacientesInternadosPage(total=0, page=page, page_size=page_size, items=[])

    return PacientesInternadosPage(
        total=total,
        page=page,
        page_size=page_size,
        items=items,
    )


@router.get("/paciente/{prontuario}", response_model=PacienteInternadoResponse)
def get_paciente_por_prontuario(
    prontuario: str,
    db: Session = Depends(get_db),
) -> PacienteInternadoResponse:
    data_inicio, data_fim = _resolve_snapshot_bounds(db, None, None)
    if data_inicio is None and data_fim is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")

    row = db.scalar(
        select(OcupacaoLeitoGHC)
        .where(_active_filter())
        .where(_date_filter_expression(data_inicio, data_fim))
        .where(OcupacaoLeitoGHC.prontuario == prontuario)
        .order_by(desc(OcupacaoLeitoGHC.dias_internacao), OcupacaoLeitoGHC.nome_paciente)
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado.")
    egas_map = _egaa_summary_map(db, [prontuario])
    return PacienteInternadoResponse.model_validate(row).model_copy(
        update=egas_map.get(prontuario, {"egaa_total_atuacoes": 0, "egaa_ultima_atuacao": None})
    )


@router.get("/export/xlsx")
def export_pacientes_xlsx(
    prontuario: str | None = Query(default=None),
    nome: str | None = Query(default=None),
    especialidade: str | None = Query(default=None),
    unidade: str | None = Query(default=None),
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
    min_dias: int | None = Query(default=None, ge=0),
    idade_minima: int | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    data_inicio, data_fim = _resolve_snapshot_bounds(db, data_inicio, data_fim)
    if data_inicio is None and data_fim is None:
        empty = BytesIO()
        pd.DataFrame([]).to_excel(empty, index=False)
        empty.seek(0)
        return StreamingResponse(
            empty,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": 'attachment; filename="egaa_pacientes.xlsx"'},
        )

    base_query = _filtered_active_query(data_inicio, data_fim)
    if especialidade:
        base_query = base_query.where(OcupacaoLeitoGHC.especialidade == especialidade)
    if unidade:
        base_query = base_query.where(OcupacaoLeitoGHC.unidade == unidade)
    if prontuario:
        base_query = base_query.where(OcupacaoLeitoGHC.prontuario.like(f"%{prontuario}%"))
    if nome:
        base_query = base_query.where(OcupacaoLeitoGHC.nome_paciente.like(f"%{nome}%"))
    if min_dias is not None:
        base_query = base_query.where(OcupacaoLeitoGHC.dias_internacao >= min_dias)
    if idade_minima is not None:
        base_query = base_query.where(OcupacaoLeitoGHC.idade_anos >= idade_minima)

    rows = db.execute(
        base_query.order_by(desc(OcupacaoLeitoGHC.dias_internacao), OcupacaoLeitoGHC.nome_paciente)
    ).scalars().all()
    egas_map = _egaa_summary_map(db, [row.prontuario for row in rows if row.prontuario])
    data = [
        PacienteInternadoResponse.model_validate(row)
        .model_copy(update=egas_map.get(row.prontuario, {"egaa_total_atuacoes": 0, "egaa_ultima_atuacao": None}))
        .model_dump(mode="json")
        for row in rows
    ]
    df = pd.DataFrame(data)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
      df.to_excel(writer, index=False, sheet_name="pacientes")
      pd.DataFrame([{
          "especialidade": especialidade or "",
          "unidade": unidade or "",
          "data_inicio": data_inicio.isoformat() if data_inicio else "",
          "data_fim": data_fim.isoformat() if data_fim else "",
          "min_dias": min_dias if min_dias is not None else "",
          "idade_minima": idade_minima if idade_minima is not None else "",
          "total_registros": len(data),
      }]).to_excel(writer, index=False, sheet_name="filtros")
    buffer.seek(0)

    filename = "egaa_pacientes.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
