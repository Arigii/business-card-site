from sqlalchemy import Column, VARCHAR, String
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class Team(AdvancedBaseModel):
    __tablename__ = 'teams'

    title = Column(VARCHAR(150), nullable=False)
    description = Column(VARCHAR(150))
    logo = Column(String)
    git_url = Column(String)

    profile = relationship("Profile", back_populates="team")
