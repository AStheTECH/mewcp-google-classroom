"""guardians group: delete_guardian, get_guardian, list_guardians"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.guardians import (
    DeleteGuardianData,
    DeleteGuardianResult,
    GetGuardianData,
    GetGuardianResult,
    ListGuardiansData,
    ListGuardiansResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.guardians")


def register_guardians_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="delete_guardian",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a guardian "
            "link. This action is irreversible — the guardian's access, so they stop receiving guardian "
            "notifications and can no longer be retrieved through the API cannot be recovered. NEVER call this "
            "tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be "
            "deleted and that it is permanent, and wait for their explicit written confirmation before "
            "proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_guardian(
        student_id: str = Field(description="The student whose guardian is to be deleted. One of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
        guardian_id: str = Field(description="The `id` field from a `Guardian`."),
    ) -> DeleteGuardianResult:
        tlog = ToolLogger(logger, "delete_guardian")
        if not student_id.strip():
            return _err(DeleteGuardianResult, tlog, "VALIDATION_ERROR", "student_id must not be empty", 400)
        if not guardian_id.strip():
            return _err(DeleteGuardianResult, tlog, "VALIDATION_ERROR", "guardian_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.userProfiles().guardians().delete(studentId=student_id, guardianId=guardian_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteGuardianResult(success=True, statusCode=status, data=DeleteGuardianData(deleted=True, studentId=student_id, guardianId=guardian_id))
            return _upstream_err(DeleteGuardianResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteGuardianResult, tlog, exc)

    @mcp.tool(
        name="get_guardian",
        description=(
            "Retrieves one guardian of a student by guardian ID and returns the guardian's profile and invited "
            "email address."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_guardian(
        student_id: str = Field(description="The student whose guardian is being requested. One of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
        guardian_id: str = Field(description="The `id` field from a `Guardian`."),
    ) -> GetGuardianResult:
        tlog = ToolLogger(logger, "get_guardian")
        if not student_id.strip():
            return _err(GetGuardianResult, tlog, "VALIDATION_ERROR", "student_id must not be empty", 400)
        if not guardian_id.strip():
            return _err(GetGuardianResult, tlog, "VALIDATION_ERROR", "guardian_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.userProfiles().guardians().get(studentId=student_id, guardianId=guardian_id))
            if 200 <= status < 300:
                tlog.success()
                return GetGuardianResult(success=True, statusCode=status, data=GetGuardianData(**data))
            return _upstream_err(GetGuardianResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetGuardianResult, tlog, exc)

    @mcp.tool(
        name="list_guardians",
        description=(
            "Lists the guardians of a student, optionally filtered by `invited_email_address`. Pass `-` as "
            "`student_id` to span every student the user can view guardians for. Returns guardians plus "
            "`nextPageToken`."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_guardians(
        student_id: str = Field(description="Filter results by the student who the guardian is linked to. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user * the string literal `\"-\"`, indicating that results should be returned for all students that the requesting user has access to view."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        invited_email_address: str | None = Field(default=None, description="Filter results by the email address that the original invitation was sent to, resulting in this guardian link. This filter can only be used by domain administrators."),
    ) -> ListGuardiansResult:
        tlog = ToolLogger(logger, "list_guardians")
        if not student_id.strip():
            return _err(ListGuardiansResult, tlog, "VALIDATION_ERROR", "student_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageSize": page_size, "pageToken": page_token, "invitedEmailAddress": invited_email_address}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.userProfiles().guardians().list(studentId=student_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListGuardiansResult(success=True, statusCode=status, data=ListGuardiansData(**data))
            return _upstream_err(ListGuardiansResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListGuardiansResult, tlog, exc)
