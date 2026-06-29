from __future__ import annotations

import argparse
import csv
import hashlib
import logging
import os
import re
import unicodedata
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


def normalize_token(value: Any) -> str:
    text = clean_string(value) or ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().upper()


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

def normalizar_status_leito(valor: Any) -> str | None:
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return None
    texto = str(valor).strip()
    if not texto:
        return None
    low = texto.lower()
    if low.startswith("ocupado"):
        return "Ocupado"
    if low.startswith("livre"):
        return "Livre"
    if low.startswith("bloqueado"):
        return "Bloqueado"
    return texto

def build_hash_registro(values: Iterable[Any]) -> str:
    base = "|".join("" if value is None else str(value).strip() for value in values)
    return hashlib.md5(base.encode("utf-8")).hexdigest()


def read_input_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".xls":
        return pd.read_excel(path, header=None, engine="xlrd")
    if suffix == ".xlsx":
        return pd.read_excel(path, header=None, engine="openpyxl")
    # CSVs do esusreport podem ter linhas de metadado com numero de colunas variavel,
    # quebrando o parser padrao do pandas; fazemos parse manual e normalizamos o shape.
    decoded = None
    last_error = None
    for encoding in ("utf-8", "utf-8-sig", "latin1", "cp1252"):
        try:
            decoded = path.read_text(encoding=encoding)
            break
        except Exception as exc:  # pragma: no cover - fallback chain
            last_error = exc
    if decoded is None:
        raise RuntimeError(f"Falha ao ler CSV {path.name}: {last_error}")

    lines = decoded.splitlines()
    if not lines:
        return pd.DataFrame()

    # Detecta delimitador usando linhas candidatas de cabecalho.
    delimiter = ","
    for line in lines[:30]:
        upper_line = normalize_token(line)
        if "DATA_INTERNACAO" in upper_line or "STATUS LEITO" in upper_line:
            comma_count = line.count(",")
            semicolon_count = line.count(";")
            tab_count = line.count("\t")
            if semicolon_count > comma_count and semicolon_count >= tab_count:
                delimiter = ";"
            elif tab_count > comma_count and tab_count > semicolon_count:
                delimiter = "\t"
            break

    reader = csv.reader(lines, delimiter=delimiter, quotechar='"')
    rows = [row for row in reader]
    if not rows:
        return pd.DataFrame()

    max_cols = max(len(row) for row in rows)
    normalized_rows = [row + [None] * (max_cols - len(row)) for row in rows]
    return pd.DataFrame(normalized_rows)


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


def _build_column_alias_map(df: pd.DataFrame) -> dict[str, str]:
    alias_map: dict[str, str] = {}
    for column in df.columns:
        key = normalize_token(column)
        if key and key not in alias_map:
            alias_map[key] = column
    return alias_map


def _get_series_by_alias(
    df: pd.DataFrame,
    alias_map: dict[str, str],
    aliases: list[str],
    *,
    required: bool = False,
    default: Any = None,
) -> pd.Series:
    for alias in aliases:
        key = normalize_token(alias)
        if key in alias_map:
            return df[alias_map[key]]
    if required:
        raise KeyError(f"Coluna obrigatoria ausente. Esperado uma das: {aliases}")
    return pd.Series([default] * len(df), index=df.index)


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
        first_norm = normalize_token(first)
        normalized_values = [normalize_token(v) for v in values if v is not None]

        if first_norm.startswith("PERIODO"):
            metadata["periodo_texto"] = first
            metadata["periodo_referencia_inicio"], metadata["periodo_referencia_fim"] = parse_period_line(first)

        if first_norm.startswith("DATA IMPRESSAO"):
            _, _, date_text = first.partition(":")
            metadata["data_impressao_arquivo"] = parse_datetime_br(date_text.strip())

        if values and any(value == "STATUS LEITO" for value in normalized_values):
            header_index = index
            metadata["tipo_arquivo_detectado"] = "censo_diario"
            break

        if values and any(value in {"PRONTUARIO", "TIPO_DE_ALTA", "TEMPO_INTERNACAO"} for value in normalized_values):
            header_index = index
            metadata["tipo_arquivo_detectado"] = "historico_internacao"
            break

        if values and any(value in {"DATA_INTERNACAO", "DATA INTERNACAO"} for value in normalized_values):
            header_index = index
            metadata["tipo_arquivo_detectado"] = "historico_internacao"
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
    alias_map = _build_column_alias_map(df)
    normalized = pd.DataFrame()
    normalized["prontuario"] = _get_series_by_alias(df, alias_map, ["PRONTUARIO", "PRONT"], required=True).apply(clean_string)
    normalized["nome_paciente"] = _get_series_by_alias(df, alias_map, ["NOME"], required=True).apply(clean_string)
    normalized["idade_anos"] = _get_series_by_alias(df, alias_map, ["IDADE_ANOS", "IDADE (a)"]).apply(clean_int)
    normalized["idade_meses"] = _get_series_by_alias(df, alias_map, ["IDADE_MES", "IDADE (m)"]).apply(clean_int)
    normalized["data_internacao"] = _get_series_by_alias(df, alias_map, ["DATA_INTERNACAO", "DATA INTERNACAO"], required=True).apply(parse_datetime_br)
    normalized["data_alta"] = _get_series_by_alias(df, alias_map, ["DATA_ALTA"]).apply(parse_datetime_br)
    normalized["especialidade"] = _get_series_by_alias(
        df,
        alias_map,
        ["ESPECIALIDADE", "CLINICA RESPONSAVEL (FORA DE CLINICA)"],
        required=True,
    ).apply(clean_string)
    normalized["unidade"] = _get_series_by_alias(df, alias_map, ["UNIDADE"]).apply(clean_string)
    normalized["enfermaria"] = _get_series_by_alias(df, alias_map, ["ENFERMARIA"]).apply(clean_string)
    normalized["leito"] = _get_series_by_alias(df, alias_map, ["LEITO"]).apply(clean_string)
    normalized["cid_internacao_codigo"] = _get_series_by_alias(df, alias_map, ["CID_INTERNACAO", "CID"]).apply(clean_string)
    normalized["cid_internacao_descricao"] = _get_series_by_alias(df, alias_map, ["CID_DESCRICAO", "CID DESCRICAO"]).apply(clean_string)
    normalized["tipo_alta"] = _get_series_by_alias(df, alias_map, ["TIPO_DE_ALTA"]).apply(clean_string)
    normalized["dias_internacao"] = _get_series_by_alias(df, alias_map, ["TEMPO_INTERNACAO", "DIAS INTER."]).apply(parse_dias_internacao)
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
    # recalcula dias_internacao de forma robusta (evita valores absurdos)
    normalized = _recalculate_dias(normalized)

    for column in ["idade_anos", "idade_meses", "dias_internacao"]:
        normalized[column] = pd.array(normalized[column], dtype="Int64")
    return normalized


