"""Gera SQL de pendências para alta com split correto por vírgula."""
from __future__ import annotations

import re
from pathlib import Path


# ── Mapping completo de pendências (label -> code) ──
PENDENCIA_MAP: dict[str, list[str]] = {
    "regulacao": ["REGULAÇÃO", "REGULACAO"],
    "manejo_clinico": ["MANEJO CLINICO", "MANEJO CLÍNICO"],
    "transporte_sanitario_eletivo": ["TRANSPORTE SANITÁRIO ELETIVO"],
    "realizando_tratamento_terapeutico": ["REALIZANDO TRATAMENTO TERAPÊUTICO"],
    "descompensacao_clinica": ["DESCOMPENSAÇÃO CLINICA", "DESCOMPENSAÇÃO CLÍNICA"],
    "definicao_diagnostica": ["DEFINICAO DIAGNOSTICA", "DEFINIÇÃO DIAGNÓSTICA"],
    "cuidados_pos_operatorios": ["CUIDADOS PÓS-OPERATÓRIOS", "CUIDADOS POS-OPERATORIOS"],
    "antibioticoterapia": ["ANTIBIOTICOTERAPIA"],
    "manejo_sintomatico": ["MANEJO SINTOMÁTICO", "MANEJO SINTOMATICO"],
    "procedimento_cirurgico": ["PROCEDIMENTO CIRÚRGICO", "PROCEDIMENTO CIRURGICO"],
    "exame_pendente": ["EXAME PENDENTE"],
    "definicao_terapeutica": [
        "DEFINIÇÃO DA TERAPEUTICA",
        "DEFINICAO DA TERAPEUTICA",
        "DEFINIÇÃO TERAPÊUTICA",
    ],
    "ajuste_medicamento": ["AJUSTE MEDICAMENTO", "AJUSTE DE MEDICAÇÃO"],
    "resultado_exame_pendente": ["RESULTADO DE EXAME PENDENTE"],
    "regulacao_clinica_satelite_hd": ["REGULAÇÃO CLÍNICA SATÉLITE DE HD", "REGULACAO CLINICA SATELITE DE HD"],
    "tratamento_lesoes": ["TRATAMENTO DE LESÕES", "TRATAMENTO LESOES"],
    "reavaliacao_medica": ["REAVALIAÇÃO MEDICA", "REAVALIAÇÃO MÉDICA"],
    "fragilidade_familiar": ["FRAGILIDADE FAMILIAR"],
    "aguardando_documentacao": ["AGUARDANDO DOCUMENTAÇÃO VIA CARTÓRIO", "AGUARDANDO DOCUMENTACAO"],
    "cuidados_paliativos": ["CUIDADOS PALIATIVOS"],
    "tratamento_oncologico_regulacao": ["TRATAMENTO ONCOLÓGICO - REGULAÇÃO"],
    "aguarda_padi_pmec": ["AGUARDA PADI / PMEC", "AGUARDA PADI/PMEC"],
    "orientacao_educativa": ["ORIENTAÇÃO EDUCATIVA", "ORIENTACAO EDUCATIVA"],
    "aguarda_parecer_especialista": ["AGUARDA PARECER DE ESPECIALISTA", "AGUARDA PARECER ESPECIALISTA"],
    "biopsia": ["BIÓPSIA", "BIOPSIA"],
}


def find_code(label: str) -> str:
    label_clean = re.sub(r"[^\w\s]", " ", label).strip().upper()
    label_clean = re.sub(r"\s+", " ", label_clean)
    for code, aliases in PENDENCIA_MAP.items():
        for alias in aliases:
            alias_clean = re.sub(r"[^\w\s]", " ", alias).strip().upper()
            alias_clean = re.sub(r"\s+", " ", alias_clean)
            if label_clean == alias_clean:
                return code
    # fallback: slugify
    slug = re.sub(r"[\s_]+", "_", re.sub(r"[^\w\s]", "", label).strip().lower())
    return slug or "pendencia_desconhecida"


