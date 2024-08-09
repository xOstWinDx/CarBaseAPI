from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from sqlalchemy import select, insert, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User

T = TypeVar("T")


class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def create_by_data(self, **user_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, **filter_by) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def is_exists(self, **filter_by) -> bool:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_by_data(self, **user_data) -> int:
        res = await self.session.execute(
            insert(User).
            values(user_data).
            returning(User.id)
        )
        return res.scalar()

    async def get_one_or_none(self, **filter_by):
        res = await self.session.scalars(
            select(User).
            filter_by(**filter_by)
        )
        return res.one_or_none()

    async def is_exists(self, **filter_by):
        return await self.session.scalar(
            select(exists(User)).
            filter_by(**filter_by)
        )
