import feedparser
from dateutil import parser

from app.core.database import SessionLocal
from app.crud.article import article_in_db, create_article
from app.schemas.article import ArticleCreate

def fetch_and_store_articles():
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
                    article_data = ArticleCreate(
                        title = title,
                        url = link,
                        description = description,
                        content = None,
                        summary = None,
                        date = pubDate
                    )
                    create_article(db, article_data)

    except Exception as e:
        db.rollback()
        print(e)
    finally:
        db.close()