def _recalculate_dias(df: pd.DataFrame) -> pd.DataFrame:
    # Garante datetimes e calcula dias_internacao de forma robusta
    if "data_internacao" in df.columns:
        df["data_internacao"] = pd.to_datetime(df["data_internacao"], errors="coerce")
    else:
        df["data_internacao"] = pd.NaT

    if "data_alta" in df.columns:
        df["data_alta"] = pd.to_datetime(df["data_alta"], errors="coerce")
    else:
        df["data_alta"] = pd.NaT

    today = pd.to_datetime("today").normalize()

    # Para registros com data_internacao presente e sem data_alta: diferença até hoje
    mask_internado = df["data_internacao"].notna() & df["data_alta"].isna()
    if mask_internado.any():
        df.loc[mask_internado, "dias_internacao"] = (today - df.loc[mask_internado, "data_internacao"]).dt.days

    # Para registros com data_internacao e data_alta: diferença entre datas
    mask_alta = df["data_internacao"].notna() & df["data_alta"].notna()
    if mask_alta.any():
        df.loc[mask_alta, "dias_internacao"] = (df.loc[mask_alta, "data_alta"] - df.loc[mask_alta, "data_internacao"]).dt.days

    # Força tipo inteiro e remove valores negativos
    df["dias_internacao"] = pd.to_numeric(df["dias_internacao"], errors="coerce")
    df.loc[df["dias_internacao"] < 0, "dias_internacao"] = 0
    return df


