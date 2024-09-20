from typing import List
from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    stock_balance: int


class ProductData(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_balance: int


class ResponseProducts(BaseModel):
    products: List[ProductData] | None


class UpdateProduct(CreateProduct):
    pass
