from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class ProfilePhoto(AdvancedBaseModel):
    __tablename__ = 'profile_photos'

    file_path = Column(String, nullable=False)

    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)

    profile = relationship('Profile', back_populates='photos')