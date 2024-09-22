from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload, subqueryload
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import OrderList, ChangeStatus

from app.database.models import Order, OrderItem, Product, OrderStatus


async def create_order(order: OrderList, session: AsyncSession):
    new_order = Order(status_id=1)

    order_list_to_db = []
    for order_item in order.order_list:
        product = await session.get(Product, order_item.product_id)
        if order_item.count > product.stock_balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Невозможно создать заказ! "
                f"Оставшееся кол-во товара '{product.name}' = {product.stock_balance}",
            )

        new_order_item = OrderItem(
            order=new_order, product_id=product.id, count=order_item.count
        )
        order_list_to_db.append(new_order_item)

        product.stock_balance -= order_item.count
        session.add(product)

    session.add(new_order)
    session.add_all(order_list_to_db)
    await session.commit()

    stmt = (
        select(Order)
        .options(selectinload(Order.status))
        .filter(Order.id == new_order.id)
    )
    res = await session.scalar(stmt)
    return res.to_json()


async def get_orders(session: AsyncSession):
    stmt = select(Order).options(selectinload(Order.status))
    result = await session.scalars(stmt)

    orders = result.all()

    return {"orders": [order.to_json() for order in orders]}


async def get_order_detail(order_id: int, session: AsyncSession):
    stmt = (
        select(Order)
        .options(
            selectinload(Order.order_items).subqueryload(OrderItem.product),
            selectinload(Order.status),
        )
        .filter(Order.id == order_id)
    )

    order = await session.scalar(stmt)

    return order.detail_data_to_json()


async def change_order_status(
    order: Order, update_data: ChangeStatus, session: AsyncSession
):
    order_status = await session.get(OrderStatus, update_data.status_id)
    if not order_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Status {update_data.status_id} not found.",
        )
    order.status = order_status
    session.add(order)
    await session.commit()

    return order.to_json()
