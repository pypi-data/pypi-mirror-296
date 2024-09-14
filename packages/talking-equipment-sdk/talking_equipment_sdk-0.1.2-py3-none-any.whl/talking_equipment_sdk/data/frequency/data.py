from dataclasses import dataclass
from typing import Union

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType
from talking_equipment_sdk.data.mixins import UnitConversionMixin


class FrequencyData(DataModel, UnitConversionMixin):
    value: Union[float, int]
    value_type: DataValueType = DataValueType.FLOAT
    unit_name: str = 'Hertz'
    unit_abbreviation: str = 'Hz'
