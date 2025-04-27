from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Team


class TeamsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Team]:
        stmt = select(Team)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, team_id: int) -> Optional[Team]:
        stmt = select(Team).filter_by(id=team_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, team: Team) -> Team:
        self.db.add(team)
        await self.db.commit()
        await self.db.refresh(team)
        return team

    async def update(self, team: Team) -> Team:
        await self.db.merge(team)
        await self.db.commit()
        return team

    async def delete(self, team: Team) -> Team:
        await self.db.delete(team)
        await self.db.commit()
        return team
