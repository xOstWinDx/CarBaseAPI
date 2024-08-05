from fastapi import Query, HTTPException
from pydantic import BaseModel, Field

from src.cars.enums import FuelType, TransmissionType
from src.schemas import BaseSchema


class CarCreateSchema(BaseModel):
    brand: str = Field(max_length=16, min_length=3)
    model: str = Field(max_length=16, min_length=3)
    year: int = Field(ge=1900)
    fuel_type: FuelType
    transmission: TransmissionType
    mileage: int = Field(ge=0)
    price: int = Field(gt=0)


class CarUpdateSchema(CarCreateSchema):
    brand: str | None = Field(default=None, max_length=16, min_length=3)
    model: str | None = Field(max_length=16, min_length=3)
    year: int | None = Field(default=None, ge=1900)
    fuel_type: FuelType | None = None
    transmission: TransmissionType | None = None
    mileage: int | None = Field(default=None, ge=0)
    price: int | None = Field(default=None, gt=0)


class CarGetSchema(CarCreateSchema, BaseSchema):
    ...


class FilterSchema:
    def __init__(
            self,
            brand: str | None = Query(default=None, max_length=16, min_length=3),
            model: str | None = Query(default=None, max_length=16, min_length=3),
            year: int | None = Query(default=None, ge=1900),
            fuel_type: FuelType | None = Query(default=None),
            transmission: TransmissionType | None = Query(default=None),
            min_price: int | None = Query(default=None, ge=0),
            max_price: int | None = Query(default=None),
            min_mileage: int | None = Query(default=None, ge=0),
            max_mileage: int | None = Query(default=None)
    ):
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel_type = fuel_type
        self.transmission = transmission
        self.min_price = min_price
        self.max_price = max_price
        self.min_mileage = min_mileage
        self.max_mileage = max_mileage

        self.validate()

    def validate(self):
        if self.min_price is not None and self.max_price is not None and self.min_price > self.max_price:
            raise HTTPException(status_code=400, detail='min_price must be less than or equal to max_price')
        if self.min_mileage is not None and self.max_mileage is not None and self.min_mileage > self.max_mileage:
            raise HTTPException(status_code=400, detail='min_mileage must be less than or equal to max_mileage')

    def model_dump(self, exclude_none: bool = False) -> dict:
        data = {
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'min_mileage': self.min_mileage,
            'max_mileage': self.max_mileage,
        }
        if exclude_none:
            return {k: v for k, v in data.items() if v is not None}
        return data
