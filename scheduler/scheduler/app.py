import asyncio
from loguru import logger

from aiormq import AMQPConnectionError
from fastapi import FastAPI, BackgroundTasks


from models import Site
from broker import rabbit_broker, AMQP_CONNECTION_ERROR_INTERVAL
from actions import process_new_site, process_new_sites


app = FastAPI(
    title="Scheduler",
    version="0.0.1",
    description="Scheduler service manages the whole crawling process",
    # lifespan=rabbit_router.lifespan_context,
)


@app.on_event("startup")
async def on_startup():
    logger.info("Starting scheduler's worker")
    while True:
        try:
            await rabbit_broker.connect()
            break
        except AMQPConnectionError:
            logger.error("RabbitMQ is not ready, retrying in 5 seconds")
            await asyncio.sleep(AMQP_CONNECTION_ERROR_INTERVAL)
        # TODO: fix this
        except KeyboardInterrupt:
            logger.info("Stopping scheduler")
            break


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Stopping scheduler's worker")
    await rabbit_broker.close()


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
