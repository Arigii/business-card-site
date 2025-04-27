from sqlalchemy import Column, VARCHAR, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.domain.models.base import AdvancedBaseModel


class User(AdvancedBaseModel):
    __tablename__ = 'users'

    login = Column(VARCHAR(150), unique=True, nullable=False)
    password = Column(String, nullable=False)

    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)

    profile = relationship('Profile', back_populates='user')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
