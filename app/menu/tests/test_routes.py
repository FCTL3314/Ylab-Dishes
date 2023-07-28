from http import HTTPStatus

import pytest
from sqlmodel import select

from app.common.tests import is_response_match_object_fields, get_model_objects_count
from app.models import Menu


def test_menu_retrieve(menu, client):
    response = client.get(f"api/v1/menus/{menu.id}/")

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        menu,
        ("id", "title", "description"),
    )


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
    assert is_response_match_object_fields(
        response.json(),
        data,
        ("title", "description"),
    )
    assert get_model_objects_count(Menu, session) == 1

    menu = session.exec(select(Menu)).first()
    session.delete(menu)
    session.commit()


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
    assert is_response_match_object_fields(
        response.json(), data, ("title", "description")
    )


def test_menu_delete(menu, client, session):
    response = client.delete(f"api/v1/menus/{menu.id}/")

    assert response.status_code == HTTPStatus.OK
    assert get_model_objects_count(Menu, session) == 0


if __name__ == "__main__":
    pytest.main()