import pytest
from conftest import async_session_maker
from httpx import AsyncClient
from sqlalchemy import select


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products(ac: AsyncClient):
    response = await ac.get("/products")
    assert response.status_code == 200

#
# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(
#         transport=transport, base_url="http://test"
#     ) as ac:
#         response = await ac.get("/products")
#     assert response.status_code == 200
