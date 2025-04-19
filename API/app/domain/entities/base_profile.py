import datetime
from typing import Optional

from pydantic import BaseModel


class BaseProfileEntity(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str] = None
    birthday: datetime.date
    email: Optional[str] = None
    phone: Optional[str] = None

    role_id: int
    team_id: int

    class Config:
        abstract = True
