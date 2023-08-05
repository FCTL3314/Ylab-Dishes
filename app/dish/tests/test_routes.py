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
from app.main import router
from app.models import Dish, Submenu


def get_base_url(menu_id: UUID, submenu_id: UUID):
    return f'api/v1/menus/{menu_id}/submenus/{submenu_id}/'


async def test_dish_retrieve(dish: Dish, client: AsyncClient, session: AsyncSession):
    path = router.url_path_for(
        'dish_retrieve',
        menu_id=dish.submenu.menu_id,
        submenu_id=dish.submenu_id,
        dish_id=dish.id,
    )
    response = await client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        dish,
        ('id', 'title', 'description', 'price'),
    )


async def test_dish_list(dish: Dish, client: AsyncClient, session: AsyncSession):
    path = router.url_path_for(
        'dish_list',
        menu_id=dish.submenu.menu_id,
        submenu_id=dish.submenu_id,
    )
    response = await client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


async def test_dish_create(
    submenu: Submenu, client: AsyncClient, session: AsyncSession
):
    data = {
        'title': 'Test title',
        'description': 'Test description',
        'price': '19.99',
    }
    path = router.url_path_for(
        'dish_create',
        menu_id=submenu.menu_id,
        submenu_id=submenu.id,
    )
    response = await client.post(path, json=data)

    assert response.status_code == HTTPStatus.CREATED
    assert is_response_match_object_fields(
        response.json(),
        data,
        ('title', 'description', 'price'),
    )
    assert await get_model_objects_count(Dish, session) == 1

    await delete_first_object(select(Dish), session)


async def test_dish_update(dish: Dish, client: AsyncClient, session: AsyncSession):
    data = {
        'title': 'Updated title',
        'description': 'Updated description',
        'price': '12.33',
    }
    path = router.url_path_for(
        'dish_patch',
        menu_id=dish.submenu.menu_id,
        submenu_id=dish.submenu_id,
        dish_id=dish.id,
    )
    response = await client.patch(path, json=data)

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(), data, ('title', 'description', 'price')
    )


async def test_dish_delete(dish: Dish, client: AsyncClient, session: AsyncSession):
    path = router.url_path_for(
        'dish_retrieve',
        menu_id=dish.submenu.menu_id,
        submenu_id=dish.submenu_id,
        dish_id=dish.id,
    )
    response = await client.delete(path)

    assert response.status_code == HTTPStatus.OK
    assert await get_model_objects_count(Dish, session) == 0


if __name__ == '__main__':
    pytest.main()
