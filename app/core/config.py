from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Métadonnées (avec valeurs par défaut)
    app_name: str = "AI News Scraper"
    version: str = "0.1.0"
    description: str = "Un scraper d'actualité IA avec résumé automatique"
    
    # Connexion BDD 
    DATABASE_URL: str

    # Clé de lancement du scraper
    SCRAPE_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings() # type: ignore[call-arg]