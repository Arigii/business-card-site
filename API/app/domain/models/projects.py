from sqlalchemy import Column, VARCHAR, String
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class Project(AdvancedBaseModel):
    __tablename__ = 'projects'

    description = Column(VARCHAR(150))
    repository_url = Column(String, nullable=False)

    contest = relationship("Contest", back_populates="project")
    files = relationship("ProjectFile", back_populates="project")
