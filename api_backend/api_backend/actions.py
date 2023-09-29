import orjson
from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException

from api_backend.logger import log
from api_backend.models import SiteIn, SiteOut, convert_site_in, TestSite, into_borsh
from api_backend.broker import (
    rabbit_broker,
    URLS_TO_CRAWL_EXCHANGE,
    URLS_TO_CRAWL_QUEUE,
)
from api_backend.database import Database, save_site_in_transaction


async def process_new_site(site: SiteIn, db: Database):
    try:
        log.info("add site %s to database", site.url)
        async with db._con_pool.acquire() as con:
            res = await save_site_in_transaction(con, site)
            if not res:
                raise UniqueViolationError

        log.info("add site %s to queue", site.url)
        # data = TestSite(url=site.url).dict()
        # data = into_borsh(data)
        data = orjson.dumps(
            {
                "event_id": site.id,
                "url": site.url,
                "user_id": "1",
                "is_pagination": False,
                "refresh_interval": 3600,
                "xpaths": {
                    "title": "//h1/span",
                    "description": "//div[@class='hatnote navigation-not-searchable']",
                },
            }
        )

        await rabbit_broker.publish(
            # exchange=URLS_TO_CRAWL_EXCHANGE,
            # queue=URLS_TO_CRAWL_QUEUE,
            exchange="scrapper_in",
            queue="scrapper_in",
            message=data,
            persist=True,
        )

        # Tets extractor TODO: remove this after testing
        # await rabbit_broker.publish(
        #     exchange="extractor_in",
        #     queue="extractor_in",
        #     message=data,
        #     persist=True,
        # )
        return res

    except UniqueViolationError as exc:
        log.exception("Site already added", exc_info=exc)
        raise HTTPException(400, "Site already added")

    except Exception as exc:
        log.exception("Error while saving to db", exc_info=exc)
        raise HTTPException(400, "Bad Request")


async def process_new_sites(sites: list[SiteIn], db: Database):
    log.info("add sites to queue and database", sites)
    for site in sites:
        await process_new_site(site)
    # await db.add_sites(sites)
