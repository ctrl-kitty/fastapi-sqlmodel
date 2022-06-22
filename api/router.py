from fastapi import APIRouter, Depends

from api import dependencies
from api.endpoints import users, login, admin
from schema.role import IRoleEnum

router = APIRouter()

router.include_router(users.router, prefix='/users', tags=['users'])
router.include_router(login.router, prefix='/login', tags=['login'])
router.include_router(admin.router, prefix='/admin', tags=['admin'],
                      dependencies=[Depends(dependencies.get_current_user(required_roles=[IRoleEnum.admin]))])
