from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import make_url
from alembic import context

from database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

target_metadata = Base.metadata


def run_migrations_for_url(url: str):
    connectable = engine_from_config(
        {"sqlalchemy.url": url}, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    base_url = os.getenv("DATABASE_URL", "sqlite:///mall_gamification.db")
    shard_count = int(os.getenv("SHARD_COUNT", "1"))
    url = make_url(base_url)
    if shard_count == 1:
        run_migrations_for_url(str(url))
    else:
        for shard in range(shard_count):
            if url.database:
                shard_url = url.set(database=f"{url.database}_shard{shard}")
            else:
                shard_url = url
            run_migrations_for_url(str(shard_url))


if context.is_offline_mode():
    raise RuntimeError("Offline migrations are not supported")
else:
    run_migrations_online()
