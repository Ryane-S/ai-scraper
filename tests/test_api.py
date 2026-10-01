from unittest.mock import patch

from starlette import status

from app.crud.article import create_article
from app.routers.news import actual_state
from app.schemas.article import ArticleCreate


# Tests de la route permettant d'accéder aux détails de l'ensemble des articles
def test_get_articles_when_db_is_empty(client):
    response = client.get("/news/articles")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_articles_returns_articles(client, db):
    for i in range(2):
        create_article(db, ArticleCreate(
            title=f"Article {i}",
            url=f"https://example.com/{i}",
            source="Test"
        ))

    response = client.get("/news/articles")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    
    titles = [a["title"] for a in response.json()]
    urls = [a["url"] for a in response.json()]
    assert "Article 0" in titles and "Article 1" in titles
    assert "https://example.com/0" in urls and "https://example.com/1" in urls

def test_get_articles_respects_skip(client, db):
    for i in range(5):
        create_article(db, ArticleCreate(
            title=f"Article {i}",
            url=f"https://example.com/{i}",
            source="Test"
        ))

    response = client.get("/news/articles?skip=3")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

def test_get_articles_respects_limit(client, db):
    for i in range(5):
        create_article(db, ArticleCreate(
            title=f"Article {i}",
            url=f"https://example.com/{i}",
            source="Test"
        ))

    response = client.get("/news/articles?limit=2")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

# Tests de la route permettant d'accéder aux détails d'un article
def test_get_article_returns_article(client, article_data, db):
    create_article(db, ArticleCreate(
        title="Article 1",
        url="https://example.com/1",
        source="Test"
    ))
    response = client.get("/news/articles/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Article 1"
    assert response.json()["url"] == "https://example.com/1"

def test_get_article_returns_404_when_not_found(client):
    response = client.get("/news/articles/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Article non trouvé."}

# Tests de la route qui gère le scraping
def test_scrape_returns_200(client):
    # On remplace fetch_and_store_articles par un mock qui ne fait rien
    with patch("app.routers.news.fetch_and_store_articles"):
        response = client.post("/news/scrape")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Scraping en cours... Actualisez la liste dans quelques instants."}

def test_scrape_returns_400_when_already_running(client):
    actual_state["status"] = "running"
    try:
        response = client.post("/news/scrape")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Scraping déjà en cours."}
    finally:
        actual_state["status"] = "idle"

# Test de la route qui vérifie l'état du scraping
def test_get_scrape_status(client):
    response = client.get("/news/scrape/status")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "idle"
    