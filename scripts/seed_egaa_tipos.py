"""Script simples para semear tipos de intervenção do EGAA.

Rode usando o venv com variáveis de ambiente configuradas (mesmas do app).
Exemplo:
    python scripts/seed_egaa_tipos.py

O script insere tipos se ainda não existirem, ignorando duplicatas.
"""
from __future__ import annotations

from datetime import datetime
from typing import List

from app.database import SessionLocal
from app.models import EgaaTipoIntervencao
from app.config import settings


DEFAULT_TIPOS: List[dict] = [
    {"nome": "Evolução EGAA", "descricao": "Registro de evolução clínica pelo EGAA", "ordem_exibicao": 0},
    {"nome": "Pendência para alta", "descricao": "Pendências operacionais para alta do paciente", "ordem_exibicao": 1},
    {"nome": "Intervenção EGAA", "descricao": "Intervenção realizada pela equipe EGAA", "ordem_exibicao": 2},
    {"nome": "Acompanhamento de paciente crônico", "descricao": "Acompanhamento longitudinal do paciente crônico", "ordem_exibicao": 3},
    {"nome": "Risco de readmissão", "descricao": "Avaliação de risco de readmissão", "ordem_exibicao": 4},
    # Sugestões adicionais
    {"nome": "Avaliação social", "descricao": "Avaliação social e suporte familiar", "ordem_exibicao": 10},
    {"nome": "Solicitação de exame", "descricao": "Solicitação de exames complementares", "ordem_exibicao": 11},
    {"nome": "Encaminhamento para especialidade", "descricao": "Encaminhamento para consulta especializada", "ordem_exibicao": 12},
    {"nome": "Alta programada", "descricao": "Planejamento de alta do paciente", "ordem_exibicao": 13},
]


def main() -> None:
    print("Usando database:", settings.database_url)
    db = SessionLocal()
    try:
        inserted = 0
        for item in DEFAULT_TIPOS:
            exists = db.execute(
                db.query(EgaaTipoIntervencao).filter(EgaaTipoIntervencao.nome == item["nome"]).exists().select()
            ).scalar()
            if exists:
                print(f"Já existe: {item['nome']}")
                continue
            row = EgaaTipoIntervencao(
                nome=item["nome"],
                descricao=item.get("descricao"),
                ativo=True,
                ordem_exibicao=item.get("ordem_exibicao", 0),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(row)
            inserted += 1
        if inserted:
            db.commit()
            print(f"Inseridos {inserted} tipos de intervenção.")
        else:
            print("Nenhum tipo novo inserido.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
