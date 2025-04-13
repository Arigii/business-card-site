from sqlalchemy import Column, VARCHAR, String

from app.domain.models.base import AdvancedBaseModel


class Team(AdvancedBaseModel):
    __tablename__ = 'teams'

    title = Column(VARCHAR(150), nullable=False)
    description = Column(VARCHAR(150))
    logo = Column(String)
    git_url = Column(String)