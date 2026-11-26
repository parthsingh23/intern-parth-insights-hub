from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base import Base


class Distributor(Base):
    __tablename__ = "distributors"

    distributor_id: Mapped[int] = mapped_column(primary_key=True)

    distributor_code: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )

    distributor_name: Mapped[str] = mapped_column(String(150), nullable=False)

    state_id: Mapped[int] = mapped_column(ForeignKey("states.state_id"), nullable=False)

    city: Mapped[str] = mapped_column(String(100), nullable=False)

    state = relationship(
        "State",
        back_populates="distributors",
    )

    sales = relationship(
        "Sale",
        back_populates="distributor",
    )
