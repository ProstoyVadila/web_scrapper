import asyncpg
from loguru import logger

from config import PostgresConfig


class Database:
    MIN_SIZE = 1
    MAX_SIZE = 10
    COMMAND_TIMEOUT = 60
    STATEMENT_TIMEOUT = 60
    INACATIVE_LIFETIME = 300

    def __init__(self, config: PostgresConfig) -> None:
        self.config = config
        self._cursor = None
        self._con_pool = None
        self._con = None

    async def connect(self):
        if not self._con_pool:
            try:
                self._con_pool = await asyncpg.create_pool(
                    host=self.config.host,
                    port=self.config.port,
                    user=self.config.user,
                    password=self.config.password,
                    database=self.config.db_name,
                    min_size=self.MIN_SIZE,
                    max_size=self.MAX_SIZE,
                    command_timeout=self.COMMAND_TIMEOUT,
                    max_inactive_connection_lifetime=self.INACATIVE_LIFETIME,
                )
                logger.info("Connected to database")
            except Exception as exc:
                logger.exception(exc)

    async def close(self):
        if self._con_pool:
            try:
                await self._con_pool.close()
                logger.info("Closed database connection")
            except Exception as exc:
                logger.exception(exc)

    async def fetch_rows(self, query: str):
        if not self._con_pool:
            await self.connect()
        self._con = await self._con_pool.acquire()
        try:
            return await self._con.fetch(query)
        except Exception as exc:
            logger.exception(exc)
        finally:
            await self._con_pool.release(self._con)


db = Database(PostgresConfig())
