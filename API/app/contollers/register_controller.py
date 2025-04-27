from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domain.entities.register import RegisterEntity
from app.domain.entities.user import UserEntity
from app.infrastructure.users_service import UsersService

router = APIRouter()


@router.post(
    '/',
    response_model=Optional[UserEntity],
    summary='User Registration',
    description='Performs user registration in the system',
)
async def register_user(
        user_data: RegisterEntity,
        db: AsyncSession = Depends(get_db)
):
    users_service = UsersService(db)
    user = await users_service.register_user(user_data)
    return user
