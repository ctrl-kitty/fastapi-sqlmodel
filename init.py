import asyncio
import logging
from sql.init_db import create_initial_data, create_database_structure
from sql.session import SessionLocal, get_sync_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_init_data() -> None:
    async with SessionLocal() as session:
        await create_initial_data(session)


async def create_db_structure() -> None:
    engine = await get_sync_engine()
    await create_database_structure(engine)


async def main() -> None:
    logger.info("Creating database structure")
    await create_db_structure()
    logger.info("Database structure created!")
    logger.info("Creating initial data")
    await create_init_data()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
