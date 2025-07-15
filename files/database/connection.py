"""
Asynchronous PostgreSQL Database Connection Module

This module provides an async connection wrapper for PostgreSQL databases using psycopg3.
It handles connection management, automatic resource cleanup, and supports both context
manager and manual connection patterns.

The module automatically configures the event loop policy for Windows compatibility
and retrieves database credentials from environment variables.

Environment Variables Required:
    PG_HOST: PostgreSQL server hostname or IP address
    PG_PORT: PostgreSQL server port (typically 5432)
    PG_USER: Database username
    PG_PASSWORD: Database user password
    PG_NAME: Database name to connect to

Example Usage:
    Basic usage with context manager (recommended):

    async def main():
        async with PgConnection() as db:
            await db.cursor.execute("SELECT version()")
            result = await db.cursor.fetchone()
            print(f"PostgreSQL version: {result[0]}")


    Manual connection management:

    async def main():
        db = PgConnection()
        await db.connect()

        try:
            await db.cursor.execute("SELECT * FROM users WHERE id = %s", (1,))
            user = await db.cursor.fetchone()
            print(f"User: {user}")
        finally:
            await db.close()

Note:
    Ensure your .env file contains all required PostgreSQL credentials before using
    this module. The connection will automatically commit transactions and close
    properly when used as a context manager.
"""
import asyncio
import sys

import psycopg
from psycopg import AsyncConnection, AsyncCursor

from log import logger
from utils import get_env_var


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class PgConnection:
    def __init__(self):
        self._host_ = get_env_var("PG_HOST")
        self._port_ = get_env_var("PG_PORT")
        self._user_ = get_env_var("PG_USER")
        self._password_ = get_env_var("PG_PASSWORD")
        self._db_name_ = get_env_var("PG_NAME")
        self._connection_: AsyncConnection | None = None
        self.cursor: AsyncCursor | None = None

    async def connect(self):
        try:
            self._connection_ = await psycopg.AsyncConnection.connect(
                host=self._host_,
                port=self._port_,
                user=self._user_,
                password=self._password_,
                dbname=self._db_name_
            )
            self.cursor = self._connection_.cursor()
            await logger.info("Database", "Connection", f"New. ID: {self._connection_.fileno()}")
        except Exception as error:
            await logger.error("Database", f"Error while connecting: {error}")

    async def close(self):
        if self._connection_:
            logger.info("Database", "Connection", f"Closed. ID: {self._connection_.fileno()}")
            await self._connection_.commit()
            await self._connection_.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
