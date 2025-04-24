from sqlalchemy.ext.asyncio import create_async_engine

from db.config import DatabaseConfig
from db.models import Base

async def init_models():
    config = DatabaseConfig()
    engine = create_async_engine(config.async_db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()