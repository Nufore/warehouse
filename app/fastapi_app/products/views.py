from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import CreateProduct, ResponseProducts, ProductData, UpdateProduct

from app.database.db_helper import db_helper

router = APIRouter(tags=["Products"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: CreateProduct,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.create_product(session=session, product=product)


@router.get("", status_code=status.HTTP_200_OK, response_model=ResponseProducts)
async def get_products(session: AsyncSession = Depends(db_helper.session_getter)):
    return await crud.get_products(session=session)


@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductData)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.get_product(session=session, product_id=product_id)


@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductData)
async def put_product(
    product_id: int,
    update_data: UpdateProduct,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_product(
        product_id=product_id, session=session, update_data=update_data
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.delete_product(session=session, product_id=product_id)
