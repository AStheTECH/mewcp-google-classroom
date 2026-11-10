"""guardian_invitations group: create_guardian_invitation, get_guardian_invitation, list_guardian_invitations, update_guardian_invitation"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.guardian_invitations import (
    CreateGuardianInvitationData,
    CreateGuardianInvitationResult,
    GetGuardianInvitationData,
    GetGuardianInvitationResult,
    GuardianInvitation,
    ListGuardianInvitationsData,
    ListGuardianInvitationsResult,
    UpdateGuardianInvitationData,
    UpdateGuardianInvitationResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.guardian_invitations")


def register_guardian_invitations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_guardian_invitation",
        description=(
            "Creates a guardian invitation for a student and emails the guardian to confirm; once they accept, "
            "the invitation state becomes COMPLETED and a guardian link is created. Only `student_id` and "
            "`invited_email_address` may be set."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_guardian_invitation(
        student_id: str = Field(description="ID of the student (in standard format)"),
        invited_email_address: str = Field(description="Email address that the invitation was sent to. This field is only visible to domain administrators."),
    ) -> CreateGuardianInvitationResult:
        tlog = ToolLogger(logger, "create_guardian_invitation")
        if not student_id.strip():
            return _err(CreateGuardianInvitationResult, tlog, "VALIDATION_ERROR", "student_id must not be empty", 400)
        body = {k: v for k, v in {"invitedEmailAddress": invited_email_address}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.userProfiles().guardianInvitations().create(studentId=student_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateGuardianInvitationResult(success=True, statusCode=status, data=CreateGuardianInvitationData(**data))
            return _upstream_err(CreateGuardianInvitationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateGuardianInvitationResult, tlog, exc)

    @mcp.tool(
        name="get_guardian_invitation",
        description=(
            "Retrieves one guardian invitation by ID and returns its state, invited email address and creation "
            "time."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_guardian_invitation(
        student_id: str = Field(description="The ID of the student whose guardian invitation is being requested."),
        invitation_id: str = Field(description="The `id` field of the `GuardianInvitation` being requested."),
    ) -> GetGuardianInvitationResult:
        tlog = ToolLogger(logger, "get_guardian_invitation")
        if not student_id.strip():
            return _err(GetGuardianInvitationResult, tlog, "VALIDATION_ERROR", "student_id must not be empty", 400)
        if not invitation_id.strip():
            return _err(GetGuardianInvitationResult, tlog, "VALIDATION_ERROR", "invitation_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.userProfiles().guardianInvitations().get(studentId=student_id, invitationId=invitation_id))
            if 200 <= status < 300:
                tlog.success()
                return GetGuardianInvitationResult(success=True, statusCode=status, data=GetGuardianInvitationData(**data))
            return _upstream_err(GetGuardianInvitationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetGuardianInvitationResult, tlog, exc)

    @mcp.tool(
        name="list_guardian_invitations",
        description=(
            "Lists the guardian invitations of a student, filtered by `invited_email_address` and `states`. "
            "Returns invitations plus `nextPageToken` for paging."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_guardian_invitations(
        student_id: str = Field(description="The ID of the student whose guardian invitations are to be returned. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user * the string literal `\"-\"`, indicating that results should be returned for all students that the requesting user is permitted to view guardian invitations."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        invited_email_address: str | None = Field(default=None, description="If specified, only results with the specified `invited_email_address` are returned."),
        states: list[str] | None = Field(default=None, description="If specified, only results with the specified `state` values are returned. Otherwise, results with a `state` of `PENDING` are returned. One of: PENDING, COMPLETE."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
    ) -> ListGuardianInvitationsResult:
        tlog = ToolLogger(logger, "list_guardian_invitations")
        if not student_id.strip():
            return _err(ListGuardianInvitationsResult, tlog, "VALIDATION_ERROR", "student_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageToken": page_token, "invitedEmailAddress": invited_email_address, "states": states, "pageSize": page_size}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.userProfiles().guardianInvitations().list(studentId=student_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListGuardianInvitationsResult(success=True, statusCode=status, data=ListGuardianInvitationsData(**data))
            return _upstream_err(ListGuardianInvitationsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListGuardianInvitationsResult, tlog, exc)

    @mcp.tool(
        name="update_guardian_invitation",
        description=(
            "Withdraws a guardian invitation by changing its `state` from PENDING to COMPLETE, the only supported "
            "change, and returns the invitation. NOTE: this overwrites the current field values — the original "
            "state is not stored by the API after the call. The response includes both the before and after state "
            "so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_guardian_invitation(
        student_id: str = Field(description="The ID of the student whose guardian invitation is to be modified."),
        invitation_id: str = Field(description="The `id` field of the `GuardianInvitation` to be modified."),
        state: str | None = Field(default=None, description="The state that this invitation is in. One of: PENDING, COMPLETE."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateGuardianInvitationResult:
        tlog = ToolLogger(logger, "update_guardian_invitation")
        if not student_id.strip():
            return _err(UpdateGuardianInvitationResult, tlog, "VALIDATION_ERROR", "student_id must not be empty", 400)
        if not invitation_id.strip():
            return _err(UpdateGuardianInvitationResult, tlog, "VALIDATION_ERROR", "invitation_id must not be empty", 400)
        body = {k: v for k, v in {"state": state}.items() if v is not None}
        if not body:
            return _err(UpdateGuardianInvitationResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.userProfiles().guardianInvitations().get(studentId=student_id, invitationId=invitation_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateGuardianInvitationResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.userProfiles().guardianInvitations().patch(studentId=student_id, invitationId=invitation_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateGuardianInvitationResult(success=True, statusCode=status, data=UpdateGuardianInvitationData(before=GuardianInvitation(**before_data), after=GuardianInvitation(**data)))
            return _upstream_err(UpdateGuardianInvitationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateGuardianInvitationResult, tlog, exc)
