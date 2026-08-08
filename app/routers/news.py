from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.article import *
from app.schemas.article import ArticleResponse
from app.services.scraper import fetch_and_store_articles

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id:int, db:Session = Depends(get_db)):
    """Route pour obtenir un article en particulier avec son id."""
    article = get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article

@router.get("/articles", response_model=list[ArticleResponse])
def get_news(db:Session = Depends(get_db)):
    """Route pour obtenir la liste de tous les articles."""
    return get_all_articles(db)

@router.get("/scrape")
def trigger_scrape(bg_tasks: BackgroundTasks):
    """Route pour déclencher le scraper en background."""
    bg_tasks.add_task(fetch_and_store_articles)
    return {"message": "Scraping en cours... Actualisez la liste dans quelques instants."}
