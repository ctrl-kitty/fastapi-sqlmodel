from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base_sqlmodel import CRUDBase
from model.role import Role
from schema.role import IRoleCreate, IRoleUpdate


class CRUDRole(CRUDBase[Role, IRoleCreate, IRoleUpdate]):
    async def get_by_id(self, role_id: int, db_session: AsyncSession):
        return await super().get(role_id, db_session)


role = CRUDRole(Role)
