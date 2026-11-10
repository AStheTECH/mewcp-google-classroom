"""students group: create_student, delete_student, get_student, list_students"""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.students import (
    CreateStudentData,
    CreateStudentResult,
    DeleteStudentData,
    DeleteStudentResult,
    GetStudentData,
    GetStudentResult,
    ListStudentsData,
    ListStudentsResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.students")


def register_students_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_student",
        description=(
            "Adds a user as a student of a course and returns the student. Domain admins can add any user in "
            "their domain directly; students can add themselves by passing the course's `enrollment_code`."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_student(
        course_id: str = Field(description="Identifier of the course to create the student in. This identifier can be either the Classroom-assigned identifier or an alias."),
        user_id: str = Field(description="Identifier of the user. When specified as a parameter of a request, this identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
        enrollment_code: str | None = Field(default=None, description="Enrollment code of the course to create the student in. This code is required if userId corresponds to the requesting user; it may be omitted if the requesting user has administrative permissions to create students for any user."),
    ) -> CreateStudentResult:
        tlog = ToolLogger(logger, "create_student")
        if not course_id.strip():
            return _err(CreateStudentResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"userId": user_id}.items() if v is not None}
        try:
            query = {k: v for k, v in {"enrollmentCode": enrollment_code}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().students().create(courseId=course_id, **query, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateStudentResult(success=True, statusCode=status, data=CreateStudentData(**data))
            return _upstream_err(CreateStudentResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateStudentResult, tlog, exc)

    @mcp.tool(
        name="delete_student",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a student from "
            "a course. This action is irreversible — the student's enrollment in the course (they must be "
            "re-added or re-invited to rejoin) cannot be recovered. NEVER call this tool autonomously or as part "
            "of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is "
            "permanent, and wait for their explicit written confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_student(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        user_id: str = Field(description="Identifier of the student to delete. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
    ) -> DeleteStudentResult:
        tlog = ToolLogger(logger, "delete_student")
        if not course_id.strip():
            return _err(DeleteStudentResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not user_id.strip():
            return _err(DeleteStudentResult, tlog, "VALIDATION_ERROR", "user_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().students().delete(courseId=course_id, userId=user_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteStudentResult(success=True, statusCode=status, data=DeleteStudentData(deleted=True, courseId=course_id, userId=user_id))
            return _upstream_err(DeleteStudentResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteStudentResult, tlog, exc)

    @mcp.tool(
        name="get_student",
        description=(
            "Retrieves one student of a course by user ID or email and returns their profile and course "
            "membership."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_student(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        user_id: str = Field(description="Identifier of the student to return. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
    ) -> GetStudentResult:
        tlog = ToolLogger(logger, "get_student")
        if not course_id.strip():
            return _err(GetStudentResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not user_id.strip():
            return _err(GetStudentResult, tlog, "VALIDATION_ERROR", "user_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().students().get(courseId=course_id, userId=user_id))
            if 200 <= status < 300:
                tlog.success()
                return GetStudentResult(success=True, statusCode=status, data=GetStudentData(**data))
            return _upstream_err(GetStudentResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetStudentResult, tlog, exc)

    @mcp.tool(
        name="list_students",
        description=(
            "Lists the students of a course that the user can view. Returns students plus `nextPageToken` for "
            "paging."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_students(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. The default is 30 if unspecified or `0`. The server may return fewer than the specified number of results."),
    ) -> ListStudentsResult:
        tlog = ToolLogger(logger, "list_students")
        if not course_id.strip():
            return _err(ListStudentsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageToken": page_token, "pageSize": page_size}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().students().list(courseId=course_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListStudentsResult(success=True, statusCode=status, data=ListStudentsData(**data))
            return _upstream_err(ListStudentsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListStudentsResult, tlog, exc)
