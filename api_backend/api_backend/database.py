import asyncpg
import orjson

from api_backend.logger import log
from api_backend.config import PostgresConfig
from api_backend.models import SiteModel, PageModel, SiteIn, convert_site_in


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
                log.info("Connected to database")
            except Exception as exc:
                log.exception(exc)

    async def close(self):
        if self._con_pool:
            try:
                await self._con_pool.close()
                log.info("Closed database connection")
            except Exception as exc:
                log.exception(exc)

    async def _fetch_rows(self, query: str):
        if not self._con_pool:
            await self.connect()
        self._con = await self._con_pool.acquire()
        try:
            return await self._con.fetch(query)
        except Exception as exc:
            log.exception(exc)
        finally:
            await self._con_pool.release(self._con)

    async def _execute(self, query: str):
        if not self._con_pool:
            await self.connect()
        self._con = await self._con_pool.acquire()
        try:
            return await self._con.execute(query)
        except Exception as exc:
            log.exception(exc)
        finally:
            await self._con_pool.release(self._con)


def transaction_wrapper(db: Database):
    async def wrapper(func, *args, **kwargs):
        async with db._con_pool.acquire() as con:
            async with con.transaction():
                await func(con, *args, **kwargs)

    return wrapper


async def get_site_by_domain(con, domain: str):
    query = """
        SELECT * FROM sites WHERE domain = $1
    """
    site = await con.fetchrow(query, domain)
    if not site:
        return
    return SiteModel(**dict(site))


async def get_page_by_url(con, url: str):
    query = """
        SELECT * FROM pages WHERE url = $1
    """
    data = await con.fetchrow(query, url)
    if not data:
        return
    page = dict(data)
    page["xpaths"] = orjson.loads(page["xpaths"])
    return PageModel(**page)


# async def get_site_info(con, siteIn):
#     site = await get_site_by_domain(con, siteIn.domain)
#     if not site:
#         return
#     return SiteModel(**site)


async def save_site(con, site: SiteModel) -> SiteModel:
    site = await con.fetchrow(
        """
        INSERT INTO sites (id, domain, created_at) VALUES ($1 , $2, $3) returning *
        """,
        site.id,
        site.domain,
        site.created_at,
    )
    log.debug(f"saved site {site}")
    return SiteModel(**dict(site))


async def save_page(con, page: PageModel) -> PageModel:
    data = await con.fetchrow(
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
    log.debug(f"saved page {data}")
    data = dict(data)
    data["xpaths"] = orjson.loads(data["xpaths"])
    return PageModel(**data)


async def save_site_in_transaction(con, site: SiteIn) -> PageModel:
    site, page = convert_site_in(site)
    async with con.transaction():
        page_from_db = await get_page_by_url(con, page.url)
        if page_from_db:
            return

        site_from_db = await get_site_by_domain(con, site.domain)
        if site_from_db:
            site.id = site_from_db.id
            page.site_id = site_from_db.id

        if not site_from_db:
            await save_site(con, site)

        page = await save_page(con, page)
        return page


db = Database(PostgresConfig())
