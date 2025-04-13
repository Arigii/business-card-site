from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class ContestFile(AdvancedBaseModel):
    __tablename__ = 'contest_files'

    file_path = Column(String, nullable=False)

    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=False)

    contest = relationship("Contest", back_populates="files")
