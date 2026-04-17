from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.order import Order

ORDER_CREATE_FIELDS: set[str] = {
    "customer_code",
    "customer_name",
    "credit_hold",
    "sales_order_number",
    "item_number",
    "description",
    "ship_qty",
    "backorder_qty",
    "estimated_ship_date",
    "notes",
    "updated_by",
}

ORDER_UPDATE_FIELDS: set[str] = {
    "customer_code",
    "customer_name",
    "credit_hold",
    "item_number",
    "description",
    "ship_qty",
    "backorder_qty",
    "estimated_ship_date",
    "notes",
    "updated_by",
}


def _filter_order_data(data: dict[str, Any], allowed_fields: set[str]) -> dict[str, Any]:
    return {
        key: value
        for key, value in data.items()
        if key in allowed_fields
    }


def list_orders(db: Session) -> list[Order]:
    statement = select(Order).order_by(Order.updated_at.desc())
    return list(db.scalars(statement).all())


def get_order(db: Session, order_id: int) -> Order | None:
    return db.get(Order, order_id)


def get_order_by_sales_order_number(db: Session, sales_order_number: str) -> Order | None:
    statement = select(Order).where(Order.sales_order_number == sales_order_number)
    return db.scalar(statement)


def create_order(
    db: Session,
    data: dict[str, Any],
    updated_by: str | None = None,
) -> Order:
    if get_order_by_sales_order_number(db, data["sales_order_number"]) is not None:
        raise ValueError("Sales order number already exists")

    order_data = _filter_order_data(data, ORDER_CREATE_FIELDS)
    if updated_by is not None:
        order_data["updated_by"] = updated_by

    order = Order(**order_data)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_order(
    db: Session,
    order_id: int,
    data: dict[str, Any],
    updated_by: str | None = None,
) -> Order | None:
    order = get_order(db, order_id)
    if order is None:
        return None

    order_data = _filter_order_data(data, ORDER_UPDATE_FIELDS)
    for key, value in order_data.items():
        setattr(order, key, value)

    if updated_by is not None:
        order.updated_by = updated_by

    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int) -> bool:
    order = get_order(db, order_id)
    if order is None:
        return False

    db.delete(order)
    db.commit()
    return True
