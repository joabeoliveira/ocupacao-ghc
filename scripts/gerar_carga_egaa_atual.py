from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from src.etl.egaa_carga_atual import build_carga_atual, load_source_rows, write_csv, write_egaa_sql


def parse_snapshot_date(value: str | None) -> date:
    if not value:
        return date.today()
    return date.fromisoformat(value)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera arquivos de carga assistida a partir da planilha atual do EGAA."
    )
    parser.add_argument(
        "--source",
        default=None,
        help="Arquivo CSV de origem. Se omitido, usa a planilha atual salva na raiz do projeto.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Diretório de saida. Se omitido, cria uma pasta temporaria em ./tmp.",
    )
    parser.add_argument(
        "--snapshot-date",
        default=None,
        help="Data de referencia da planilha no formato AAAA-MM-DD.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    source_path = Path(args.source) if args.source else repo_root / "carga para o bd egaa - EGAA_27-06-2026.csv"
    output_dir = Path(args.output_dir) if args.output_dir else repo_root / "tmp" / "carga-egaa-atual"
    snapshot_date = parse_snapshot_date(args.snapshot_date)

    rows = load_source_rows(source_path)
    resultado = build_carga_atual(rows, snapshot_date=snapshot_date)

    ocupacao_csv = output_dir / f"carga_ocupacao_{snapshot_date.isoformat()}.csv"
    egaa_csv = output_dir / f"carga_egaa_intervencoes_{snapshot_date.isoformat()}.csv"
    egaa_sql = output_dir / f"carga_egaa_intervencoes_{snapshot_date.isoformat()}.sql"

    write_csv(
        ocupacao_csv,
        resultado.ocupacao_rows,
        [
            "STATUS LEITO",
            "PRONT",
            "NOME",
            "IDADE (a)",
            "IDADE (m)",
            "DATA INTERNACAO",
            "CLINICA RESPONSAVEL (FORA DE CLINICA)",
            "UNIDADE",
            "ENFERMARIA",
            "LEITO",
            "CID",
            "CID DESCRICAO",
            "DIAS INTER.",
        ],
    )
    write_csv(
        egaa_csv,
        resultado.egaa_rows,
        [
            "prontuario",
            "tipo_intervencao_nome",
            "titulo",
            "descricao",
            "status",
            "usuario_responsavel",
            "data_atuacao",
            "data_prevista",
            "data_conclusao",
            "observacao",
            "origem_coluna",
        ],
    )
    write_egaa_sql(egaa_sql, resultado.egaa_rows)

    print(f"Planilha de origem: {source_path}")
    print(f"Linhas de ocupacao geradas: {len(resultado.ocupacao_rows)}")
    print(f"Linhas de EGAA geradas: {len(resultado.egaa_rows)}")
    print(f"CSV de ocupacao: {ocupacao_csv}")
    print(f"CSV de EGAA: {egaa_csv}")
    print(f"SQL de EGAA: {egaa_sql}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
