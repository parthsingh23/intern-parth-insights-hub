from datetime import date
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    Float,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base import Base


class Sale(Base):
    __tablename__ = "sales"

    __table_args__ = (
        CheckConstraint(
            """
            (is_return = TRUE AND quantity < 0)
            OR
            (is_return = FALSE AND quantity > 0)
            """,
            name="ck_sales_return_quantity",
        ),
    )

    sale_id: Mapped[int] = mapped_column(primary_key=True)

    invoice_no: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    distributor_id: Mapped[int] = mapped_column(
        ForeignKey("distributors.distributor_id"),
        nullable=False,
    )

    sku_id: Mapped[int] = mapped_column(
        ForeignKey("skus.sku_id"),
        nullable=False,
    )

    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    net_value: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    is_return: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    distributor = relationship(
        "Distributor",
        back_populates="sales",
    )

    sku = relationship(
        "SKU",
        back_populates="sales",
    )
