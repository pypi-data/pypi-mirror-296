from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import Union, Type

from pydantic import BaseModel


class DataValueType(StrEnum):
    BOOL = 'bool'
    FLOAT = 'float'
    INT = 'int'
    JSON = 'json'
    STR = 'str'


class UnitScaleValue(BaseModel):
    scale: Union[int, float]
    abbreviation: str


class UnitScaleValues(Enum):
    MICRO = UnitScaleValue(scale=0.000_001, abbreviation='u')
    MILLI = UnitScaleValue(scale=0.001, abbreviation='m')
    KILO = UnitScaleValue(scale=1_000, abbreviation='k')
    MEGA = UnitScaleValue(scale=1_000_000, abbreviation='M')
    GIGA = UnitScaleValue(scale=1_000_000_000, abbreviation='G')
    TERA = UnitScaleValue(scale=1_000_000_000_000, abbreviation='T')
    PETA = UnitScaleValue(scale=1_000_000_000_000_000, abbreviation='P')
    EXA = UnitScaleValue(scale=1_000_000_000_000_000_000, abbreviation='E')

    @property
    def scale(self):
        return self._value_.scale

    @property
    def abbreviation(self):
        return self._value_.abbreviation