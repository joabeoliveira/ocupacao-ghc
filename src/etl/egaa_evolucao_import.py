from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return text


def sql_quote(value: Any) -> str:
    if value is None:
        return "NULL"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def find_column(keys: list[str], candidates: list[str]) -> str | None:
    low = {k.lower(): k for k in keys}
    for cand in candidates:
        for k_low, k in low.items():
            if cand in k_low:
                return k
    return None


def generate_evolucoes_sql(csv_path: Path, out_path: Path) -> tuple[int, int]:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    inserted = 0
    skipped = 0
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        keys = list(reader.fieldnames or [])
        pront_col = find_column(keys, ["pront", "prontuario"])
        evol_col = find_column(keys, ["evolu", "evolucoes", "evoluções"])
        if pront_col is None or evol_col is None:
            raise SystemExit(f"Colunas não encontradas no CSV. Cabeçalho detectado: {keys}")

        lines: list[str] = [
            "-- Upsert de evoluções do EGAA (gerado automaticamente)",
            "-- Execute em ambiente de produção com cuidado",
            "",
        ]

        for row in reader:
            pront = clean_text(row.get(pront_col))
            evol = clean_text(row.get(evol_col))
            if not pront:
                skipped += 1
                continue
            if not evol:
                # ainda assim criamos um registro vazio? optamos por pular
                skipped += 1
                continue

            lines.append("INSERT INTO egaa_evolucao_paciente (prontuario, evolucao, created_at, updated_at) VALUES")
            lines.append(f"  ({sql_quote(pront)}, {sql_quote(evol)}, NOW(), NOW())")
            lines.append("ON DUPLICATE KEY UPDATE evolucao=VALUES(evolucao), updated_at=VALUES(updated_at);")
            lines.append("")
            inserted += 1

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return inserted, skipped


def main(argv: list[str] | None = None) -> None:
    import sys

    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("Uso: python egga_evolucao_import.py <caminho_csv> [arquivo_saida.sql]")
        raise SystemExit(1)

    csv_path = Path(argv[0])
    out_path = Path(argv[1]) if len(argv) >= 2 else Path("sql_output/evolucoes_only.sql")

    if not csv_path.exists():
        print(f"CSV não encontrado: {csv_path}")
        raise SystemExit(1)

    inserted, skipped = generate_evolucoes_sql(csv_path, out_path)
    print(f"Arquivo gerado: {out_path.resolve()}\nRegistros preparados: {inserted}, pulados: {skipped}")


if __name__ == "__main__":
    main()
