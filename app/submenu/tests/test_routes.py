from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.common.tests import (delete_first_object, get_model_objects_count,
                              is_response_match_object_fields)
from app.models import Dish, Menu, Submenu


def get_base_url(menu_id):
    return f"api/v1/menus/{menu_id}/"


async def test_submenu_retrieve(submenu: Submenu, client: AsyncClient):
    response = await client.get(
        get_base_url(submenu.menu_id) + f"submenus/{submenu.id}/"
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        submenu,
        ("id", "title", "description"),
    )


async def test_submenu_list(submenu: Submenu, client: AsyncClient):
    response = await client.get(get_base_url(submenu.menu_id) + "submenus/")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


async def test_submenu_create(menu: Menu, client: AsyncClient, session: AsyncSession):
    data = {
        "title": "Test title",
        "description": "Test description",
    }
    response = await client.post(
        get_base_url(menu.id) + "submenus/",
        json=data,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert is_response_match_object_fields(
        response.json(),
        data,
        ("title", "description"),
    )
    assert await get_model_objects_count(Submenu, session) == 1

    await delete_first_object(select(Submenu), session)


async def test_submenu_update(submenu: Submenu, client: AsyncClient):
    data = {
        "title": "Updated title",
        "description": "Updated description",
    }
    response = await client.patch(
        get_base_url(submenu.menu_id) + f"submenus/{submenu.id}/",
        json=data,
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(), data, ("title", "description")
    )


async def test_submenu_delete(
    submenu: Submenu, client: AsyncClient, session: AsyncSession
):
    response = await client.delete(
        get_base_url(submenu.menu_id) + f"submenus/{submenu.id}/"
    )

    assert response.status_code == HTTPStatus.OK
    assert await get_model_objects_count(Submenu, session) == 0


async def test_counting(dish: Dish, client: AsyncClient, session: AsyncSession):
    submenu_retrieve = await client.get(
        get_base_url(dish.submenu.menu_id) + f"submenus/{dish.submenu_id}/"
    )
    response = submenu_retrieve.json()

    assert response["dishes_count"] == 1


if __name__ == "__main__":
    pytest.main()
