from typing import Optional

from pydantic import BaseModel


class ProjectMemberEntity(BaseModel):
    id: Optional[int] = None
    description: str
    project_id: int
    profile_id: int
