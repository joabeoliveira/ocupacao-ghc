from __future__ import annotations

import os
import tempfile
import uuid
import logging
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, engine as db_engine
from app.models import EgaaDesfecho, OcupacaoLeitoGHC
from app.schemas import UploadCensoResponse
from etl_process import process_file, processar_censo_diario, processar_historico


router = APIRouter(prefix="/upload", tags=["Upload"])
ALLOWED_SUFFIXES = {".xls", ".xlsx", ".csv"}
LOGGER = logging.getLogger(__name__)


def _criar_desfechos_do_lote(lote_importacao_id: str):
    """Cria registros em egaa_desfecho para pacientes com data_alta no lote importado.

    Regras:
    - data_obito preenchida → tipo='obito', data=data_obito
    - tipo_alta contém 'ÓBITO' → tipo='obito', data=data_alta
    - Senão → tipo='alta', data=data_alta
    - Ignora prontuários que já possuem desfecho registrado
    """
    from sqlalchemy import MetaData, Table, create_engine, text

    from app.config import settings

    engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
    metadata = MetaData()
    ocupacao = Table("ocupacao_leitos_ghc", metadata, autoload_with=engine)
    desfecho = Table("egaa_desfecho", metadata, autoload_with=engine)

    now = datetime.utcnow()
    criados = 0

    with engine.connect() as conn:
        # Buscar registros do lote com data_alta
        subq = (
            select(
                ocupacao.c.prontuario,
                func.max(
                    func.coalesce(ocupacao.c.data_obito, ocupacao.c.data_alta)
                ).label("data_desfecho_max"),
            )
            .where(
                and_(
                    ocupacao.c.lote_importacao_id == lote_importacao_id,
                    ocupacao.c.fonte_dado == "historico_internacao",
                    ocupacao.c.data_alta.isnot(None),
                    ocupacao.c.prontuario.isnot(None),
                )
            )
            .group_by(ocupacao.c.prontuario)
        ).subquery()

        rows = conn.execute(
            select(ocupacao)
            .join(
                subq,
                and_(
                    ocupacao.c.prontuario == subq.c.prontuario,
                    func.coalesce(ocupacao.c.data_obito, ocupacao.c.data_alta) == subq.c.data_desfecho_max,
                ),
            )
            .where(
                and_(
                    ocupacao.c.lote_importacao_id == lote_importacao_id,
                    ocupacao.c.fonte_dado == "historico_internacao",
                    ocupacao.c.data_alta.isnot(None),
                    ocupacao.c.prontuario.isnot(None),
                )
            )
        ).fetchall()

        for row in rows:
            row_dict = dict(row._mapping)
            prontuario = row_dict["prontuario"]
            tipo_alta = row_dict.get("tipo_alta")
            data_obito = row_dict.get("data_obito")
            data_alta = row_dict.get("data_alta")

            # Determinar tipo e data
            if data_obito is not None:
                tipo = "obito"
                data_desfecho = data_obito.date() if hasattr(data_obito, "date") else data_obito
            elif tipo_alta and "ÓBITO" in tipo_alta.upper():
                tipo = "obito"
                data_desfecho = data_alta.date() if hasattr(data_alta, "date") else data_alta
            else:
                tipo = "alta"
                data_desfecho = data_alta.date() if hasattr(data_alta, "date") else data_alta

            if data_desfecho is None:
                continue

            # Verificar se já existe desfecho
            existing = conn.execute(
                select(desfecho.c.id).where(desfecho.c.prontuario == prontuario).limit(1)
            ).fetchone()

            if existing:
                continue

            conn.execute(
                desfecho.insert().values(
                    prontuario=prontuario,
                    tipo=tipo,
                    data_desfecho=data_desfecho,
                    descricao=tipo_alta or "Importado automaticamente do histórico",
                    usuario_responsavel=None,
                    created_at=now,
                    updated_at=now,
                )
            )
            criados += 1

        conn.commit()

    if criados:
        LOGGER.info("Criados %s desfechos automaticamente do lote %s.", criados, lote_importacao_id)
    return criados


def _ensure_supported_file(file: UploadFile) -> str:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=400, detail="Envie um arquivo .xls, .xlsx ou .csv.")
    return suffix


async def _store_temp_file(file: UploadFile, suffix: str) -> Path:
    os.makedirs(settings.upload_tmp_dir, exist_ok=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=settings.upload_tmp_dir) as tmp_file:
        contents = await file.read()
        tmp_file.write(contents)
        return Path(tmp_file.name)


@router.post("/censo", response_model=UploadCensoResponse)
async def upload_censo(file: UploadFile = File(...)) -> UploadCensoResponse:
    suffix = _ensure_supported_file(file)
    lote_importacao_id = str(uuid.uuid4())
    tmp_path = await _store_temp_file(file, suffix)

    try:
        df = processar_censo_diario(tmp_path, persist=True, lote_importacao_id=lote_importacao_id)
        return UploadCensoResponse(
            message="Arquivo processado com sucesso na rotina de censo.",
            nome_arquivo=file.filename or tmp_path.name,
            lote_importacao_id=lote_importacao_id,
            linhas_processadas=len(df),
        )
    except Exception as exc:
        LOGGER.exception("Falha no upload de censo. arquivo=%s lote=%s", file.filename, lote_importacao_id)
        raise HTTPException(status_code=500, detail=f"Falha ao processar arquivo de censo: {exc}") from exc
    finally:
        tmp_path.unlink(missing_ok=True)


@router.post("/historico", response_model=UploadCensoResponse)
async def upload_historico(file: UploadFile = File(...)) -> UploadCensoResponse:
    suffix = _ensure_supported_file(file)
    lote_importacao_id = str(uuid.uuid4())
    tmp_path = await _store_temp_file(file, suffix)

    try:
        df = processar_historico(tmp_path, persist=True, lote_importacao_id=lote_importacao_id)
        return UploadCensoResponse(
            message="Arquivo processado com sucesso na rotina histórica.",
            nome_arquivo=file.filename or tmp_path.name,
            lote_importacao_id=lote_importacao_id,
            linhas_processadas=len(df),
        )
    except Exception as exc:
        LOGGER.exception("Falha no upload historico. arquivo=%s lote=%s", file.filename, lote_importacao_id)
        raise HTTPException(status_code=500, detail=f"Falha ao processar arquivo historico: {exc}") from exc
    finally:
        tmp_path.unlink(missing_ok=True)


@router.post("/arquivo", response_model=UploadCensoResponse)
async def upload_arquivo_auto(file: UploadFile = File(...)) -> UploadCensoResponse:
    suffix = _ensure_supported_file(file)
    lote_importacao_id = str(uuid.uuid4())
    tmp_path = await _store_temp_file(file, suffix)

    try:
        # Auto detecta historico/censo a partir do cabecalho do arquivo.
        df = process_file(tmp_path, persist=True, lote_importacao_id=lote_importacao_id)
        return UploadCensoResponse(
            message="Arquivo processado com sucesso (modo automático).",
            nome_arquivo=file.filename or tmp_path.name,
            lote_importacao_id=lote_importacao_id,
            linhas_processadas=len(df),
        )
    except Exception as exc:
        LOGGER.exception("Falha no upload automatico. arquivo=%s lote=%s", file.filename, lote_importacao_id)
        raise HTTPException(status_code=500, detail=f"Falha ao processar arquivo (auto): {exc}") from exc
    finally:
        tmp_path.unlink(missing_ok=True)