from loguru import logger

from models import Site
from broker import rabbit_broker, URLS_TO_CRAWL_EXCHANGE, URLS_TO_CRAWL_QUEUE
from database import add_site, add_sites


async def process_new_site(site: Site):
    logger.info("add site %s to queue", site.url)
    await rabbit_broker.publish(
        exchange=URLS_TO_CRAWL_EXCHANGE,
        queue=URLS_TO_CRAWL_QUEUE,
        message=site.json(),
        persist=True,
    )

    logger.info("add site %s to database", site.url)
    await add_site(site)


async def process_new_sites(sites: list[Site]):
    logger.info("add sites to queue and database", sites)
    for site in sites:
        await rabbit_broker.publish(
            exchange=URLS_TO_CRAWL_EXCHANGE,
            queue=URLS_TO_CRAWL_QUEUE,
            message=site.json(),
            persist=True,
        )
    await add_sites(sites)
