from typing import Generic, cast

from ...middlewareable import Middlewareable
from ..data_structurable.data_structurable import DataStructurable
from ..data_structurable.dtos.request_data import RequestData
from ..data_structurable.dtos.response_data import TResponseData
from ..data_structurable.dtos.transport_data import TTransportData
from ..data_structurable.mixins.request_mixin import TRequest


class AutoInstantiable(
    DataStructurable,
    Generic[TRequest, TResponseData, TTransportData],
):
    request_class: type[TRequest]
    response_data_class: type[TResponseData]
    transport_data_class: type[TTransportData]

    async def process_middlewares_from_payload(
        self,
        data: RequestData,
    ) -> TResponseData:
        this = cast(Middlewareable[TRequest], self)  # type: ignore

        request = self.make_request(request_data=data)

        result = await this.process_middlewares(request)

        return self.extract_response_data(result)

    def extract_response_data(self, request: TRequest) -> TResponseData:
        return request.response_data

    def make_request(self, request_data: RequestData) -> TRequest:
        return self.request_class(
            request_data=request_data,
            response_data=self.make_response_data(),
            transport_data=self.make_transport_data(),
        )

    def make_response_data(self) -> TResponseData:
        return self.response_data_class()

    def make_transport_data(self) -> TTransportData:
        return self.transport_data_class()
