from sqlalchemy import VARCHAR, Column, String, ForeignKey, Integer, Boolean

from app.domain.models.base import AdvancedBaseModel


class Contest(AdvancedBaseModel):
    __tablename__ = 'contests'

    title = Column(VARCHAR(150), unique=True, nullable=False)
    description = Column(String)
    web_url = Column(String, nullable=False)
    photo = Column(String)
    results = Column(String)
    is_win = Column(Boolean)

    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('contest_status.id'), nullable=False)
