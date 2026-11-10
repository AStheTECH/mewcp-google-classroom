"""teachers group: create_teacher, delete_teacher, get_teacher, list_teachers"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.teachers import (
    CreateTeacherData,
    CreateTeacherResult,
    DeleteTeacherData,
    DeleteTeacherResult,
    GetTeacherData,
    GetTeacherResult,
    ListTeachersData,
    ListTeachersResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.teachers")


def register_teachers_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_teacher",
        description=(
            "Adds a user as a teacher of a course and returns the teacher. Only domain admins can add teachers "
            "directly; other users must send an invitation with create_invitation instead."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_teacher(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        user_id: str | None = Field(default=None, description="Identifier of the user. When specified as a parameter of a request, this identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
    ) -> CreateTeacherResult:
        tlog = ToolLogger(logger, "create_teacher")
        if not course_id.strip():
            return _err(CreateTeacherResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"userId": user_id}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().teachers().create(courseId=course_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateTeacherResult(success=True, statusCode=status, data=CreateTeacherData(**data))
            return _upstream_err(CreateTeacherResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateTeacherResult, tlog, exc)

    @mcp.tool(
        name="delete_teacher",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a teacher from "
            "a course. This action is irreversible — the teacher's membership in the course (they must be "
            "re-added or re-invited to rejoin) cannot be recovered. NEVER call this tool autonomously or as part "
            "of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is "
            "permanent, and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_teacher(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        user_id: str = Field(description="Identifier of the teacher to delete. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
    ) -> DeleteTeacherResult:
        tlog = ToolLogger(logger, "delete_teacher")
        if not course_id.strip():
            return _err(DeleteTeacherResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not user_id.strip():
            return _err(DeleteTeacherResult, tlog, "VALIDATION_ERROR", "user_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().teachers().delete(courseId=course_id, userId=user_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteTeacherResult(success=True, statusCode=status, data=DeleteTeacherData(deleted=True, courseId=course_id, userId=user_id))
            return _upstream_err(DeleteTeacherResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteTeacherResult, tlog, exc)

    @mcp.tool(
        name="get_teacher",
        description=(
            "Retrieves one teacher of a course by user ID or email and returns their profile and course "
            "membership."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_teacher(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        user_id: str = Field(description="Identifier of the teacher to return. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
    ) -> GetTeacherResult:
        tlog = ToolLogger(logger, "get_teacher")
        if not course_id.strip():
            return _err(GetTeacherResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not user_id.strip():
            return _err(GetTeacherResult, tlog, "VALIDATION_ERROR", "user_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().teachers().get(courseId=course_id, userId=user_id))
            if 200 <= status < 300:
                tlog.success()
                return GetTeacherResult(success=True, statusCode=status, data=GetTeacherData(**data))
            return _upstream_err(GetTeacherResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetTeacherResult, tlog, exc)

    @mcp.tool(
        name="list_teachers",
        description=(
            "Lists the teachers of a course that the user can view. Returns teachers plus `nextPageToken` for "
            "paging."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_teachers(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. The default is 30 if unspecified or `0`. The server may return fewer than the specified number of results."),
    ) -> ListTeachersResult:
        tlog = ToolLogger(logger, "list_teachers")
        if not course_id.strip():
            return _err(ListTeachersResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageToken": page_token, "pageSize": page_size}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().teachers().list(courseId=course_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListTeachersResult(success=True, statusCode=status, data=ListTeachersData(**data))
            return _upstream_err(ListTeachersResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListTeachersResult, tlog, exc)
