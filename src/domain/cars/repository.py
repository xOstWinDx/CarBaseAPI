from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.cars.entities import Car


class AbstractCarRepository(ABC):
    @abstractmethod
    async def create_by_data(self, **car_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, car_id: int) -> Car:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int, limit: int, **filter_by) -> Sequence[Car]:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, car_id: int, **new_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, car_id: int) -> int:
        raise NotImplementedError
