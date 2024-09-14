from dataclasses import dataclass
from typing import Union

from pydantic import field_validator

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType
from talking_equipment_sdk.data.mixins import UnitConversionMixin
from talking_equipment_sdk.data.three_phase.data import ThreePhaseDataContainer


class VoltAmpsData(DataModel, UnitConversionMixin):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit_name: str = 'Volt Amps'
    unit_abbreviation: str = 'VA'

    def __post_init__(self):
        self.value = float(self.value)


class ThreePhaseVoltAmpsData(ThreePhaseDataContainer):
    a: Union[VoltAmpsData, float, int]
    b: Union[VoltAmpsData, float, int]
    c: Union[VoltAmpsData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, VoltAmpsData)


class VoltAmpsReactiveData(VoltAmpsData):
    unit: str = 'Volt Amps Reactive'
    unit_abbreviation: str = 'VAR'


class ThreePhaseVoltAmpsReactiveData(ThreePhaseDataContainer):
    a: Union[VoltAmpsReactiveData, float, int]
    b: Union[VoltAmpsReactiveData, float, int]
    c: Union[VoltAmpsReactiveData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, VoltAmpsReactiveData)

