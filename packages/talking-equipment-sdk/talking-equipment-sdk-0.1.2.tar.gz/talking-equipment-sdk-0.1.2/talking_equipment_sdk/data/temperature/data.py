from dataclasses import dataclass
from enum import Enum
from typing import Union

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType


class TemperatureType(Enum):
    CELSIUS = 1
    FAHRENHEIT = 0


class TemperatureData(DataModel):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit_name: str = 'Temperature'
    unit_abbreviation: str = 'TEMP'

    type: TemperatureType = TemperatureType.CELSIUS

    @property
    def celsius(self) -> float:
        if self.type == TemperatureType.FAHRENHEIT:
            return (self.value - 32) * 5 / 9
        elif self.type == TemperatureType.CELSIUS:
            return self.value

    @property
    def fahrenheit(self) -> float:
        if self.type == TemperatureType.CELSIUS:
            return self.value * 9 / 5 + 32
        elif self.type == TemperatureType.FAHRENHEIT:
            return self.value

