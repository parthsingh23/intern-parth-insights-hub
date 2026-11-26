from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base import Base


class Region(Base):
    __tablename__ = "regions"

    region_id: Mapped[int] = mapped_column(primary_key=True)
    region_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    states = relationship("State", back_populates="region")
