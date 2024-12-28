import os

from dotenv import load_dotenv
from gigachat import GigaChat

from .models import ModelData, ModelsResponse


class GigaChatService:
    def __init__(self, **kwargs):
        load_dotenv()
        config = self._get_config_from_env()
        config.update(kwargs)
        self._client = GigaChat(**config)
        self._client.get_token()

    def _get_config_from_env(self):
        return {
            "base_url": os.getenv("GIGACHAT_BASE_URL"),
            "auth_url": os.getenv("GIGACHAT_AUTH_URL"),
            "credentials": os.getenv("GIGACHAT_CREDENTIALS"),
            "scope": os.getenv("GIGACHAT_SCOPE"),
            "access_token": os.getenv("GIGACHAT_ACCESS_TOKEN"),
            "model": os.getenv("GIGACHAT_MODEL"),
            "profanity_check": os.getenv("GIGACHAT_PROFANITY_CHECK"),
            "user": os.getenv("GIGACHAT_USER"),
            "password": os.getenv("GIGACHAT_PASSWORD"),
            "timeout": os.getenv("GIGACHAT_TIMEOUT"),
            "verify_ssl_certs": os.getenv("GIGACHAT_VERIFY_SSL_CERTS"),
            "verbose": os.getenv("GIGACHAT_VERBOSE"),
            "ca_bundle_file": os.getenv("GIGACHAT_CA_BUNDLE_FILE"),
            "cert_file": os.getenv("GIGACHAT_CERT_FILE"),
            "key_file": os.getenv("GIGACHAT_KEY_FILE"),
            "key_file_password": os.getenv("GIGACHAT_KEY_FILE_PASSWORD"),
        }

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
