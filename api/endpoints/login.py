from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

import crud
from api import dependencies
from core import security
from core.config import settings
from schema.token import TokenRead

router = APIRouter()


@router.post("/access-token", response_model=TokenRead)
async def login_access_token(
        db_session: AsyncSession = Depends(dependencies.get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user_id = await crud.user.authenticate(user_email=form_data.username,
                                           user_password_raw=form_data.password,
                                           db_session=db_session)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": await security.create_access_token(
            user_id, expires_delta=access_token_expires
        )
    }
