from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from api import dependencies
from api.exceptions import UserWithThatUserIdNotFoundException
from model.user import User
from schema.response import IPostResponseBase, IPutResponseBase
from schema.role import IRoleEnum
from schema.user import IUserRead, IUserRegister

router = APIRouter()


@router.get('/{user_id}', response_model=IPostResponseBase[IUserRead])
async def get_user_by_id(user_id: int,
                         db_session: AsyncSession = Depends(dependencies.get_db),
                         curr_user: User = Depends(dependencies.get_current_user(required_roles=[IRoleEnum.admin]))):
    user = await crud.user.get_user_by_id(user_id, db_session)
    if user is None:
        raise UserWithThatUserIdNotFoundException(user_id=user_id)
    return IPostResponseBase[IUserRead](data=user[0])


@router.post('/register', response_model=IPostResponseBase[IUserRead])
async def register(user: IUserRegister, db_session: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.user.register(user, db_session)
    return IPostResponseBase[IUserRead](data=user)


@router.put('/set_role', response_model=IPutResponseBase[IUserRead])
async def set_role_by_user_id(user_id: int, new_role_id: int,
                              db_session: AsyncSession = Depends(dependencies.get_db),
                              curr_user: User = Depends(
                                  dependencies.get_current_user(required_roles=[IRoleEnum.admin]))):
    user = await crud.user.set_role(user_id=user_id, role_id=new_role_id, db_session=db_session)
    return IPutResponseBase[IUserRead](data=user)


