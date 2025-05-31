from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.profiles_repository import ProfilesRepository
from app.application.project_members_repository import ProjectMembersRepository
from app.application.projects_repository import ProjectsRepository
from app.domain.entities.project_member import ProjectMemberEntity
from app.domain.models import ProjectMember


class ProjectMembersService:
    def __init__(self, db: AsyncSession):
        self.project_members_repository = ProjectMembersRepository(db)
        self.projects_repository = ProjectsRepository(db)
        self.profiles_repository = ProfilesRepository(db)

    async def get_project_members_by_project_id(self, project_id: int) -> list[ProjectMemberEntity]:
        project_members = await self.project_members_repository.get_by_project_id(project_id)
        return [
            self.model_to_entity(project_member)
            for project_member in project_members
        ]

    async def get_project_members_by_profile_id(self, profile_id: int) -> list[ProjectMemberEntity]:
        project_members = await self.project_members_repository.get_by_profile_id(profile_id)
        return [
            self.model_to_entity(project_member)
            for project_member in project_members
        ]

    async def create_list_project_members(self, project_id: int, project_members: list[ProjectMemberEntity]) -> \
            Optional[
                list[ProjectMemberEntity]
            ]:
        project = await self.projects_repository.get_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The project with this ID was not found',
            )

        project_members_models = []

        for project_member in project_members:
            if project_member.project_id != project_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='The project ID from the request parameter and the project ID from the transmitted data do not match'
                )

            profile = await self.profiles_repository.get_by_id(project_member.profile_id)

            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='The profile with this ID was not found',
                )

            project_members_models.append(
                self.entity_to_model(project_member)
            )

        await self.project_members_repository.create_list(project_members_models)

        return [
            self.model_to_entity(member)
            for member in project_members_models
        ]

    async def update_list_project_members(
            self,
            project_id: int,
            project_members: list[ProjectMemberEntity]
    ) -> Optional[list[ProjectMemberEntity]]:
        project = await self.projects_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The project with this ID was not found',
            )

        old_members = await self.project_members_repository.get_by_project_id(project_id)

        if old_members:
            await self.project_members_repository.delete_list_members(list(old_members))

        return await self.create_list_project_members(project_id, project_members)

    async def delete_project_members_by_project_id(self, project_id: int) -> Optional[list[ProjectMemberEntity]]:
        project = await self.projects_repository.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The project with this ID was not found',
            )

        project_members = await self.project_members_repository.get_by_project_id(project_id)

        if project_members:
            await self.project_members_repository.delete_list_members(list(project_members))

        return [
            self.model_to_entity(project_member)
            for project_member in project_members
        ]

    @staticmethod
    def model_to_entity(project: ProjectMember) -> ProjectMemberEntity:
        return ProjectMemberEntity(
            id=project.id,
            description=project.description,
            project_id=project.project_id,
            profile_id=project.profile_id,
        )

    @staticmethod
    def entity_to_model(project: ProjectMemberEntity) -> ProjectMember:
        project_model = ProjectMember(
            description=project.description,
            project_id=project.project_id,
            profile_id=project.profile_id,
        )

        if project.id:
            project_model.id = project.id

        return project_model
