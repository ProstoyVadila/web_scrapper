from loguru import logger
from fastapi import FastAPI, BackgroundTasks, Request

from models import Site
from broker import rabbit_broker, init_broker
from actions import process_new_site, process_new_sites
from database import db


app = FastAPI(
    title="API Backend",
    version="0.0.1",
    description="API Backend to set up sites to parse and check their statuses",
    # lifespan=rabbit_router.lifespan_context,
)


@app.on_event("startup")
async def on_startup():
    logger.info("Starting api backend's worker")
    await db.connect()
    app.state.db = db
    await init_broker()


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Stopping api backend's worker")
    await rabbit_broker.close()
    if app.state.db:
        await app.state.db.close()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/site")
async def add_site(site: Site, background_tasks: BackgroundTasks):
    logger.info("add site {} to queue".format(site.url))
    background_tasks.add_task(process_new_site, site)
    return {"message": "add site {} to queue and database".format(site.url)}


@app.post("/sites")
async def add_sites(sites: list[Site], background_tasks: BackgroundTasks):
    background_tasks.add_task(process_new_sites, sites)
    return {"message": "add sites to queue and database"}
