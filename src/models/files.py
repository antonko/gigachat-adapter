from enum import Enum
from pydantic import BaseModel, Field


class FilePurpose(str, Enum):
    FINE_TUNE = "fine-tune"
    ASSISTANTS = "assistants"
    VISION = "vision"
    BATCH = "batch"
    GENERAL = "general"


class FileUploadResponse(BaseModel):
    id: str = Field(..., description="The ID of the uploaded file.")
    object: str = Field("file", description="The object type (always 'file')")
    bytes: int = Field(..., description="The size of the file in bytes")
    created_at: int = Field(..., description="Unix timestamp of when the file was created")
    filename: str = Field(..., description="The name of the file")
    purpose: FilePurpose = Field(..., description="The intended purpose of the file")
