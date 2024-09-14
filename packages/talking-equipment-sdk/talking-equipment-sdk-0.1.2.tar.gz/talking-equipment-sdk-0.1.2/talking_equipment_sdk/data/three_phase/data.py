from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Any, Union

from pydantic import field_validator

from talking_equipment_sdk.data.data import DataModel, DataModelContainer


class ThreePhaseDataContainer(DataModelContainer, ABC):
    a: DataModel
    b: DataModel
    c: DataModel

    def __init__(
            self,
            a: Union[DataModel, float, int],
            b: Union[DataModel, float, int],
            c: Union[DataModel, float, int],
            **kwargs
    ):
        super().__init__(a=a, b=b, c=c, **kwargs)

    @classmethod
    @abstractmethod
    @field_validator('a', 'b', 'c')
    def validate_a_b_c(cls, v): ...

    @property
    def avg(self) -> Union[float, int]:
        return self.average

    @property
    def average(self) -> Union[float, int]:
        return (self.a.value + self.b.value + self.c.value) / 3

    @property
    def min(self) -> Union[float, int]:
        return self.minimum

    @property
    def minimum(self) -> Union[float, int]:
        return min(self.a.value, self.b.value, self.c.value)

    @property
    def max(self) -> Union[float, int]:
        return self.maximum

    @property
    def maximum(self) -> Union[float, int]:
        return max(self.a.value, self.b.value, self.c.value)
