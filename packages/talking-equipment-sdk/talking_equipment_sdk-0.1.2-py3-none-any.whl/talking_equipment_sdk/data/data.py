import json
from abc import ABC, abstractmethod
from typing import Union, Any, Type, ClassVar

from pydantic import BaseModel, field_validator, ValidationError
from talking_equipment_sdk.data.enums import DataValueType


class BaseDataModel(BaseModel, ABC):
    _FIELDS_TO_EXCLUDE: ClassVar[list] = ['value_type', 'unit_name', 'unit_abbreviation', 'type']

    @staticmethod
    def _convert_value(value: Any, data_model_class: Type[BaseModel]) -> Any:
        if value is None or isinstance(value, (dict, list, tuple)):
            return value
        else:
            return value if isinstance(value, data_model_class) else data_model_class(value=value)

    def to_row_value(self) -> dict:
        return self._get_row_list_value()

    @classmethod
    def to_column_header_list(cls) -> list[dict]:
        if cls.model_fields['value_type'].default == DataValueType.JSON:
            return [{'title': 'Date & Time', 'field': 'period'}] + cls._get_column_header_list()
        else:
            return [
                {'title': 'Date & Time', 'field': 'period'},
                {'title': cls.model_fields.get('unit_name').default, 'field': 'value'}
            ]

    def _get_row_list_value(self, value: dict | None = None) -> dict:
        row_data = {}
        items = value.items() if value else self.model_dump().items()
        for key, value in items:
            if isinstance(value, dict):
                if value.get('value_type') == DataValueType.JSON:
                    row_key_data = self._get_row_list_value(value)
                    row_data[key] = row_key_data
                else:
                    if key not in self._FIELDS_TO_EXCLUDE:
                        row_data[key] = value.get('value', None) if value else None
            else:
                if key not in self._FIELDS_TO_EXCLUDE:
                    row_data[key] = value

        return row_data

    @classmethod
    def _get_column_header_list(cls, value: Type['DataModel'] | None = None) -> list[dict]:
        # Override this method on individual data sources to manually define structure of column headers
        column_data = []
        data_source_class = value if value else cls
        items = data_source_class.model_fields.items()

        for field, field_value in items:
            title = field.replace('_', ' ').title()
            if field not in cls._FIELDS_TO_EXCLUDE:
                if data_source_class.model_fields.get('value_type').default == DataValueType.JSON:
                    annotation_class = data_source_class.model_fields.get(field).annotation.__args__[0]
                    
                    if annotation_class.model_fields.get('value_type').default == DataValueType.JSON:
                        group_columns = cls._get_column_header_list(annotation_class)
                        # If we have nested data, we need to format the field values to match
                        # the structure of the column groups. (i.e. 'voltage.a')
                        for column in group_columns:
                            column['field'] = f'{field}.{column["field"]}'

                        column_data.append({'title': title, 'columns': group_columns})
                    else:
                        column_data.append({'title': title, 'field': field})
                else:
                    column_data.append({'title': title, 'field': field})

        return column_data


class DataModel(BaseDataModel, ABC):
    value: Union[int, float, str, bool]
    value_type: DataValueType = None
    unit_name: str = ''
    unit_abbreviation: str = ''

    def __init__(self, value: Union[int, float, str], **kwargs):
        super().__init__(value=value, **kwargs)

    def __str__(self):
        return self.value_verbose

    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        value_type = cls.model_fields['value_type'].default

        if value_type is None:
            raise ValidationError(f'Value type is required for {cls.__name__}')

        if value_type == DataValueType.BOOL:
            return bool(v)

        if value_type == DataValueType.INT:
            return int(v)

        if value_type == DataValueType.FLOAT:
            return float(v)

        if value_type == DataValueType.STR:
            return str(v)

        return v

    @classmethod
    @property
    def value_type_str(cls) -> str:
        return cls.value_type.__name__

    @property
    def value_verbose(self) -> str:
        return f'{self.value}{self.unit_abbreviation}'

    @property
    def value_verbose_full(self) -> str:
        return f'{self.value} {self.unit_name}'

    @property
    def is_bool(self) -> bool:
        return isinstance(self.value, bool)

    @property
    def is_float(self) -> bool:
        return isinstance(self.value, float)

    @property
    def is_int(self) -> bool:
        return isinstance(self.value, int)

    @property
    def is_json(self) -> bool:
        try:
            json.loads(self.value)
            return True
        except ValueError:
            return False

    @property
    def is_str(self) -> bool:
        return isinstance(self.value, str)


class DataModelContainer(BaseDataModel, ABC):
    value_type: DataValueType = DataValueType.JSON

    @property
    def value(self):
        return self.model_dump_json()