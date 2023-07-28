from http import HTTPStatus

import pytest
from sqlmodel import select

from app.common.tests import (get_model_objects_count,
                              is_response_match_object_fields)
from app.models import Dish, Submenu


def get_base_url(menu_id, submenu_id):
    return f"api/v1/menus/{menu_id}/submenus/{submenu_id}/"


def get_related_submenu(dish, session):
    return session.exec(select(Submenu).where(Submenu.id == dish.submenu_id)).first()


def test_dish_retrieve(dish, client, session):
    submenu = get_related_submenu(dish, session)
    response = client.get(
        get_base_url(submenu.menu_id, submenu.id) + f"dishes/{dish.id}/"
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        dish,
        ("id", "title", "description", "price"),
    )


def test_dish_list(dish, client, session):
    submenu = get_related_submenu(dish, session)
    response = client.get(get_base_url(submenu.menu_id, submenu.id) + "dishes/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


def test_dish_create(submenu, client, session):
    data = {
        "title": "Test title",
        "description": "Test description",
        "price": "19.99",
    }
    response = client.post(
        get_base_url(submenu.menu_id, submenu.id) + "dishes/",
        json=data,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert is_response_match_object_fields(
        response.json(),
        data,
        ("title", "description", "price"),
    )
    assert get_model_objects_count(Dish, session) == 1


def test_dish_update(dish, client, session):
    data = {
        "title": "Updated title",
        "description": "Updated description",
        "price": "12.33",
    }
    submenu = get_related_submenu(dish, session)
    response = client.patch(
        get_base_url(submenu.menu_id, submenu.id) + f"/dishes/{dish.id}/",
        json=data,
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(), data, ("title", "description", "price")
    )


def test_dish_delete(dish, client, session):
    submenu = get_related_submenu(dish, session)
    response = client.delete(
        get_base_url(submenu.menu_id, submenu.id) + f"dishes/{dish.id}/"
    )

    assert response.status_code == HTTPStatus.OK
    assert get_model_objects_count(Dish, session) == 0


if __name__ == "__main__":
    pytest.main()
