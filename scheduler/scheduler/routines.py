from loguru import logger
from fastapi_utils.tasks import repeat_every

from database import session, get_sites_to_update
from actions import process_new_site

PROCESS_OLD_SITES_INTERVAL = 10 * 60 * 60  # 10 hours


@repeat_every(seconds=PROCESS_OLD_SITES_INTERVAL)
async def process_old_sites():
    logger.info("Recrawling old sites from db")
    # with session.context_session() as db:
    #     sites = await get_sites_to_update(db)
    # for site in sites:
    #     await process_new_site(site)
    pass
