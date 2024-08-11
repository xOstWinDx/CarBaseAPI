from abc import ABC, abstractmethod

from src.domain.cars import AbstractCarRepository


class AbstractCarUnitOfWork(ABC):

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        self.cars = AbstractCarRepository()
        return self

    async def __aexit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            await self.commit()
        else:
            await self.rollback()
