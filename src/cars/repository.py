from typing import Sequence

from sqlalchemy import select, update, delete

from src.abstract import AbstractCarRepository
from src.cars.model import Car
from src.mixins import PostgresCreateMixin, PostgresReadMixin


class CarPostgresRepository(
    AbstractCarRepository[Car],
    PostgresCreateMixin[Car],
    PostgresReadMixin[Car],
):

    def __init__(self, session):
        super().__init__(session=session, model=Car)

    async def get_all(self, offset: int, limit: int, **filter_by) -> Sequence[Car]:
        query = (
            select(self.model).
            offset(offset).
            limit(limit)
        )
        filters = []

        for key, value in filter_by.items():
            if key == "max_mileage":
                filters.append(self.model.mileage <= value)
            elif key == "min_mileage":
                filters.append(self.model.mileage >= value)
            elif key == "max_price":
                filters.append(self.model.price <= value)
            elif key == "min_price":
                filters.append(self.model.price >= value)
            else:
                filters.append(getattr(self.model, key) == value)

        if filters:
            query = query.where(*filters)
        res = await self.session.scalars(query)
        return res.all()

    async def update_by_id(self, entity_id: int, **new_data) -> int:
        stmt = (
            update(self.model).
            filter_by(id=entity_id).
            values(**new_data)
        )
        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore

    async def delete_by_id(self, entity_id: int) -> int:
        stmt = (
            delete(self.model).
            where(self.model.id == entity_id)
        )
        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore
