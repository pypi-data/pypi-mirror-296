from dataclasses import dataclass

from talking_equipment_sdk.data.data import DataModel
from talking_equipment_sdk.data.enums import DataValueType


class ControlData(DataModel):
    value: str
    value_type: DataValueType = DataValueType.STR
    unit_name: str = 'Control'
    unit_abbreviation: str = 'CTRL'

    key: str = 'RelayState1|RelayState2'

    @property
    def values(self) -> list:
        return self.value.split('|')

    @property
    def keys(self) -> list:
        return self.key.split('|')

    def as_dict(self) -> dict:
        return dict(zip(self.keys, self.values))
