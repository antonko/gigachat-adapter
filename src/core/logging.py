import logging

from .settings import get_app_settings

app_settings = get_app_settings()
local_logger = logging.getLogger("uvicorn")
local_logger.setLevel(logging.DEBUG if app_settings.debug else logging.INFO)
