from __future__ import annotations

import argparse
import hashlib
import logging
import os
import re
import uuid
from datetime import date
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
from sqlalchemy import CHAR, DATE, DATETIME, Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.dialects.mysql import ENUM, insert as mysql_insert


LOGGER = logging.getLogger(__name__)
TABLE_NAME = "ocupacao_leitos_ghc"


def clean_string(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    return text or None


def clean_int(value: Any) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    match = re.search(r"(\d+)", str(value))
    if not match:
        return None
    return int(match.group(1))


def parse_datetime_br(value: Any) -> pd.Timestamp | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    parsed = pd.to_datetime(value, format="%d/%m/%Y %H:%M", errors="coerce")
    if pd.isna(parsed):
        parsed = pd.to_datetime(value, format="%d/%m/%Y", errors="coerce")
    if pd.isna(parsed):
        parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
    if pd.isna(parsed):
        return None
    return parsed


def parse_date_br(value: Any) -> date | None:
    parsed = parse_datetime_br(value)
    if parsed is None:
        return None
    return parsed.date()


def parse_period_line(value: str | None) -> tuple[date | None, date | None]:
    if not value:
        return None, None
    matches = re.findall(r"(\d{2}/\d{2}/\d{4})", value)
    if len(matches) < 2:
        return None, None
    return parse_date_br(matches[0]), parse_date_br(matches[1])


def parse_dias_internacao(value: Any) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    direct = re.fullmatch(r"\d+", text)
    if direct:
        return int(text)
    days = re.search(r"(\d+)d", text)
    if days:
        return int(days.group(1))
    return clean_int(text)


def build_hash_registro(values: Iterable[Any]) -> str:
    base = "|".join("" if value is None else str(value).strip() for value in values)
    return hashlib.md5(base.encode("utf-8")).hexdigest()


def read_input_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".xls":
        return pd.read_excel(path, header=None, engine="xlrd")
    if suffix == ".xlsx":
        return pd.read_excel(path, header=None, engine="openpyxl")
    return pd.read_csv(path, header=None)


def make_unique_headers(headers: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    unique_headers: list[str] = []
    for header in headers:
        count = seen.get(header, 0)
        if count == 0:
            unique_headers.append(header)
        else:
            unique_headers.append(f"{header}_{count + 1}")
        seen[header] = count + 1
    return unique_headers


def extract_metadata_and_table(path: Path) -> tuple[dict[str, Any], pd.DataFrame]:
    raw = read_input_file(path)
    metadata: dict[str, Any] = {
        "nome_arquivo": path.name,
        "fonte_caminho": str(path),
    }

    header_index = None
    for index, row in raw.iterrows():
        values = [clean_string(value) for value in row.tolist()]
        first = values[0] if values else None

        if first and first.startswith("Período"):
            metadata["periodo_texto"] = first
            metadata["periodo_referencia_inicio"], metadata["periodo_referencia_fim"] = parse_period_line(first)

        if first and first.startswith("Data Impressão"):
            _, _, date_text = first.partition(":")
            metadata["data_impressao_arquivo"] = parse_datetime_br(date_text.strip())

        if values and any(value == "DATA_INTERNACAO" for value in values):
            header_index = index
            metadata["tipo_arquivo_detectado"] = "historico_internacao"
            break

        if values and any(value == "STATUS LEITO" for value in values):
            header_index = index
            metadata["tipo_arquivo_detectado"] = "censo_diario"
            break

    if header_index is None:
        raise ValueError(f"Nao foi possivel identificar o cabecalho do arquivo {path}")

    header = [clean_string(value) or f"coluna_{idx}" for idx, value in enumerate(raw.iloc[header_index].tolist())]
    header = make_unique_headers(header)
    df = raw.iloc[header_index + 1 :].copy()
    df.columns = header
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    return metadata, df.reset_index(drop=True)


def normalize_historico(df: pd.DataFrame, metadata: dict[str, Any], lote_importacao_id: str) -> pd.DataFrame:
    normalized = pd.DataFrame()
    normalized["prontuario"] = df["PRONTUARIO"].apply(clean_string)
    normalized["nome_paciente"] = df["NOME"].apply(clean_string)
    normalized["idade_anos"] = df["IDADE_ANOS"].apply(clean_int)
    normalized["idade_meses"] = df["IDADE_MES"].apply(clean_int)
    normalized["data_internacao"] = df["DATA_INTERNACAO"].apply(parse_datetime_br)
    normalized["data_alta"] = df["DATA_ALTA"].apply(parse_datetime_br)
    normalized["especialidade"] = df["ESPECIALIDADE"].apply(clean_string)
    normalized["unidade"] = df["UNIDADE"].apply(clean_string)
    normalized["enfermaria"] = df["ENFERMARIA"].apply(clean_string)
    normalized["leito"] = df["LEITO"].apply(clean_string)
    normalized["cid_internacao_codigo"] = df["CID_INTERNACAO"].apply(clean_string)
    normalized["cid_internacao_descricao"] = df["CID_DESCRICAO"].apply(clean_string)
    normalized["tipo_alta"] = df["TIPO_DE_ALTA"].apply(clean_string)
    normalized["dias_internacao"] = df["TEMPO_INTERNACAO"].apply(parse_dias_internacao)
    normalized["fonte_dado"] = "historico_internacao"
    normalized["lote_importacao_id"] = lote_importacao_id
    normalized["nome_arquivo"] = metadata["nome_arquivo"]
    normalized["data_snapshot"] = None
    normalized["periodo_referencia_inicio"] = metadata.get("periodo_referencia_inicio")
    normalized["periodo_referencia_fim"] = metadata.get("periodo_referencia_fim")
    normalized["data_impressao_arquivo"] = metadata.get("data_impressao_arquivo")
    normalized["hash_registro"] = normalized.apply(
        lambda row: build_hash_registro(
            [
                row["prontuario"],
                row["data_internacao"],
                row["data_alta"],
                row["leito"],
                row["cid_internacao_codigo"],
                row["fonte_dado"],
            ]
        ),
        axis=1,
    )
    for column in ["idade_anos", "idade_meses", "dias_internacao"]:
        normalized[column] = pd.array(normalized[column], dtype="Int64")
    return normalized


def normalize_censo(df: pd.DataFrame, metadata: dict[str, Any], lote_importacao_id: str) -> pd.DataFrame:
    normalized = pd.DataFrame()
    normalized["prontuario"] = df["PRONT"].apply(clean_string)
    normalized["nome_paciente"] = df["NOME"].apply(clean_string)
    normalized["idade_anos"] = df["IDADE (a)"].apply(clean_int)
    normalized["idade_meses"] = df["IDADE (m)"].apply(clean_int)
    normalized["data_internacao"] = df["DATA INTERNACAO"].apply(parse_datetime_br)
    normalized["data_alta"] = None
    normalized["especialidade"] = df["CLINICA RESPONSAVEL (FORA DE CLINICA)"].apply(clean_string)
    normalized["unidade"] = df["UNIDADE"].apply(clean_string)
    normalized["enfermaria"] = df["ENFERMARIA"].apply(clean_string)
    normalized["leito"] = df["LEITO"].apply(clean_string)
    normalized["cid_internacao_codigo"] = df["CID"].apply(clean_string)
    normalized["cid_internacao_descricao"] = df["CID DESCRICAO"].apply(clean_string)
    normalized["tipo_alta"] = None
    normalized["dias_internacao"] = df["DIAS INTER."].apply(clean_int)
    normalized["fonte_dado"] = "censo_diario"
    normalized["lote_importacao_id"] = lote_importacao_id
    normalized["nome_arquivo"] = metadata["nome_arquivo"]
    snapshot = None
    data_impressao = metadata.get("data_impressao_arquivo")
    if data_impressao is not None:
        snapshot = data_impressao.date()
    normalized["data_snapshot"] = snapshot
    normalized["periodo_referencia_inicio"] = None
    normalized["periodo_referencia_fim"] = None
    normalized["data_impressao_arquivo"] = data_impressao
    normalized["hash_registro"] = normalized.apply(
        lambda row: build_hash_registro(
            [
                row["prontuario"],
                row["data_internacao"],
                row["data_snapshot"],
                row["leito"],
                row["cid_internacao_codigo"],
                row["fonte_dado"],
            ]
        ),
        axis=1,
    )
    for column in ["idade_anos", "idade_meses", "dias_internacao"]:
        normalized[column] = pd.array(normalized[column], dtype="Int64")
    return normalized


def prepare_dataframe(path: Path, lote_importacao_id: str | None = None) -> pd.DataFrame:
    metadata, raw_df = extract_metadata_and_table(path)
    lote_id = lote_importacao_id or str(uuid.uuid4())
    if metadata["tipo_arquivo_detectado"] == "historico_internacao":
        return normalize_historico(raw_df, metadata, lote_id)
    if metadata["tipo_arquivo_detectado"] == "censo_diario":
        return normalize_censo(raw_df, metadata, lote_id)
    raise ValueError(f"Tipo de arquivo nao suportado: {metadata['tipo_arquivo_detectado']}")


def get_mysql_engine():
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE")
    if not all([user, password, host, database]):
        raise RuntimeError("Defina MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST e MYSQL_DATABASE no ambiente.")
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    return create_engine(url, future=True)


def get_ocupacao_table_definition(metadata: MetaData) -> Table:
    return Table(
        TABLE_NAME,
        metadata,
        Column("prontuario", String(50), nullable=False),
        Column("nome_paciente", String(255)),
        Column("idade_anos", Integer),
        Column("idade_meses", Integer),
        Column("data_internacao", DATETIME),
        Column("data_alta", DATETIME),
        Column("dias_internacao", Integer),
        Column("especialidade", String(150), nullable=False),
        Column("unidade", String(150)),
        Column("enfermaria", String(150)),
        Column("leito", String(50)),
        Column("cid_internacao_codigo", String(20)),
        Column("cid_internacao_descricao", String(255)),
        Column("tipo_alta", String(100)),
        Column("fonte_dado", ENUM("historico_internacao", "censo_diario"), nullable=False),
        Column("lote_importacao_id", CHAR(36), nullable=False),
        Column("nome_arquivo", String(255), nullable=False),
        Column("hash_registro", CHAR(64), nullable=False),
        Column("data_snapshot", DATE),
        Column("periodo_referencia_inicio", DATE),
        Column("periodo_referencia_fim", DATE),
        Column("data_impressao_arquivo", DATETIME),
    )


def persist_dataframe(df: pd.DataFrame, engine) -> int:
    metadata = MetaData()
    table = get_ocupacao_table_definition(metadata)
    records = df.where(pd.notna(df), None).to_dict(orient="records")
    if not records:
        return 0

    with engine.begin() as connection:
        statement = mysql_insert(table).values(records)
        upsert = statement.on_duplicate_key_update(
            nome_paciente=statement.inserted.nome_paciente,
            idade_anos=statement.inserted.idade_anos,
            idade_meses=statement.inserted.idade_meses,
            data_alta=statement.inserted.data_alta,
            dias_internacao=statement.inserted.dias_internacao,
            especialidade=statement.inserted.especialidade,
            unidade=statement.inserted.unidade,
            enfermaria=statement.inserted.enfermaria,
            leito=statement.inserted.leito,
            cid_internacao_codigo=statement.inserted.cid_internacao_codigo,
            cid_internacao_descricao=statement.inserted.cid_internacao_descricao,
            tipo_alta=statement.inserted.tipo_alta,
            data_snapshot=statement.inserted.data_snapshot,
            periodo_referencia_inicio=statement.inserted.periodo_referencia_inicio,
            periodo_referencia_fim=statement.inserted.periodo_referencia_fim,
            data_impressao_arquivo=statement.inserted.data_impressao_arquivo,
            lote_importacao_id=statement.inserted.lote_importacao_id,
            nome_arquivo=statement.inserted.nome_arquivo,
        )
        result = connection.execute(upsert)
    return result.rowcount or 0


def process_file(path: Path, persist: bool = False, lote_importacao_id: str | None = None) -> pd.DataFrame:
    df = prepare_dataframe(path, lote_importacao_id=lote_importacao_id)
    LOGGER.info("Arquivo %s processado com %s linhas normalizadas", path.name, len(df))
    if persist:
        engine = get_mysql_engine()
        affected = persist_dataframe(df, engine)
        LOGGER.info("Persistencia concluida. Linhas afetadas: %s", affected)
    return df


def processar_censo_diario(path: str | Path, persist: bool = True, lote_importacao_id: str | None = None) -> pd.DataFrame:
    return process_file(Path(path), persist=persist, lote_importacao_id=lote_importacao_id)


def processar_historico(path: str | Path, persist: bool = True, lote_importacao_id: str | None = None) -> pd.DataFrame:
    return process_file(Path(path), persist=persist, lote_importacao_id=lote_importacao_id)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ETL para carga historica e censo diario do EGAA")
    parser.add_argument("--historico", type=Path, default=Path("data/samples/relatorio-internacao.xls"))
    parser.add_argument("--censo", type=Path, default=Path("data/samples/censo-hospitalar.xls"))
    parser.add_argument("--persist", action="store_true")
    parser.add_argument("--lote-id", default=None)
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    for path in [args.historico, args.censo]:
        if path.exists():
            process_file(path, persist=args.persist, lote_importacao_id=args.lote_id)
        else:
            LOGGER.warning("Arquivo nao encontrado: %s", path)


if __name__ == "__main__":
    main()