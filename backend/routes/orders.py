from __future__ import annotations

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services import order_service

router = APIRouter(prefix="/api/orders")

DbSession = Annotated[Session, Depends(get_db)]


class OrderCreate(BaseModel):
    customer_code: str
    customer_name: str
    credit_hold: bool = False
    sales_order_number: str
    item_number: str
    description: str
    ship_qty: int = 0
    backorder_qty: int = 0
    estimated_ship_date: date | None = None
    notes: str | None = None


class OrderUpdate(BaseModel):
    customer_code: str | None = None
    customer_name: str | None = None
    credit_hold: bool | None = None
    item_number: str | None = None
    description: str | None = None
    ship_qty: int | None = None
    backorder_qty: int | None = None
    estimated_ship_date: date | None = None
    notes: str | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_code: str
    customer_name: str
    credit_hold: bool
    sales_order_number: str
    item_number: str
    description: str
    ship_qty: int
    backorder_qty: int
    total_qty: int
    estimated_ship_date: date | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    updated_by: str | None


@router.get("", response_model=list[OrderResponse])
def list_orders(db: DbSession) -> list[OrderResponse]:
    return order_service.list_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: DbSession) -> OrderResponse:
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(body: OrderCreate, db: DbSession) -> OrderResponse:
    try:
        return order_service.create_order(
            db,
            data=body.model_dump(),
            updated_by=None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, body: OrderUpdate, db: DbSession) -> OrderResponse:
    order = order_service.update_order(
        db,
        order_id,
        data=body.model_dump(exclude_unset=True),
        updated_by=None,
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: DbSession) -> Response:
    deleted = order_service.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
