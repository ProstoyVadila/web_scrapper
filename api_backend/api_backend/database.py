import asyncpg
from loguru import logger

from config import PostgresConfig
from models import SiteModel, PageModel, SiteIn, convert_site_in


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

    async def _fetch_rows(self, query: str):
        if not self._con_pool:
            await self.connect()
        self._con = await self._con_pool.acquire()
        try:
            return await self._con.fetch(query)
        except Exception as exc:
            logger.exception(exc)
        finally:
            await self._con_pool.release(self._con)

    async def _execute(self, query: str):
        if not self._con_pool:
            await self.connect()
        self._con = await self._con_pool.acquire()
        try:
            return await self._con.execute(query)
        except Exception as exc:
            logger.exception(exc)
        finally:
            await self._con_pool.release(self._con)


def transaction_wrapper(db: Database):
    async def wrapper(func, *args, **kwargs):
        async with db._con_pool.acquire() as con:
            async with con.transaction():
                await func(con, *args, **kwargs)

    return wrapper


async def save_site_in_transaction(con, site: SiteIn):
    site, page = convert_site_in(site)
    async with con.transaction():
        await con.execute(
            """
            INSERT INTO sites (id, domain, created_at) VALUES ($1 , $2, $3)
            """,
            site.id,
            site.domain,
            site.created_at,
        )
        return await con.execute(
            """
            INSERT INTO pages (
                id, site_id, url, created_at, updated_at,
                status, is_pagination, refresh_interval,
                refresh_at, last_refresh, xpaths)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) returning *
            """,
            page.id,
            page.site_id,
            page.url,
            page.created_at,
            page.updated_at,
            page.status,
            page.is_pagination,
            page.refresh_interval,
            page.refresh_at,
            page.last_refresh_at,
            page.xpaths_json,
        )


db = Database(PostgresConfig())
