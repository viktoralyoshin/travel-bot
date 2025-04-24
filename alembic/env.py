from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from alembic import context
import asyncio

from db.db import DATABASE_URL
from db.models import Base


# Конфигурация Alembic
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Создаём async engine
engine = create_async_engine(DATABASE_URL, echo=True)

async def run_migrations():
    async with engine.begin() as conn:  # Важно: await внутри
        await conn.run_sync(do_run_migrations)

def do_run_migrations(sync_connection):
    context.configure(connection=sync_connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    asyncio.run(run_migrations())

run_migrations_online()