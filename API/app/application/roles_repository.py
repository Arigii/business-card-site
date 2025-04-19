from select import select
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Role


class RolesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, role_id: int) -> Optional[Role]:
        stmt = select(Role).filter_by(id=role_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
