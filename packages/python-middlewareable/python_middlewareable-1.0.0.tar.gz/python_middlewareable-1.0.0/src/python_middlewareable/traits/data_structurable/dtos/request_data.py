from abc import ABC
from typing import TypeVar


class RequestData(ABC):
    pass


TRequestData = TypeVar("TRequestData", bound=RequestData)
