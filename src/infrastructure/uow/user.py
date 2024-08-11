from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database import DEFAULT_SESSION_FACTORY
from src.domain.users import AbstractUserUnitOfWork
from src.infrastructure.repositories import SqlAlchemyUserRepository


class SqlAlchemyUserUnitOfWork(AbstractUserUnitOfWork):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = SqlAlchemyUserRepository(session=self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
