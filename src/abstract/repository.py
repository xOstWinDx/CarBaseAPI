from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Sequence

from src.database import BaseModel

T = TypeVar('T', bound=BaseModel)


class AbstractCreateRepository(Generic[T], ABC):
    @abstractmethod
    async def create_by_data(self, **entity_data) -> int:
        raise NotImplementedError


class AbstractReadRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get_one_or_none(self, **filter_by) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **filter_by) -> Sequence[T]:
        raise NotImplementedError


class AbstractUpdateRepository(Generic[T], ABC):
    @abstractmethod
    async def update_by_id(self, entity_id: int, **new_data) -> int:
        raise NotImplementedError


class AbstractDeleteRepository(Generic[T], ABC):
    @abstractmethod
    async def delete_by_id(self, entity_id: int) -> int:
        raise NotImplementedError


class AbstractExistsRepository(Generic[T], ABC):

    @abstractmethod
    async def is_exists(self, **filter_by) -> bool:
        raise NotImplementedError


class AbstractAuthRepository(
    AbstractCreateRepository[T],
    AbstractReadRepository[T],
    AbstractExistsRepository[T], ABC
):
    ...


class AbstractCarRepository(
    AbstractCreateRepository[T],
    AbstractReadRepository[T],
    AbstractUpdateRepository[T],
    AbstractDeleteRepository[T],
    ABC
):
    @abstractmethod
    async def get_all(self, offset: int, limit: int, **filter_by) -> Sequence[T]: ...
