from uuid import uuid4

from talking_equipment_sdk.api.handlers import RequestHandler
from talking_equipment_sdk.data.choices import DataClass
from talking_equipment_sdk.data.data import BaseDataModel
from talking_equipment_sdk.utils import validate_uuid4


class DataSourceRequestHandler(RequestHandler):
    _endpoint_path = 'data_sources'

    @classmethod
    def add_value(cls, pk: uuid4, data: BaseDataModel):
        cls.validate_pk(pk)
        cls.validate_data(data)

        url_path = cls.generate_url_path(pk, 'values')

        body = {
            'data_source_id': pk,
            'data_class_key': DataClass.from_class(data).CLASS_KEY,
            'value': data.value,
            'value_type': data.value_type,
        }

        return cls.post_request(url_path, body)

    @classmethod
    def validate_data(cls, data: BaseDataModel):
        if not isinstance(data, BaseDataModel):
            raise TypeError(
                f'{data} is not an instance of BaseDataModel')

    @classmethod
    def validate_pk(cls, pk: uuid4):
        if not validate_uuid4(pk):
            raise ValueError(f'{pk} is not a valid uuid4')
