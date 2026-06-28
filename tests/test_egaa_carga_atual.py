from datetime import date

from src.etl.egaa_carga_atual import build_carga_atual, split_action_text


def test_split_action_text_breaks_lines_and_semicolons():
    assert split_action_text("Pedido de exame;\nContato com o social") == [
        "Pedido de exame",
        "Contato com o social",
    ]


def test_build_carga_atual_separa_ocupacao_e_egaa():
    rows = [
        {
            "LEITO": "111.01",
            "NOME": "FERNANDO PEREIRA DE SOUZA",
            "PRONT": "8428328",
            "IDADE": "73",
            "SEXO": "M",
            "ESPECIALIDADE DA ENFERMARIA": "Emerg. Adulto - SALA VERMELHA",
            "CID": "G419",
            "DIAGNÓSTICO": "Estado de mal epiléptico, não especificado",
            "ESPECIALIDADE ASSISTENTE": "Clinica Médica",
            "PROCEDIMENTO": "0301060088 DIAGNOSTICO E/OU ATENDIMENTO DE URGENCIA EM CLINICA MEDICA",
            "PARÂMETRO TMI PARA O PROCEDIMENTO": "1",
            "DATA DE INTERNAÇÃO": "13/06/2026",
            "DATA PREVISTA PARA ALTA O MOMENTO DA INTERNAÇÃO": "",
            "TEMPO ATUAL DE PERMANÊNCIA (EM 27/06/2026)": "14",
            "EVOLUÇÕES EGAA": "Pedido de exames",
            "DATA DA ALTA": "",
            "DESTINO": "",
            "PENDÊNCIAS PARA A ALTA": "Contato com serviço social",
            "INTERVENÇÕES EGAA": "Acompanhamento multiprofissional",
        }
    ]

    resultado = build_carga_atual(rows, snapshot_date=date(2026, 6, 27))

    assert len(resultado.ocupacao_rows) == 1
    assert resultado.ocupacao_rows[0]["PRONT"] == "8428328"
    assert resultado.ocupacao_rows[0]["ENFERMARIA"] == "Emerg. Adulto - SALA VERMELHA"
    assert len(resultado.egaa_rows) == 3
    assert {row["tipo_intervencao_nome"] for row in resultado.egaa_rows} == {
        "Evolução EGAA",
        "Pendência para alta",
        "Intervenção EGAA",
    }
    assert all(row["data_atuacao"] == "2026-06-27" for row in resultado.egaa_rows)
