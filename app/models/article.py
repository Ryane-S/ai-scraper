from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class Article(Base):
    """Modèle SQLAlchemy pour la table des articles."""
    __tablename__ = "articles"

    # Colonnes de la table
    id = Column(Integer, primary_key=True, index=True) # Clé primaire
    title = Column(String(255), index=True, nullable=False) # Titre de l'article
    url = Column(String(512), index=True, unique=True, nullable=True) # URL unique
    content = Column(Text, nullable=True) # Contenu de l'article (HTML/md brut)
    summary = Column(Text, nullable=True) # Résumé de l'article
    category = Column(String(100), nullable=True) # Catégorie de l'article
    is_fallback = Column(Boolean, nullable=False, default=False) # Si pas fetchable
    scraped_at = Column(DateTime(timezone=True), server_default=func.now()) # Date de scraping de l'article

    def __repr__(self):
        return f"<Article(id={self.id}, title={self.title}, url={self.url})>"