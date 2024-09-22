from typing import List
from pydantic import BaseModel


class OrderItem(BaseModel):
    product_id: int
    count: int


class OrderList(BaseModel):
    order_list: List[OrderItem]


class ChangeStatus(BaseModel):
    status_id: int
