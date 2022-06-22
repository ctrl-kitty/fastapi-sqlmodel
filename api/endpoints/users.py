from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from api import dependencies
from model.user import User
from schema.response import IPostResponseBase, IGetResponseBase, IDeleteResponseBase
from schema.user import IUserRead, IUserRegister

router = APIRouter()


@router.get('/me', response_model=IGetResponseBase[IUserRead])
async def get_user_by_id(curr_user: User = Depends(dependencies.get_current_user())):
    return IGetResponseBase[IUserRead](data=curr_user)


@router.post('/register', response_model=IPostResponseBase[IUserRead])
async def register(user: IUserRegister, db_session: AsyncSession = Depends(dependencies.get_db)):
    user = await crud.user.register(user, db_session)
    return IPostResponseBase[IUserRead](data=user)


@router.delete('/delete', response_model=IDeleteResponseBase[IUserRead])
async def delete_user(db_session: AsyncSession = Depends(dependencies.get_db),
                      curr_user: User = Depends(dependencies.get_current_user())):
    user = await crud.user.delete(id=curr_user.id, db_session=db_session)
    return IDeleteResponseBase[IUserRead](data=user)
