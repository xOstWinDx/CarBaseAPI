from abc import ABC, abstractmethod

from src.domain.users.entities import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_by_data(self, **user_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, **filter_by) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def is_exists(self, **filter_by) -> bool:
        raise NotImplementedError
