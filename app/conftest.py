import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.config import Config
from app.db import get_session
from app.main import app
from app.models import Menu, Submenu, Dish

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


@pytest.fixture()
def menu(session):
    menu = Menu(title="Test title", description="Test description")
    session.add(menu)
    session.commit()
    yield menu
    session.delete(menu)
    session.commit()


@pytest.fixture()
def submenu(menu, session):
    submenu = Submenu(
        title="Test title", description="Test description", menu_id=menu.id
    )
    session.add(submenu)
    session.commit()
    yield submenu
    session.delete(submenu)
    session.commit()


@pytest.fixture()
def dish(submenu, session):
    dish = Dish(
        title="Test title", description="Test description", price="19.99", submenu_id=submenu.id
    )
    session.add(dish)
    session.commit()
    yield dish
    session.delete(dish)
    session.commit()
