from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False
    environment: str = "production"
    bearer_token: str = Field(
        ...,
        description="Bearer token is required to authorize requests.",
    )
    cors_allowed_hosts: list[str] | None = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        extra = "allow"


def get_app_settings() -> AppSettings:
    return AppSettings()  # type: ignore
