from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from ..dtos.request_data import TRequestData
from ..dtos.response_data import TResponseData
from ..dtos.transport_data import TTransportData


@dataclass
class RequestMixin(Generic[TRequestData, TResponseData, TTransportData]):
    request_data: TRequestData
    response_data: TResponseData
    transport_data: TTransportData


TRequest = TypeVar("TRequest", bound=RequestMixin[Any, Any, Any])
