from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine, Base
from app.models.article import Article
from app.routers import health, news

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description
)

app.include_router(health.router)
app.include_router(news.router)

@app.get("/")
def root():
    return {"name": settings.app_name, "version": settings.version, "docs": "/docs"}
