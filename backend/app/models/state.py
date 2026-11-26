from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base import Base


class State(Base):
    __tablename__ = "states"

    __table_args__ = (
        UniqueConstraint("state_name", "region_id", name="uq_states_name_region"),
    )

    state_id: Mapped[int] = mapped_column(primary_key=True)

    state_name: Mapped[str] = mapped_column(String(100), nullable=False)

    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.region_id"), nullable=False
    )

    region = relationship("Region", back_populates="states")

    distributors = relationship("Distributor", back_populates="state")
