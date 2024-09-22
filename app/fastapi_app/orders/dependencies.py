from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.database.models import Order


async def order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Order:
    stmt = (
        select(Order).options(selectinload(Order.status)).filter(Order.id == order_id)
    )
    order = await session.scalar(stmt)
    if order:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order {order_id} not found.",
    )
