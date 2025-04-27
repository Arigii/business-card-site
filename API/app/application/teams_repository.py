from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Team


class TeamsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, team_id: int) -> Optional[Team]:
        stmt = select(Team).filter_by(id=team_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
