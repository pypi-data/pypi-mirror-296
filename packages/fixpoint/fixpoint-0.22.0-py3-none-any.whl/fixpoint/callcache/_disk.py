"""Call cache that stores to disk"""

__all__ = [
    "StepDiskCallCache",
    "TaskDiskCallCache",
]

import json
import tempfile
from typing import Any, Callable, Optional, Type

import diskcache

from fixpoint._constants import (
    DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES as DEFAULT_SIZE_LIMIT_BYTES,
)
from ._shared import (
    CallCache,
    CallCacheKind,
    CacheResult,
    serialize_step_cache_key,
    serialize_task_cache_key,
    serialize_func_cache_key,
    default_json_dumps,
    T,
    logger,
    format_cache_key,
)
from ._converter import value_to_type


def _step_key(run_id: str, step_id: str, args: str) -> str:
    return serialize_step_cache_key(run_id=run_id, step_id=step_id, args=args)


def _task_key(run_id: str, task_id: str, args: str) -> str:
    return serialize_task_cache_key(run_id=run_id, task_id=task_id, args=args)


def _func_key(run_id: str, func_name: str, args: str) -> str:
    return serialize_func_cache_key(run_id=run_id, func_name=func_name, args=args)


class _BaseDiskCallCache(CallCache):
    cache_kind: CallCacheKind

    _ttl_s: Optional[float]
    _cache: diskcache.Cache
    _key_serializer: Callable[[str, str, str], str]

    def __init__(
        self,
        cache: diskcache.Cache,
        cache_kind: CallCacheKind,
        key_serializer: Callable[[str, str, str], str],
        ttl_s: Optional[float] = None,
    ) -> None:
        self._cache = cache
        self._ttl_s = ttl_s
        self.cache_kind = cache_kind
        self._key_serializer = key_serializer

    def check_cache(
        self,
        run_id: str,
        kind_id: str,
        serialized_args: str,
        type_hint: Optional[Type[Any]] = None,
    ) -> CacheResult[T]:
        """Get the cached result, if it exists.

        Check the cache for the cached result for the given run, task/step, and
        arguments. If it exists, return the cached result. Otherwise, return
        None.

        If you provide a `type_hint`, we will load the cached result into that
        type. We can load in Pydantic models and dataclasses.
        """

        key = self._key_serializer(run_id, kind_id, serialized_args)
        formatted_cache_key = format_cache_key(
            self.cache_kind, kind_id, serialized_args
        )
        if key in self._cache:
            logger.debug(f"Cache hit for {formatted_cache_key}")
            return CacheResult[T](
                found=True, result=_deserialize_val(self._cache[key], type_hint)
            )
        logger.debug(f"Cache miss for {formatted_cache_key}")
        return CacheResult[T](found=False, result=None)

    def store_result(
        self, run_id: str, kind_id: str, serialized_args: str, res: Any
    ) -> None:
        """Stores the results of a task or step into the call cache."""
        key = self._key_serializer(run_id, kind_id, serialized_args)
        res_serialized = default_json_dumps(res)
        self._cache.set(key, res_serialized, expire=self._ttl_s)
        formatted_cache_key = format_cache_key(
            self.cache_kind, kind_id, serialized_args
        )
        logger.debug(f"Stored result for {formatted_cache_key}")


class FuncDiskCallCache(_BaseDiskCallCache):
    """An on-disk call-cache for normal functions"""

    def __init__(
        self,
        cache: diskcache.Cache,
        ttl_s: Optional[float] = None,
    ) -> None:
        super().__init__(cache, CallCacheKind.FUNC, _func_key, ttl_s=ttl_s)

    @classmethod
    def from_tmpdir(
        cls,
        ttl_s: Optional[float] = None,
        size_limit_bytes: int = DEFAULT_SIZE_LIMIT_BYTES,
    ) -> "FuncDiskCallCache":
        """Create a new cache from inside a temporary directory"""
        cache_dir = tempfile.mkdtemp()
        cache = diskcache.Cache(directory=cache_dir, size_limit=size_limit_bytes)
        return cls(cache, ttl_s)


class StepDiskCallCache(_BaseDiskCallCache):
    """An on-disk call-cache for steps"""

    def __init__(
        self,
        cache: diskcache.Cache,
        ttl_s: Optional[float] = None,
    ) -> None:
        super().__init__(cache, CallCacheKind.STEP, _step_key, ttl_s=ttl_s)

    @classmethod
    def from_tmpdir(
        cls,
        ttl_s: Optional[float] = None,
        size_limit_bytes: int = DEFAULT_SIZE_LIMIT_BYTES,
    ) -> "StepDiskCallCache":
        """Create a new cache from inside a temporary directory"""
        cache_dir = tempfile.mkdtemp()
        cache = diskcache.Cache(directory=cache_dir, size_limit=size_limit_bytes)
        return cls(cache, ttl_s)


class TaskDiskCallCache(_BaseDiskCallCache):
    """An on-disk call-cache for tasks"""

    def __init__(
        self,
        cache: diskcache.Cache,
        ttl_s: Optional[float] = None,
    ) -> None:
        super().__init__(cache, CallCacheKind.TASK, _task_key, ttl_s=ttl_s)

    @classmethod
    def from_tmpdir(
        cls,
        ttl_s: Optional[float] = None,
        size_limit_bytes: int = DEFAULT_SIZE_LIMIT_BYTES,
    ) -> "TaskDiskCallCache":
        """Create a new cache from inside a temporary directory"""
        cache_dir = tempfile.mkdtemp()
        cache = diskcache.Cache(directory=cache_dir, size_limit=size_limit_bytes)
        return cls(cache, ttl_s)


def _deserialize_val(
    value_str: str,
    type_hint: Optional[Type[Any]] = None,
) -> Any:
    deserialized = json.loads(value_str)
    if type_hint is None:
        return deserialized
    return value_to_type(hint=type_hint, value=deserialized)
