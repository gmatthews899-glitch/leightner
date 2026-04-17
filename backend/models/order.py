from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.models import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_code: Mapped[str] = mapped_column(String, index=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    credit_hold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sales_order_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    item_number: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    ship_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    backorder_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_ship_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_by: Mapped[str | None] = mapped_column(String, nullable=True)

    @property
    def total_qty(self) -> int:
        return self.ship_qty + self.backorder_qty
