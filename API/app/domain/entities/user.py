from typing import Optional

from app.domain.entities.base_user import BaseUserEntity
from app.domain.entities.profile import ProfileEntity


class UserEntity(BaseUserEntity):
    id: Optional[int] = None

    profile_id: int

    profile: Optional[ProfileEntity] = None
