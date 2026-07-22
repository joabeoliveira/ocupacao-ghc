"""
Script one-shot para gerar registros de desfecho (egaa_desfecho)
a partir de dados históricos já persistidos em ocupacao_leitos_ghc.

Regras de mapeamento:
  - Se DATA_OBITO preenchida → tipo = "obito", data = DATA_OBITO
  - Se TIPO_DE_ALTA contém "ÓBITO" → tipo = "obito", data = DATA_ALTA
  - Senão → tipo = "alta", data = DATA_ALTA
  - Para prontuários com múltiplos registros, usa o último (maior data_alta ou data_obito)
  - Nunca sobrescreve desfechos já existentes (INSERT ... ON DUPLICATE KEY UPDATE
    apenas quando o novo registro é mais recente)

Uso:
  $env:PYTHONPATH='backend'; python scripts/gerar_desfechos_do_historico.py
"""

from __future__ import annotations

import logging
import os
from datetime import datetime

from sqlalchemy import MetaData, Table, create_engine, select, func, and_, text

LOGGER = logging.getLogger(__name__)


def get_engine():
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE")
    if not all([user, password, host, database]):
        raise RuntimeError("Defina MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST e MYSQL_DATABASE no ambiente.")
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
    return create_engine(url, future=True)


def mapear_tipo_desfecho(tipo_alta: str | None, data_obito: any) -> str:
    """Define se o desfecho é 'alta' ou 'obito' baseado nos dados do registro."""
    if data_obito is not None:
        return "obito"
    if tipo_alta and "ÓBITO" in tipo_alta.upper():
        return "obito"
    return "alta"


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    engine = get_engine()
    metadata = MetaData()

    # Reflexão das tabelas
    ocupacao = Table("ocupacao_leitos_ghc", metadata, autoload_with=engine)
    desfecho = Table("egaa_desfecho", metadata, autoload_with=engine)

    # 1. Buscar todos os prontuários com data_alta no histórico
    LOGGER.info("Buscando registros do histórico com data_alta preenchida...")
    with engine.connect() as conn:
        # Subquery: para cada prontuário, pegar o registro mais recente (maior data_alta/data_obito)
        subq = (
            select(
                ocupacao.c.prontuario,
                func.max(
                    func.coalesce(ocupacao.c.data_obito, ocupacao.c.data_alta)
                ).label("data_desfecho_max"),
            )
            .where(
                and_(
                    ocupacao.c.fonte_dado == "historico_internacao",
                    ocupacao.c.data_alta.isnot(None),
                    ocupacao.c.prontuario.isnot(None),
                )
            )
            .group_by(ocupacao.c.prontuario)
        ).subquery()

        # Joins para pegar o registro completo
        query = (
            select(ocupacao)
            .join(
                subq,
                and_(
                    ocupacao.c.prontuario == subq.c.prontuario,
                    func.coalesce(ocupacao.c.data_obito, ocupacao.c.data_alta) == subq.c.data_desfecho_max,
                ),
            )
            .where(
                and_(
                    ocupacao.c.fonte_dado == "historico_internacao",
                    ocupacao.c.data_alta.isnot(None),
                    ocupacao.c.prontuario.isnot(None),
                )
            )
        )
        rows = conn.execute(query).fetchall()
        LOGGER.info("Encontrados %s registros para processar.", len(rows))

        if not rows:
            LOGGER.info("Nenhum registro para processar.")
            return

        now = datetime.utcnow()
        criados = 0
        pulados = 0

        for row in rows:
            row_dict = dict(row._mapping)
            prontuario = row_dict["prontuario"]
            tipo_alta = row_dict.get("tipo_alta")
            data_obito = row_dict.get("data_obito")
            data_alta = row_dict.get("data_alta")

            tipo = mapear_tipo_desfecho(tipo_alta, data_obito)
            data_desfecho = data_obito.date() if data_obito else data_alta.date() if data_alta else None

            if data_desfecho is None:
                LOGGER.warning("Prontuário %s sem data de desfecho válida, pulando.", prontuario)
                pulados += 1
                continue

            # Upsert: insere apenas se não existir desfecho para este prontuário
            stmt = text("""
                INSERT INTO egaa_desfecho (prontuario, tipo, data_desfecho, descricao, usuario_responsavel, created_at, updated_at)
                VALUES (:prontuario, :tipo, :data_desfecho, :descricao, :usuario_responsavel, :created_at, :updated_at)
                ON DUPLICATE KEY UPDATE
                    tipo = VALUES(tipo),
                    data_desfecho = VALUES(data_desfecho),
                    descricao = VALUES(descricao),
                    updated_at = VALUES(updated_at)
            """)
            # Note: ON DUPLICATE KEY não se aplica pois não há unique key em prontuario.
            # Usamos um INSERT simples e ignoramos duplicatas manualmente.
            # Verificamos se já existe desfecho para este prontuário
            existing = conn.execute(
                select(desfecho.c.id).where(desfecho.c.prontuario == prontuario).limit(1)
            ).fetchone()

            if existing:
                LOGGER.debug("Prontuário %s já possui desfecho, pulando.", prontuario)
                pulados += 1
                continue

            conn.execute(
                desfecho.insert().values(
                    prontuario=prontuario,
                    tipo=tipo,
                    data_desfecho=data_desfecho,
                    descricao=tipo_alta or "Importado automaticamente do histórico",
                    usuario_responsavel=None,
                    created_at=now,
                    updated_at=now,
                )
            )
            criados += 1
            LOGGER.info("Desfecho criado: %s -> %s em %s", prontuario, tipo, data_desfecho)

        conn.commit()
        LOGGER.info("Concluído! %s desfechos criados, %s pulados (já existentes).", criados, pulados)


if __name__ == "__main__":
    main()
