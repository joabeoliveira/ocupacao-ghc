from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.schemas import UploadCensoResponse
from etl_process import processar_censo_diario


router = APIRouter(prefix="/upload", tags=["Upload"])
ALLOWED_SUFFIXES = {".xls", ".xlsx", ".csv"}


@router.post("/censo", response_model=UploadCensoResponse)
async def upload_censo(file: UploadFile = File(...)) -> UploadCensoResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=400, detail="Envie um arquivo .xls, .xlsx ou .csv do censo diario.")

    os.makedirs(settings.upload_tmp_dir, exist_ok=True)
    lote_importacao_id = str(uuid.uuid4())

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=settings.upload_tmp_dir) as tmp_file:
        contents = await file.read()
        tmp_file.write(contents)
        tmp_path = Path(tmp_file.name)

    try:
        df = processar_censo_diario(tmp_path, persist=True, lote_importacao_id=lote_importacao_id)
        return UploadCensoResponse(
            message="Arquivo de censo processado com sucesso.",
            nome_arquivo=file.filename or tmp_path.name,
            lote_importacao_id=lote_importacao_id,
            linhas_processadas=len(df),
        )
    finally:
        tmp_path.unlink(missing_ok=True)