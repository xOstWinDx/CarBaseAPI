from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.cars.repository import AbstractRepository, SqlAlchemyRepository
from src.database import DEFAULT_SESSION_FACTORY


class AbstractUnitOfWork(ABC):

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        self.cars = AbstractRepository()
        return self

    async def __aexit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            await self.commit()
        else:
            await self.rollback()


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        self.session = self.session_factory()
        self.cars = SqlAlchemyRepository(session=self.session)
        return self
