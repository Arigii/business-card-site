from sqlalchemy import Column, String, ForeignKey, Integer

from app.domain.models.base import AdvancedBaseModel


class ContestFile(AdvancedBaseModel):
    __tablename__ = 'contest_files'

    file_path = Column(String, nullable=False)

    contest_id = Column(Integer, ForeignKey('contests.id'), nullable=False)
