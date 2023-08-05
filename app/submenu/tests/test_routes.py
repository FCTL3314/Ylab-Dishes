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
from app.models import Dish, Menu, Submenu


async def test_submenu_retrieve(submenu: Submenu, client: AsyncClient):
    path = router.url_path_for(
        'submenu:retrieve',
        menu_id=submenu.menu_id,
        submenu_id=submenu.id,
    )
    response = await client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(),
        submenu,
        ('id', 'title', 'description'),
    )


async def test_submenu_list(submenu: Submenu, client: AsyncClient):
    path = router.url_path_for('submenu:list', menu_id=submenu.menu_id)
    response = await client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1


async def test_submenu_create(menu: Menu, client: AsyncClient, session: AsyncSession):
    data = {
        'title': 'Test title',
        'description': 'Test description',
    }
    response = await client.post(
        router.url_path_for('submenu:create', menu_id=menu.id),
        json=data,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert is_response_match_object_fields(
        response.json(),
        data,
        ('title', 'description'),
    )
    assert await get_model_objects_count(Submenu, session) == 1

    await delete_first_object(select(Submenu), session)


async def test_submenu_update(submenu: Submenu, client: AsyncClient):
    data = {
        'title': 'Updated title',
        'description': 'Updated description',
    }
    path = router.url_path_for(
        'submenu:update',
        menu_id=submenu.menu_id,
        submenu_id=submenu.id,
    )
    response = await client.patch(path, json=data)

    assert response.status_code == HTTPStatus.OK
    assert is_response_match_object_fields(
        response.json(), data, ('title', 'description')
    )


async def test_submenu_delete(
        submenu: Submenu, client: AsyncClient, session: AsyncSession
):
    path = router.url_path_for(
        'submenu:delete',
        menu_id=submenu.menu_id,
        submenu_id=submenu.id,
    )
    response = await client.delete(path)

    assert response.status_code == HTTPStatus.OK
    assert await get_model_objects_count(Submenu, session) == 0


async def test_counting(dish: Dish, client: AsyncClient, session: AsyncSession):
    path = router.url_path_for(
        'submenu:retrieve',
        menu_id=dish.submenu.menu_id,
        submenu_id=dish.submenu.id,
    )
    response = await client.get(path)
    response_json = response.json()

    assert response_json['dishes_count'] == 1


if __name__ == '__main__':
    pytest.main()
