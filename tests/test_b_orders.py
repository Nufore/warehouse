import pytest
from conftest import async_session_maker
from httpx import AsyncClient
from sqlalchemy import select

from app.database.models import Order


@pytest.mark.asyncio(loop_scope="session")
async def test_get_orders(ac: AsyncClient):
    response = await ac.get("/orders")
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_post_orders(ac: AsyncClient):
    data = {
        "order_list": [
            {
                "product_id": 2,
                "count": 10
            }
        ]
    }
    response = await ac.post("/orders", json=data)
    assert response.status_code == 201
    assert response.json()["status_id"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_post_orders_wrong_data_count(ac: AsyncClient):
    data = {
        "order_list": [
            {
                "product_id": 2,
                "count": 101
            }
        ]
    }
    response = await ac.post("/orders", json=data)
    assert response.status_code == 400
    assert response.json()["detail"][-3:] == "100"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_order(ac: AsyncClient):
    order_id = 1

    response = await ac.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.json()["products"][0]["count"] == 10


@pytest.mark.asyncio(loop_scope="session")
async def test_get_order_wrong_data(ac: AsyncClient):
    order_id = 100 * 100

    response = await ac.get(f"/orders/{order_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Order {order_id} not found."


@pytest.mark.asyncio(loop_scope="session")
async def test_put_change_order_status(ac: AsyncClient):
    order_id = 1
    status_id = 2
    data = {
        "status_id": status_id
    }
    response = await ac.put(f"/orders/{order_id}/status", json=data)

    assert response.status_code == 200
    assert response.json()["status_id"] == 2
    assert response.json()["status"] == "отправлен"


@pytest.mark.asyncio(loop_scope="session")
async def test_put_change_order_status_wrong_id(ac: AsyncClient):
    order_id = 100 * 100
    status_id = 2
    data = {
        "status_id": status_id
    }
    response = await ac.put(f"/orders/{order_id}/status", json=data)

    assert response.status_code == 404
    assert response.json()["detail"] == f"Order {order_id} not found."


@pytest.mark.asyncio(loop_scope="session")
async def test_put_change_order_status_wrong_status_id(ac: AsyncClient):
    order_id = 1
    status_id = 100
    data = {
        "status_id": status_id
    }
    response = await ac.put(f"/orders/{order_id}/status", json=data)

    assert response.status_code == 404
    assert response.json()["detail"] == f"Status {status_id} not found."
