from typing import List

from pydantic import BaseModel, Field


class ModelData(BaseModel):
    id: str = Field(
        ...,
        description="The model identifier, which can be referenced in the API endpoints.",
    )
    created: int = Field(
        ..., description="The Unix timestamp (in seconds) when the model was created."
    )
    object: str = Field(
        "model", description='The object type, which is always "model".'
    )
    owned_by: str = Field(..., description="The organization that owns the model.")


class ListModelsResponse(BaseModel):
    object: str = Field("list", description='The object type, which is always "list".')
    data: List[ModelData]
