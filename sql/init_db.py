from datetime import datetime

from sqlalchemy.future import Engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core import config
from core.security import get_password_hash
from model.role import Role
from model.user import User


# todo подумать над добавлением дебаг информации
async def create_database_structure(sync_engine: Engine) -> None:
    SQLModel.metadata.create_all(sync_engine)


# todo insert init data
async def create_initial_data(session: AsyncSession) -> None:
    default_role = Role(name="user", description="Default role for all users")
    admin_role = Role(name="admin", description="Role for admin staff")
    session.add(default_role)
    session.add(admin_role)
    await session.commit()
    await session.refresh(admin_role)
    print("Base roles added")
    print("Adding first user...")
    first_user = User(
        first_name="First",
        last_name="User",
        email=config.settings.FIRST_SUPERUSER_EMAIL,
        is_superuser=True,
        hashed_password=await get_password_hash(config.settings.FIRST_SUPERUSER_PASSWORD),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        role_id=admin_role.id)
    session.add(first_user)
    await session.commit()
    print("First user added")
