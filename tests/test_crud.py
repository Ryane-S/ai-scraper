import uuid
from datetime import datetime, timedelta

from app.crud.article import (
    article_in_db,
    create_article,
    delete_all_articles,
    delete_old_articles,
    get_all_articles,
    get_article_by_id,
)
from app.schemas.article import ArticleCreate


# Tests de création d'un article
def test_create_article_persists_in_db(db, article_data):
    create_article(db, article_data)
    assert article_in_db(db, article_data.url)

def test_create_article_returns_correct_non_empty_fields(db, article_data):
    article = create_article(db, article_data)
    assert article.id is not None
    assert article.title == article_data.title
    assert article.url == article_data.url
    assert article.source == article_data.source
    assert article.description == article_data.description
    assert article.scraped_at is not None

# Tests de lecture d'un article par son id
def test_get_article_by_id_when_article_exists(db, article_data):
    article = create_article(db, article_data)
    retrieved_article = get_article_by_id(db, article.id)
    assert retrieved_article is not None
    assert retrieved_article.url == article_data.url

def test_get_article_by_id_when_article_does_not_exist(db):
    assert get_article_by_id(db, 999999) is None

# Tests de lecture de tous les articles présents dans la BDD
def test_get_all_articles_when_db_is_empty(db):
    assert get_all_articles(db) == []

def test_get_all_articles_with_3_articles(db):
    for _ in range(3):
        unique = uuid.uuid4().hex[:8]
        create_article(db, ArticleCreate(
            title=f"Article {unique}",
            url=f"https://example.com/{unique}",
            source="Test"
        ))
    assert len(get_all_articles(db)) == 3

def test_get_all_articles_respects_skip(db):
    for _ in range(5):
        unique = uuid.uuid4().hex[:8]
        create_article(db, ArticleCreate(
            title=f"Article {unique}",
            url=f"https://example.com/{unique}",
            source="Test"
        ))
    assert len(get_all_articles(db, skip=3)) == 2

def test_get_all_articles_respects_limit(db):
    for _ in range(5):
        unique = uuid.uuid4().hex[:8]
        create_article(db, ArticleCreate(
            title=f"Article {unique}",
            url=f"https://example.com/{unique}",
            source="Test"
        ))
    assert len(get_all_articles(db, limit=2)) == 2

def test_get_all_articles_sorted_by_date_desc(db):
    for i in range(3):
        unique = uuid.uuid4().hex[:8]
        create_article(db, ArticleCreate(
            title=f"Article {i}",
            url=f"https://example.com/{unique}",
            source="Test",
            date=datetime.now() - timedelta(days=i)
        ))
    
    articles = get_all_articles(db)
    
    assert articles[0].title == "Article 0"
    assert articles[1].title == "Article 1"
    assert articles[2].title == "Article 2"

# Tests de vérification de la présence d'un article
def test_article_in_db(db, article_data):
    article = create_article(db, article_data)
    assert article_in_db(db, article.url)
    assert not article_in_db(db, "https://example.com/false_sample")

# Tests de suppression d'articles
def test_delete_old_articles(db):
    for i in range(3):
        unique = uuid.uuid4().hex[:8]
        create_article(db, ArticleCreate(
            title=f"Article {unique}",
            url=f"https://example.com/{unique}",
            source="Test",
            date=datetime.now() - timedelta(days=i)
        ))

    articles = get_all_articles(db)

    deleted_count = delete_old_articles(db, articles[0].date)
    assert deleted_count == 2

def test_delete_all_articles(db):
    for _ in range(3):
        unique = uuid.uuid4().hex[:8]
        create_article(db, ArticleCreate(
            title=f"Article {unique}",
            url=f"https://example.com/{unique}",
            source="Test",
        ))

    deleted_count = delete_all_articles(db)
    assert deleted_count == 3
    assert get_all_articles(db) == []
