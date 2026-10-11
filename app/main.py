from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import Base, engine
from app.services.scheduler import start_scheduler, shutdown_scheduler
from app.routers import health, news

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
