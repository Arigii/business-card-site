from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.projects_repository import ProjectsRepository
from app.domain.entities.project import ProjectEntity
from app.domain.models import Project


class ProjectsService:
    def __init__(self, db: AsyncSession):
        self.projects_repository = ProjectsRepository(db)

    async def get_all_projects(self) -> list[ProjectEntity]:
        projects = await self.projects_repository.get_all()
        return [
            self.model_to_entity(project)
            for project in projects
        ]

    async def create_project(self, project: ProjectEntity) -> Optional[ProjectEntity]:
        project_model = self.entity_to_model(project)

        await self.projects_repository.create(project_model)

        return self.model_to_entity(project_model)

    async def update_project(self, project_id: int, project: ProjectEntity) -> Optional[ProjectEntity]:
        project_model = await self.projects_repository.get_by_id(project_id)

        if not project_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        project_model.description = project.description
        project_model.repository_url = project.repository_url

        await self.projects_repository.update(project_model)

        return self.model_to_entity(project_model)

    async def delete_project(self, project_id: int) -> Optional[ProjectEntity]:
        project_model = await self.projects_repository.get_by_id(project_id)

        if not project_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        result = await self.projects_repository.delete(project_model)

        return self.model_to_entity(result)

    @staticmethod
    def model_to_entity(project_model: Project) -> ProjectEntity:
        return ProjectEntity(
            id=project_model.id,
            description=project_model.description,
            repository_url=project_model.repository_url,
        )

    @staticmethod
    def entity_to_model(project_entity: ProjectEntity) -> Project:
        project_model = Project(
            description=project_entity.description,
            repository_url=project_entity.repository_url,
        )

        if project_entity.id:
            project_model.id = project_entity.id

        return project_model
