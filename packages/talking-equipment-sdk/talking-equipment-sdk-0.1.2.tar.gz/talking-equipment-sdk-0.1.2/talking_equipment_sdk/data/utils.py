import uuid

from talking_equipment_sdk.data.choices import DataClass


def data_class_key_to_data_value_type_value(data_class_key: uuid.uuid4) -> str:
    return DataClass.from_key(data_class_key).CLASS.model_fields['value_type'].default


def data_class_key_to_data_class(data_class_key: uuid.uuid4):
    return DataClass.from_key(data_class_key).CLASS
