import logging

import bcrypt

from src.domain.users.interfaces import AbstractUserUnitOfWork

logger = logging.getLogger("domain.users.service")


class UserService:
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def get_one_or_none(self, **filter_by):
        async with self.uow as uow:
            user = await uow.users.get_one_or_none(**filter_by)
            await uow.commit()
        return user

    async def register_by_email(
            self,
            email: str,
            name: str,
            password: str | None = None,
    ):
        if await self.is_exists(email=email):
            raise ValueError(f"User with email: {email} already exists")
        return await self.__register(name=name, email=email, password=password)

    async def __register(
            self,
            name: str,
            email: str | None = None,
            password: str | None = None,
            is_admin: bool = False
    ) -> None:
        logger.debug("Add user: %s", id)
        if password is not None:
            password = self._hash_password(password)
        try:
            async with self.uow as uow:
                await uow.users.create_by_data(
                    email=email,
                    name=name,
                    hashed_password=password,
                    is_admin=is_admin
                )
                await uow.commit()
        except Exception as e:
            logger.exception("Exception while adding user: %s", e)
            raise

    @staticmethod
    def _hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    async def is_exists(self, **filter_by) -> bool:
        logger.debug("Check if user exists: %s", filter_by)
        try:
            async with self.uow as uow:
                res = await uow.users.is_exists(**filter_by)
                await uow.commit()
                return res
        except Exception as e:
            logger.exception("Exception while checking if user exists: %s", e)
            raise
