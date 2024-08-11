from fastapi import APIRouter, Depends, Query

from src.domain.cars import CarService
from src.infrastructure.uow.car import SqlAlchemyCarUnitOfWork
from src.presentation.api.v1.dependencies import authorization_user, authorization_admin
from src.presentation.api.v1.cars.schemas import CarCreateSchema, FilterSchema, CarGetSchema, CarUpdateSchema
from src.presentation.api.v1.exceptions import NotFoundExc

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("/", status_code=201, description="Create new car")
async def add_car(car_data: CarCreateSchema, _=Depends(authorization_user)) -> int:
    car_service = CarService(uow=SqlAlchemyCarUnitOfWork())
    return await car_service.create(**car_data.model_dump())


@router.get("/{car_id}", response_model=CarGetSchema, description="Get car by id")
async def get_car_by_id(car_id: int, _=Depends(authorization_user)):
    car_service = CarService(uow=SqlAlchemyCarUnitOfWork())
    res = await car_service.get_by_id(car_id)
    if not res:
        raise NotFoundExc("Car not found")
    return res


@router.get("/", response_model=list[CarGetSchema], description="Get all cars")
async def get_all_cars(
        filters: FilterSchema = Depends(),
        offset: int = Query(default=0),
        limit: int = Query(default=10, ge=1, le=100),
        _=Depends(authorization_user)
):
    car_service = CarService(uow=SqlAlchemyCarUnitOfWork())
    res = await car_service.get_all(
        offset=offset,
        limit=limit,
        **filters.model_dump(exclude_none=True)
    )
    return res


@router.patch("/{car_id}", description="Update car by id")
async def update_car(
        car_id: int,
        car_data: CarUpdateSchema,
        _=Depends(authorization_admin)
):
    car_service = CarService(uow=SqlAlchemyCarUnitOfWork())
    try:
        res = await car_service.update(car_id, **car_data.model_dump(exclude_none=True))
        return res
    except ValueError:
        raise NotFoundExc("Car not found")


@router.delete("/{car_id}", description="Delete car by id")
async def delete_car(car_id: int, _=Depends(authorization_admin)):
    car_service = CarService(uow=SqlAlchemyCarUnitOfWork())
    try:
        res = await car_service.delete_by_id(car_id)
        return res
    except ValueError:
        raise NotFoundExc("Car not found")
