from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domain.entities.project_member import ProjectMemberEntity
from app.infrastructure.dependencies import require_admin
from app.infrastructure.project_members_service import ProjectMembersService

router = APIRouter()


@router.get(
    '/by-project/{project_id}/',
    response_model=list[ProjectMemberEntity],
    summary='Get project members by project ID',
    description='Returns all project members with the specified project ID'
)
async def get_members_by_project_id(
        project_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = ProjectMembersService(db)
    return await service.get_project_members_by_project_id(project_id)


@router.get(
    '/by-profile/{profile_id}/',
    response_model=list[ProjectMemberEntity],
    summary='Get project members by profile ID',
    description='Returns all project member records where the profile is involved'
)
async def get_members_by_profile_id(
        profile_id: int,
        db: AsyncSession = Depends(get_db)
):
    service = ProjectMembersService(db)
    return await service.get_project_members_by_profile_id(profile_id)


@router.post(
    '/{project_id}/',
    response_model=Optional[list[ProjectMemberEntity]],
    summary='Create a list of project members',
    description='Creates a list of project members for the specified project ID'
)
async def create_project_members(
        project_id: int,
        project_members: list[ProjectMemberEntity],
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    service = ProjectMembersService(db)
    return await service.create_list_project_members(project_id, project_members)


@router.put(
    '/{project_id}/',
    response_model=Optional[list[ProjectMemberEntity]],
    summary='Update the list of project members',
    description='Deletes all current project members and creates new records'
)
async def update_project_members(
        project_id: int,
        project_members: list[ProjectMemberEntity],
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    service = ProjectMembersService(db)
    return await service.update_list_project_members(project_id, project_members)


@router.delete(
    '/{project_id}/',
    summary='Delete all project members by project ID',
    description='Deletes all project members with the specified project ID',
)
async def delete_project_members(
        project_id: int,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    service = ProjectMembersService(db)
    await service.delete_project_members_by_project_id(project_id)
    return {"message": "All project members have been successfully deleted."}
