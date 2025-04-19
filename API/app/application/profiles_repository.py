from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Profile


class ProfilesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, profile: Profile) -> Profile:
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile