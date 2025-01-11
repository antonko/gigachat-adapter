import tomllib

from pydantic import Field
from pydantic_settings import BaseSettings


def get_version() -> str:
    """Получает версию из pyproject.toml"""
    try:
        with open("pyproject.toml", "rb") as f:
            return tomllib.load(f)["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "unknown"


class AppSettings(BaseSettings):
    debug: bool = False
    environment: str = "production"
    bearer_token: str = Field(
        ...,
        description="Bearer token is required to authorize requests.",
    )
    cors_allowed_hosts: list[str] | None = ["http://localhost:5173"]
    version: str = Field(default_factory=get_version)

    class Config:
        env_file = ".env"
        extra = "allow"


def get_app_settings() -> AppSettings:
    return AppSettings()  # type: ignore
