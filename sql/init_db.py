from sqlalchemy.future import Engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from model.role import Role
from model.user import User


# todo подумать над добавлением дебаг информации
async def create_database_structure(sync_engine: Engine) -> None:
    SQLModel.metadata.create_all(sync_engine)


# todo insert init data
async def create_initial_data(session: AsyncSession) -> None:
    print('pass')
