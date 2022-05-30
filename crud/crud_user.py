from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.exceptions import UserWithThatEmailExistException
from core.security import get_password_hash
from crud.base_sqlmodel import CRUDBase
from model.user import User
from schema.response import IResponseBase
from schema.user import IUserCreate, IUserUpdate, IUserRegister


class CRUDUser(CRUDBase[User, IUserCreate, IUserUpdate]):
    async def get_user_by_email(self, user_email: EmailStr, db_session: AsyncSession):
        return (await db_session.exec(select(User).where(User.email == user_email))).first()

    async def get_user_by_id(self, user_id: int, db_session: AsyncSession):
        return await super().get(user_id, db_session)

    async def register(self, user: IUserRegister, db_session: AsyncSession):
        return await self.create(IUserCreate.parse_obj(user.dict()), db_session)

    async def create(self, user: IUserCreate, db_session: AsyncSession) -> User:
        if (await self.get_user_by_email(user.email, db_session)) is None:
            db_obj = User(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_superuser=user.is_superuser,
                hashed_password=get_password_hash(user.password),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                role_id=user.role_id
            )
            db_session.add(db_obj)
            await db_session.commit()
            await db_session.refresh(db_obj)
            return db_obj
        else:
            raise UserWithThatEmailExistException(email=user.email)


user = CRUDUser(User)
