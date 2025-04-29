from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.domain.entities.user import UserEntity
from app.infrastructure.dependencies import require_admin
from app.infrastructure.users_service import UsersService

router = APIRouter()


@router.put(
    '/{user_id}/',
    response_model=Optional[UserEntity],
    summary='Change user password',
    description='Change user password',
)
async def create_team(
        user_id: int,
        new_password: str,
        db: AsyncSession = Depends(get_db),
        user=Depends(require_admin),
):
    users_service = UsersService(db)
    return await users_service.change_user_password(user_id, new_password)
