from sqlalchemy import String, Column, Integer, ForeignKey

from app.domain.models.base import AdvancedBaseModel


class ContestCarouselPhotos(AdvancedBaseModel):
    __tablename__ = 'contest_carousel_photos'

    file_path = Column(String, nullable=False)
    number = Column(Integer, nullable=False)

    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=False)
