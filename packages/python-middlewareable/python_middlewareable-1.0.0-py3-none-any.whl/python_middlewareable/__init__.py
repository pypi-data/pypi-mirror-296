from .middleware import Middleware as MiddlewareBase
from .middleware import MiddlewareNextCall as MiddlewareNextCallBase
from .request import Request as RequestBase
from .middlewareable import Middlewareable as MiddlewareableBase
from .traits.data_structurable.data_structurable import DataStructurable
from .traits.data_structurable.mixins.request_mixin import (
    RequestMixin as DataStructurableRequestMixin,
)
from .traits.data_structurable.dtos.request_data import (
    RequestData as RequestDataBase,
)
from .traits.data_structurable.dtos.response_data import (
    ResponseData as ResponseDataBase,
)
from .traits.data_structurable.dtos.transport_data import (
    TransportData as TransportDataBase,
)
from .traits.auto_instantiable.auto_instantiable import AutoInstantiable

# Version of the package
# DO NOT MODIFY MANUALLY
# This will be updated by `bumpver` command.
# - Make sure to commit all changes first before running `bumpver`.
# - Run `bumpver update --[minor|major|patch]`
__version__ = "1.0.0"

__all__ = [
    # Core
    "MiddlewareBase",
    "MiddlewareNextCallBase",
    "MiddlewareableBase",
    "RequestBase",
    # `DataStructurable` trait
    "DataStructurable",
    "DataStructurableRequestMixin",
    "RequestDataBase",
    "ResponseDataBase",
    "TransportDataBase",
    # `AutoInstantiable` trait
    "AutoInstantiable",
]
