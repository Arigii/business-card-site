from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class ProjectFile(AdvancedBaseModel):
    __tablename__ = 'project_files'

    file_path = Column(String, unique=True, nullable=False)

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship("Project", back_populates="files")
