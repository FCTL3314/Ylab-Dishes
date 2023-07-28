from http import HTTPStatus

import pytest
from sqlmodel import select

from app.models import Menu


def test_menu_retrieve(menu, client):
    response = client.get(f"api/v1/menus/{menu.id}/")

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data["id"] == str(menu.id)


def test_menu_list(menu, client):
    response = client.get("api/v1/menus/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


def test_menu_create(client, session):
    data = {
        "title": "Test title",
        "description": "Test description",
    }
    response = client.post(
        "api/v1/menus/",
        json=data,
    )

    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json()
    assert response_data["title"] == data["title"]
    assert response_data["description"] == data["description"]
    assert len(session.exec(select(Menu)).all()) == 1


def test_menu_update(menu, client):
    data = {
        "title": "Updated title",
        "description": "Updated description",
    }
    response = client.patch(
        f"api/v1/menus/{menu.id}/",
        json=data,
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data["id"] == str(menu.id)
    assert response_data["title"] == data["title"]
    assert response_data["description"] == data["description"]


def test_menu_delete(client, session):
    menu = session.exec(select(Menu)).first()
    response = client.delete(f"api/v1/menus/{menu.id}/")

    assert response.status_code == HTTPStatus.OK
    assert len(session.exec(select(Menu)).all()) == 0


if __name__ == "__main__":
    pytest.main()
