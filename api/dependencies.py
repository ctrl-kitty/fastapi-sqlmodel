from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sql.session import SessionLocal



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
