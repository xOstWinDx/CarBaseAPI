from abc import ABC, abstractmethod

from src.domain.users import AbstractUserRepository


class AbstractUserUnitOfWork(ABC):

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        self.users = AbstractUserRepository()
        return self

    async def __aexit__(self, *args):
        await self.rollback()
