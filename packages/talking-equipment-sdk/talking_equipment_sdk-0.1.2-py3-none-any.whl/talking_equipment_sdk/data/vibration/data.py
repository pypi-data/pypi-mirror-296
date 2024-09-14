from dataclasses import dataclass

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType



class VibrationData(DataModel):
    value: str
    value_type: DataValueType = DataValueType.STR
    unit_name: str = 'Vibration'
    unit_abbreviation: str = 'VIBR'

    key: str = 'X-Axis Speed|Y-Axis Speed|Z-Axis Speed|X-Axis Frequency|Y-Axis Frequency|Z-Axis Frequency|Duty Cycle'

    @property
    def values(self) -> list:
        return self.value.split('|')

    @property
    def keys(self) -> list:
        return self.key.split('|')

    def as_dict(self) -> dict:
        return dict(zip(self.keys, self.values))