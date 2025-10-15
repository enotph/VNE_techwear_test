from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from .database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False, index = True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable = True)
    price: Mapped[float] = mapped_column(Float, nullable = False)
    category: Mapped[str] = mapped_column(String(50), nullable = False, index = True)
    sizes: Mapped[Optional[str]] = mapped_column(Text, nullable = True)


    def __repr__(self) -> str:
        return f'Product(id = {self.id}, name = "{self.name}", price = {self.price})'
