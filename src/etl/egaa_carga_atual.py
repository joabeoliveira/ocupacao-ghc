from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


DATE_FIELDS = ("DATA DE INTERNAÇÃO", "DATA DA ALTA")
ACTION_COLUMNS = (
    ("EVOLUÇÕES EGAA", "Evolução EGAA", "concluida"),
    ("PENDÊNCIAS PARA A ALTA", "Pendência para alta", "aberta"),
    ("INTERVENÇÕES EGAA", "Intervenção EGAA", "concluida"),
)


@dataclass(slots=True)
class CargaAtualResultado:
    ocupacao_rows: list[dict[str, Any]]
    egaa_rows: list[dict[str, Any]]


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return text


def parse_int(value: Any) -> int | None:
    text = clean_text(value)
    if not text:
        return None
    match = re.search(r"\d+", text)
    return int(match.group(0)) if match else None


def parse_date_br(value: Any) -> date | None:
    text = clean_text(value)
    if not text:
        return None
    for fmt in ("%d/%m/%Y", "%d/%m/%Y %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    try:
        return pd_to_date(text)
    except Exception:
        return None


def pd_to_date(value: str) -> date | None:
    try:
        import pandas as pd

        parsed = pd.to_datetime(value, dayfirst=True, errors="coerce")
        if pd.isna(parsed):
            return None
        return parsed.date()
    except Exception:
        return None


def split_action_text(value: Any) -> list[str]:
    text = clean_text(value)
    if not text:
        return []

    text = re.sub(r"[•·]", "\n", text)
    parts = re.split(r"\n+|;\s*", text)
    items: list[str] = []
    for part in parts:
        piece = re.sub(r"^\s*(?:\d+[\.\)]\s*|[-*]\s*)", "", part).strip()
        if piece:
            items.append(piece)
    return items or [text]


def _snapshot_suffix(snapshot_date: date) -> str:
    return snapshot_date.strftime("%d/%m/%Y")


def build_carga_atual(rows: list[dict[str, str]], snapshot_date: date) -> CargaAtualResultado:
    ocupacao_rows: list[dict[str, Any]] = []
    egaa_rows: list[dict[str, Any]] = []

    snapshot_label = _snapshot_suffix(snapshot_date)
    for index, row in enumerate(rows, start=2):
        prontuario = clean_text(row.get("PRONT"))
        nome = clean_text(row.get("NOME"))
        if not prontuario or not nome:
            continue

        data_internacao = parse_date_br(row.get("DATA DE INTERNAÇÃO"))
        data_alta = parse_date_br(row.get("DATA DA ALTA"))
        if data_internacao is None:
            continue

        if data_alta is not None and data_alta <= snapshot_date:
            continue

        dias_internacao = (snapshot_date - data_internacao).days
        if data_alta is not None:
            dias_internacao = max((data_alta - data_internacao).days, 0)

        ocupacao_rows.append(
            {
                "STATUS LEITO": "OCUPADO",
                "PRONT": prontuario,
                "NOME": nome,
                "IDADE (a)": parse_int(row.get("IDADE")),
                "IDADE (m)": None,
                "DATA INTERNACAO": data_internacao.strftime("%d/%m/%Y"),
                "CLINICA RESPONSAVEL (FORA DE CLINICA)": clean_text(row.get("ESPECIALIDADE ASSISTENTE")),
                "UNIDADE": clean_text(row.get("UNIDADE")) or None,
                "ENFERMARIA": clean_text(row.get("ESPECIALIDADE DA ENFERMARIA")) or None,
                "LEITO": clean_text(row.get("LEITO")) or None,
                "CID": clean_text(row.get("CID")) or None,
                "CID DESCRICAO": clean_text(row.get("DIAGNÓSTICO")) or None,
                "DIAS INTER.": dias_internacao,
            }
        )

        for source_column, tipo_nome, status in ACTION_COLUMNS:
            for action_text in split_action_text(row.get(source_column)):
                egaa_rows.append(
                    {
                        "prontuario": prontuario,
                        "tipo_intervencao_nome": tipo_nome,
                        "titulo": tipo_nome,
                        "descricao": action_text,
                        "status": status,
                        "usuario_responsavel": None,
                        "data_atuacao": snapshot_date.isoformat(),
                        "data_prevista": None,
                        "data_conclusao": None,
                        "observacao": f"Importado da planilha de controle em {snapshot_label} (linha {index}).",
                        "origem_coluna": source_column,
                    }
                )

    return CargaAtualResultado(ocupacao_rows=ocupacao_rows, egaa_rows=egaa_rows)


def load_source_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def sql_quote(value: Any) -> str:
    if value is None:
        return "NULL"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def write_egaa_sql(path: Path, egga_rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "-- Carga assistida gerada a partir da planilha do EGAA.",
        "-- Execute uma vez no phpMyAdmin ou no cliente SQL da produção.",
        "",
    ]
    for row in egga_rows:
        lines.extend(
            [
                "INSERT INTO egaa_intervencao_paciente (",
                "  ocupacao_leito_id, prontuario, tipo_intervencao_id, titulo, descricao, status, usuario_responsavel, data_atuacao, data_prevista, data_conclusao, observacao",
                ")",
                "SELECT",
                f"  NULL, {sql_quote(row['prontuario'])}, t.id, {sql_quote(row['titulo'])}, {sql_quote(row['descricao'])}, {sql_quote(row['status'])},",
                f"  {sql_quote(row['usuario_responsavel'])}, {sql_quote(row['data_atuacao'])}, {sql_quote(row['data_prevista'])}, {sql_quote(row['data_conclusao'])}, {sql_quote(row['observacao'])}",
                "FROM egaa_tipo_intervencao t",
                f"WHERE t.nome = {sql_quote(row['tipo_intervencao_nome'])};",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


PENDENCIA_ROTULOS: dict[str, str] = {
    "regulacao": "Regulação",
    "ajuste_inr": "Ajuste INR",
    "ajuste_medicamento": "Ajuste de medicação",
    "tratamento_lesoes": "Tratamento de lesões",
    "antibioticoterapia": "Antibioticoterapia",
    "definicao_diagnostica": "Definição diagnóstica",
    "ajuste_laboratorial": "Ajuste laboratorial",
    "exame_pendente": "Exame pendente",
    "aguarda_parecer_especialista": "Aguarda parecer especialista",
    "definicao_terapeutica": "Definição terapêutica",
    "reavaliacao_medica": "Reavaliação médica",
    "descompensacao_clinica": "Descompensação clínica",
    "procedimento_cirurgico": "Procedimento cirúrgico",
    "aguarda_gtt_por_eda": "Aguarda GTT por EDA",
    "aguarda_cirurgia_cardiaca": "Aguarda cirurgia cardíaca",
    "manejo_clinico": "Manejo clínico",
    "manejo_sintomatico": "Manejo sintomático",
    "cuidados_paliativos": "Cuidados paliativos",
    "cuidados_pos_operatorios": "Cuidados pós-operatórios",
    "cuidados_fim_vida": "Cuidados de fim de vida",
    "fragilidade_familiar": "Fragilidade familiar",
    "vulnerabilidade_social": "Vulnerabilidade social",
    "vulnerabilidade_socioeconomica": "Vulnerabilidade socioeconômica",
    "vulnerabilidade_emocional": "Vulnerabilidade emocional",
    "documento_identidade": "Documento de identidade",
    "familia_nao_cooperativa": "Família não cooperativa",
    "aguarda_padi_pmec": "Aguarda PADI/PMEC",
    "aguarda_home_care": "Aguarda home care",
    "aguarda_vaga_abrigo": "Aguarda vaga em abrigo",
    "aguardando_documentacao": "Aguardando documentação",
    "transporte_sanitario_eletivo": "Transporte sanitário eletivo",
    "familiar_acompanhante_alta": "Familiar acompanhante para alta",
    "aguarda_leito_cuidados_prolongados": "Aguarda leito cuidados prolongados",
    "aguarda_regulacao_transferencia": "Aguarda regulação transferência",
    "aguarda_regulacao_marcapasso": "Aguarda regulação marcapasso",
}


def _slugify(text: str) -> str:
    value = re.sub(r"[^\w\s-]", "", text, flags=re.U).strip().lower()
    return re.sub(r"[\s_-]+", "_", value)


def write_pendencias_sql(path: Path, egaa_rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "-- Inserção de pendências para alta gerada a partir da planilha do EGAA.",
        "-- Não resolve pendências existentes; evita duplicatas por prontuario+codigo.",
        "",
    ]

    pendencias = [r for r in egaa_rows if r.get("tipo_intervencao_nome") == "Pendência para alta"]
    for row in pendencias:
        pront = sql_quote(row.get("prontuario"))
        label = clean_text(row.get("descricao") or row.get("titulo") or "")
        codigo = None
        # tenta mapear por rótulo exato
        for k, v in PENDENCIA_ROTULOS.items():
            if label.lower() == v.lower():
                codigo = k
                break
        # tenta conter o rótulo
        if codigo is None:
            for k, v in PENDENCIA_ROTULOS.items():
                if v.lower() in label.lower():
                    codigo = k
                    break
        if codigo is None:
            codigo = _slugify(label) or "pendencia_desconhecida"

        lines.append(
            "INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)"
        )
        lines.append(
            f"SELECT {pront}, '{codigo}', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario={pront} AND codigo='{codigo}');"
        )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_evolucoes_sql(path: Path, egaa_rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = [
        "-- Upsert de evoluções do EGAA gerado a partir da planilha.",
        "-- Atualiza campo 'evolucao' para prontuários existentes ou insere novo registro.",
        "",
    ]

    evolucoes = [r for r in egaa_rows if r.get("tipo_intervencao_nome") == "Evolução EGAA"]
    for row in evolucoes:
        pront = sql_quote(row.get("prontuario"))
        evol_text = sql_quote(row.get("descricao") or row.get("titulo") or "")
        lines.append(
            "INSERT INTO egaa_evolucao_paciente (prontuario, evolucao, created_at, updated_at) VALUES"
        )
        lines.append(f"  ({pront}, {evol_text}, NOW(), NOW())")
        lines.append("ON DUPLICATE KEY UPDATE evolucao=VALUES(evolucao), updated_at=VALUES(updated_at);")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_all_sql(output_dir: Path, egaa_rows: list[dict[str, Any]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_egaa_sql(output_dir / "intervencoes_egaa.sql", [r for r in egaa_rows if r.get("tipo_intervencao_nome") == "Intervenção EGAA"])
    write_evolucoes_sql(output_dir / "evolucoes_egaa.sql", egaa_rows)
    write_pendencias_sql(output_dir / "pendencias_egaa.sql", egaa_rows)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python egga_carga_atual.py <caminho_csv> [snapshot_date:YYYY-MM-DD] [output_dir]")
        raise SystemExit(1)

    csv_path = Path(sys.argv[1])
    snap = None
    if len(sys.argv) >= 3:
        try:
            snap = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        except Exception:
            print("Formato de data inválido. Use YYYY-MM-DD.")
            raise
    else:
        snap = date.today()

    out = Path(sys.argv[3]) if len(sys.argv) >= 4 else Path("./sql_output")

    source_rows = load_source_rows(csv_path)
    resultado = build_carga_atual(source_rows, snap)
    write_all_sql(out, resultado.egaa_rows)
    print(f"Arquivos SQL gerados em: {out.resolve()}")

