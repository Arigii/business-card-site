from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domain.entities.profile import ProfileEntity
from app.infrastructure.dependencies import get_current_user, require_admin
from app.infrastructure.profiles_service import ProfilesService

router = APIRouter()


@router.post(
    '/',
    response_model=Optional[ProfileEntity],
    summary='Create a new profile',
    description='Creates a new profile',
)
async def create_team(
        profile: ProfileEntity,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    profiles_service = ProfilesService(db)
    return await profiles_service.create_profile(profile)


@router.put(
    '/{profile_id}/',
    response_model=Optional[ProfileEntity],
    summary='Update a profile',
    description='Updates a profile',
)
async def create_team(
        profile_id: int,
        profile: ProfileEntity,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    profiles_service = ProfilesService(db)
    return await profiles_service.update_profile(profile_id, profile, user)


@router.delete(
    '/{profile_id}/',
    response_model=Optional[ProfileEntity],
    summary='Delete a profile',
    description='Delete a profile',
)
async def create_team(
        profile_id: int,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    profiles_service = ProfilesService(db)
    return await profiles_service.delete(profile_id, user)
