from pathlib import Path

import pandas as pd

from src.etl.etl_process import build_hash_registro, clean_int, normalize_censo, normalize_historico, parse_dias_internacao


def test_clean_int_extracts_digits():
    assert clean_int("74a") == 74
    assert clean_int("02m") == 2
    assert clean_int(None) is None


def test_parse_dias_internacao_accepts_historico_text():
    assert parse_dias_internacao("29d 22h") == 29
    assert parse_dias_internacao("5") == 5


def test_build_hash_registro_is_stable():
    left = build_hash_registro(["8429393", "2026-06-20", "117.01"])
    right = build_hash_registro(["8429393", "2026-06-20", "117.01"])
    assert left == right


def test_normalize_historico_maps_core_columns():
    df = pd.DataFrame(
        {
            "PRONTUARIO": ["7485204"],
            "NOME": ["JOSE CARLOS RIBEIRO"],
            "IDADE_ANOS": ["74a"],
            "IDADE_MES": ["02m"],
            "DATA_INTERNACAO": ["01/05/2026"],
            "DATA_ALTA": ["31/05/2026"],
            "ESPECIALIDADE": ["MEDICINA INTENSIVA"],
            "UNIDADE": ["PREDIO 1"],
            "ENFERMARIA": ["GHC P1 1A"],
            "LEITO": ["117.01"],
            "CID_INTERNACAO": ["K83"],
            "CID_DESCRICAO": ["DOENCAS DAS VIAS BILIARES"],
            "TIPO_DE_ALTA": ["ALTA"],
            "TEMPO_INTERNACAO": ["29d 22h"],
        }
    )
    metadata = {
        "nome_arquivo": "historico.xls",
        "periodo_referencia_inicio": pd.Timestamp("2026-05-01").date(),
        "periodo_referencia_fim": pd.Timestamp("2026-06-30").date(),
        "data_impressao_arquivo": pd.Timestamp("2026-06-25 07:45"),
    }
    out = normalize_historico(df, metadata, "lote-1")
    assert out.loc[0, "prontuario"] == "7485204"
    assert out.loc[0, "idade_anos"] == 74
    assert out.loc[0, "dias_internacao"] == 29
    assert out.loc[0, "fonte_dado"] == "historico_internacao"


def test_normalize_censo_maps_core_columns():
    df = pd.DataFrame(
        {
            "PRONT": ["8429393"],
            "NOME": ["CLEA COSTA MATIAS"],
            "IDADE (a)": [65],
            "IDADE (m)": [9],
            "DATA INTERNACAO": ["20/06/2026"],
            "CLINICA RESPONSAVEL (FORA DE CLINICA)": ["MEDICINA INTENSIVA"],
            "UNIDADE": ["PREDIO 1"],
            "ENFERMARIA": ["GHC P1 1A"],
            "LEITO": ["117.01"],
            "CID": ["R229"],
            "CID DESCRICAO": ["TUMEFACAO"],
            "DIAS INTER.": [5],
        }
    )
    metadata = {
        "nome_arquivo": "censo.xls",
        "data_impressao_arquivo": pd.Timestamp("2026-06-25 07:57"),
    }
    out = normalize_censo(df, metadata, "lote-2")
    assert out.loc[0, "prontuario"] == "8429393"
    assert out.loc[0, "idade_anos"] == 65
    assert out.loc[0, "data_snapshot"] == pd.Timestamp("2026-06-25").date()
    assert out.loc[0, "fonte_dado"] == "censo_diario"
