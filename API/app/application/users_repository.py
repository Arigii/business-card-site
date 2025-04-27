from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing_extensions import Optional

from app.domain.models import User, Profile


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).filter_by(id=user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_login(self, login: str) -> Optional[User]:
        stmt = (
            select(User)
            .filter_by(login=login)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
