from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from api import dependencies
from model.user import User
from schema.response import IGetResponseBase, IPostResponseBase
from schema.user import IUserCreate, IUserRead, IUserRegister

router = APIRouter()


@router.get('/{id}', response_model=IPostResponseBase[IUserRead])
async def get_user_by_id(user_id: int, db_session: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.user.get_user_by_id(user_id, db_session)
    return IPostResponseBase[IUserRead](data=user)


@router.post('/register', response_model=IPostResponseBase[IUserRead])
async def register(user: IUserRegister, db_session: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.user.register(user, db_session)
    return IPostResponseBase[IUserRead](data=user)

