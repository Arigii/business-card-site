from sqlalchemy import Column, VARCHAR, ForeignKey, Integer

from app.domain.models.base import AdvancedBaseModel


class User(AdvancedBaseModel):
    __tablename__ = 'users'

    login = Column(VARCHAR(150), unique=True, nullable=False)
    password = Column(VARCHAR(150), nullable=False)

    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
