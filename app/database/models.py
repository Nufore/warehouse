import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.types import String, Numeric, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(precision=9, scale=2))
    stock_balance: Mapped[int] = mapped_column(Integer())

    order_items: Mapped["OrderItem"] = relationship(back_populates="product")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock_balance": self.stock_balance,
        }


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(), default=datetime.datetime.now()
    )
    status_id: Mapped[int] = mapped_column(ForeignKey("order_statuses.id"))
    status: Mapped["OrderStatus"] = relationship("OrderStatus")

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    def to_json(self):
        return {
            "id": self.id,
            "created_date": self.created_date,
            "status": self.status.name,
            "status_id": self.status_id,
        }

    def detail_data_to_json(self):
        return {
            "order_id": self.id,
            "order_status": self.status.name,
            "order_date": self.created_date,
            "products": [order_item.to_json() for order_item in self.order_items],
        }


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    order: Mapped[Order] = relationship("Order", back_populates="order_items")

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped[Product] = relationship("Product", back_populates="order_items")

    count: Mapped[int] = mapped_column(Integer())

    def to_json(self):
        return {
            "product_id": self.product.id,
            "product_name": self.product.name,
            "count": self.count,
        }