def normalize_censo(df: pd.DataFrame, metadata: dict[str, Any], lote_importacao_id: str) -> pd.DataFrame:
    alias_map = _build_column_alias_map(df)
    normalized = pd.DataFrame()
    # Para censo diário, prontuario/nome podem estar ausentes (leitos livres/bloqueados)
    normalized["prontuario"] = _get_series_by_alias(df, alias_map, ["PRONT", "PRONTUARIO"], required=False).apply(clean_string)
    normalized["nome_paciente"] = _get_series_by_alias(df, alias_map, ["NOME"], required=False).apply(clean_string)
    normalized["idade_anos"] = _get_series_by_alias(df, alias_map, ["IDADE (a)", "IDADE_ANOS"]).apply(clean_int)
    normalized["idade_meses"] = _get_series_by_alias(df, alias_map, ["IDADE (m)", "IDADE_MES"]).apply(clean_int)
    normalized["data_internacao"] = _get_series_by_alias(df, alias_map, ["DATA INTERNACAO", "DATA_INTERNACAO"], required=True).apply(parse_datetime_br)
    normalized["data_alta"] = None
    normalized["especialidade"] = _get_series_by_alias(
        df,
        alias_map,
        ["CLINICA RESPONSAVEL (FORA DE CLINICA)", "ESPECIALIDADE"],
        required=True,
    ).apply(clean_string)
    normalized["unidade"] = _get_series_by_alias(df, alias_map, ["UNIDADE"]).apply(clean_string)
    normalized["enfermaria"] = _get_series_by_alias(df, alias_map, ["ENFERMARIA"]).apply(clean_string)
    normalized["leito"] = _get_series_by_alias(df, alias_map, ["LEITO"]).apply(clean_string)
    normalized["status_leito"] = _get_series_by_alias(df, alias_map, ["STATUS LEITO", "STATUS_LEITO"]).apply(clean_string).apply(normalizar_status_leito)
    normalized["cid_internacao_codigo"] = _get_series_by_alias(df, alias_map, ["CID", "CID_INTERNACAO"]).apply(clean_string)
    normalized["cid_internacao_descricao"] = _get_series_by_alias(df, alias_map, ["CID DESCRICAO", "CID_DESCRICAO"]).apply(clean_string)
    normalized["tipo_alta"] = None
    normalized["dias_internacao"] = _get_series_by_alias(df, alias_map, ["DIAS INTER.", "TEMPO_INTERNACAO"]).apply(clean_int)
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
                row.get("data_snapshot"),
                row.get("unidade"),
                row.get("enfermaria"),
                row.get("leito"),
                row.get("status_leito"),
                row.get("prontuario"),
                row.get("data_internacao"),
                row.get("fonte_dado"),
            ]
        ),
        axis=1,
    )
    for column in ["idade_anos", "idade_meses", "dias_internacao"]:
        normalized[column] = pd.array(normalized[column], dtype="Int64")

    # No censo diário, dias_internacao deve refletir exclusivamente a coluna "DIAS INTER.".
    # Não recalcular por data_internacao/data_snapshot para evitar alterar a fonte oficial do relatório.
    ocupados_sem_dias = (
        (normalized["status_leito"] == "Ocupado")
        & normalized["dias_internacao"].isna()
    ).sum()
    if ocupados_sem_dias:
        LOGGER.warning(
            "Censo diario com %s leitos ocupados sem DIAS INTER.; mantendo dias_internacao nulo sem recalculo.",
            int(ocupados_sem_dias),
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
        Column("prontuario", String(50), nullable=True),
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
        Column("status_leito", String(100)),
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


def _sanitize_record_for_sql(record: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in record.items():
        if value is None:
            sanitized[key] = None
            continue

        # Garante que NaT/NaN/<NA> nao cheguem ao MySQL como strings invalidas.
        if pd.isna(value):
            sanitized[key] = None
            continue

        if isinstance(value, pd.Timestamp):
            sanitized[key] = value.to_pydatetime()
            continue

        sanitized[key] = value
    return sanitized


def persist_dataframe(df: pd.DataFrame, engine) -> int:
    # Higienizacao final para evitar erros de NOT NULL por linhas incompletas do arquivo.
    work = df.copy()
    initial_len = len(work)

    work["prontuario"] = work["prontuario"].apply(clean_string)
    work["especialidade"] = work["especialidade"].apply(clean_string)
    work["fonte_dado"] = work["fonte_dado"].apply(clean_string)
    work["lote_importacao_id"] = work["lote_importacao_id"].apply(clean_string)
    work["nome_arquivo"] = work["nome_arquivo"].apply(clean_string)
    work["hash_registro"] = work["hash_registro"].apply(clean_string)

    work["especialidade"] = work["especialidade"].fillna("NAO INFORMADA")
    # Para censo_diario, prontuario pode ser nulo (leitos livres/bloqueados).
    base_required = (
        work["especialidade"].notna()
        & work["fonte_dado"].notna()
        & work["lote_importacao_id"].notna()
        & work["nome_arquivo"].notna()
        & work["hash_registro"].notna()
    )
    required_mask = base_required & (
        (work["fonte_dado"] != "historico_internacao") | work["prontuario"].notna()
    )
    work = work.loc[required_mask].copy()
    dropped = initial_len - len(work)
    if dropped > 0:
        LOGGER.warning("Descartadas %s linhas invalidas antes da persistencia (campos obrigatorios ausentes).", dropped)

    metadata = MetaData()
    table = get_ocupacao_table_definition(metadata)
    raw_records = work.to_dict(orient="records")
    records = [_sanitize_record_for_sql(record) for record in raw_records]
    if not records:
        LOGGER.warning("Nenhuma linha valida para persistir apos higienizacao.")
        return 0

    total_affected = 0
    batch_size = int(os.getenv("ETL_BATCH_SIZE", "1000"))

    with engine.begin() as connection:
        for start in range(0, len(records), batch_size):
            batch = records[start : start + batch_size]
            statement = mysql_insert(table).values(batch)
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
                status_leito=statement.inserted.status_leito,
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
            affected = result.rowcount or 0
            total_affected += affected
            LOGGER.info(
                "Persistencia em lote: inicio=%s tamanho=%s afetadas=%s",
                start,
                len(batch),
                affected,
            )

    return total_affected


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