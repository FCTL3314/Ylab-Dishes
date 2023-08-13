import asyncio
from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import router


async def test_all_menus_task(client: AsyncClient, session: AsyncSession):
    """
    Tests the creation of a task to get all the menus,
    and result getting.
    """
    path = router.url_path_for('all-menus:create-task')
    response = await client.post(path)
    task_id = response.json()['task_id']

    assert response.status_code == HTTPStatus.CREATED

    await asyncio.sleep(1)

    path = router.url_path_for('all-menus:list', task_id=task_id)
    response = await client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert response.json()


if __name__ == '__main__':
    pytest.main()
