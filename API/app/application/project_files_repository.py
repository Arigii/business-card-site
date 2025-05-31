from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ProjectFile


class ProjectFilesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, file_id: int) -> Optional[ProjectFile]:
        stmt = select(ProjectFile).filter_by(id=file_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_project_id(self, project_id: int) -> Sequence[ProjectFile]:
        stmt = select(ProjectFile).filter_by(project_id=project_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, project_file: ProjectFile) -> ProjectFile:
        self.db.add(project_file)
        await self.db.commit()
        await self.db.refresh(project_file)
        return project_file

    async def delete(self, project_file: ProjectFile) -> ProjectFile:
        await self.db.delete(project_file)
        await self.db.commit()
        return project_file
