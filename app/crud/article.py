from sqlalchemy.orm import Session
from app.models.article import Article
from app.schemas.article import ArticleCreate

from typing import Optional

def create_article(db:Session, article_data:ArticleCreate) -> Article:
    """Méthode de création d'un article en BDD."""
    data_dict = article_data.model_dump() # Pour passer de Pydantic à SQLAlchemy
    db_article = Article(**data_dict)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_article_by_id(db:Session, article_id:int) -> Optional[Article]:
    """Méthode de lecture d'un article en particulier."""
    return db.query(Article).filter(Article.id == article_id).first()

def get_all_articles(db:Session, skip:int = 0, limit:int = 20) -> list[Article]:
    """Méthode de lecture des 20 articles les plus récents en BDD."""
    return db.query(Article).order_by(Article.scraped_at.desc()).offset(skip).limit(limit).all()