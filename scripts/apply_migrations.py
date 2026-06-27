from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS_DIR = ROOT / "migrations"
MIGRATIONS_TABLE = "schema_migrations"

sys.path.insert(0, str(ROOT / "backend"))

from app.config import settings  # noqa: E402


def _split_statements(sql_text: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []

    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        buffer.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(buffer).strip().rstrip(";").strip()
            if statement:
                statements.append(statement)
            buffer = []

    tail = "\n".join(buffer).strip().rstrip(";").strip()
    if tail:
        statements.append(tail)

    return statements


def main() -> None:
    engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

    with engine.begin() as conn:
        conn.execute(
            text(
                f"""
                CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    migration_name VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """
            )
        )
        applied = {
            row[0]
            for row in conn.execute(text(f"SELECT migration_name FROM {MIGRATIONS_TABLE}"))
        }

        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
        if not migration_files:
            print("Nenhuma migration encontrada em", MIGRATIONS_DIR)
            return

        for migration_path in migration_files:
            migration_name = migration_path.name
            if migration_name in applied:
                print(f"[skip] {migration_name}")
                continue

            sql_text = migration_path.read_text(encoding="utf-8")
            statements = _split_statements(sql_text)
            print(f"[apply] {migration_name} ({len(statements)} statements)")
            for statement in statements:
                conn.exec_driver_sql(statement)

            conn.execute(
                text(
                    f"INSERT INTO {MIGRATIONS_TABLE} (migration_name) VALUES (:migration_name)"
                ),
                {"migration_name": migration_name},
            )
            print(f"[ok] {migration_name}")


if __name__ == "__main__":
    main()
