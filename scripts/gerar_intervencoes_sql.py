"""Gera SQL de intervenções EGAA a partir do CSV com dados padronizados."""
from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path


CSV_PATH = Path("sql_output/dados para bd egaa - Página6.csv")
OUT_DIR = Path("sql_output")
TIPO_SEED_PATH = OUT_DIR / "seed_tipos_intervencao.sql"
INTERV_SQL_PATH = OUT_DIR / "intervencoes.sql"


def clean_text(val: str | None) -> str:
    if val is None:
        return ""
    return val.strip()


def parse_date_br(val: str | None) -> str | None:
    """Converte DD/MM/YYYY para YYYY-MM-DD ou retorna None."""
    text = clean_text(val)
    if not text:
        return None
    for fmt in ("%d/%m/%Y", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def normalizar_status(val: str | None) -> str | None:
    text = clean_text(val).lower()
    if not text:
        return None
    if text in ("concluída", "concluida"):
        return "concluida"
    if text in ("em andamento", "em_andamento"):
        return "em_andamento"
    if text in ("aberta", "aberto"):
        return "aberta"
    if text in ("cancelada", "cancelado"):
        return "cancelada"
    return text


def sql_val(val: str | None) -> str:
    """Retorna valor formatado para SQL (NULL ou string escapada)."""
    if val is None:
        return "NULL"
    escaped = val.replace("'", "''")
    return f"'{escaped}'"


def extrair_tipos_unicos(rows: list[dict[str, str]]) -> list[str]:
    seen: set[str] = set()
    tipos: list[str] = []
    for row in rows:
        t = clean_text(row.get("TIPO DE INTERVENÇÃO", ""))
        if t and t not in seen:
            seen.add(t)
            tipos.append(t)
    return tipos


def gerar_seed_tipos(tipos: list[str], out_path: Path) -> None:
    lines: list[str] = [
        "-- Seed de tipos de intervenção extraídos do CSV de intervenções.",
        "-- Insere apenas se não existirem (IGNORE).",
        "",
    ]
    for tipo in tipos:
        nome_escaped = tipo.replace("'", "''")
        lines.append(
            "INSERT IGNORE INTO egaa_tipo_intervencao (nome, descricao, ativo, ordem_exibicao, created_at, updated_at)"
        )
        lines.append(f"  VALUES ('{nome_escaped}', '', 1, 50, NOW(), NOW());")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Seed de tipos: {out_path} ({len(tipos)} tipos)")


def gerar_sql_intervencoes(rows: list[dict[str, str]], out_path: Path) -> None:
    lines: list[str] = [
        "-- Intervenções EGAA geradas a partir do CSV padronizado.",
        "-- Resolve tipo_intervencao_id via JOIN com egaa_tipo_intervencao.",
        "",
    ]

    total = 0
    for row in rows:
        pront = clean_text(row.get("PRONT", ""))
        tipo_nome = clean_text(row.get("TIPO DE INTERVENÇÃO", ""))
        descricao = clean_text(row.get("DESCRIÇÃO", ""))
        status = normalizar_status(row.get("STATUS", ""))
        responsavel = clean_text(row.get("RESPONSÁVEL", ""))
        data_atuacao = parse_date_br(row.get("DATA DA ATUAÇÃO", ""))
        data_prevista = parse_date_br(row.get("DATA PREVISTA", ""))
        data_conclusao = parse_date_br(row.get("DATA DE CONCLUSÃO", ""))
        observacao = clean_text(row.get("OBSERVAÇÃO", ""))

        if not pront or not tipo_nome:
            continue

        titulo = tipo_nome  # usa o nome do tipo como título

        total += 1
        lines.append(
            "INSERT INTO egaa_intervencao_paciente ("
        )
        lines.append(
            "  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao,"
        )
        lines.append(
            "  status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao"
        )
        lines.append(")")
        lines.append("SELECT")
        lines.append(
            f"  NULL, {sql_val(pront)}, t.id, {sql_val(titulo)},"
        )
        lines.append(
            f"  {sql_val(descricao)}, {sql_val(status)},"
        )
        lines.append(
            f"  {sql_val(responsavel)}, {sql_val(data_atuacao)},"
        )
        lines.append(
            f"  {sql_val(data_prevista)}, {sql_val(data_conclusao)}, {sql_val(observacao)}"
        )
        lines.append(
            "FROM egaa_tipo_intervencao t"
        )
        lines.append(f"WHERE t.nome = {sql_val(tipo_nome)};")
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"SQL de intervenções: {out_path} ({total} registros)")


def main() -> None:
    if not CSV_PATH.exists():
        print(f"CSV não encontrado: {CSV_PATH}")
        return

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"CSV lido: {len(rows)} linhas")

    # Extrai tipos únicos e ordena
    tipos = extrair_tipos_unicos(rows)
    print(f"Tipos de intervenção únicos: {len(tipos)}")
    for t in tipos:
        print(f"  - {t}")

    # Gera seed SQL para criar os tipos no banco
    gerar_seed_tipos(tipos, TIPO_SEED_PATH)

    # Gera SQL de INSERT para as intervenções
    gerar_sql_intervencoes(rows, INTERV_SQL_PATH)

    print("\nPronto! Execute nesta ordem:")
    print(f"  1. {TIPO_SEED_PATH.name}")
    print(f"  2. {INTERV_SQL_PATH.name}")


if __name__ == "__main__":
    main()
