import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.article import Article
from app.schemas.article import ArticleCreate

# On crée une db de test en mémoire
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSession = sessionmaker(bind=test_engine)

# Fixture : session de test
@pytest.fixture
def db():
    Base.metadata.create_all(bind=test_engine)
    test_db = TestSession()
    try:
        yield test_db
    finally:
        test_db.close()
        Base.metadata.drop_all(bind=test_engine)

# Fixture : client FastAPI
@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Fixture : article
@pytest.fixture
def article_data():
    unique = uuid.uuid4().hex[:8]
    return ArticleCreate(
        title=f"Sample Article {unique}",
        url=f"https://example.com/sample-{unique}",
        source="Test",
        description="A test article"
    )