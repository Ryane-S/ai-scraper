import feedparser
from dateutil import parser

from app.core.database import SessionLocal
from app.crud.article import article_in_db, create_article
from app.schemas.article import ArticleCreate
from app.services.summarizer import summarize_article
from app.services.utils import extract_full_article


def fetch_and_store_articles() -> None:
    """Fetch les nouveaux articles, les traite et les stocke en BDD."""
    URLS = ["https://techcrunch.com/category/artificial-intelligence/feed/"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    
    db = SessionLocal()
    try:
        for URL in URLS:
            # On lit le flux RSS
            feed = feedparser.parse(URL, request_headers=headers)

            # On extrait les articles
            for entry in feed.entries:
                # On extrait les différentes composantes de l'article
                title = entry.get('title') # Titre
                link = entry.get('link') # URL
                description = entry.get('description') # Description
                pubDate = None # Date de publication
                if hasattr(entry, 'published'):
                                    try:
                                        pubDate = parser.parse(entry.published)
                                    except (ValueError, TypeError):
                                        # Si la date est mal formée, on laisse None
                                        pass

                # On vérifie si l'objet existe déjà en BDD
                if article_in_db(db, link):
                    continue
                # Sinon on le crée et on l'insère
                else:
                    # On récupère l'HTML brut de l'article et une image d'illustration
                    article = extract_full_article(link)
                    article_content = article["content"]
                    image_url = article["image"]
                    # On génère un résumé de l'article
                    article_summary = summarize_article(article_content=article_content)
                    # On enregistre l'article dans la BDD
                    article_data = ArticleCreate(
                        title = title,
                        url = link,
                        description = description,
                        image_url= image_url,
                        content = article_content,
                        summary = article_summary,
                        date = pubDate
                    )
                    create_article(db, article_data)

    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()
