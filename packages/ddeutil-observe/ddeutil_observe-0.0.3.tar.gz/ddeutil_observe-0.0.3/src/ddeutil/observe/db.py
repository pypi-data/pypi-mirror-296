# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import MetaData, event

# from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

# from sqlalchemy.orm import Session
from .conf import config
from .utils import get_logger

logger = get_logger("ddeutil.observe")


class DatabaseManageException(Exception): ...


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Read more:
    - https://docs.sqlalchemy.org/en/20/dialects/sqlite.html -
        #foreign-key-support
    """
    cursor = dbapi_connection.cursor()
    settings: dict[str, Any] = {
        # "journal_mode": "WAL",
        "journal_mode": "OFF",
        "foreign_keys": "ON",
        "page_size": 4096,
        "cache_size": 10000,
        # "locking_mode": 'EXCLUSIVE',
        # "synchronous": "NORMAL",
        "synchronous": "OFF",
    }
    for k, v in settings.items():
        cursor.execute(f"PRAGMA {k} = {v};")
    cursor.close()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    conn.info.setdefault("query_start_time", []).append(time.time())
    if config.LOG_SQLALCHEMY_DEBUG_MODE:
        logger.debug("Start Query: %s", statement)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    if config.LOG_SQLALCHEMY_DEBUG_MODE:
        total = time.time() - conn.info["query_start_time"].pop(-1)
        logger.debug("Query Complete! Total Time: %f", total)


# @event.listens_for(Session, "before_commit")
# def before_commit(session):
#     logger.debug(f"before commit: {session.info}")
#     session.info["before_commit_hook"] = "yup"
#
#
# @event.listens_for(Session, "after_commit")
# def after_commit(session):
#     logger.debug(
#         f"before commit: {session.info['before_commit_hook']}, "
#         f"after update: {session.info.get('after_update_hook', 'null')}"
#     )


class DBSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(
            host,
            echo=False,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False},
        )
        self._sessionmaker = async_sessionmaker(
            autoflush=False,
            autocommit=False,
            future=True,
            expire_on_commit=False,
            bind=self._engine,
        )

    def is_opened(self) -> bool:
        return self._engine is not None

    async def close(self):
        if self._engine is None:
            raise DatabaseManageException(
                "DatabaseSessionManager is not initialized"
            )
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DatabaseManageException(
                "DatabaseSessionManager is not initialized"
            )

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseManageException(
                "DatabaseSessionManager is not initialized"
            )

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @staticmethod
    async def create_all(connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_all(connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DBSessionManager()


DB_INDEXES_NAMING_CONVENTION: dict[str, str] = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


# NOTE:
#       Attributes that are lazy-loading relationships, deferred columns or
#   expressions, or are being accessed in expiration scenarios can take
#   advantage of the AsyncAttrs mixin.
#   Read more: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html -
#       #preventing-implicit-io-when-using-asyncsession
#
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=DB_INDEXES_NAMING_CONVENTION,
        # NOTE: In SQLite schema, the value should be `main` only because it
        #   does not implement with schema system.
        schema="main",
    )

    def __repr__(self) -> str:
        columns = ", ".join(
            [
                f"{k}={repr(v)}"
                for k, v in self.__dict__.items()
                if not k.startswith("_")
            ]
        )
        return f"<{self.__class__.__name__}({columns})>"


# NOTE: Alias function of the SQLAlchemy for shorter name.
Col = mapped_column
Dtype = Mapped


# @event.listens_for(Base, "after_update")
# def after_update(mapper, connection, target):
#     session = inspect(target).session
#     session.info["after_update_hook"] = "yup"
