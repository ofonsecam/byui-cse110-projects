"""
Modelos SQLAlchemy para la base de datos.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Product(Base):
    """Tabla de productos del inventario (esquema público)."""

    __tablename__ = "products"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        return f"Product(product_id={self.product_id!r}, name={self.name!r}, quantity={self.quantity})"
