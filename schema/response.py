from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel
from fastapi import Request

from api.exceptions import BaseAPIException

DataType = TypeVar("DataType")


class IResponseBase(GenericModel, Generic[DataType]):
    message: str = ""
    data: Optional[DataType] = None


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


class ErrorResponse:
    def __init__(self, exc: BaseAPIException, request: Request):
        self.message = exc.message
        self.method = request.method
        self.path = str(request.url)
        self.detailed = exc.__dict__
