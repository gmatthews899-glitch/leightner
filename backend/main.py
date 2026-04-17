from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import init_db
from backend.models import order as _order


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
