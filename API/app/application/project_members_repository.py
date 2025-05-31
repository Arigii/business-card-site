from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ProjectMember


class ProjectMembersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, project_member_id: int) -> Optional[ProjectMember]:
        stmt = select(ProjectMember).filter_by(id=project_member_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_by_project_id(self, project_id: int) -> Sequence[ProjectMember]:
        stmt = select(ProjectMember).filter_by(project_id=project_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_profile_id(self, profile_id: int) -> Sequence[ProjectMember]:
        stmt = select(ProjectMember).filter_by(profile_id=profile_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_project_id_and_profile_id(self, project_id: int, profile_id: int) -> Optional[ProjectMember]:
        stmt = select(ProjectMember).filter_by(project_id=project_id, profile_id=profile_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_list(self, project_members: list[ProjectMember]) -> list[ProjectMember]:
        self.db.add_all(project_members)
        await self.db.commit()

        for project_member in project_members:
            await self.db.refresh(project_member)

        return project_members

    async def delete_list_members(self, project_members: list[ProjectMember]) -> list[ProjectMember]:
        for project_member in project_members:
            await self.db.delete(project_member)

        await self.db.commit()
        return project_members
