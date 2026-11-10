"""registrations group: create_registration, delete_registration"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.registrations import (
    CreateRegistrationData,
    CreateRegistrationResult,
    DeleteRegistrationData,
    DeleteRegistrationResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.registrations")


def register_registrations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_registration",
        description=(
            "Creates a push-notification registration so Classroom sends the given `feed` to a Cloud Pub/Sub "
            "topic, and returns the registration with its server-assigned ID and expiry. The topic must already "
            "exist and Classroom must be allowed to publish to it."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_registration(
        cloud_pubsub_topic: dict[str, Any] = Field(description="The Cloud Pub/Sub topic that notifications are to be sent to. Keys: topicName."),
        feed: dict[str, Any] = Field(description="Specification for the class of notifications that Classroom should deliver to the destination. Keys: feedType, courseWorkChangesInfo, courseRosterChangesInfo."),
    ) -> CreateRegistrationResult:
        tlog = ToolLogger(logger, "create_registration")
        body = {k: v for k, v in {"cloudPubsubTopic": cloud_pubsub_topic, "feed": feed}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.registrations().create(body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateRegistrationResult(success=True, statusCode=status, data=CreateRegistrationData(**data))
            return _upstream_err(CreateRegistrationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateRegistrationResult, tlog, exc)

    @mcp.tool(
        name="delete_registration",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a "
            "push-notification registration. This action is irreversible — the registration, so Classroom stops "
            "sending notifications for its feed cannot be recovered. NEVER call this tool autonomously or as part "
            "of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is "
            "permanent, and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_registration(
        registration_id: str = Field(description="The `registration_id` of the `Registration` to be deleted."),
    ) -> DeleteRegistrationResult:
        tlog = ToolLogger(logger, "delete_registration")
        if not registration_id.strip():
            return _err(DeleteRegistrationResult, tlog, "VALIDATION_ERROR", "registration_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.registrations().delete(registrationId=registration_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteRegistrationResult(success=True, statusCode=status, data=DeleteRegistrationData(deleted=True, registrationId=registration_id))
            return _upstream_err(DeleteRegistrationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteRegistrationResult, tlog, exc)
