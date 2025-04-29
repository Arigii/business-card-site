from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.application.users_repository import UsersRepository
from app.database.session import get_db
from app.domain.models.users import User
from app.settings import get_auth_data

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    auth_data = get_auth_data()

    try:
        payload = jwt.decode(credentials.credentials, auth_data["secret_key"], algorithms=[auth_data["algorithm"]])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await UsersRepository(db).get_by_id_with_role(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def require_admin(user: User = Depends(get_current_user)) -> Optional[User]:
    if user.profile.role.title != "Администратор":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return user
