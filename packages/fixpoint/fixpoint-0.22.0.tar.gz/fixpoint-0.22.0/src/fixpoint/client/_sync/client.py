"""Client for interacting with the Fixpoint API"""

__all__ = ["FixpointClient"]

from typing import Optional

import httpx

from .._common import ApiCoreConfig
from ._config import Config
from .agents import Agents
from .human import Human
from .documents import Documents


class FixpointClient:
    """Client for interacting with the Fixpoint API"""

    _config: Config
    agents: Agents
    human: Human
    documents: Documents
    timeout: float = 10.0

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        *,
        timeout: float = 10.0,
        _transport: Optional[httpx.WSGITransport] = None,
    ):
        core_config = ApiCoreConfig.from_api_info(api_key=api_key, api_url=api_url)
        http_client = httpx.Client(transport=_transport, timeout=timeout)
        self._config = Config(core_config, http_client)
        self.agents = Agents(self._config)
        self.human = Human(self._config)
        self.documents = Documents(self._config)

    @property
    def docs(self) -> Documents:
        """Interface to documents."""
        return self.documents