def split_pendencias(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


# ── Dados fornecidos pelo usuário ──
PENDENCIAS_DATA: list[tuple[str, str]] = [
    ("8399062", "REGULAÇÃO, MANEJO CLINICO, TRANSPORTE SANITÁRIO ELETIVO"),
    ("163119", "REALIZANDO TRATAMENTO TERAPÊUTICO, DESCOMPENSAÇÃO CLINICA"),
    ("2231704", "DEFINICAO DIAGNOSTICA, MANEJO CLINICO"),
    ("8429434", "CUIDADOS PÓS-OPERATÓRIOS, ANTIBIOTICOTERAPIA, DESCOMPENSAÇÃO CLINICA"),
    ("8417830", "ANTIBIOTICOTERAPIA, CUIDADOS PÓS-OPERATÓRIOS, DESCOMPENSAÇÃO CLINICA"),
    ("8380681", "ANTIBIOTICOTERAPIA, DESCOMPENSAÇÃO CLINICA"),
    ("8422810", "MANEJO CLINICO"),
    ("8421512", "REALIZANDO TRATAMENTO TERAPÊUTICO, DESCOMPENSAÇÃO CLINICA"),
    ("2054019", "ANTIBIOTICOTERAPIA, REALIZANDO TRATAMENTO TERAPÊUTICO"),
    ("8243725", "Biópsia, REALIZANDO TRATAMENTO TERAPÊUTICO"),
    ("8336103", "ANTIBIOTICOTERAPIA, REALIZANDO TRATAMENTO TERAPÊUTICO, MANEJO SINTOMÁTICO"),
    ("8390556", "PROCEDIMENTO CIRÚRGICO"),
    ("8382864", "EXAME PENDENTE, DEFINIÇÃO DA TERAPEUTICA"),
    ("8413091", "AJUSTE MEDICAMENTO, DEFINICAO DIAGNOSTICA, DEFINIÇÃO DA TERAPEUTICA, RESULTADO DE EXAME PENDENTE"),
    ("8401430", "MANEJO CLINICO, DEFINIÇÃO DA TERAPEUTICA"),
    ("8422196", "EXAME PENDENTE"),
    ("1387163", "REALIZANDO TRATAMENTO TERAPÊUTICO, ANTIBIOTICOTERAPIA, REGULAÇÃO"),
    ("8301440", "DEFINICAO DIAGNOSTICA, MANEJO SINTOMÁTICO, EXAME PENDENTE"),
    ("8423357", "REALIZANDO TRATAMENTO TERAPÊUTICO, ANTIBIOTICOTERAPIA"),
    ("1250960", "REALIZANDO TRATAMENTO TERAPÊUTICO, FRAGILIDADE FAMILIAR, AGUARDANDO DOCUMENTAÇÃO VIA CARTÓRIO"),
    ("8421778", "MANEJO SINTOMÁTICO, DEFINIÇÃO DA TERAPEUTICA"),
    ("8422486", "REALIZANDO TRATAMENTO TERAPÊUTICO, EXAME PENDENTE"),
    ("8110761", "PROCEDIMENTO CIRÚRGICO, CUIDADOS PALIATIVOS, TRATAMENTO ONCOLÓGICO - REGULAÇÃO"),
    ("8416248", "ANTIBIOTICOTERAPIA, REGULAÇÃO CLÍNICA SATÉLITE DE HD, RESULTADO DE EXAME PENDENTE, PROCEDIMENTO CIRÚRGICO"),
    ("1373852", "TRATAMENTO DE LESÕES, EXAME PENDENTE, REAVALIAÇÃO MEDICA"),
    ("8083480", "ANTIBIOTICOTERAPIA, DESCOMPENSAÇÃO CLINICA, PROCEDIMENTO CIRÚRGICO"),
    ("8429429", "TRATAMENTO DE LESÕES, AGUARDA PARECER DE ESPECIALISTA, MANEJO CLINICO, FRAGILIDADE FAMILIAR, ORIENTAÇÃO EDUCATIVA"),
    ("8377747", "AGUARDA PADI / PMEC"),
    ("8410268", "ANTIBIOTICOTERAPIA, REGULAÇÃO CLÍNICA SATÉLITE DE HD, TRANSPORTE SANITÁRIO ELETIVO"),
    ("8388949", "AGUARDA PADI / PMEC"),
]


def main() -> None:
    out_dir = Path("sql_output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "pendencias.sql"

    lines: list[str] = [
        "-- Pendências para alta geradas a partir da planilha de controle do EGAA.",
        "-- Cada pendência é um registro separado (split por vírgula).",
        "-- Não duplica registros existentes (usa WHERE NOT EXISTS).",
        "",
    ]

    total = 0
    for pront, pend_text in PENDENCIAS_DATA:
        items = split_pendencias(pend_text)
        for item in items:
            codigo = find_code(item)
            total += 1
            lines.append(
                "INSERT INTO egaa_pendencia_alta (prontuario, codigo, resolvida, created_at, updated_at)"
            )
            lines.append(
                f"SELECT '{pront}', '{codigo}', 0, NOW(), NOW() FROM DUAL WHERE NOT EXISTS"
            )
            lines.append(
                f"  (SELECT 1 FROM egaa_pendencia_alta WHERE prontuario='{pront}' AND codigo='{codigo}');"
            )
            lines.append("")

    # validacao: mostra os pares pront-codigo
    print("=== VALIDAÇÃO: pares (prontuario, codigo) gerados ===")
    for pront, pend_text in PENDENCIAS_DATA:
        items = split_pendencias(pend_text)
        for item in items:
            codigo = find_code(item)
            print(f"  {pront} -> {codigo:<40} | {item}")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nArquivo gerado: {out_path}")
    print(f"Total de pendências individuais: {total}")
    print(f"Prontuários com pendência: {len(PENDENCIAS_DATA)}")


if __name__ == "__main__":
    main()
