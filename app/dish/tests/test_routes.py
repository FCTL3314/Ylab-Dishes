from http import HTTPStatus
from uuid import UUID

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.common.tests import (
    delete_first_object,
    get_model_objects_count,
    is_response_match_object_fields,
)
from app.models import Dish, Submenu


def get_base_url(menu_id: UUID, submenu_id: UUID):
    return f"api/v1/menus/{menu_id}/submenus/{submenu_id}/"


async def get_related_submenu(dish: Dish, session: AsyncSession):
    result = await session.execute(select(Submenu).where(Submenu.id == dish.submenu_id))
    return result.first()


async def test_dish_retrieve(dish: Dish, client: AsyncClient, session: AsyncSession):
    response = await client.get(
        get_base_url(dish.submenu.menu_id, dish.submenu.id) + f"dishes/{dish.id}/"
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        dish,
        ("id", "title", "description", "price"),
    )


async def test_dish_list(dish: Dish, client: AsyncClient, session: AsyncSession):
    response = await client.get(
        get_base_url(dish.submenu.menu_id, dish.submenu.id) + "dishes/"
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


async def test_dish_create(
    submenu: Submenu, client: AsyncClient, session: AsyncSession
):
    data = {
        "title": "Test title",
        "description": "Test description",
        "price": "19.99",
    }
    response = await client.post(
        get_base_url(submenu.menu_id, submenu.id) + "dishes/",
        json=data,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert is_response_match_object_fields(
        response.json(),
        data,
        ("title", "description", "price"),
    )
    assert await get_model_objects_count(Dish, session) == 1

    await delete_first_object(select(Dish), session)


async def test_dish_update(dish: Dish, client: AsyncClient, session: AsyncSession):
    data = {
        "title": "Updated title",
        "description": "Updated description",
        "price": "12.33",
    }
    response = await client.patch(
        get_base_url(dish.submenu.menu_id, dish.submenu.id) + f"dishes/{dish.id}/",
        json=data,
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(), data, ("title", "description", "price")
    )


async def test_dish_delete(dish: Dish, client: AsyncClient, session: AsyncSession):
    response = await client.delete(
        get_base_url(dish.submenu.menu_id, dish.submenu.id) + f"dishes/{dish.id}/"
    )

    assert response.status_code == HTTPStatus.OK
    assert await get_model_objects_count(Dish, session) == 0


if __name__ == "__main__":
    pytest.main()
