import os
from pathlib import Path
from pydantic_settings import BaseSettings


_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_path.exists():
    for _line in _env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" in _line and not _line.strip().startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ[_k.strip()] = _v.strip().strip("'").strip('"')


class Settings(BaseSettings):
    SECRET_KEY_ACCESS: str = "super_access_token_key_12345"
    SECRET_KEY_REFRESH: str = "super_refresh_token_key_12345"
    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"
    PATH_TO_DB: str = "database.db"
    JWT_SIGNING_ALGORITHM: str = "HS256"
    LOGIN_TIME_DAYS: int = 7
    PATH_TO_MOVIES_CSV: str = "movies.csv"

    class Config:
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()


def get_jwt_auth_manager():
    from security.token_manager import JWTAuthManager
    settings = get_settings()
    return JWTAuthManager(
        secret_key_access=settings.SECRET_KEY_ACCESS,
        secret_key_refresh=settings.SECRET_KEY_REFRESH,
        algorithm=settings.JWT_SIGNING_ALGORITHM
    )
