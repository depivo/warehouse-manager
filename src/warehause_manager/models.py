from sqlalchemy.orm import Mapped, mapped_column

from warehause_manager.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    quantity: Mapped[int]
    comment: Mapped[str | None]
