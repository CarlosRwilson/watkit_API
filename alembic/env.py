import asyncio
from logging.config import fileConfig
import os 
import sys

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.infraestructure.database.models import Base
from sqlalchemy.ext.asyncio import create_async_engine

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))



#objeto de configuracion de alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)



target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url = url,
        target_metadata = target_metadata,
        literal_binds = True,
        dialect_opts= {"paramstyle": "pyformat"}
    )
    with context.begin_transaction():
        context.run_migrations()
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    config_section = config.get_section(config.config_ini_section, {})
    url = config_section.get("sqlalchemy.url") or config.get_main_option("sqlalchemy.url")
    print(config_section)
    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


