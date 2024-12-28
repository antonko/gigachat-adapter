from dotenv import load_dotenv
from gigachat import GigaChat
from pydantic_settings import BaseSettings

from .models import ModelData, ModelsResponse


class GigaChatSettings(BaseSettings):
    base_url: str | None = None
    auth_url: str | None = None
    credentials: str | None = None
    scope: str | None = None
    access_token: str | None = None
    model: str | None = None
    profanity_check: bool | None = None
    user: str | None = None
    password: str | None = None
    timeout: int | None = None
    verify_ssl_certs: bool | None = None
    verbose: bool | None = None
    ca_bundle_file: str | None = None
    cert_file: str | None = None
    key_file: str | None = None
    key_file_password: str | None = None

    class Config:
        env_file = ".env"
        env_prefix = "GIGACHAT_"
        extra = "allow"


class GigaChatService:
    def __init__(self, **kwargs):
        load_dotenv()
        self._settings = GigaChatSettings(**kwargs)
        self._client = GigaChat(
            base_url=self._settings.base_url,
            auth_url=self._settings.auth_url,
            credentials=self._settings.credentials,
            scope=self._settings.scope,
            access_token=self._settings.access_token,
            model=self._settings.model,
            profanity_check=self._settings.profanity_check,
            user=self._settings.user,
            password=self._settings.password,
            timeout=self._settings.timeout,
            verify_ssl_certs=self._settings.verify_ssl_certs,
            verbose=self._settings.verbose,
            ca_bundle_file=self._settings.ca_bundle_file,
            cert_file=self._settings.cert_file,
            key_file=self._settings.key_file,
            key_file_password=self._settings.key_file_password,
        )
        self._client.get_token()

    def get_models(self) -> ModelsResponse:
        raw_models = self._client.get_models()
        data = [
            ModelData(
                id=m.id_, object=m.object_, owned_by=m.owned_by, created=1735689600
            )
            for m in raw_models.data
        ]
        return ModelsResponse(data=data, object="list")


gigachat_service = GigaChatService()
