from datetime import datetime
from typing import Optional, Tuple
from pydantic import EmailStr
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from api.exceptions import UserWithThatEmailExistException, UserWithThatEmailNotFoundException, \
    IncorrectPasswordException, UserWithThatUserIdNotFoundException
from core.security import get_password_hash, verify_password
from crud.base_sqlmodel import CRUDBase
from model.user import User
from schema.user import IUserCreate, IUserUpdate, IUserRegister


class CRUDUser(CRUDBase[User, IUserCreate, IUserUpdate]):
    async def authenticate(self, user_email: EmailStr, user_password_raw: str, db_session: AsyncSession) -> int:
        user_obj = await self.get_user_by_email(user_email=user_email, db_session=db_session)
        if user_obj is None:
            raise UserWithThatEmailNotFoundException(email=user_email)
        user_obj = user_obj[0]
        if await verify_password(plain_password=user_password_raw, hashed_password=user_obj.hashed_password) is False:
            raise IncorrectPasswordException(email=user_email)
        return user_obj.id

    async def get_user_by_email(self, user_email: EmailStr, db_session: AsyncSession) -> Tuple[Optional[User]]:
        user_obj = (await db_session.exec(select(User).where(User.email == user_email))).first()
        return user_obj

    async def get_user_by_id(self, user_id: int, db_session: AsyncSession) -> Tuple[Optional[User]]:
        return await super().get(user_id, db_session)

    async def register(self, user_schema: IUserRegister, db_session: AsyncSession):
        return await self.create(IUserCreate.parse_obj(user_schema.dict()), db_session)

    async def create(self, user_schema: IUserCreate, db_session: AsyncSession) -> User:
        if (await self.get_user_by_email(user_schema.email, db_session)) is None:
            db_obj = User(
                first_name=user_schema.first_name,
                last_name=user_schema.last_name,
                email=user_schema.email,
                is_superuser=user_schema.is_superuser,
                hashed_password=await get_password_hash(user_schema.password),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                role_id=user_schema.role_id
            )
            db_session.add(db_obj)
            await db_session.commit()
            await db_session.refresh(db_obj)
            return db_obj
        else:
            raise UserWithThatEmailExistException(email=user_schema.email)

    async def set_role(self, user_id: int, role_id: int, db_session: AsyncSession):
        user_obj = await self.get_user_by_id(user_id=user_id, db_session=db_session)
        if user_obj is None:
            raise UserWithThatUserIdNotFoundException(user_id=user_id)
        user_obj = user_obj[0]
        user_obj.role_id = role_id
        db_session.add(user_obj)
        await db_session.commit()
        await db_session.refresh(user_obj)
        return user_obj


user = CRUDUser(User)
