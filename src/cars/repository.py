from abc import ABC, abstractmethod
from typing import Sequence, Generic, TypeVar

from sqlalchemy import select, update, delete, insert

from src.cars.model import Car

T = TypeVar("T")


class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def create_by_data(self, **car_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, car_id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int, limit: int, **filter_by) -> Sequence[T]:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, car_id: int, **new_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, car_id: int) -> int:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository[Car]):

    async def create_by_data(self, **car_data) -> int:
        stmt = (
            insert(Car).
            values(**car_data).
            returning(Car.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar()

    async def get_by_id(self, car_id: int) -> T:
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
