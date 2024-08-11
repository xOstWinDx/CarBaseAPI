import logging

from src.domain.cars.entities import FuelType, TransmissionType, Car
from src.domain.cars.interfaces import AbstractCarUnitOfWork

logger = logging.getLogger("domain.cars.service")


class CarService:

    def __init__(self, uow: AbstractCarUnitOfWork):
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
                res = await uow.cars.create_by_data(
                    brand=brand,
                    model=model,
                    year=year,
                    fuel_type=fuel_type,
                    transmission=transmission,
                    mileage=mileage,
                    price=price
                )
                await uow.commit()
                return res
        except Exception as e:
            logger.exception("Exception while creating car: %s", e)
            raise

    async def get_all(self, offset: int, limit: int, **filter_by) -> list[Car]:
        logger.debug("Get all cars: %s", filter_by)
        try:
            async with self.uow as uow:
                res = await uow.cars.get_all(
                    offset=offset,
                    limit=limit,
                    **filter_by
                )
                await uow.commit()
                return res
        except Exception as e:
            logger.exception("Exception while getting all cars: %s", e)
            raise

    async def get_by_id(self, car_id: int):
        logger.debug("Get car by id: %s", id)
        try:
            async with self.uow as uow:
                res = await uow.cars.get_by_id(car_id=car_id)
                await uow.commit()
                return res
        except Exception as e:
            logger.exception("Exception while getting car by id: %s", e)
            raise

    async def update(self, car_id: int, **new_data):
        logger.debug("Update car: %s", car_id)
        try:
            async with self.uow as uow:
                row_count = await uow.cars.update_by_id(car_id=car_id, **new_data)
                await uow.commit()
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
                await uow.commit()
            if row_count == 0:
                raise ValueError("Car not found")
        except Exception as e:
            logger.exception("Exception while deleting car: %s", e)
            raise
