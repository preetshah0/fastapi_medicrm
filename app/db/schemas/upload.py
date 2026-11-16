from typing import Optional
from pydantic import BaseModel, ConfigDict


class FileUploadResponse(BaseModel):
    file_name: str
    file_path: str
    file_url: str
    file_size: int
    mime_type: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

