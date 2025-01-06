from typing import Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    message: str = Field(..., description="Human-readable error message")
    type: str = Field(..., description="The type of error that occurred")
    param: Optional[str] = Field(
        None, description="The parameter that caused the error, if applicable"
    )
    code: str = Field(..., description="Machine-readable error code")


class ErrorResponse(BaseModel):
    error: ErrorDetail = Field(..., description="The error details")
