from http import HTTPStatus

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
from app.models import Dish, Menu


async def test_menu_retrieve(menu: Menu, client: AsyncClient):
    response = await client.get(
        router.url_path_for('menu:retrieve', menu_id=menu.id)
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        menu,
        ('id', 'title', 'description'),
    )


async def test_menu_list(menu: Menu, client: AsyncClient):
    response = await client.get(router.url_path_for('menu:list'))

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


async def test_menu_create(client: AsyncClient, session: AsyncSession):
    data = {
        'title': 'Test title',
        'description': 'Test description',
    }
    response = await client.post(
        router.url_path_for('menu:create'),
        json=data,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert is_response_match_object_fields(
        response.json(),
        data,
        ('title', 'description'),
    )
    assert await get_model_objects_count(Menu, session) == 1

    await delete_first_object(select(Menu), session)


async def test_menu_update(menu: Menu, client: AsyncClient):
    data = {
        'title': 'Updated title',
        'description': 'Updated description',
    }
    response = await client.patch(
        router.url_path_for('menu:update', menu_id=menu.id),
        json=data,
    )

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(), data, ('title', 'description')
    )


async def test_menu_delete(menu: Menu, client: AsyncClient, session: AsyncSession):
    response = await client.delete(
        router.url_path_for('menu:retrieve', menu_id=menu.id)
    )

    assert response.status_code == HTTPStatus.OK
    assert await get_model_objects_count(Menu, session) == 0


async def test_counting(dish: Dish, client: AsyncClient, session: AsyncSession):
    menu_retrieve = await client.get(
        router.url_path_for('menu:retrieve', menu_id=dish.submenu.menu_id),
    )
    response = menu_retrieve.json()

    assert response['submenus_count'] == 1
    assert response['dishes_count'] == 1


if __name__ == '__main__':
    pytest.main()
