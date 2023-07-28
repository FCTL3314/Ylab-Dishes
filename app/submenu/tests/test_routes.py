from http import HTTPStatus

import pytest

from app.common.tests import is_response_match_object_fields, get_model_objects_count
from app.models import Submenu


def get_base_url(menu_id):
    return f"api/v1/menus/{menu_id}/"


def test_submenu_retrieve(submenu, client):
    response = client.get(get_base_url(submenu.menu_id) + f"submenus/{submenu.id}/")

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        submenu,
        ("id", "title", "description"),
    )


def test_submenu_list(submenu, client):
    response = client.get(get_base_url(submenu.menu_id) + "submenus/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


def test_submenu_create(menu, client, session):
    data = {
        "title": "Test title",
        "description": "Test description",
    }
    response = client.post(
        get_base_url(menu.id) + "submenus/",
        json=data,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert is_response_match_object_fields(
        response.json(),
        data,
        ("title", "description"),
    )
    assert get_model_objects_count(Submenu, session) == 1


def test_submenu_update(submenu, client):
    data = {
        "title": "Updated title",
        "description": "Updated description",
    }
    response = client.patch(
        get_base_url(submenu.menu_id) + f"submenus/{submenu.id}/",
        json=data,
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        data,
        ("title", "description")
    )


def test_submenu_delete(submenu, client, session):
    response = client.delete(get_base_url(submenu.menu_id) + f"submenus/{submenu.id}/")

    assert response.status_code == HTTPStatus.OK
    assert get_model_objects_count(Submenu, session) == 0


if __name__ == "__main__":
    pytest.main()
