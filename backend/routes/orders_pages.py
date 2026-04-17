from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated, Any
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services import order_service

CENTRAL_TZ = ZoneInfo("America/Chicago")
TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _build_template_order(order: Any, now_utc: datetime) -> dict[str, Any]:
    updated_at_utc = _as_utc(order.updated_at)
    return {
        "customer_code": order.customer_code,
        "customer_name": order.customer_name,
        "credit_hold": order.credit_hold,
        "sales_order_number": order.sales_order_number,
        "item_number": order.item_number,
        "description": order.description,
        "ship_qty": order.ship_qty,
        "backorder_qty": order.backorder_qty,
        "total_qty": order.total_qty,
        "estimated_ship_date": order.estimated_ship_date,
        "updated_at_iso": updated_at_utc.isoformat(),
        "recently_updated": now_utc - updated_at_utc <= timedelta(hours=24),
    }


@router.get("/orders")
def orders_list_page(request: Request, db: DbSession) -> Response:
    now_utc = datetime.now(timezone.utc)
    orders = [
        _build_template_order(order, now_utc)
        for order in order_service.list_orders(db)
    ]
    context = {
        "request": request,
        "orders": orders,
        "today_central": datetime.now(CENTRAL_TZ).date(),
    }
    return templates.TemplateResponse("orders/list.html", context)
