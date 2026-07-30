from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.article import *
from app.schemas.article import ArticleResponse

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id:int, db:Session = Depends(get_db)):
    """Route pour obtenir un article en particulier avec son id."""
    article = get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Artile non trouvé")
    return article

@router.get("/articles", response_model=list[ArticleResponse])
def get_news(db:Session = Depends(get_db)):
    """Route pour obtenir tous les articles."""
    return get_all_articles(db)
