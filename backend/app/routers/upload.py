from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.schemas import UploadCensoResponse
from etl_process import process_file, processar_censo_diario, processar_historico


router = APIRouter(prefix="/upload", tags=["Upload"])
ALLOWED_SUFFIXES = {".xls", ".xlsx", ".csv"}


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
            message="Arquivo processado com sucesso na rotina historica.",
            nome_arquivo=file.filename or tmp_path.name,
            lote_importacao_id=lote_importacao_id,
            linhas_processadas=len(df),
        )
    except Exception as exc:
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
            message="Arquivo processado com sucesso (modo automatico).",
            nome_arquivo=file.filename or tmp_path.name,
            lote_importacao_id=lote_importacao_id,
            linhas_processadas=len(df),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Falha ao processar arquivo (auto): {exc}") from exc
    finally:
        tmp_path.unlink(missing_ok=True)