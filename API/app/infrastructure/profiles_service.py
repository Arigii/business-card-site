from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.profiles_repository import ProfilesRepository
from app.application.roles_repository import RolesRepository
from app.application.teams_repository import TeamsRepository
from app.application.users_repository import UsersRepository
from app.domain.entities.profile import ProfileEntity
from app.domain.models import Profile, User


class ProfilesService:
    def __init__(self, db: AsyncSession):
        self.profiles_repository = ProfilesRepository(db)
        self.teams_repository = TeamsRepository(db)
        self.roles_repository = RolesRepository(db)
        self.users_repository = UsersRepository(db)

    async def create_profile(self, profile: ProfileEntity) -> Optional[ProfileEntity]:
        team = await self.teams_repository.get_by_id(profile.team_id)
        if team is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The team with this ID was not found",
            )

        role = await self.roles_repository.get_by_id(profile.role_id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The role with this ID was not found",
            )

        profile_model = self.entity_to_model(profile)

        profile_model = await self.profiles_repository.create(profile_model)

        return self.model_to_entity(profile_model)

    async def update_profile(self, profile_id: int, profile: ProfileEntity, user: User) -> Optional[
        ProfileEntity
    ]:
        user = await self.users_repository.get_by_id(user.id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this ID was not found",
            )

        profile_model = await self.profiles_repository.get_by_id(profile_id)
        if profile_model.id != user.profile_id and user.profile.role.title != 'Администратор':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        team = await self.teams_repository.get_by_id(profile.team_id)
        if team is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The team with this ID was not found",
            )

        role = await self.roles_repository.get_by_id(profile.role_id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The role with this ID was not found",
            )

        profile_model.first_name = profile.first_name
        profile_model.last_name = profile.last_name
        profile_model.patronymic = profile.patronymic
        profile_model.birthday = profile.birthday
        profile_model.email = profile.email
        profile_model.phone = profile.phone
        profile_model.role_id = profile.role_id
        profile_model.team_id = profile.team_id

        profile_model = await self.profiles_repository.update(profile_model)

        return self.model_to_entity(profile_model)

    async def delete(self, profile_id: int, user: User):
        user = await self.users_repository.get_by_id(user.id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this ID was not found",
            )

        profile_model = await self.profiles_repository.get_by_id(profile_id)
        if profile_model.id != user.profile_id and user.profile.role.title != 'Администратор':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        result = await self.profiles_repository.delete(profile_model)

        return self.model_to_entity(result)

    @staticmethod
    def model_to_entity(profile_model: Profile) -> ProfileEntity:
        return ProfileEntity(
            id=profile_model.id,
            first_name=profile_model.first_name,
            last_name=profile_model.last_name,
            patronymic=profile_model.patronymic,
            birthday=profile_model.birthday,
            email=profile_model.email,
            phone=profile_model.phone,
            role_id=profile_model.role_id,
            team_id=profile_model.team_id,
        )

    @staticmethod
    def entity_to_model(profile_entity: ProfileEntity) -> Profile:
        profile_model = Profile(
            first_name=profile_entity.first_name,
            last_name=profile_entity.last_name,
            patronymic=profile_entity.patronymic,
            birthday=profile_entity.birthday,
            email=profile_entity.email,
            phone=profile_entity.phone,
            role_id=profile_entity.role_id,
            team_id=profile_entity.team_id,
        )

        if profile_entity.id is not None:
            profile_model.id = profile_entity.id

        return profile_model
