from dataclasses import dataclass
from typing import Union

from pydantic import field_validator

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType
from talking_equipment_sdk.data.mixins import UnitConversionMixin
from talking_equipment_sdk.data.three_phase.data import ThreePhaseDataContainer


class PowerFactorData(DataModel, UnitConversionMixin):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit_name: str = 'Power Factor'
    unit_abbreviation: str = 'PF'

    def __post_init__(self):
        self.value = float(self.value)


class ThreePhasePowerFactorData(ThreePhaseDataContainer):
    a: Union[PowerFactorData, float, int]
    b: Union[PowerFactorData, float, int]
    c: Union[PowerFactorData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, PowerFactorData)