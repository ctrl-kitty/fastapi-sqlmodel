from sqlmodel.ext.asyncio.session import AsyncSession

from crud.base_sqlmodel import CRUDBase
from model.role import Role
from model.user import User
from schema.role import IRoleCreate, IRoleUpdate


class CRUDRole(CRUDBase[Role, IRoleCreate, IRoleUpdate]):
    async def add_role_to_user(self, db_session: AsyncSession, user: User, role_id: int) -> Role:
        role_obj = await super().get(id=role_id, db_session=db_session)
        role_obj.users.append(user)
        db_session.add(role_obj)
        await db_session.commit()
        await db_session.refresh(role_obj)
        return role_obj


role = CRUDRole(Role)
