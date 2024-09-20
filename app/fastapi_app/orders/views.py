from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import OrderList
from app.database.db_helper import db_helper


router = APIRouter(tags=["Orders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderList, session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud.create_order(order=order, session=session)
