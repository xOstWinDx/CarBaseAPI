from sqlalchemy import insert, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.entities import User
from src.domain.users.repository import AbstractUserRepository


class SqlAlchemyUserRepository(AbstractUserRepository):
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
