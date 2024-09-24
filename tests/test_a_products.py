import pytest
from conftest import async_session_maker
from httpx import AsyncClient
from sqlalchemy import select

from app.database.models import Product


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products(ac: AsyncClient):
    response = await ac.get("/products")
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = select(Product).order_by(-Product.id).limit(1)
        product_from_db = await session.scalar(stmt)
    last_product_id = 0
    if product_from_db:
        last_product_id = product_from_db.id

    data = {
        "name": "Test product №1",
        "description": "Some description to Test product №1",
        "price": 100,
        "stock_balance": 10
    }
    response = await ac.post("/products", json=data)
    current_product_id = response.json()["id"]

    assert response.status_code == 201
    assert current_product_id == last_product_id + 1


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_wrong_data(ac: AsyncClient):
    data = {
        "name": "Test product №2",
        "description": "Some description to Test product №1",
        "stock_balance": 10
    }
    response = await ac.post("/products", json=data)

    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_wrong_data_int_type(ac: AsyncClient):
    data = {
        "name": 12345,
        "description": "Some description to Test product №1",
        "price": 100,
        "stock_balance": 10
    }
    response = await ac.post("/products", json=data)

    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = select(Product).order_by(-Product.id).limit(1)
        product_from_db = await session.scalar(stmt)
    last_product_id = 0
    if product_from_db:
        last_product_id = product_from_db.id

    response = await ac.get(f"/products/{last_product_id}")
    current_product_id = response.json()["id"]

    assert response.status_code == 200
    assert last_product_id == current_product_id


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_wrong_data(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = select(Product).order_by(-Product.id).limit(1)
        product_from_db = await session.scalar(stmt)
    last_product_id = 0
    if product_from_db:
        last_product_id = product_from_db.id

    test_id = last_product_id + 100 * 100
    response = await ac.get(f"/products/{test_id}")
    detail = response.json()["detail"]

    assert response.status_code == 404
    assert detail == f"Product {test_id} not found."


@pytest.mark.asyncio(loop_scope="session")
async def test_put_product(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = select(Product).order_by(-Product.id).limit(1)
        product_from_db = await session.scalar(stmt)
    last_product_id = 0
    if product_from_db:
        last_product_id = product_from_db.id

    data = {
        "name": "Changed name",
        "description": "Changed description",
        "price": 5000,
        "stock_balance": 1000
    }

    response = await ac.put(f"/products/{last_product_id}", json=data)

    assert response.status_code == 200
    assert response.json()["name"].startswith("Changed")
    assert response.json()["price"] == 5000
    assert response.json()["stock_balance"] == 1000


@pytest.mark.asyncio(loop_scope="session")
async def test_put_product_wrong_data(ac: AsyncClient):
    product_id = 1

    data = {
        "name": "Changed name",
        "description": "Changed description",
        "price": 5000
    }

    response = await ac.put(f"/products/{product_id}", json=data)

    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_wrong_data(ac: AsyncClient):
    product_id = 100 * 100
    response = await ac.delete(f"/products/{product_id}")
    detail = response.json()["detail"]

    assert response.status_code == 404
    assert detail == f"Product {product_id} not found."


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product(ac: AsyncClient):
    product_id = 1
    response = await ac.delete(f"/products/{product_id}")

    async with async_session_maker() as session:
        new_product = Product(
            name="Test product №2",
            description="Some description to Test product №2",
            price=200,
            stock_balance=110
        )
        session.add(new_product)
        await session.commit()

    assert response.status_code == 204
    assert new_product.id == product_id + 1
