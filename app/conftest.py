import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.config import Config
from app.db import get_session
from app.main import app

TEST_SQLALCHEMY_URI = (
    f"postgresql://"
    f"{Config.TEST_DATABASE_USER}:"
    f"{Config.TEST_DATABASE_PASSWORD}@"
    f"{Config.TEST_DATABASE_HOST}/"
    f"{Config.TEST_DATABASE_NAME}"
)
test_engine = create_engine(TEST_SQLALCHEMY_URI)
SQLModel.metadata.bind = test_engine


def override_get_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(autouse=True, scope="session")
def prepare_database():
    with test_engine.begin() as conn:
        SQLModel.metadata.create_all(conn)
    yield
    with test_engine.begin() as conn:
        SQLModel.metadata.drop_all(conn)


@pytest.fixture(scope="session")
def session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
