from sqlalchemy import VARCHAR, Column
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class ContestStatus(AdvancedBaseModel):
    __tablename__ = 'contest_statuses'

    title = Column(VARCHAR(150), unique=True, nullable=False)

    contests = relationship("Contest", back_populates="status")
