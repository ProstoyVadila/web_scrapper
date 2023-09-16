from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException
from loguru import logger

from models import SiteIn, SiteOut, convert_site_in
from broker import rabbit_broker, URLS_TO_CRAWL_EXCHANGE, URLS_TO_CRAWL_QUEUE
from database import Database, save_site_in_transaction


async def process_new_site(site: SiteIn, db: Database):
    try:
        logger.info("add site %s to queue", site.url)
        await rabbit_broker.publish(
            exchange=URLS_TO_CRAWL_EXCHANGE,
            queue=URLS_TO_CRAWL_QUEUE,
            message=site.json(),
            persist=True,
        )

        logger.info("add site %s to database", site.url)
        async with db._con_pool.acquire() as con:
            await save_site_in_transaction(con, site)
            return site
    except UniqueViolationError as exc:
        logger.exception(exc)
        raise HTTPException(400, "Site already added")
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(400, "Bad Request")


async def process_new_sites(sites: list[SiteIn], db: Database):
    logger.info("add sites to queue and database", sites)
    for site in sites:
        await process_new_site(site)
    # await db.add_sites(sites)
