from typing import List

from pydantic import BaseModel


class ModelData(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str


class ModelsResponse(BaseModel):
    data: List[ModelData]
    object: str
