from enum import StrEnum


class FuelType(StrEnum):
    PETROL = "БЕНЗИН"
    DIESEL = "ДИЗЕЛЬ"
    ELECTRIC = "ЭЛЕКТРИЧЕСТВО"
    HYBRID = "ГИБРИД"


class TransmissionType(StrEnum):
    MECHANICAL = "МЕХАНИЧЕСКАЯ"
    AUTOMATIC = "АВТОМАТИЧЕСКАЯ"
    VARIATE = "ВАРИАТОР"
    ROBOT = "РОБОТ"


