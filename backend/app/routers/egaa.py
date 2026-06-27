from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EgaaIntervencaoPaciente, EgaaTipoIntervencao
from app.schemas import (
    EgaaIntervencaoPacienteCreate,
    EgaaIntervencaoPacienteResponse,
    EgaaTipoIntervencaoCreate,
    EgaaTipoIntervencaoResponse,
)


router = APIRouter(prefix="/egaa", tags=["EGAA"])


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

    rows = db.execute(query.order_by(desc(EgaaIntervencaoPaciente.created_at), desc(EgaaIntervencaoPaciente.id))).scalars().all()
    return [EgaaIntervencaoPacienteResponse.model_validate(row) for row in rows]


@router.post("/intervencoes", response_model=EgaaIntervencaoPacienteResponse, status_code=201)
def create_intervencao(
    payload: EgaaIntervencaoPacienteCreate,
    db: Session = Depends(get_db),
) -> EgaaIntervencaoPacienteResponse:
    tipo = db.scalar(select(EgaaTipoIntervencao).where(EgaaTipoIntervencao.id == payload.tipo_intervencao_id))
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de intervenção não encontrado.")

    row = EgaaIntervencaoPaciente(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return EgaaIntervencaoPacienteResponse.model_validate(row)
