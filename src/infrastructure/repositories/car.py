from typing import Sequence

from sqlalchemy import insert, select, update, delete

from src.domain.cars.entities import Car
from src.domain.cars.repository import AbstractCarRepository


class SqlAlchemyCarRepository(AbstractCarRepository):

    async def create_by_data(self, **car_data) -> int:
        stmt = (
            insert(Car).
            values(**car_data).
            returning(Car.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar()

    async def get_by_id(self, car_id: int) -> Car:
        return await self.session.get(Car, car_id)

    def __init__(self, session):
        self.session = session

    async def get_all(self, offset: int, limit: int, **filter_by) -> Sequence[Car]:
        query = (
            select(Car).
            offset(offset).
            limit(limit)
        )
        filters = []

        for key, value in filter_by.items():
            if key == "max_mileage":
                filters.append(Car <= value)
            elif key == "min_mileage":
                filters.append(Car >= value)
            elif key == "max_price":
                filters.append(Car <= value)
            elif key == "min_price":
                filters.append(Car >= value)
            else:
                filters.append(getattr(Car, key) == value)

        if filters:
            query = query.where(*filters)
        res = await self.session.scalars(query)
        return res.all()

    async def update_by_id(self, car_id: int, **new_data) -> int:
        stmt = (
            update(Car).
            filter_by(id=car_id).
            values(**new_data)
        )
        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore

    async def delete_by_id(self, car_id: int) -> int:
        stmt = (
            delete(Car).
            where(Car.id == car_id)
        )
        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore
