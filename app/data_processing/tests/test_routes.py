from http import HTTPStatus

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import router


async def test_all_menus(client: AsyncClient, session: AsyncSession):
    path = router.url_path_for('all-menus:list')
    response = await client.get(path)

    assert response.status_code == HTTPStatus.OK
    assert response.json() is not None


if __name__ == '__main__':
    pytest.main()
