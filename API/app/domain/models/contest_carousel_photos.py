from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class ContestCarouselPhoto(AdvancedBaseModel):
    __tablename__ = 'contest_carousel_photos'

    file_path = Column(String, nullable=False)
    number = Column(Integer, nullable=False)

    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=False)

    contest = relationship('Contest', back_populates='carousel_photos')
