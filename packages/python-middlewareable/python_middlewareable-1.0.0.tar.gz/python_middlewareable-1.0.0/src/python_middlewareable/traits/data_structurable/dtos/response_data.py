from typing import TypeVar


class ResponseData:
    pass


TResponseData = TypeVar("TResponseData", bound=ResponseData)
