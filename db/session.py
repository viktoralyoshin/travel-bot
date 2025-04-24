from db.config import DatabaseConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


config = DatabaseConfig()
engine = create_async_engine(config.async_db_url, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
) 

async def get_db() -> AsyncSession:
    return AsyncSessionLocal()