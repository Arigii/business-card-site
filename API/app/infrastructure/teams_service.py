from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.teams_repository import TeamsRepository
from app.domain.entities.team import TeamEntity
from app.domain.models import Team


class TeamsService:
    def __init__(self, db: AsyncSession):
        self.teams_repository = TeamsRepository(db)

    async def get_all_teams(self) -> list[TeamEntity]:
        teams = await self.teams_repository.get_all()
        return [
            self.model_to_entity(team)
            for team in teams
        ]

    async def create_team(self, team: TeamEntity) -> Optional[TeamEntity]:
        team_model = self.entity_to_model(team)

        await self.teams_repository.create(team_model)

        return self.model_to_entity(team_model)

    async def update_team(self, team_id: int, team: TeamEntity) -> Optional[TeamEntity]:
        team_model = await self.teams_repository.get_by_id(team_id)

        if not team_model:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not found")

        team_model.title = team.title
        team_model.description = team.description
        team_model.git_url = team.git_url

        await self.teams_repository.update(team_model)

        return self.model_to_entity(team_model)

    async def delete_team(self, team_id: int) -> Optional[TeamEntity]:
        team_model = await self.teams_repository.get_by_id(team_id)

        if not team_model:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not found")

        result = await self.teams_repository.delete(team_model)

        return self.model_to_entity(result)

    @staticmethod
    def model_to_entity(team_model: Team) -> TeamEntity:
        return TeamEntity(
            id=team_model.id,
            title=team_model.title,
            description=team_model.description,
            logo=team_model.logo,
            git_url=team_model.git_url,
        )

    @staticmethod
    def entity_to_model(team_entity: TeamEntity) -> Team:
        team_model = Team(
            title=team_entity.title,
            description=team_entity.description,
            logo=team_entity.logo,
            git_url=team_entity.git_url,
        )

        if team_entity.id:
            team_model.id = team_entity.id

        return team_model
