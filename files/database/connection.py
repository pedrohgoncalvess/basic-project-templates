"""This module provides the connection to a database
PostgreSQL. Check the .env file and make sure that
the credentials are correct in the correct places.
"""
import psycopg
from psycopg import connection

from logs.config import logger
from utils.env_var import get_env_var


class PgConnection:
    def __init__(self):
        self._host_ = get_env_var('PG_HOST')
        self._port_ = get_env_var('PG_PORT')
        self._user_ = get_env_var('PG_USER')
        self._password_ = get_env_var('PG_PASSWORD')
        self._db_name_ = get_env_var('PG_NAME')
        try:
            self._connection_: connection = psycopg.connect(
                host=self._host_,
                port=self._port_,
                user=self._user_,
                password=self._password_,
                dbname=self._db_name_
            )
            self.cursor = self._connection_.cursor()
        except Exception as error:
            logger.error(f"Error while connecting to database. {error}")

    def __enter__(self):
        logger.info(f"New connection. ID: {self._connection_.fileno()}")
        return self._connection_

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Closed connection. ID: {self._connection_.fileno()}")
        self._connection_.commit()
        return self._connection_.close()