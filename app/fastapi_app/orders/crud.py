from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import OrderList

from app.database.models import Order, OrderItem, Product


async def create_order(order: OrderList, session: AsyncSession):
    new_order = Order(status_id=1)
    session.add(new_order)
    await session.commit()

    order_list_to_db = []
    for order_item in order.order_list:

        product = await session.get(Product, order_item.product_id)
        if order_item.count > product.stock_balance:
            await session.delete(new_order)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Невозможно создать заказ! "
                       f"Оставшееся кол-во товара '{product.name}' = {product.stock_balance}",
            )

        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=order_item.product_id,
            count=order_item.count,
        )
        order_list_to_db.append(new_order_item)

    session.add_all(order_list_to_db)
    await session.commit()

    return new_order.to_json()
