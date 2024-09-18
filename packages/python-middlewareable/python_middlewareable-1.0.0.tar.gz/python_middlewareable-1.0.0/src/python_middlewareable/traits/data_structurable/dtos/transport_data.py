from typing import TypeVar


class TransportData:
    pass


TTransportData = TypeVar("TTransportData", bound=TransportData)
