import pytest

from app.models import Menu


@pytest.fixture()
def menu(session):
    menu = Menu(title="Test title", description="Test description")
    session.add(menu)
    session.commit()
    yield menu
    session.delete(menu)
    session.commit()
