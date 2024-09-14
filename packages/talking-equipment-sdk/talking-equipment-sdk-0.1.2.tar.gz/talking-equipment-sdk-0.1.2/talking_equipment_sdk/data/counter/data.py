from dataclasses import dataclass
from typing import Union

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType


class CounterData(DataModel):
    value: Union[int, float]
    value_type: DataValueType = DataValueType.INT
    unit_name: str = 'Count'
    unit_abbreviation: str = 'CNT'
