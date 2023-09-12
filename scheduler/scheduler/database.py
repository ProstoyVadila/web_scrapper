from loguru import logger
from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.orm import Session

from models import Site
from config import get_config

conf = get_config()
session = FastAPISessionMaker(conf.postgres.pg_url)


async def add_site(db: Session, site: Site):
    logger.info("adding site {} to database".format(site.url))
    pass


async def add_sites(db: Session, sites: list[Site]):
    pass


async def get_sites_to_update(db: Session) -> list[Site]:
    logger.info("getting sites from database to recrawl")
    pass
