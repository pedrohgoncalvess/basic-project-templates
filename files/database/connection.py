"""This module provides an async connection to a PostgreSQL database.
Check the .env file and ensure credentials are correctly set.
"""

import psycopg
from psycopg import AsyncConnection, AsyncCursor

from log.config import logger
from utils.env_var import get_env_var


class PgConnection:
    def __init__(self):
        self._host_ = get_env_var('PG_HOST')
        self._port_ = get_env_var('PG_PORT')
        self._user_ = get_env_var('PG_USER')
        self._password_ = get_env_var('PG_PASSWORD')
        self._db_name_ = get_env_var('PG_NAME')
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
            self.cursor = await self._connection_.cursor()
            logger.info(f"New connection. ID: {self._connection_.fileno()}")
        except Exception as error:
            logger.error(f"Error while connecting to database: {error}")

    async def close(self):
        if self._connection_:
            logger.info(f"Closed async connection. ID: {self._connection_.fileno()}")
            await self._connection_.commit()
            await self._connection_.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
