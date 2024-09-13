"""
This module contains authentication checkers that can call out to other
authentication services.
"""

__all__ = ["AuthChecker", "propel_auth_checker"]

import os
from typing import Any, Dict, Optional
from propelauth_py import init_base_auth, UnauthorizedException, Auth

from fixpoint.types import AsyncFunc
from .auth_info import AuthnInfo


class PropelAuthState:
    """
    This class is used to store the PropelAuth state.
    """

    auth: Optional[Auth] = None

    @classmethod
    def get_auth(cls) -> Auth:
        """
        This method retrieves the PropelAuth state.
        """
        if cls.auth is None:
            auth_url = os.environ["PROPELAUTH_AUTH_URL"]
            api_key = os.environ["PROPELAUTH_API_KEY"]
            cls.auth = init_base_auth(auth_url, api_key)
        return cls.auth


# Takes the API key, and returns True if the key is valid, False otherwise.
AuthChecker = AsyncFunc[[str, Dict[str, Any]], Optional[AuthnInfo]]


async def propel_auth_checker(
    api_key: str, additional_headers: Dict[str, str]
) -> Optional[AuthnInfo]:
    """Authenticate with PropelAuth"""
    auth = PropelAuthState.get_auth()
    user = auth.validate_access_token_and_get_user(api_key)
    org_id = additional_headers.get("x-org-id")
    if org_id is None or org_id == "personal":
        org_id = f"org-user:{user.user_id}"
    else:
        # If the org is not personal, check that the user has access to org
        org = user.get_org(org_id)
        if org is None:
            raise UnauthorizedException("Invalid organization")
        org_id = f"org:{org_id}"
    return AuthnInfo(user_id=user.user_id, org_id=org_id, auth_token=api_key)
