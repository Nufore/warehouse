from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from app.database.models import Base, OrderStatus
from app.database.db_helper import DatabaseHelper, db_helper
from app.main import app

DATABASE_URL_TEST = "postgresql+asyncpg://admin:admin@localhost/test_db"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

db_helper_test = DatabaseHelper(url=DATABASE_URL_TEST, echo=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[db_helper.session_getter] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with db_helper_test.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_helper_test.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
async def prepare_db_create_order_statuses():
    async with async_session_maker() as session:
        status_1 = OrderStatus(name="в процессе")
        status_2 = OrderStatus(name="отправлен")
        status_3 = OrderStatus(name="доставлен")
        session.add_all([status_1, status_2, status_3])
        await session.commit()


transport = ASGITransport(app=app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=transport,
            base_url="http://localhost:8000/",
    ) as ac:
        yield ac
