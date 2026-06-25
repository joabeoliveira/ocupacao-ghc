"""ETL base para ingestão de arquivos do esusreport.

Funções principais:
- parse_age: extrai dígitos de campo de idade
- load_file_to_df: lê CSV/XLSX e normaliza colunas mínimas
- transform_df: aplica regras de negócio (internado, idade inteira, tempo de internação)
- persist_df: opcionalmente persiste no banco via SQLAlchemy
"""
from __future__ import annotations
import re
from datetime import datetime
from typing import Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def parse_age(age_raw: Optional[str]) -> Optional[int]:
    if age_raw is None:
        return None
    s = str(age_raw)
    m = re.search(r"(\d+)", s)
    if not m:
        return None
    return int(m.group(1))


def load_file_to_df(path: str) -> pd.DataFrame:
    if path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    return df


def transform_df(df: pd.DataFrame, source: Optional[str] = None) -> pd.DataFrame:
    df = df.copy()

    # Normalizar nomes de colunas esperadas (tentar várias variações)
    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if 'idade' in lc:
            col_map[c] = 'idade_raw'
        if 'data_intern' in lc or 'dt_intern' in lc or 'data_interna' in lc or 'data_internacao' in lc:
            col_map[c] = 'data_internacao'
        if 'data_alta' in lc or 'dt_alta' in lc:
            col_map[c] = 'data_alta'
        if 'especialid' in lc:
            col_map[c] = 'especialidade'
        if 'unidade' in lc or 'enferm' in lc:
            col_map[c] = 'unidade'
        if 'paciente' in lc or 'prontuario' in lc or 'nome' in lc:
            col_map[c] = 'paciente_id'

    df = df.rename(columns=col_map)

    # Idade
    if 'idade_raw' in df.columns:
        df['idade_anos_int'] = df['idade_raw'].apply(parse_age)
    else:
        df['idade_anos_int'] = None

    # Datas
    for col in ('data_internacao', 'data_alta'):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        else:
            df[col] = pd.NaT

    # Status: internado se data_alta é NaT
    df['status'] = df['data_alta'].apply(lambda x: 'internado' if pd.isna(x) else 'alta')

    # length_of_stay em dias
    today = pd.to_datetime(datetime.utcnow())
    def calc_los(row):
        if pd.isna(row['data_internacao']):
            return None
        end = row['data_alta'] if not pd.isna(row['data_alta']) else today
        try:
            return int((end - row['data_internacao']).days)
        except Exception:
            return None

    df['length_of_stay'] = df.apply(calc_los, axis=1)

    # origem_arquivo
    df['origem_arquivo'] = source

    # limpar colunas pesadas antes de persistir (opcional)
    return df


def persist_df(df: pd.DataFrame, table_name: str, engine=None, if_exists: str = 'append') -> None:
    """Persiste o dataframe usando SQLAlchemy engine se fornecido."""
    if engine is None:
        logger.info('Nenhum engine fornecido; skipping persistência.')
        return
    # Selecionar colunas que queremos persistir
    cols = ['paciente_id', 'data_internacao', 'data_alta', 'idade_anos_int', 'especialidade', 'unidade', 'status', 'origem_arquivo', 'length_of_stay']
    to_write = df[[c for c in cols if c in df.columns]]
    to_write.to_sql(table_name, con=engine, if_exists=if_exists, index=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='ETL ingestion base')
    parser.add_argument('path')
    parser.add_argument('--source', default=None)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    df = load_file_to_df(args.path)
    df2 = transform_df(df, source=args.source or args.path)
    print(df2.head().to_dict(orient='records'))
