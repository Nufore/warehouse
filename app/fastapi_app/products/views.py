from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .dependencies import product_by_id
from .schemas import CreateProduct, ResponseProducts, ProductData, UpdateProduct

from app.database.db_helper import db_helper
from app.database.models import Product

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
async def get_product(product: Product = Depends(product_by_id)):
    return product.to_json()


@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductData)
async def put_product(
    update_data: UpdateProduct,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.update_product(
        product=product, session=session, update_data=update_data
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.delete_product(session=session, product=product)
