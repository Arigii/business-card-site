from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Profile


class ProfilesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, profile_id: int) -> Optional[Profile]:
        stmt = select(Profile).filter_by(id=profile_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, profile: Profile) -> Profile:
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def update(self, profile: Profile) -> Profile:
        await self.db.merge(profile)
        await self.db.commit()
        return profile

    async def delete(self, profile: Profile) -> Profile:
        await self.db.delete(profile)
        await self.db.commit()
        return profile
