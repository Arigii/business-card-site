from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class Role(AdvancedBaseModel):
    __tablename__ = 'roles'

    title = Column(VARCHAR(150), unique=True, nullable=False)

    profiles = relationship('Profile', back_populates='role')
