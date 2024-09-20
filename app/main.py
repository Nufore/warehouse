from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.models import Base
from app.database.db_helper import db_helper
from app.fastapi_app.products.views import router as products_router
from app.fastapi_app.orders.views import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=products_router, prefix=settings.products_prefix)
app.include_router(router=orders_router, prefix=settings.orders_prefix)


@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "result": False,
            "error_type": type(exc).__name__,
            "error_message": exc.__repr__(),
        },
    )


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)
