"""
Этот "хак" (монки-патчинг) необходим для корректной работы потокового получения данных из GigaChat.
Проблема заключается в том, что библиотека httpx по умолчанию не использует HTTP/2,
что приводит к тому, что GigaChat не отправляет данные потоками, а возвращает их сразу целиком.
Данный код исправляет это поведение, включая поддержку HTTP/2 при подключении к API GigaChat.
"""

from typing import Any, Dict

import gigachat.client
import httpx
from gigachat.settings import Settings


def _get_kwargs(settings: Settings) -> Dict[str, Any]:
    """Настройки для подключения к API GIGACHAT"""
    kwargs = {
        "base_url": settings.base_url,
        "verify": settings.verify_ssl_certs,
        "timeout": httpx.Timeout(settings.timeout),
        "http2": True,  # Включаем поддержку HTTP/2
    }
    if settings.ca_bundle_file:
        kwargs["verify"] = settings.ca_bundle_file
    if settings.cert_file:
        kwargs["cert"] = (
            settings.cert_file,
            settings.key_file,
            settings.key_file_password,
        )
    return kwargs


gigachat.client._get_kwargs = _get_kwargs
