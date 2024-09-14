from dataclasses import dataclass
from typing import Union

from pydantic import field_validator

from talking_equipment_sdk.data.current.data import CurrentData
from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType
from talking_equipment_sdk.data.mixins import UnitConversionMixin
from talking_equipment_sdk.data.three_phase.data import ThreePhaseDataContainer
from talking_equipment_sdk.data.voltage.data import VoltageData


class WattsData(DataModel, UnitConversionMixin):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit_name: str = 'Watts'
    unit_abbreviation: str = 'W'

    def to_voltage(self, current: CurrentData) -> float:
        return self.value / current.value

    def to_current(self, voltage: VoltageData) -> float:
        return self.value / voltage.value

    def set_from_voltage_and_current(self, voltage: VoltageData, current: CurrentData):
        self.value = voltage.value * current.value


class ThreePhaseWattsData(ThreePhaseDataContainer):
    a: Union[WattsData, float, int]
    b: Union[WattsData, float, int]
    c: Union[WattsData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, WattsData)


class WattHoursData(WattsData):
    unit: str = 'Watt Hours'
    unit_abbreviation: str = 'Wh'


class ThreePhaseWattHoursData(ThreePhaseDataContainer):
    a: Union[WattHoursData, float, int]
    b: Union[WattHoursData, float, int]
    c: Union[WattHoursData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, WattHoursData)