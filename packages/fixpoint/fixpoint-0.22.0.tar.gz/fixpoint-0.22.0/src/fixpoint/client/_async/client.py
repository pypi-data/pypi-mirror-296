"""Async client for interacting with the Fixpoint API"""

__all__ = ["AsyncFixpointClient"]

from typing import Optional

import httpx

from .._common import ApiCoreConfig
from ._config import AsyncConfig
from .agents import AsyncAgents
from .human import AsyncHuman
from .documents import AsyncDocuments


class AsyncFixpointClient:
    """Async client for interacting with the Fixpoint API"""

    _config: AsyncConfig
    agents: AsyncAgents
    human: AsyncHuman
    documents: AsyncDocuments

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        *,
        timeout: float = 10.0,
        _transport: Optional[httpx.ASGITransport] = None,
    ):
        core_config = ApiCoreConfig.from_api_info(api_key=api_key, api_url=api_url)
        http_client = httpx.AsyncClient(transport=_transport, timeout=timeout)
        self._config = AsyncConfig(core_config, http_client)
        self.agents = AsyncAgents(self._config)
        self.human = AsyncHuman(self._config)
        self.documents = AsyncDocuments(self._config)

    @property
    def docs(self) -> AsyncDocuments:
        """Async interface for interacting with documents."""
        return self.documents
