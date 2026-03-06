import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.app import app as fastapi_app
from app.core.database import Base, get_db

# Import ALL models so Base.metadata knows every table
import app.models  # noqa: F401


# ── In-memory SQLite for tests ──────────────────────────────────────
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Create all tables once per test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    """Provide a transactional DB session that rolls back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    """FastAPI TestClient with the DB session overridden."""

    def override_get_db():
        yield db

    fastapi_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fastapi_app) as c:
        yield c

    fastapi_app.dependency_overrides.clear()


# ── Auth helpers ────────────────────────────────────────────────────


def _register_and_login(client, email: str, password: str = "secret123"):
    """Register a user and login, returning the auth header dict."""
    client.post("/auth/register", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _make_superuser(db, email: str):
    """Promote a user to superuser directly in the DB."""
    from app.models.user import User

    user = db.query(User).filter(User.email == email).first()
    user.is_superuser = True
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture()
def auth_headers(client):
    """Register + login a normal user; return auth headers."""
    return _register_and_login(client, "testuser@test.com")


@pytest.fixture()
def admin_headers(client, db):
    """Register + login a superuser; return auth headers."""
    headers = _register_and_login(client, "admin@test.com")
    _make_superuser(db, "admin@test.com")
    return headers