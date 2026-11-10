"""student_submissions group: get_student_submission, list_student_submissions, modify_student_submission_attachments, reclaim_student_submission, return_student_submission, turn_in_student_submission, update_student_submission"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.student_submissions import (
    GetStudentSubmissionData,
    GetStudentSubmissionResult,
    ListStudentSubmissionsData,
    ListStudentSubmissionsResult,
    ModifyStudentSubmissionAttachmentsData,
    ModifyStudentSubmissionAttachmentsResult,
    ReclaimStudentSubmissionData,
    ReclaimStudentSubmissionResult,
    ReturnStudentSubmissionData,
    ReturnStudentSubmissionResult,
    StudentSubmission,
    TurnInStudentSubmissionData,
    TurnInStudentSubmissionResult,
    UpdateStudentSubmissionData,
    UpdateStudentSubmissionResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.student_submissions")


def register_student_submissions_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_student_submission",
        description=(
            "Retrieves one student submission by ID and returns its state, grades, late flag, attachments and "
            "submission history."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_student_submission(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
        student_submission_id: str = Field(description="Identifier of the student submission."),
    ) -> GetStudentSubmissionResult:
        tlog = ToolLogger(logger, "get_student_submission")
        if not course_id.strip():
            return _err(GetStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(GetStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not student_submission_id.strip():
            return _err(GetStudentSubmissionResult, tlog, "VALIDATION_ERROR", "student_submission_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            if 200 <= status < 300:
                tlog.success()
                return GetStudentSubmissionResult(success=True, statusCode=status, data=GetStudentSubmissionData(**data))
            return _upstream_err(GetStudentSubmissionResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetStudentSubmissionResult, tlog, exc)

    @mcp.tool(
        name="list_student_submissions",
        description=(
            "Lists student submissions for a course work item, filtered by `states`, `user_id` and `late`. Pass "
            "`-` as `course_work_id` to span all course work in the course; students see only their own work, "
            "teachers and domain admins see all. Returns submissions plus `nextPageToken`."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_student_submissions(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the student work to request. This may be set to the string literal `\"-\"` to request student work for all course work in the specified course."),
        states: list[str] | None = Field(default=None, description="Requested submission states. If specified, returned student submissions match one of the specified submission states. One of: NEW, CREATED, TURNED_IN, RETURNED, RECLAIMED_BY_STUDENT."),
        user_id: str | None = Field(default=None, description="Optional argument to restrict returned student work to those owned by the student with the specified identifier. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user"),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
        late: str | None = Field(default=None, description="Requested lateness value. If specified, returned student submissions are restricted by the requested value. If unspecified, submissions are returned regardless of `late` value. One of: LATE_ONLY, NOT_LATE_ONLY."),
    ) -> ListStudentSubmissionsResult:
        tlog = ToolLogger(logger, "list_student_submissions")
        if not course_id.strip():
            return _err(ListStudentSubmissionsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(ListStudentSubmissionsResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"states": states, "userId": user_id, "pageToken": page_token, "pageSize": page_size, "late": late}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().list(courseId=course_id, courseWorkId=course_work_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListStudentSubmissionsResult(success=True, statusCode=status, data=ListStudentSubmissionsData(**data))
            return _upstream_err(ListStudentSubmissionsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListStudentSubmissionsResult, tlog, exc)

    @mcp.tool(
        name="modify_student_submission_attachments",
        description=(
            "Adds attachments to a student submission and returns it. Only works for submissions of ASSIGNMENT "
            "course work, and the call must use the OAuth client's project that created the course work. NOTE: "
            "this overwrites the current field values — the original state is not stored by the API after the "
            "call. The response includes both the before and after state so you have a full record of what "
            "changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def modify_student_submission_attachments(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
        student_submission_id: str = Field(description="Identifier of the student submission."),
        add_attachments: list[dict[str, Any]] | None = Field(default=None, description="Attachments to add. A student submission may not have more than 20 attachments. Form attachments are not supported. Keys: youTubeVideo, driveFile, link, form."),
    ) -> ModifyStudentSubmissionAttachmentsResult:
        tlog = ToolLogger(logger, "modify_student_submission_attachments")
        if not course_id.strip():
            return _err(ModifyStudentSubmissionAttachmentsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(ModifyStudentSubmissionAttachmentsResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not student_submission_id.strip():
            return _err(ModifyStudentSubmissionAttachmentsResult, tlog, "VALIDATION_ERROR", "student_submission_id must not be empty", 400)
        body = {k: v for k, v in {"addAttachments": add_attachments}.items() if v is not None}
        if not body:
            return _err(ModifyStudentSubmissionAttachmentsResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            if not 200 <= status < 300:
                return _upstream_err(ModifyStudentSubmissionAttachmentsResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().modifyAttachments(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return ModifyStudentSubmissionAttachmentsResult(success=True, statusCode=status, data=ModifyStudentSubmissionAttachmentsData(before=StudentSubmission(**before_data), after=StudentSubmission(**data)))
            return _upstream_err(ModifyStudentSubmissionAttachmentsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ModifyStudentSubmissionAttachmentsResult, tlog, exc)

    @mcp.tool(
        name="reclaim_student_submission",
        description=(
            "Reclaims a turned-in student submission on behalf of the student who owns it, returning ownership of "
            "attached Drive files to the student, and returns the submission afterwards. Only the owning student "
            "can call it, using the OAuth client's project that created the course work. NOTE: this overwrites "
            "the current field values — the original state is not stored by the API after the call. The response "
            "includes both the before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def reclaim_student_submission(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
        student_submission_id: str = Field(description="Identifier of the student submission."),
    ) -> ReclaimStudentSubmissionResult:
        tlog = ToolLogger(logger, "reclaim_student_submission")
        if not course_id.strip():
            return _err(ReclaimStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(ReclaimStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not student_submission_id.strip():
            return _err(ReclaimStudentSubmissionResult, tlog, "VALIDATION_ERROR", "student_submission_id must not be empty", 400)
        body: dict[str, Any] = {}
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            if not 200 <= status < 300:
                return _upstream_err(ReclaimStudentSubmissionResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().reclaim(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id, body=body))
            if not 200 <= status < 300:
                return _upstream_err(ReclaimStudentSubmissionResult, tlog, status, data, retry_after)
            after_data, after_status, _ = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            tlog.success()
            return ReclaimStudentSubmissionResult(success=True, statusCode=status, data=ReclaimStudentSubmissionData(before=StudentSubmission(**before_data), after=StudentSubmission(**after_data) if 200 <= after_status < 300 else None))
        except Exception as exc:
            return _handle_request_exc(ReclaimStudentSubmissionResult, tlog, exc)

    @mcp.tool(
        name="return_student_submission",
        description=(
            "Returns a student submission to the student, transferring ownership of attached Drive files to them, "
            "and returns the submission afterwards. It does not copy `draftGrade` into `assignedGrade`. Only a "
            "teacher of the course can call it, using the OAuth client's project that created the course work. "
            "NOTE: this overwrites the current field values — the original state is not stored by the API after "
            "the call. The response includes both the before and after state so you have a full record of what "
            "changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def return_student_submission(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
        student_submission_id: str = Field(description="Identifier of the student submission."),
    ) -> ReturnStudentSubmissionResult:
        tlog = ToolLogger(logger, "return_student_submission")
        if not course_id.strip():
            return _err(ReturnStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(ReturnStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not student_submission_id.strip():
            return _err(ReturnStudentSubmissionResult, tlog, "VALIDATION_ERROR", "student_submission_id must not be empty", 400)
        body: dict[str, Any] = {}
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            if not 200 <= status < 300:
                return _upstream_err(ReturnStudentSubmissionResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().return_(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id, body=body))
            if not 200 <= status < 300:
                return _upstream_err(ReturnStudentSubmissionResult, tlog, status, data, retry_after)
            after_data, after_status, _ = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            tlog.success()
            return ReturnStudentSubmissionResult(success=True, statusCode=status, data=ReturnStudentSubmissionData(before=StudentSubmission(**before_data), after=StudentSubmission(**after_data) if 200 <= after_status < 300 else None))
        except Exception as exc:
            return _handle_request_exc(ReturnStudentSubmissionResult, tlog, exc)

    @mcp.tool(
        name="turn_in_student_submission",
        description=(
            "Turns in a student submission, transferring ownership of attached Drive files to the teacher, and "
            "returns the submission afterwards. Only the owning student can call it, using the OAuth client's "
            "project that created the course work. NOTE: this overwrites the current field values — the original "
            "state is not stored by the API after the call. The response includes both the before and after state "
            "so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def turn_in_student_submission(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
        student_submission_id: str = Field(description="Identifier of the student submission."),
    ) -> TurnInStudentSubmissionResult:
        tlog = ToolLogger(logger, "turn_in_student_submission")
        if not course_id.strip():
            return _err(TurnInStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(TurnInStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not student_submission_id.strip():
            return _err(TurnInStudentSubmissionResult, tlog, "VALIDATION_ERROR", "student_submission_id must not be empty", 400)
        body: dict[str, Any] = {}
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            if not 200 <= status < 300:
                return _upstream_err(TurnInStudentSubmissionResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().turnIn(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id, body=body))
            if not 200 <= status < 300:
                return _upstream_err(TurnInStudentSubmissionResult, tlog, status, data, retry_after)
            after_data, after_status, _ = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            tlog.success()
            return TurnInStudentSubmissionResult(success=True, statusCode=status, data=TurnInStudentSubmissionData(before=StudentSubmission(**before_data), after=StudentSubmission(**after_data) if 200 <= after_status < 300 else None))
        except Exception as exc:
            return _handle_request_exc(TurnInStudentSubmissionResult, tlog, exc)

    @mcp.tool(
        name="update_student_submission",
        description=(
            "Updates the provided fields of a student submission, such as `draft_grade` or `assigned_grade`, and "
            "returns it. Must use the OAuth client's project that created the course work (or a grade-sync add-on "
            "attachment on it). NOTE: this overwrites the current field values — the original state is not stored "
            "by the API after the call. The response includes both the before and after state so you have a full "
            "record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_student_submission(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
        student_submission_id: str = Field(description="Identifier of the student submission."),
        assigned_grade: float | None = Field(default=None, description="Optional grade. If unset, no grade was set. This value must be non-negative. Decimal (that is, non-integer) values are allowed, but are rounded to two decimal places. This may be modified only by course teachers."),
        short_answer_submission: dict[str, Any] | None = Field(default=None, description="Submission content when course_work_type is SHORT_ANSWER_QUESTION. Keys: answer."),
        draft_grade: float | None = Field(default=None, description="Optional pending grade. If unset, no grade was set. This value must be non-negative. Decimal (that is, non-integer) values are allowed, but are rounded to two decimal places. This is only visible to and modifiable by course teachers."),
        multiple_choice_submission: dict[str, Any] | None = Field(default=None, description="Submission content when course_work_type is MULTIPLE_CHOICE_QUESTION. Keys: answer."),
        assignment_submission: dict[str, Any] | None = Field(default=None, description="Submission content when course_work_type is ASSIGNMENT. Students can modify this content using ModifyAttachments. Keys: attachments."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateStudentSubmissionResult:
        tlog = ToolLogger(logger, "update_student_submission")
        if not course_id.strip():
            return _err(UpdateStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(UpdateStudentSubmissionResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        if not student_submission_id.strip():
            return _err(UpdateStudentSubmissionResult, tlog, "VALIDATION_ERROR", "student_submission_id must not be empty", 400)
        body = {k: v for k, v in {"assignedGrade": assigned_grade, "shortAnswerSubmission": short_answer_submission, "draftGrade": draft_grade, "multipleChoiceSubmission": multiple_choice_submission, "assignmentSubmission": assignment_submission}.items() if v is not None}
        if not body:
            return _err(UpdateStudentSubmissionResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateStudentSubmissionResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().studentSubmissions().patch(courseId=course_id, courseWorkId=course_work_id, id=student_submission_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateStudentSubmissionResult(success=True, statusCode=status, data=UpdateStudentSubmissionData(before=StudentSubmission(**before_data), after=StudentSubmission(**data)))
            return _upstream_err(UpdateStudentSubmissionResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateStudentSubmissionResult, tlog, exc)
