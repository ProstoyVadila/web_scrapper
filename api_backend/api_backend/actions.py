import orjson
from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException
from loguru import logger

from models import SiteIn, SiteOut, convert_site_in, TestSite, into_borsh
from broker import rabbit_broker, URLS_TO_CRAWL_EXCHANGE, URLS_TO_CRAWL_QUEUE
from database import Database, save_site_in_transaction


async def process_new_site(site: SiteIn, db: Database):
    try:
        logger.info("add site %s to database", site.url)
        async with db._con_pool.acquire() as con:
            res = await save_site_in_transaction(con, site)
            if not res:
                raise UniqueViolationError

        logger.info("add site %s to queue", site.url)
        # data = TestSite(url=site.url).dict()
        # data = into_borsh(data)

        # await rabbit_broker.publish(
        #     exchange=URLS_TO_CRAWL_EXCHANGE,
        #     queue=URLS_TO_CRAWL_QUEUE,
        #     message=data,
        #     persist=True,
        # )

        # Tets extractor TODO: remove this after testing
        data = orjson.dumps(
            {
                "html": "<kek>kek</kek>",
                "url": site.url,
                "xpaths": {
                    "title": "//title/text()",
                    "description": "//meta[@name='description']/@content",
                }
            }
        )
        await rabbit_broker.publish(
            exchange="extractor_in",
            queue="extractor_in",
            message=data,
            persist=True,
        )
        return res

    except UniqueViolationError as exc:
        logger.exception("Site already added", exc_info=exc)
        raise HTTPException(400, "Site already added")

    except Exception as exc:
        logger.exception("Error while saving to db", exc_info=exc)
        raise HTTPException(400, "Bad Request")


async def process_new_sites(sites: list[SiteIn], db: Database):
    logger.info("add sites to queue and database", sites)
    for site in sites:
        await process_new_site(site)
    # await db.add_sites(sites)
