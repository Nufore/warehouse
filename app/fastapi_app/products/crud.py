from fastapi import status, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CreateProduct, UpdateProduct
from app.database.models import Product


async def create_product(product: CreateProduct, session: AsyncSession):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_balance=product.stock_balance,
    )

    session.add(new_product)
    await session.commit()

    return new_product.to_json()


async def get_products(session: AsyncSession):
    stmt = select(Product)
    result = await session.scalars(stmt)

    products = result.all()

    return {"products": [product.to_json() for product in products]}


async def get_product(product_id: int, session: AsyncSession):
    product: Product | None = await session.get(Product, product_id)
    if product:
        return product.to_json()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found.",
    )


async def update_product(
    product: Product, session: AsyncSession, update_data: UpdateProduct
):
    product.name = update_data.name
    product.description = update_data.description
    product.price = update_data.price
    product.stock_balance = update_data.stock_balance

    session.add(product)
    await session.commit()

    return product.to_json()


async def delete_product(product: Product, session: AsyncSession):
    await session.delete(product)
    await session.commit()
    return {"Message": f"Product {product.id} deleted successfully."}
