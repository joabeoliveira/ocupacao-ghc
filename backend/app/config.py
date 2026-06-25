from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def _split_csv(value: str | None, default: list[str]) -> list[str]:
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(slots=True)
class Settings:
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "EGAA API"))
    app_env: str = field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    api_prefix: str = field(default_factory=lambda: os.getenv("API_PREFIX", "/api"))
    mysql_user: str = field(default_factory=lambda: os.getenv("MYSQL_USER", ""))
    mysql_password: str = field(default_factory=lambda: os.getenv("MYSQL_PASSWORD", ""))
    mysql_host: str = field(default_factory=lambda: os.getenv("MYSQL_HOST", "localhost"))
    mysql_port: str = field(default_factory=lambda: os.getenv("MYSQL_PORT", "3306"))
    mysql_database: str = field(default_factory=lambda: os.getenv("MYSQL_DATABASE", "nir"))
    cors_origins: list[str] = field(
        default_factory=lambda: _split_csv(
            os.getenv(
                "CORS_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000,https://localhost:3000",
            ),
            ["http://localhost:3000"],
        )
    )
    upload_tmp_dir: str = field(default_factory=lambda: os.getenv("UPLOAD_TMP_DIR", "backend/tmp"))

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )


settings = Settings()