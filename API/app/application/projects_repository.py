from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Project


class ProjectsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Project]:
        stmt = select(Project)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        stmt = select(Project).filter_by(id=project_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, project: Project) -> Project:
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def update(self, project: Project) -> Project:
        await self.db.merge(project)
        await self.db.commit()
        return project

    async def delete(self, project: Project) -> Project:
        await self.db.delete(project)
        await self.db.commit()
        return project
