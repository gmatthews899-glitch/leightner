from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.models import order as _order
from backend.routes import orders as orders_routes
from backend.routes import orders_pages


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).resolve().parent.parent / "frontend" / "static")),
    name="static",
)
app.include_router(orders_routes.router)
app.include_router(orders_pages.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
