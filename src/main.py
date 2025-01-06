from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import src.core.gigachat_monkey_patch  # noqa: F401

from .core.settings import get_app_settings
from .endpoints import router
from .models.common import ErrorDetail, ErrorResponse


def get_application() -> FastAPI:
    settings = get_app_settings()
    app = FastAPI(
        title="GigaChat Adapter API",
        description="Connector to GigaChat API using OpenAI",
        debug=settings.debug,
        cors_allowed_origins=settings.cors_allowed_hosts,
    )

    if settings.cors_allowed_hosts:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allowed_hosts,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(router)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=ErrorDetail(
                    message=str(exc.detail),
                    type="http",
                    code="HTTP_EXCEPTION",
                )
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error=ErrorDetail(
                    message=str(exc.errors()),
                    type="invalid_request_error",
                    code="BAD_REQUEST",
                )
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error=ErrorDetail(
                    message=str(exc),
                    type="http",
                    code="HTTP_EXCEPTION",
                )
            ).model_dump(),
        )

    return app


app = get_application()
