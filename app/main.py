import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import health, news
from app.services.scheduler import shutdown_scheduler, start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage du scheduler
    start_scheduler()
    yield
    # Arrêt du scheduler
    shutdown_scheduler()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(health.router)
app.include_router(news.router)

@app.get("/")
def serve_front():
    return FileResponse("app/static/index.html")
