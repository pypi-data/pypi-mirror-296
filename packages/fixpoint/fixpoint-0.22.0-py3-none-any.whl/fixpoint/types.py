"""Types for the Fixpoint package"""

__all__ = [
    "AsyncFunc",
    "AwaitableRet",
    "ListResponse",
    "Params",
    "Ret_co",
    "Ret",
]

from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Generic,
    List,
    Literal,
    Optional,
    ParamSpec,
    TypeVar,
)

from pydantic import BaseModel, Field


BM = TypeVar("BM", bound=BaseModel)
Params = ParamSpec("Params")
Ret = TypeVar("Ret")
Ret_co = TypeVar("Ret_co", covariant=True)
AwaitableRet = TypeVar("AwaitableRet", bound=Awaitable[Any])
AsyncFunc = Callable[Params, Coroutine[Any, Any, Ret]]


# TODO(jakub): Add total number of results and pages to the API below
class ListResponse(BaseModel, Generic[BM]):
    """An API list response"""

    data: List[BM] = Field(description="The list of items")
    next_page_token: Optional[str] = Field(
        default=None,
        description="Token to get the next page of results. If no more pages, it is None",
    )
    kind: Literal["list"] = "list"
