from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base import Base


class SKU(Base):
    __tablename__ = "skus"

    sku_id: Mapped[int] = mapped_column(primary_key=True)

    sku_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    sku_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.brand_id"),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    pack_size: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    mrp: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    brand = relationship(
        "Brand",
        back_populates="skus",
    )

    sales = relationship(
        "Sale",
        back_populates="sku",
    )
