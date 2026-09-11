import time
import feedparser
from dateutil import parser

from app.core.database import SessionLocal
from app.crud.article import article_in_db, create_article
from app.schemas.article import ArticleCreate
from app.services.summarizer import summarize_article
from app.services.utils import extract_full_article


def fetch_and_store_articles() -> None:
    """Fetch les nouveaux articles, les traite et les stocke en BDD."""
    URLS = [
        {"name": "TechCrunch", "url":"https://techcrunch.com/category/artificial-intelligence/feed/"},
        {"name": "HackerNews", "url":"https://hnrss.org/newest?points=100"},
        {"name": "Science Daily", "url":"https://www.sciencedaily.com/rss/all.xml"},
        {"name": "FranceInfo", "url":"https://www.franceinfo.fr//politique.rss"},
        {"name": "The Guardian", "url":"https://www.theguardian.com/world/rss"}
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
    
    db = SessionLocal()
    try:
        nb_added_articles = 0
        for URL in URLS:
            try:
                # On lit le flux RSS
                feed = feedparser.parse(URL["url"], request_headers=headers)

                # On extrait les articles
                for entry in feed.entries[:10]:
                    time.sleep(1)
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
                        article_summary = summarize_article(article_content=article_content) if article["error"] is None else None
                        # On enregistre l'article dans la BDD
                        article_data = ArticleCreate(
                            title = title,
                            url = link,
                            description = description,
                            source = URL["name"],
                            image_url= image_url,
                            content = article_content,
                            summary = article_summary,
                            date = pubDate
                        )
                        create_article(db, article_data)
                        nb_added_articles += 1
            except Exception as e:
                db.rollback()
                print(e, f"La source {URL} est inaccessible ou intraitable")
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        print(f"Nombre d'articles ajoutés : {nb_added_articles}")
        db.close()
