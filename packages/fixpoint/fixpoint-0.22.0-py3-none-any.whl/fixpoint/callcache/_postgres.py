"""A callcache that uses Postgres as a backend"""

__all__ = ["StepPostgresCallCache", "TaskPostgresCallCache"]

from typing import Any, Literal, Optional, Type

from psycopg_pool import ConnectionPool

from ._shared import CallCache, CallCacheKind, CacheResult

CacheBehavior = Literal["unimplemented", "noop"]

_DEFAULT_CACHE_BEHAVIOR: CacheBehavior = "noop"


class StepPostgresCallCache(CallCache):
    """A step callcache that uses Postgres as a backend"""

    cache_kind = CallCacheKind.STEP

    _pg_pool: ConnectionPool
    _cache_behavior: CacheBehavior

    def __init__(
        self,
        pg_pool: ConnectionPool,
        cache_behavior: CacheBehavior = _DEFAULT_CACHE_BEHAVIOR,
    ):
        self._pg_pool = pg_pool
        self._cache_behavior = cache_behavior

    def check_cache(
        self,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        if self._cache_behavior == "unimplemented":
            raise NotImplementedError("Not implemented")
        return CacheResult(found=False, result=None)

    def store_result(
        self, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        if self._cache_behavior == "unimplemented":
            raise NotImplementedError("Not implemented")


class TaskPostgresCallCache(CallCache):
    """A task callcache that uses Postgres as a backend"""

    cache_kind = CallCacheKind.TASK

    _pg_pool: ConnectionPool
    _cache_behavior: CacheBehavior

    def __init__(
        self,
        pg_pool: ConnectionPool,
        cache_behavior: CacheBehavior = _DEFAULT_CACHE_BEHAVIOR,
    ):
        self._pg_pool = pg_pool
        self._cache_behavior = cache_behavior

    def check_cache(
        self,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[Any]:
        """Check if the result of a task or step call is cached"""
        if self._cache_behavior == "unimplemented":
            raise NotImplementedError("Not implemented")
        return CacheResult(found=False, result=None)

    def store_result(
        self, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Store the result of a task or step call"""
        if self._cache_behavior == "unimplemented":
            raise NotImplementedError("Not implemented")
