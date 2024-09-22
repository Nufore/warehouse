from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import OrderList, ChangeStatus
from .dependencies import order_by_id

from app.database.db_helper import db_helper
from app.database.models import Order


router = APIRouter(tags=["Orders"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderList, session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.create_order(order=order, session=session)


@router.get("", status_code=status.HTTP_200_OK)
async def get_orders(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_orders(session=session)


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_detail(order: Order = Depends(order_by_id)):
    return order.detail_data_to_json()


@router.put("/{order_id}/status", status_code=status.HTTP_200_OK)
async def change_order_status(
    update_data: ChangeStatus,
    order: Order = Depends(order_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.change_order_status(
        order=order, update_data=update_data, session=session
    )
