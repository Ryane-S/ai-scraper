from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Métadonnées (avec valeurs par défaut)
    app_name: str = "AI News Scraper"
    version: str = "0.1.0"
    description: str = "Un scraper d'actualité IA avec résumé automatique"
    
    # Connexion BDD (obligatoire - Pydantic va lever une erreur si absent du .env)
    DATABASE_URL: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()