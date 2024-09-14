from dataclasses import dataclass
from typing import Union, get_type_hints

from pydantic import validator, field_validator

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.three_phase.data import ThreePhaseDataContainer
from talking_equipment_sdk.data.enums import DataValueType
from talking_equipment_sdk.data.mixins import UnitConversionMixin


class VoltageData(DataModel, UnitConversionMixin):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit_name: str = 'Volts'
    unit_abbreviation: str = 'V'


class ThreePhaseVoltageData(ThreePhaseDataContainer):
    a: Union[VoltageData, float, int]
    b: Union[VoltageData, float, int]
    c: Union[VoltageData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, VoltageData)