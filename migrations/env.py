import asyncio
from logging.config import fileConfig
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.models.base_model import Base  # твой Base
from app.core.config import settings
from app.models import *
# Подключаем метаданные для автогенерации миграций
target_metadata = Base.metadata

# Alembic Config
config = context.config

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# --- Offline режим ---
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --- Online режим ---
def run_migrations_online() -> None:
    """Run migrations in 'online' mode using AsyncEngine."""

    connectable = create_async_engine(
        settings.DB_URL,
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:

            # Настраиваем Alembic через run_sync
            def sync_migrate(sync_conn):
                context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                    compare_type=True,  # автоизменения типа колонок
                )
                with context.begin_transaction():
                    context.run_migrations()

            await connection.run_sync(sync_migrate)

    asyncio.run(do_run_migrations())


# --- Выбор режима ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
