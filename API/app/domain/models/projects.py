from sqlalchemy import Column, VARCHAR, String

from app.domain.models.base import AdvancedBaseModel


class Project(AdvancedBaseModel):
    __tablename__ = 'projects'

    description = Column(VARCHAR(150))
    repository_url = Column(String, nullable=False)
