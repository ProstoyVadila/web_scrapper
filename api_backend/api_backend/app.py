from fastapi import FastAPI, BackgroundTasks, Request, APIRouter, HTTPException

from api_backend.models import SiteIn
from api_backend.broker import rabbit_broker, init_broker
from api_backend.actions import process_new_site, process_new_sites
from api_backend.database import db
from api_backend.logger import log

router = APIRouter()
app = FastAPI(
    title="API Backend",
    version="0.0.1",
    description="API Backend to set up sites to parse and check their statuses",
    # lifespan=rabbit_router.lifespan_context,
)


@app.on_event("startup")
async def on_startup():
    log.info("Starting api backend's worker")
    await db.connect()
    app.state.db = db
    await init_broker()


@app.on_event("shutdown")
async def on_shutdown():
    log.info("Stopping api backend's worker")
    await rabbit_broker.close()
    if app.state.db:
        await app.state.db.close()


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@router.post("/site")
async def add_site(req: Request, site: SiteIn):
    log.info("add site {} to queue".format(site.url))
    site_out = await process_new_site(site, req.app.state.db)
    return site_out


@router.post("/sites")
async def add_sites(
    req: Request, sites: list[SiteIn], background_tasks: BackgroundTasks
):
    background_tasks.add_task(process_new_sites, sites, req.app.state.db)
    return {"data": "add sites to queue and database"}


app.include_router(router, prefix="/api/v1")
