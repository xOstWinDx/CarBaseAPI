import logging

from src.cars.enums import FuelType, TransmissionType
from src.cars.schemas import CarGetSchema
from src.cars.unit_of_work import AbstractUnitOfWork

logger = logging.getLogger("cars.service")


class CarService:

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create(
            self,
            brand: str,
            model: str,
            year: int,
            fuel_type: FuelType,
            transmission: TransmissionType,
            mileage: int,
            price: int
    ) -> int:
        logger.debug(
            "Create car: "
            "brand=%s, "
            "model=%s, "
            "year=%s, "
            "fuel_type=%s, "
            "transmission=%s, "
            "mileage=%s, "
            "price=%s",
            brand, model, year, fuel_type, transmission, mileage, price
        )
        try:
            async with self.uow as uow:
                return await uow.cars.create_by_data(
                    brand=brand,
                    model=model,
                    year=year,
                    fuel_type=fuel_type,
                    transmission=transmission,
                    mileage=mileage,
                    price=price
                )
        except Exception as e:
            logger.exception("Exception while creating car: %s", e)
            raise

    async def get_all(self, offset: int, limit: int, **filter_by) -> list[CarGetSchema]:
        logger.debug("Get all cars: %s", filter_by)
        try:
            async with self.uow as uow:
                return [
                    CarGetSchema.model_validate(car) for car in await uow.cars.get_all(
                        offset=offset,
                        limit=limit,
                        **filter_by
                    )
                ]
        except Exception as e:
            logger.exception("Exception while getting all cars: %s", e)
            raise

    async def get_by_id(self, car_id: int):
        logger.debug("Get car by id: %s", id)
        try:
            async with self.uow as uow:
                return await uow.cars.get_by_id(car_id=car_id)
        except Exception as e:
            logger.exception("Exception while getting car by id: %s", e)
            raise

    async def update(self, car_id: int, **new_data):
        logger.debug("Update car: %s", car_id)
        try:
            async with self.uow as uow:
                row_count = await uow.cars.update_by_id(car_id=car_id, **new_data)
            if row_count == 0:
                raise ValueError("Car not found")
        except Exception as e:
            logger.exception("Exception while updating car: %s", e)
            raise

    async def delete_by_id(self, car_id: int):
        logger.debug("Delete car: %s", car_id)
        try:
            async with self.uow as uow:
                row_count = await uow.cars.delete_by_id(car_id=car_id)
            if row_count == 0:
                raise ValueError("Car not found")
        except Exception as e:
            logger.exception("Exception while deleting car: %s", e)
            raise
