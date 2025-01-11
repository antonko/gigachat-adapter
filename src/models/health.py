from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field("ok", description="The status of the service")
    version: str = Field(..., description="The version of the service")
