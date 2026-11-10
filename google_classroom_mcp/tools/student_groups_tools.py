"""student_groups group: create_student_group, delete_student_group, list_student_groups, update_student_group"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.student_groups import (
    CreateStudentGroupData,
    CreateStudentGroupResult,
    DeleteStudentGroupData,
    DeleteStudentGroupResult,
    ListStudentGroupsData,
    ListStudentGroupsResult,
    StudentGroup,
    UpdateStudentGroupData,
    UpdateStudentGroupResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.student_groups")


def register_student_groups_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_student_group",
        description="Creates a student group in a course and returns it.",
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_student_group(
        course_id: str = Field(description="The identifier of the course."),
        title: str = Field(description="The title of the student group."),
    ) -> CreateStudentGroupResult:
        tlog = ToolLogger(logger, "create_student_group")
        if not course_id.strip():
            return _err(CreateStudentGroupResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"title": title}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().studentGroups().create(courseId=course_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateStudentGroupResult(success=True, statusCode=status, data=CreateStudentGroupData(**data))
            return _upstream_err(CreateStudentGroupResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateStudentGroupResult, tlog, exc)

    @mcp.tool(
        name="delete_student_group",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a student "
            "group. This action is irreversible — the group and its memberships (the students stay enrolled in "
            "the course) cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. "
            "You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for "
            "their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_student_group(
        course_id: str = Field(description="The identifier of the course containing the student group to delete."),
        student_group_id: str = Field(description="The identifier of the student group to delete."),
    ) -> DeleteStudentGroupResult:
        tlog = ToolLogger(logger, "delete_student_group")
        if not course_id.strip():
            return _err(DeleteStudentGroupResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not student_group_id.strip():
            return _err(DeleteStudentGroupResult, tlog, "VALIDATION_ERROR", "student_group_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().studentGroups().delete(courseId=course_id, id=student_group_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteStudentGroupResult(success=True, statusCode=status, data=DeleteStudentGroupData(deleted=True, courseId=course_id, id=student_group_id))
            return _upstream_err(DeleteStudentGroupResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteStudentGroupResult, tlog, exc)

    @mcp.tool(
        name="list_student_groups",
        description="Lists the student groups of a course. Returns groups plus `nextPageToken` for paging.",
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_student_groups(
        course_id: str = Field(description="The identifier of the course."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum, which is currently set to 75 items. The server may return fewer than the specified number of results."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
    ) -> ListStudentGroupsResult:
        tlog = ToolLogger(logger, "list_student_groups")
        if not course_id.strip():
            return _err(ListStudentGroupsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageSize": page_size, "pageToken": page_token}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().studentGroups().list(courseId=course_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListStudentGroupsResult(success=True, statusCode=status, data=ListStudentGroupsData(**data))
            return _upstream_err(ListStudentGroupsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListStudentGroupsResult, tlog, exc)

    @mcp.tool(
        name="update_student_group",
        description=(
            "Updates the provided fields of a student group (its title) and returns the updated group. NOTE: this "
            "overwrites the current field values — the original state is not stored by the API after the call. "
            "The response includes both the before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_student_group(
        course_id: str = Field(description="Identifier of the course."),
        student_group_id: str = Field(description="Identifier of the student group."),
        title: str | None = Field(default=None, description="The title of the student group."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateStudentGroupResult:
        tlog = ToolLogger(logger, "update_student_group")
        if not course_id.strip():
            return _err(UpdateStudentGroupResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not student_group_id.strip():
            return _err(UpdateStudentGroupResult, tlog, "VALIDATION_ERROR", "student_group_id must not be empty", 400)
        body = {k: v for k, v in {"title": title}.items() if v is not None}
        if not body:
            return _err(UpdateStudentGroupResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data: dict[str, Any] = {}
            page_token = None
            for _ in range(20):
                page, status, retry_after = service.execute(
                    lambda s: s.courses().studentGroups().list(courseId=course_id, pageSize=100, **({"pageToken": page_token} if page_token else {}))
                )
                if not 200 <= status < 300:
                    return _upstream_err(UpdateStudentGroupResult, tlog, status, page, retry_after)
                before_data = next((g for g in page.get("studentGroups", []) if g.get("id") == student_group_id), {})
                page_token = page.get("nextPageToken")
                if before_data or not page_token:
                    break
            if not before_data:
                return _err(UpdateStudentGroupResult, tlog, "NOT_FOUND", "Student group not found in this course", 404)
            data, status, retry_after = service.execute(lambda s: s.courses().studentGroups().patch(courseId=course_id, id=student_group_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateStudentGroupResult(success=True, statusCode=status, data=UpdateStudentGroupData(before=StudentGroup(**before_data), after=StudentGroup(**data)))
            return _upstream_err(UpdateStudentGroupResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateStudentGroupResult, tlog, exc)
