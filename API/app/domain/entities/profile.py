from typing import Optional

from app.domain.entities.base_profile import BaseProfileEntity


class ProfileEntity(BaseProfileEntity):
    id: Optional[int] = None