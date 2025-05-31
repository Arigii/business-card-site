from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domain.entities.project import ProjectEntity
from app.infrastructure.dependencies import require_admin
from app.infrastructure.projects_service import ProjectsService

router = APIRouter()


@router.get(
    '/',
    response_model=list[ProjectEntity],
    summary='Get all projects',
    description='Returns all projects',
)
async def get_all_projects(
        db: AsyncSession = Depends(get_db),
):
    projects_service = ProjectsService(db)
    return await projects_service.get_all_projects()


@router.post(
    '/',
    response_model=Optional[ProjectEntity],
    summary='Create a new project',
    description='Creates a new project',
)
async def create_project(
        project: ProjectEntity,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    projects_service = ProjectsService(db)
    return await projects_service.create_project(project)


@router.put(
    '/{project_id}/',
    response_model=Optional[ProjectEntity],
    summary='Update a project',
    description='Updates a project',
)
async def update_project(
        project_id: int,
        project: ProjectEntity,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    projects_service = ProjectsService(db)
    return await projects_service.update_project(project_id, project)


@router.delete(
    '/{project_id}/',
    response_model=Optional[ProjectEntity],
    summary='Delete a project',
    description='Delete a project',
)
async def delete_project(
        project_id: int,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    projects_service = ProjectsService(db)
    return await projects_service.delete_project(project_id)
