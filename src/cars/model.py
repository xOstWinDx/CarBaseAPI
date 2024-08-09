from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseModel, str16


class Car(BaseModel):
    __tablename__ = "cars"

    brand: Mapped[str16] = mapped_column(index=True)
    model: Mapped[str16]
    year: Mapped[int]
    fuel_type: Mapped[str16]  # Были созданы ENUM, но в БД используется просто str (валидация на уровне Pydantic)
    transmission: Mapped[str16]  # что бы избежать проблем с миграциями Alembic (он не удаляет ENUM)
    mileage: Mapped[int]
    price: Mapped[int]
