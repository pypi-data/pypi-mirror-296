from dataclasses import dataclass
from typing import Union

from pydantic import field_validator

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType
from talking_equipment_sdk.data.three_phase.data import ThreePhaseDataContainer


class TotalHarmonicDistortionData(DataModel):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit_name: str = 'Total Harmonic Distortion'
    unit_abbreviation: str = 'THD'

    def __str__(self):
        return self.auto_scale


class ThreePhaseTotalHarmonicDistortionData(ThreePhaseDataContainer):
    a: Union[TotalHarmonicDistortionData, float, int]
    b: Union[TotalHarmonicDistortionData, float, int]
    c: Union[TotalHarmonicDistortionData, float, int]

    @field_validator('a', 'b', 'c')
    @classmethod
    def validate_a_b_c(cls, v):
        return cls._convert_value(v, TotalHarmonicDistortionData)
