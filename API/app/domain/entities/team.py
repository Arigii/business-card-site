from typing import Optional

from pydantic import BaseModel

from app.domain.entities.profile import ProfileEntity


class TeamEntity(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    logo: Optional[str] = None
    git_url: Optional[str] = None

    profiles: Optional[list[ProfileEntity]] = None
