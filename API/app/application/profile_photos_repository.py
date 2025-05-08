from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ProfilePhoto


class ProfilePhotosRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, photo_id: int) -> Optional[ProfilePhoto]:
        stmt = select(ProfilePhoto).filter_by(id=photo_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_profile_id(self, profile_id: int) -> Sequence[ProfilePhoto]:
        stmt = select(ProfilePhoto).filter_by(profile_id=profile_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, photo: ProfilePhoto) -> ProfilePhoto:
        self.db.add(photo)
        await self.db.commit()
        await self.db.refresh(photo)
        return photo

    async def delete(self, photo: ProfilePhoto) -> ProfilePhoto:
        await self.db.delete(photo)
        await self.db.commit()
        return photo
