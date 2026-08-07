
from sqlalchemy.orm import Session

from app.models.article import Article
from app.schemas.article import ArticleCreate


def create_article(db:Session, article_data:ArticleCreate) -> Article:
    """Méthode de création d'un article en BDD."""
    data_dict = article_data.model_dump() # Pour passer de Pydantic à SQLAlchemy
    db_article = Article(**data_dict)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def article_in_db(db:Session, article_url:str) -> bool:
    """Méthode vérifiant la présence d'un article dans la Bdd."""
    return db.query(Article).filter(Article.url == article_url).first() is not None

def get_article_by_id(db:Session, article_id:int) -> Article | None:
    """Méthode de lecture d'un article en particulier."""
    return db.query(Article).filter(Article.id == article_id).first()

def get_all_articles(db:Session, skip:int = 0, limit:int = 20) -> list[Article]:
    """Méthode de lecture des 20 articles les plus récents en BDD."""
    return db.query(Article).order_by(Article.scraped_at.desc()).offset(skip).limit(limit).all()

def delete_article(db:Session, article_id:int) -> bool:
    """Méthode qui supprime un article de la BDD."""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return False
    db.delete(article)
    db.commit()
    return True

def delete_all_articles(db:Session) -> int:
    """Méthode pour supprimer tous les articles de la BDD."""
    deleted_count = db.query(Article).delete()
    db.commit()
    return deleted_count