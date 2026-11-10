"""user_profiles group: get_user_profile"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.user_profiles import (
    GetUserProfileData,
    GetUserProfileResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.user_profiles")


def register_user_profiles_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_user_profile",
        description=(
            "Retrieves the profile of a user by ID, email or `me` and returns their name and, with the matching "
            "scopes, email address and photo URL."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_user_profile(
        user_id: str = Field(description="Identifier of the profile to return. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
    ) -> GetUserProfileResult:
        tlog = ToolLogger(logger, "get_user_profile")
        if not user_id.strip():
            return _err(GetUserProfileResult, tlog, "VALIDATION_ERROR", "user_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.userProfiles().get(userId=user_id))
            if 200 <= status < 300:
                tlog.success()
                return GetUserProfileResult(success=True, statusCode=status, data=GetUserProfileData(**data))
            return _upstream_err(GetUserProfileResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetUserProfileResult, tlog, exc)
