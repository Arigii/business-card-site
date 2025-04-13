from sqlalchemy import Column, VARCHAR, Date, ForeignKey, Integer

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
