from typing import AsyncGenerator, List
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
import crud
from api.exceptions import UserWithThatUserIdNotFoundException, InactiveUserException, InvalidRoleException
from core.security import decode_user_id_from_token
from model.user import User
from sql.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login/access-token"
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def get_current_user(required_roles: List[str] = None) -> User:
    async def current_user(
            db_session: AsyncSession = Depends(get_db),
            token: str = Depends(reusable_oauth2)
    ) -> User:
        user_id = await decode_user_id_from_token(token=token)
        user = await crud.user.get_user_by_id(user_id=user_id, db_session=db_session)

        if not user:
            raise UserWithThatUserIdNotFoundException(user_id=user_id)
        user = user[0]
        await db_session.refresh(user)
        if not user.is_active:
            raise InactiveUserException(user_id=user_id)

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user.role.name:
                    is_valid_role = True

            if is_valid_role is False:
                raise InvalidRoleException(req_roles=required_roles)

        return user

    return current_user
