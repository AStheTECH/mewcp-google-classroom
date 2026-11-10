"""invitations group: accept_invitation, create_invitation, delete_invitation, get_invitation, list_invitations"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.invitations import (
    AcceptInvitationData,
    AcceptInvitationResult,
    CreateInvitationData,
    CreateInvitationResult,
    DeleteInvitationData,
    DeleteInvitationResult,
    GetInvitationData,
    GetInvitationResult,
    Invitation,
    ListInvitationsData,
    ListInvitationsResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.invitations")


def register_invitations_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="accept_invitation",
        description=(
            "Accepts a course invitation, which consumes it and adds the invited user as a teacher or student of "
            "the course. Only the invited user can accept; returns the invitation as it was before. NOTE: this "
            "overwrites the current field values — the original state is not stored by the API after the call. "
            "The response includes both the before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def accept_invitation(
        invitation_id: str = Field(description="Identifier of the invitation to accept."),
    ) -> AcceptInvitationResult:
        tlog = ToolLogger(logger, "accept_invitation")
        if not invitation_id.strip():
            return _err(AcceptInvitationResult, tlog, "VALIDATION_ERROR", "invitation_id must not be empty", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.invitations().get(id=invitation_id))
            if not 200 <= status < 300:
                return _upstream_err(AcceptInvitationResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.invitations().accept(id=invitation_id))
            if not 200 <= status < 300:
                return _upstream_err(AcceptInvitationResult, tlog, status, data, retry_after)
            tlog.success()
            return AcceptInvitationResult(success=True, statusCode=status, data=AcceptInvitationData(before=Invitation(**before_data), accepted=True))
        except Exception as exc:
            return _handle_request_exc(AcceptInvitationResult, tlog, exc)

    @mcp.tool(
        name="create_invitation",
        description=(
            "Creates an invitation for a user to join a course as student, teacher or owner and returns it. Only "
            "one invitation per user and course can exist, so delete and re-create it to change it."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_invitation(
        course_id: str = Field(description="Identifier of the course to invite the user to."),
        role: str = Field(description="Role to invite the user to have. Must not be `COURSE_ROLE_UNSPECIFIED`. One of: STUDENT, TEACHER, OWNER."),
        user_id: str = Field(description="Identifier of the invited user. When specified as a parameter of a request, this identifier can be set to one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
    ) -> CreateInvitationResult:
        tlog = ToolLogger(logger, "create_invitation")
        body = {k: v for k, v in {"courseId": course_id, "role": role, "userId": user_id}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.invitations().create(body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateInvitationResult(success=True, statusCode=status, data=CreateInvitationData(**data))
            return _upstream_err(CreateInvitationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateInvitationResult, tlog, exc)

    @mcp.tool(
        name="delete_invitation",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a course "
            "invitation. This action is irreversible — the pending invitation (a new one must be created to "
            "invite the user again) cannot be recovered. NEVER call this tool autonomously or as part of an "
            "automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, "
            "and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_invitation(
        invitation_id: str = Field(description="Identifier of the invitation to delete."),
    ) -> DeleteInvitationResult:
        tlog = ToolLogger(logger, "delete_invitation")
        if not invitation_id.strip():
            return _err(DeleteInvitationResult, tlog, "VALIDATION_ERROR", "invitation_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.invitations().delete(id=invitation_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteInvitationResult(success=True, statusCode=status, data=DeleteInvitationData(deleted=True, id=invitation_id))
            return _upstream_err(DeleteInvitationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteInvitationResult, tlog, exc)

    @mcp.tool(
        name="get_invitation",
        description="Retrieves one course invitation by ID and returns the invited user, course and role.",
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_invitation(
        invitation_id: str = Field(description="Identifier of the invitation to return."),
    ) -> GetInvitationResult:
        tlog = ToolLogger(logger, "get_invitation")
        if not invitation_id.strip():
            return _err(GetInvitationResult, tlog, "VALIDATION_ERROR", "invitation_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.invitations().get(id=invitation_id))
            if 200 <= status < 300:
                tlog.success()
                return GetInvitationResult(success=True, statusCode=status, data=GetInvitationData(**data))
            return _upstream_err(GetInvitationResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetInvitationResult, tlog, exc)

    @mcp.tool(
        name="list_invitations",
        description=(
            "Lists course invitations the user can view, filtered by `user_id` and `course_id`; at least one of "
            "the two must be provided. Returns invitations plus `nextPageToken`; Google can return an empty page "
            "with a `nextPageToken`, so keep paging until the token is empty."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_invitations(
        user_id: str | None = Field(default=None, description="Restricts returned invitations to those for a specific user. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. The default is 500 if unspecified or `0`. The server may return fewer than the specified number of results."),
        course_id: str | None = Field(default=None, description="Restricts returned invitations to those for a course with the specified identifier."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
    ) -> ListInvitationsResult:
        tlog = ToolLogger(logger, "list_invitations")
        try:
            query = {k: v for k, v in {"userId": user_id, "pageSize": page_size, "courseId": course_id, "pageToken": page_token}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.invitations().list(**query))
            if 200 <= status < 300:
                tlog.success()
                return ListInvitationsResult(success=True, statusCode=status, data=ListInvitationsData(**data))
            return _upstream_err(ListInvitationsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListInvitationsResult, tlog, exc)
