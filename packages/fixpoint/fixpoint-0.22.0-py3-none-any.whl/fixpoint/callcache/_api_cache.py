"""A callcache that uses the Fixpoint API as a backend"""

__all__ = ["StepApiCallCache", "TaskApiCallCache"]

from typing import Any, Optional, Type

from ._shared import CallCache, CallCacheKind, CacheResult


class StepApiCallCache(CallCache):
    """A step callcache that uses the Fixpoint API as a backend"""

    cache_kind = CallCacheKind.STEP

    _api_key: str
    _api_url: str

    def __init__(self, api_key: str, api_url: str):
        self._api_key = api_key
        self._api_url = api_url

    def check_cache(
        self,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        raise NotImplementedError("Not implemented")

    def store_result(
        self, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        raise NotImplementedError("Not implemented")


class TaskApiCallCache(CallCache):
    """A task callcache that uses the Fixpoint API as a backend"""

    cache_kind = CallCacheKind.TASK

    _api_key: str
    _api_url: str

    def __init__(self, api_key: str, api_url: str):
        self._api_key = api_key
        self._api_url = api_url

    def check_cache(
        self,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        raise NotImplementedError("Not implemented")

    def store_result(
        self, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        raise NotImplementedError("Not implemented")
