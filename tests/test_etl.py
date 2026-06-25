import pandas as pd
from src.etl.ingest import parse_age, transform_df


def test_parse_age():
    assert parse_age('74a') == 74
    assert parse_age(' 03 ') == 3
    assert parse_age(None) is None
    assert parse_age('idade: 45 anos') == 45


def test_transform_df_basic():
    data = {
        'Paciente': ['p1', 'p2'],
        'Data_Internacao': ['2026-06-20', '2026-06-10'],
        'Data_Alta': [None, '2026-06-15'],
        'Idade': ['74a', '03']
    }
    df = pd.DataFrame(data)
    out = transform_df(df, source='teste')
    assert 'idade_anos_int' in out.columns
    assert out.loc[0, 'idade_anos_int'] == 74
    assert out.loc[1, 'idade_anos_int'] == 3
    assert out.loc[0, 'status'] == 'internado'
    assert out.loc[1, 'status'] == 'alta'
