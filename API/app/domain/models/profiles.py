from sqlalchemy import Column, VARCHAR, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.domain.models.base import AdvancedBaseModel


class Profile(AdvancedBaseModel):
    __tablename__ = 'profiles'

    first_name = Column(VARCHAR(150), nullable=False)
    last_name = Column(VARCHAR(150), nullable=False)
    patronymic = Column(VARCHAR(150))
    birthday = Column(Date, nullable=False)
    email = Column(VARCHAR(150))
    phone = Column(VARCHAR(28))

    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    role = relationship('Role', back_populates='profiles')
    team = relationship('Team', back_populates='profiles')

    user = relationship('User', back_populates='profile')
    profile_photos = relationship('ProfilePhoto', back_populates='profile')
    projects = relationship('ProjectMember', back_populates='profile')
