from datetime import datetime
from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    """Schema de base pour un article."""
    title: str = Field(..., min_length=1, max_length=255, description="Titre de l'article")
    url: str = Field(..., min_length=10, max_length=512, description="Url de l'article")
    content: str|None = Field(default=None, min_length=1, description="Contenu de l'article")
    summary: str|None = Field(default=None, min_length=1, description="Résumé de l'article")

class ArticleCreate(ArticleBase):
    """Schema de base pour créer un article."""

class ArticleResponse(ArticleBase):
    id: int
    scraped_at: datetime # Puisque la BDD a un server_default=func.now(), il y aura toujours une date.

    class Config:
        from_attributes = True # Conversion SQLAlchemy -> Pydantic
