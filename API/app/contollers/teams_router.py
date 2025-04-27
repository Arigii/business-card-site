from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domain.entities.team import TeamEntity
from app.infrastructure.dependencies import get_current_user, require_admin
from app.infrastructure.teams_service import TeamsService

router = APIRouter()


@router.get(
    '/',
    response_model=list[TeamEntity],
    summary='Get all teams',
    description='Returns all teams',
)
async def get_all_teams(
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
):
    teams_service = TeamsService(db)
    return await teams_service.get_all_teams()


@router.post(
    '/',
    response_model=Optional[TeamEntity],
    summary='Create a new team',
    description='Creates a new team',
)
async def create_team(
        team: TeamEntity,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
):
    teams_service = TeamsService(db)
    return await teams_service.create_team(team)


@router.put(
    '/{team_id}/',
    response_model=Optional[TeamEntity],
    summary='Update a team',
    description='Updates a team',
)
async def create_team(
        team_id: int,
        team: TeamEntity,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
):
    teams_service = TeamsService(db)
    return await teams_service.update_team(team_id, team)


@router.delete(
    '/{team_id}/',
    response_model=Optional[TeamEntity],
    summary='Delete a team',
    description='Delete a team',
)
async def create_team(
        team_id: int,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    teams_service = TeamsService(db)
    return await teams_service.delete_team(team_id)
