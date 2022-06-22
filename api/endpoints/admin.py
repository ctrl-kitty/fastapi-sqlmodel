from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from sqlmodel.ext.asyncio.session import AsyncSession

import crud
from api import dependencies
from api.exceptions import UserWithThatUserIdNotFoundException
from schema.response import IPostResponseBase, IPutResponseBase, IGetResponseBase
from schema.role import IRoleCreate, IRoleRead
from schema.user import IUserRead

router = APIRouter()


@router.get('/users', response_model=IPostResponseBase[IUserRead])
async def get_user_by_id(user_id: int,
                         db_session: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.user.get_user_by_id(user_id, db_session)
    if user is None:
        raise UserWithThatUserIdNotFoundException(user_id=user_id)
    return IPostResponseBase[IUserRead](data=user[0])


@router.put('/users/set_role', response_model=IPutResponseBase[IUserRead])
async def set_role_by_user_id(user_id: int, new_role_id: int,
                              db_session: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.user.set_role(user_id=user_id, role_id=new_role_id, db_session=db_session)
    return IPutResponseBase[IUserRead](data=user)


@router.get('/users/list', response_model=IGetResponseBase[Page[IUserRead]])
async def get_user_list(params: Params = Depends(), db_session: AsyncSession = Depends(dependencies.get_db)):
    users = await crud.user.get_multi_paginated(db_session=db_session, params=params)
    return IGetResponseBase[Page[IUserRead]](data=users)


@router.post('/roles/add', response_model=IPostResponseBase[IRoleRead])
async def create_new_role(role: IRoleCreate, db_session: AsyncSession = Depends(dependencies.get_db)):
    role = await crud.role.create(obj_in=role, db_session=db_session)
    return IPostResponseBase[IRoleRead](data=role)


@router.get('/roles/list', response_model=IGetResponseBase[Page[IRoleRead]])
async def get_roles_list(params: Params = Depends(), db_session: AsyncSession = Depends(dependencies.get_db)):
    roles = await crud.role.get_multi_paginated(db_session=db_session, params=params)
    return IGetResponseBase[Page[IUserRead]](data=roles)
