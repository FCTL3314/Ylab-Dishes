from http import HTTPStatus

import pytest
from sqlmodel import select

from app.common.tests import (get_model_objects_count,
                              is_response_match_object_fields)
from app.models import Menu, Submenu


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


def test_counting(dish, client, session):
    submenu = session.exec(select(Submenu).where(Submenu.id == dish.submenu_id)).first()
    menu = session.exec(select(Menu).where(Menu.id == submenu.menu_id)).first()

    menu_retrieve = client.get(f"api/v1/menus/{menu.id}/").json()

    assert menu_retrieve["submenus_count"] == 1
    assert menu_retrieve["dishes_count"] == 1


if __name__ == "__main__":
    pytest.main()
