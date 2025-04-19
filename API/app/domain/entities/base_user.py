from pydantic import BaseModel


class BaseUserEntity(BaseModel):
    login: str
    password: str

    class Config:
        abstract = True
