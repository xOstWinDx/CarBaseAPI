import pytest
from httpx import AsyncClient

from src.cars.enums import FuelType, TransmissionType


@pytest.mark.parametrize(
    "brand, model, year, fuel_type, transmission, mileage, price, status_code",
    [
        ("brand1", "model1", 2020, FuelType.PETROL, TransmissionType.AUTOMATIC, 100, 10000, 201),
        ("brand2", "model2", 2020, FuelType.DIESEL, TransmissionType.ROBOT, 200, 30000, 201),
        ("brand3", "model3", 1700, FuelType.HYBRID, TransmissionType.AUTOMATIC, 432, 345000, 422),
        ("brand3", "model3", 2022, "IncorrectFuel", TransmissionType.VARIATE, 500, 450000, 422),
        ("brand3", "model3", 2022, FuelType.PETROL, "IncorrectTransmission", 430, 5000000, 422)
    ]
)
async def test_create_car(
        authorized_client: AsyncClient,
        brand: str,
        model: str,
        year: int,
        fuel_type: FuelType,
        transmission: TransmissionType,
        mileage: int,
        price: int,
        status_code: int
):
    response = await authorized_client.post(
        "/cars/",
        json={
            "brand": brand,
            "model": model,
            "year": year,
            "fuel_type": fuel_type,
            "transmission": transmission,
            "mileage": mileage,
            "price": price
        }
    )
    assert response.status_code == status_code


async def test_get_all_cars(authorized_client: AsyncClient):
    response = await authorized_client.get("/cars/")
    assert response.status_code == 200
    assert len(response.json()) >= 4


async def test_update_car(authorized_client: AsyncClient, admin_client: AsyncClient):
    new_data = {
        "brand": "UpdatedBrand",
        "model": "UpdatedModel",
        "year": 2020,
        "fuel_type": FuelType.PETROL,
        "transmission": TransmissionType.AUTOMATIC,
        "mileage": 100,
        "price": 10000
    }
    auth_response = await authorized_client.patch(
        "/cars/1",
        json=new_data
    )
    admin_response = await admin_client.patch(
        "/cars/1",
        json=new_data
    )
    assert auth_response.status_code == 403
    assert admin_response.status_code == 200


async def test_delete_car(authorized_client: AsyncClient, admin_client: AsyncClient):
    auth_response = await authorized_client.delete("/cars/2")
    admin_response = await admin_client.delete("/cars/2")
    assert auth_response.status_code == 403
    assert admin_response.status_code == 200

    get_response = await authorized_client.get("/cars/2")
    assert get_response.status_code == 404