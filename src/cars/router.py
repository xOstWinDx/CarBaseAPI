from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import authorization_user, authorization_admin
from src.cars.repository import CarPostgresRepository
from src.cars.schemas import CarCreateSchema, FilterSchema, CarGetSchema, CarUpdateSchema
from src.cars.service import CarService
from src.database import get_async_session
from src.exceptions import NotFoundExc

router = APIRouter(prefix="/cars")


@router.post("/", status_code=201)
async def add_car(
        car_data: CarCreateSchema,
        session: AsyncSession = Depends(get_async_session),
        _=Depends(authorization_user)
):
    car_service = CarService(CarPostgresRepository(session))
    try:
        res = await car_service.create(**car_data.model_dump())
        await session.commit()
        return res
    except Exception:
        await session.rollback()
        raise


@router.get("/{car_id}", response_model=CarGetSchema)
async def get_car_by_id(
        car_id: int,
        session: AsyncSession = Depends(get_async_session),
        _=Depends(authorization_user)
):
    car_service = CarService(CarPostgresRepository(session))
    try:
        res = await car_service.get_by_id(car_id)
        if not res:
            raise NotFoundExc("Car not found")
        return res
    except Exception:
        await session.rollback()
        raise


@router.get("/", response_model=list[CarGetSchema])
async def get_all_cars(
        filters: FilterSchema = Depends(),
        session: AsyncSession = Depends(get_async_session),
        offset: int = Query(default=0),
        limit: int = Query(default=10, ge=1, le=100),
        _=Depends(authorization_user)
):
    car_service = CarService(CarPostgresRepository(session))
    try:
        res = await car_service.get_all(
            offset=offset,
            limit=limit,
            **filters.model_dump(exclude_none=True)
        )
        return res
    except Exception:
        await session.rollback()
        raise


@router.patch("/{car_id}")
async def update_car(
        car_id: int,
        car_data: CarUpdateSchema,
        session: AsyncSession = Depends(get_async_session),
        _=Depends(authorization_admin)
):
    car_service = CarService(CarPostgresRepository(session))
    try:
        res = await car_service.update(car_id, **car_data.model_dump(exclude_none=True))
        await session.commit()
        return res
    except ValueError:
        raise NotFoundExc("Car not found")
    except Exception:
        await session.rollback()
        raise


@router.delete("/{car_id}")
async def delete_car(
        car_id: int,
        session: AsyncSession = Depends(get_async_session),
        _=Depends(authorization_admin)
):
    car_service = CarService(CarPostgresRepository(session))
    try:
        res = await car_service.delete_by_id(car_id)
        await session.commit()
        return res
    except ValueError:
        raise NotFoundExc("Car not found")
    except Exception:
        await session.rollback()
        raise
