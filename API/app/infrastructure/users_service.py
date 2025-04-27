from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.profiles_repository import ProfilesRepository
from app.application.roles_repository import RolesRepository
from app.application.teams_repository import TeamsRepository
from app.application.users_repository import UsersRepository
from app.domain.entities.profile import ProfileEntity
from app.domain.entities.register import RegisterEntity
from app.domain.entities.user import UserEntity
from app.domain.models import User, Profile


class UsersService:
    def __init__(self, db: AsyncSession):
        self.users_repository = UsersRepository(db)
        self.teams_repository = TeamsRepository(db)
        self.roles_repository = RolesRepository(db)
        self.profiles_repository = ProfilesRepository(db)

    async def register_user(self, register_entity: RegisterEntity) -> Optional[UserEntity]:
        team = await self.teams_repository.get_by_id(register_entity.team_id)
        if team is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The team with this ID was not found",
            )

        role = await self.roles_repository.get_by_id(register_entity.role_id)
        if role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The role with this ID was not found",
            )

        user_model, profile_model = self.register_entity_to_models(register_entity)

        profile_model = await self.profiles_repository.create(profile_model)
        user_model.profile_id = profile_model.id
        user_model = await self.users_repository.create(user_model)

        user_entity = self.user_model_to_entity(user_model)
        user_entity.profile = self.profile_model_to_entity(profile_model)

        return user_entity

    @staticmethod
    def is_strong_password(password):
        if len(password) < 8:
            return False

        if not any(char.isupper() for char in password):
            return False

        if not any(char.islower() for char in password):
            return False

        if not any(char.isdigit() for char in password):
            return False

        if not any(char in "!@#$%^&*()_+" for char in password):
            return False

        if not any(char.isalpha() for char in password):
            return False

        return True

    @staticmethod
    def register_entity_to_models(register_entity: RegisterEntity) -> tuple[User, Profile]:
        user = User(
            login=register_entity.login,
        )

        user.set_password(register_entity.password)

        pofile = Profile(
            first_name=register_entity.first_name,
            last_name=register_entity.last_name,
            patronymic=register_entity.patronymic,
            birthday=register_entity.birthday,
            email=register_entity.email,
            phone=register_entity.phone,
            role_id=register_entity.role_id,
            team_id=register_entity.team_id
        )

        return user, pofile

    @staticmethod
    def profile_model_to_entity(profile_model: Profile) -> ProfileEntity:
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
    def user_model_to_entity(user_model: User) -> UserEntity:
        return UserEntity(
            id=user_model.id,
            login=user_model.login,
            profile_id=user_model.profile_id,
        )
