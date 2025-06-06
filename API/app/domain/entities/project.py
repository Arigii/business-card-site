from typing import Optional

from pydantic import BaseModel


class ProjectEntity(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    repository_url: Optional[str] = None