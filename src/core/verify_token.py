from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .settings import AppSettings, get_app_settings

router = APIRouter()
bearer_scheme = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    settings: AppSettings = Depends(get_app_settings),
):
    if (
        credentials.scheme.lower() != "bearer"
        or credentials.credentials != settings.bearer_token
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing Bearer token",
        )
