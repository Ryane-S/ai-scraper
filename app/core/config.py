from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Métadonnées (avec valeurs par défaut)
    app_name: str = "SIFT - News Scraper & Summarizer"
    version: str = "0.1.0"
    description: str = "Un scraper d'actualité avec résumé automatique"

    # Paramètres du scheduler
    DISABLE_SCHEDULER: bool = False
    SCRAPE_HOUR: int = 2
    CLEANUP_HOUR: int = 4
    CLEANUP_DAYS_OLD: int = 7
    
    # Connexion BDD 
    DATABASE_URL: str

    # Clé de lancement du scraper
    SCRAPE_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings() # type: ignore[call-arg]