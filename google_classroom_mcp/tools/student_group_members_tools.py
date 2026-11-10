"""student_group_members group: create_student_group_member, delete_student_group_member, list_student_group_members"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.student_group_members import (
    CreateStudentGroupMemberData,
    CreateStudentGroupMemberResult,
    DeleteStudentGroupMemberData,
    DeleteStudentGroupMemberResult,
    ListStudentGroupMembersData,
    ListStudentGroupMembersResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.student_group_members")


def register_student_group_members_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_student_group_member",
        description=(
            "Adds a student to a student group and returns the membership. Fails with ALREADY_EXISTS if the "
            "student is already a member."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_student_group_member(
        course_id: str = Field(description="The identifier of the course."),
        student_group_id: str = Field(description="The identifier of the student group."),
        user_id: str = Field(description="Identifier of the student."),
    ) -> CreateStudentGroupMemberResult:
        tlog = ToolLogger(logger, "create_student_group_member")
        if not course_id.strip():
            return _err(CreateStudentGroupMemberResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not student_group_id.strip():
            return _err(CreateStudentGroupMemberResult, tlog, "VALIDATION_ERROR", "student_group_id must not be empty", 400)
        body = {k: v for k, v in {"userId": user_id}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().studentGroups().studentGroupMembers().create(courseId=course_id, studentGroupId=student_group_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateStudentGroupMemberResult(success=True, statusCode=status, data=CreateStudentGroupMemberData(**data))
            return _upstream_err(CreateStudentGroupMemberResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateStudentGroupMemberResult, tlog, exc)

    @mcp.tool(
        name="delete_student_group_member",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a student from "
            "a student group. This action is irreversible — the student's membership in the group (the student "
            "stays enrolled in the course) cannot be recovered. NEVER call this tool autonomously or as part of "
            "an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is "
            "permanent, and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_student_group_member(
        course_id: str = Field(description="The identifier of the course containing the relevant student group."),
        student_group_id: str = Field(description="The identifier of the student group containing the student group member to delete."),
        user_id: str = Field(description="The identifier of the student group member to delete."),
    ) -> DeleteStudentGroupMemberResult:
        tlog = ToolLogger(logger, "delete_student_group_member")
        if not course_id.strip():
            return _err(DeleteStudentGroupMemberResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not student_group_id.strip():
            return _err(DeleteStudentGroupMemberResult, tlog, "VALIDATION_ERROR", "student_group_id must not be empty", 400)
        if not user_id.strip():
            return _err(DeleteStudentGroupMemberResult, tlog, "VALIDATION_ERROR", "user_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().studentGroups().studentGroupMembers().delete(courseId=course_id, studentGroupId=student_group_id, userId=user_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteStudentGroupMemberResult(success=True, statusCode=status, data=DeleteStudentGroupMemberData(deleted=True, courseId=course_id, studentGroupId=student_group_id, userId=user_id))
            return _upstream_err(DeleteStudentGroupMemberResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteStudentGroupMemberResult, tlog, exc)

    @mcp.tool(
        name="list_student_group_members",
        description="Lists the student members of a student group. Returns members plus `nextPageToken` for paging.",
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_student_group_members(
        course_id: str = Field(description="The identifier of the course."),
        student_group_id: str = Field(description="The identifier of the student group."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
    ) -> ListStudentGroupMembersResult:
        tlog = ToolLogger(logger, "list_student_group_members")
        if not course_id.strip():
            return _err(ListStudentGroupMembersResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not student_group_id.strip():
            return _err(ListStudentGroupMembersResult, tlog, "VALIDATION_ERROR", "student_group_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageToken": page_token, "pageSize": page_size}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().studentGroups().studentGroupMembers().list(courseId=course_id, studentGroupId=student_group_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListStudentGroupMembersResult(success=True, statusCode=status, data=ListStudentGroupMembersData(**data))
            return _upstream_err(ListStudentGroupMembersResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListStudentGroupMembersResult, tlog, exc)
