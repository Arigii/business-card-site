from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class ProjectMember(AdvancedBaseModel):
    __tablename__ = 'project_members'

    description = Column(String)

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)

    project = relationship('Project', back_populates='members')
    profile = relationship('Profile', back_populates='projects')
