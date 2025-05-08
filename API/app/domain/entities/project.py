from typing import Optional

from pydantic import BaseModel


class ProjectEntity(BaseModel):
    id: Optional[int] = None
    description: str
    repository_url: Optional[str] = None