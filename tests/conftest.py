from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.cars.entities import FuelType, TransmissionType
from src.domain.cars.entities import Car
from src.config import CONFIG
from src.domain.users.entities import User
from src.database import DEFAULT_SESSION_FACTORY, engine, BaseModel

from src.presentation.api.v1.auth.dependencies import encode_jwt
from src.presentation.api.v1.auth.schemas import JwtPayloadSchema

from src.main import app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    assert CONFIG.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    async with DEFAULT_SESSION_FACTORY() as session:
        admin_user = User(
            email="admin@admin.com",
            name="Admin",
            is_admin=True,
        )
        base_user = User(
            email="base@base.com",
            name="Base",
            is_admin=False,
        )
        session.add(admin_user)
        session.add(base_user)

        first_car = Car(
            brand="Toyota",
            model="Camry",
            year=2022,
            fuel_type=FuelType.PETROL,
            transmission=TransmissionType.AUTOMATIC,
            mileage=500,
            price=1200000,

        )
        second_car = Car(
            brand="Mazda",
            model="CX-5",
            year=2022,
            fuel_type=FuelType.DIESEL,
            transmission=TransmissionType.ROBOT,
            mileage=250,
            price=1200000,

        )
        session.add(first_car)
        session.add(second_car)

        await session.commit()
    yield


@pytest.fixture(scope="session")
async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with DEFAULT_SESSION_FACTORY() as session:
        yield session


@pytest.fixture(scope="function")
async def unauthorized_client() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1"
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_client(unauthorized_client: AsyncClient) -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1"
    ) as client:
        client.cookies.set("token", encode_jwt(payload=JwtPayloadSchema(id=1, name="Admin")))
        yield client


@pytest.fixture(scope="function")
async def authorized_client(unauthorized_client: AsyncClient) -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1"
    ) as client:
        client.cookies.set("token", encode_jwt(payload=JwtPayloadSchema(id=2, name="Base")))
        yield client
