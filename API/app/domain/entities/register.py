from app.domain.entities.base_profile import BaseProfileEntity
from app.domain.entities.base_user import BaseUserEntity


class RegisterEntity(BaseUserEntity, BaseProfileEntity):
    pass
