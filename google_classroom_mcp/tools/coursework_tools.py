"""coursework group: create_course_work, delete_course_work, get_course_work, list_course_work, modify_course_work_assignees, update_course_work"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.coursework import (
    CourseWork,
    CreateCourseWorkData,
    CreateCourseWorkResult,
    DeleteCourseWorkData,
    DeleteCourseWorkResult,
    GetCourseWorkData,
    GetCourseWorkResult,
    ListCourseWorkData,
    ListCourseWorkResult,
    ModifyCourseWorkAssigneesData,
    ModifyCourseWorkAssigneesResult,
    UpdateCourseWorkData,
    UpdateCourseWorkResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.coursework")


def register_coursework_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_course_work",
        description=(
            "Creates course work (assignment, short-answer or multiple-choice question) in a course and returns "
            "it. The item is tied to the OAuth client's project, so later edits and deletes must use a client "
            "from the same project."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_course_work(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        due_time: dict[str, Any] | None = Field(default=None, description="Optional time of day, in UTC, that submissions for this course work are due. This must be specified if `due_date` is specified. Keys: hours, minutes, seconds, nanos."),
        grading_period_id: str | None = Field(default=None, description="Identifier of the grading period associated with the coursework. * At creation, if unspecified, the grading period ID will be set based on the `dueDate` (or `scheduledTime` if no `dueDate` is set). * To indicate no association to any grading period, set this field to an empty string (\"\"). * If specified, it must match an existing grading period ID in the course."),
        scheduled_time: str | None = Field(default=None, description="Optional timestamp when this course work is scheduled to be published."),
        title: str | None = Field(default=None, description="Title of this course work. The title must be a valid UTF-8 string containing between 1 and 3000 characters."),
        assignee_mode: str | None = Field(default=None, description="Assignee mode of the coursework. If unspecified, the default value is `ALL_STUDENTS`. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        max_points: float | None = Field(default=None, description="Maximum grade for this course work. If zero or unspecified, this assignment is considered ungraded. This must be a non-negative integer value."),
        due_date: dict[str, Any] | None = Field(default=None, description="Optional date, in UTC, that submissions for this course work are due. This must be specified if `due_time` is specified. Keys: month, day, year."),
        submission_modification_mode: str | None = Field(default=None, description="Setting to determine when students are allowed to modify submissions. If unspecified, the default value is `MODIFIABLE_UNTIL_TURNED_IN`. One of: MODIFIABLE_UNTIL_TURNED_IN, MODIFIABLE."),
        topic_id: str | None = Field(default=None, description="Identifier for the topic that this coursework is associated with. Must match an existing topic in the course."),
        work_type: str | None = Field(default=None, description="Type of this course work. The type is set when the course work is created and cannot be changed. One of: ASSIGNMENT, SHORT_ANSWER_QUESTION, MULTIPLE_CHOICE_QUESTION."),
        materials: list[dict[str, Any]] | None = Field(default=None, description="Additional materials. CourseWork must have no more than 20 material items. Keys: youtubeVideo, driveFile, link."),
        individual_students_options: dict[str, Any] | None = Field(default=None, description="Identifiers of students with access to the coursework. This field is set only if `assigneeMode` is `INDIVIDUAL_STUDENTS`. If the `assigneeMode` is `INDIVIDUAL_STUDENTS`, then only students specified in this field are assigned the coursework. Keys: studentIds."),
        description: str | None = Field(default=None, description="Optional description of this course work. If set, the description must be a valid UTF-8 string containing no more than 30,000 characters."),
        state: str | None = Field(default=None, description="Status of this course work. If unspecified, the default state is `DRAFT`. One of: PUBLISHED, DRAFT, DELETED."),
        multiple_choice_question: dict[str, Any] | None = Field(default=None, description="Multiple choice question details. For read operations, this field is populated only when `work_type` is `MULTIPLE_CHOICE_QUESTION`. For write operations, this field must be specified when creating course work with a `work_type` of `MULTIPLE_CHOICE_QUESTION`, and it must not be set otherwise. Keys: choices."),
    ) -> CreateCourseWorkResult:
        tlog = ToolLogger(logger, "create_course_work")
        if not course_id.strip():
            return _err(CreateCourseWorkResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"dueTime": due_time, "gradingPeriodId": grading_period_id, "scheduledTime": scheduled_time, "title": title, "assigneeMode": assignee_mode, "maxPoints": max_points, "dueDate": due_date, "submissionModificationMode": submission_modification_mode, "topicId": topic_id, "workType": work_type, "materials": materials, "individualStudentsOptions": individual_students_options, "description": description, "state": state, "multipleChoiceQuestion": multiple_choice_question}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().create(courseId=course_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateCourseWorkResult(success=True, statusCode=status, data=CreateCourseWorkData(**data))
            return _upstream_err(CreateCourseWorkResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateCourseWorkResult, tlog, exc)

    @mcp.tool(
        name="delete_course_work",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a course work "
            "item. This action is irreversible — the item and its student submissions cannot be recovered. NEVER "
            "call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly "
            "what will be deleted and that it is permanent, and wait for their explicit written confirmation "
            "before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_course_work(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work to delete. This identifier is a Classroom-assigned identifier."),
    ) -> DeleteCourseWorkResult:
        tlog = ToolLogger(logger, "delete_course_work")
        if not course_id.strip():
            return _err(DeleteCourseWorkResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(DeleteCourseWorkResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().delete(courseId=course_id, id=course_work_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteCourseWorkResult(success=True, statusCode=status, data=DeleteCourseWorkData(deleted=True, courseId=course_id, id=course_work_id))
            return _upstream_err(DeleteCourseWorkResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteCourseWorkResult, tlog, exc)

    @mcp.tool(
        name="get_course_work",
        description=(
            "Retrieves one course work item by ID and returns its title, work type, state, due date, max points, "
            "materials, assignee mode and topic."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_course_work(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
    ) -> GetCourseWorkResult:
        tlog = ToolLogger(logger, "get_course_work")
        if not course_id.strip():
            return _err(GetCourseWorkResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(GetCourseWorkResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().get(courseId=course_id, id=course_work_id))
            if 200 <= status < 300:
                tlog.success()
                return GetCourseWorkResult(success=True, statusCode=status, data=GetCourseWorkData(**data))
            return _upstream_err(GetCourseWorkResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetCourseWorkResult, tlog, exc)

    @mcp.tool(
        name="list_course_work",
        description=(
            "Lists course work in a course, filtered by `course_work_states` and ordered by `order_by`. Students "
            "only see PUBLISHED items; teachers and domain admins see all. Returns items plus `nextPageToken`."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_course_work(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
        order_by: str | None = Field(default=None, description="Optional sort ordering for results. A comma-separated list of fields with an optional sort direction keyword. Supported fields are `updateTime` and `dueDate`. Supported direction keywords are `asc` and `desc`. If not specified, `updateTime desc` is the default behavior. Examples: `dueDate asc,updateTime desc`, `updateTime,dueDate desc`"),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
        course_work_states: list[str] | None = Field(default=None, description="Restriction on the work status to return. Only courseWork that matches is returned. If unspecified, items with a work status of `PUBLISHED` is returned. One of: PUBLISHED, DRAFT, DELETED."),
    ) -> ListCourseWorkResult:
        tlog = ToolLogger(logger, "list_course_work")
        if not course_id.strip():
            return _err(ListCourseWorkResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            query = {k: v for k, v in {"pageToken": page_token, "orderBy": order_by, "pageSize": page_size, "courseWorkStates": course_work_states}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().list(courseId=course_id, **query))
            if 200 <= status < 300:
                tlog.success()
                return ListCourseWorkResult(success=True, statusCode=status, data=ListCourseWorkData(**data))
            return _upstream_err(ListCourseWorkResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListCourseWorkResult, tlog, exc)

    @mcp.tool(
        name="modify_course_work_assignees",
        description=(
            "Changes the assignee mode of a course work item (all students or specific students) and adds or "
            "removes individual students, then returns the item. Only a teacher of the course can call it. NOTE: "
            "this overwrites the current field values — the original state is not stored by the API after the "
            "call. The response includes both the before and after state so you have a full record of what "
            "changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def modify_course_work_assignees(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the coursework."),
        assignee_mode: str | None = Field(default=None, description="Mode of the coursework describing whether it will be assigned to all students or specified individual students. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        modify_individual_students_options: dict[str, Any] | None = Field(default=None, description="Set which students are assigned or not assigned to the coursework. Must be specified only when `assigneeMode` is `INDIVIDUAL_STUDENTS`. Keys: addStudentIds, removeStudentIds."),
    ) -> ModifyCourseWorkAssigneesResult:
        tlog = ToolLogger(logger, "modify_course_work_assignees")
        if not course_id.strip():
            return _err(ModifyCourseWorkAssigneesResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(ModifyCourseWorkAssigneesResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        body = {k: v for k, v in {"assigneeMode": assignee_mode, "modifyIndividualStudentsOptions": modify_individual_students_options}.items() if v is not None}
        if not body:
            return _err(ModifyCourseWorkAssigneesResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().get(courseId=course_id, id=course_work_id))
            if not 200 <= status < 300:
                return _upstream_err(ModifyCourseWorkAssigneesResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().modifyAssignees(courseId=course_id, id=course_work_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return ModifyCourseWorkAssigneesResult(success=True, statusCode=status, data=ModifyCourseWorkAssigneesData(before=CourseWork(**before_data), after=CourseWork(**data)))
            return _upstream_err(ModifyCourseWorkAssigneesResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ModifyCourseWorkAssigneesResult, tlog, exc)

    @mcp.tool(
        name="update_course_work",
        description=(
            "Updates the provided fields of a course work item and returns it. Must be called with an OAuth "
            "client from the project that created the item. NOTE: this overwrites the current field values — the "
            "original state is not stored by the API after the call. The response includes both the before and "
            "after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_course_work(
        course_id: str = Field(description="Identifier of the course. This identifier can be either the Classroom-assigned identifier or an alias."),
        course_work_id: str = Field(description="Identifier of the course work."),
        due_time: dict[str, Any] | None = Field(default=None, description="Optional time of day, in UTC, that submissions for this course work are due. This must be specified if `due_date` is specified. Keys: hours, minutes, seconds, nanos."),
        grading_period_id: str | None = Field(default=None, description="Identifier of the grading period associated with the coursework. * At creation, if unspecified, the grading period ID will be set based on the `dueDate` (or `scheduledTime` if no `dueDate` is set). * To indicate no association to any grading period, set this field to an empty string (\"\"). * If specified, it must match an existing grading period ID in the course."),
        scheduled_time: str | None = Field(default=None, description="Optional timestamp when this course work is scheduled to be published."),
        title: str | None = Field(default=None, description="Title of this course work. The title must be a valid UTF-8 string containing between 1 and 3000 characters."),
        assignee_mode: str | None = Field(default=None, description="Assignee mode of the coursework. If unspecified, the default value is `ALL_STUDENTS`. One of: ALL_STUDENTS, INDIVIDUAL_STUDENTS."),
        max_points: float | None = Field(default=None, description="Maximum grade for this course work. If zero or unspecified, this assignment is considered ungraded. This must be a non-negative integer value."),
        due_date: dict[str, Any] | None = Field(default=None, description="Optional date, in UTC, that submissions for this course work are due. This must be specified if `due_time` is specified. Keys: month, day, year."),
        submission_modification_mode: str | None = Field(default=None, description="Setting to determine when students are allowed to modify submissions. If unspecified, the default value is `MODIFIABLE_UNTIL_TURNED_IN`. One of: MODIFIABLE_UNTIL_TURNED_IN, MODIFIABLE."),
        topic_id: str | None = Field(default=None, description="Identifier for the topic that this coursework is associated with. Must match an existing topic in the course."),
        work_type: str | None = Field(default=None, description="Type of this course work. The type is set when the course work is created and cannot be changed. One of: ASSIGNMENT, SHORT_ANSWER_QUESTION, MULTIPLE_CHOICE_QUESTION."),
        materials: list[dict[str, Any]] | None = Field(default=None, description="Additional materials. CourseWork must have no more than 20 material items. Keys: youtubeVideo, driveFile, link."),
        individual_students_options: dict[str, Any] | None = Field(default=None, description="Identifiers of students with access to the coursework. This field is set only if `assigneeMode` is `INDIVIDUAL_STUDENTS`. If the `assigneeMode` is `INDIVIDUAL_STUDENTS`, then only students specified in this field are assigned the coursework. Keys: studentIds."),
        description: str | None = Field(default=None, description="Optional description of this course work. If set, the description must be a valid UTF-8 string containing no more than 30,000 characters."),
        state: str | None = Field(default=None, description="Status of this course work. If unspecified, the default state is `DRAFT`. One of: PUBLISHED, DRAFT, DELETED."),
        multiple_choice_question: dict[str, Any] | None = Field(default=None, description="Multiple choice question details. For read operations, this field is populated only when `work_type` is `MULTIPLE_CHOICE_QUESTION`. For write operations, this field must be specified when creating course work with a `work_type` of `MULTIPLE_CHOICE_QUESTION`, and it must not be set otherwise. Keys: choices."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateCourseWorkResult:
        tlog = ToolLogger(logger, "update_course_work")
        if not course_id.strip():
            return _err(UpdateCourseWorkResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        if not course_work_id.strip():
            return _err(UpdateCourseWorkResult, tlog, "VALIDATION_ERROR", "course_work_id must not be empty", 400)
        body = {k: v for k, v in {"dueTime": due_time, "gradingPeriodId": grading_period_id, "scheduledTime": scheduled_time, "title": title, "assigneeMode": assignee_mode, "maxPoints": max_points, "dueDate": due_date, "submissionModificationMode": submission_modification_mode, "topicId": topic_id, "workType": work_type, "materials": materials, "individualStudentsOptions": individual_students_options, "description": description, "state": state, "multipleChoiceQuestion": multiple_choice_question}.items() if v is not None}
        if not body:
            return _err(UpdateCourseWorkResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().courseWork().get(courseId=course_id, id=course_work_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateCourseWorkResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().courseWork().patch(courseId=course_id, id=course_work_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateCourseWorkResult(success=True, statusCode=status, data=UpdateCourseWorkData(before=CourseWork(**before_data), after=CourseWork(**data)))
            return _upstream_err(UpdateCourseWorkResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateCourseWorkResult, tlog, exc)
