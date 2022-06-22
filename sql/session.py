from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from core.config import settings


async def get_sync_engine() -> Engine:
    return create_engine(settings.SYNC_DATABASE_URI, echo=settings.DEBUG, future=True)


engine = create_async_engine(settings.ASYNC_DATABASE_URI, echo=settings.DEBUG, future=True,
                             max_overflow=64)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False)
