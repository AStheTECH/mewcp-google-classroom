"""courses group: create_course, delete_course, get_course, get_grading_period_settings, list_courses, replace_course, update_course, update_grading_period_settings"""

import logging
from typing import Any

from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from .. import service
from ..logging_utils import ToolLogger
from ..schemas.courses import (
    Course,
    CreateCourseData,
    CreateCourseResult,
    DeleteCourseData,
    DeleteCourseResult,
    GetCourseData,
    GetCourseResult,
    GetGradingPeriodSettingsData,
    GetGradingPeriodSettingsResult,
    GradingPeriodSettings,
    ListCoursesData,
    ListCoursesResult,
    ReplaceCourseData,
    ReplaceCourseResult,
    UpdateCourseData,
    UpdateCourseResult,
    UpdateGradingPeriodSettingsData,
    UpdateGradingPeriodSettingsResult,
)
from ._helpers import _err, _handle_request_exc, _upstream_err

logger = logging.getLogger("google-classroom-mcp.tools.courses")


def register_courses_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="create_course",
        description=(
            "Creates a course owned by `owner_id`, who is also added as its teacher, and returns the new course. "
            "Non-admin users can only create courses they own; domain admins can create courses owned by any user "
            "in their domain, and an alias passed in `id` fails with ALREADY_EXISTS if it is taken."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def create_course(
        name: str = Field(description="Name of the course. For example, \"10th Grade Biology\". It must be between 1 and 750 characters and a valid UTF-8 string."),
        owner_id: str = Field(description="The identifier of the owner of a course. When specified as a parameter of a create course request, this field is required. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user This must be set in a create request. Admins can also specify this field in a patch course request to transfer ownership. In other contexts, it is read-only."),
        section: str | None = Field(default=None, description="Section of the course. For example, \"Period 2\". If set, this field must be a valid UTF-8 string and no longer than 2800 characters."),
        subject: str | None = Field(default=None, description="Optional. The subject of the course."),
        room: str | None = Field(default=None, description="Optional room location. For example, \"301\". If set, this field must be a valid UTF-8 string and no longer than 650 characters."),
        course_state: str | None = Field(default=None, description="State of the course. If unspecified, the default state is `PROVISIONED`. One of: ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED."),
        id: str | None = Field(default=None, description="Identifier for this course assigned by Classroom. When creating a course, you may optionally set this identifier to an alias string in the request to create a corresponding alias. The `id` is still assigned by Classroom and cannot be updated after the course is created. Specifying this field in a course update mask results in an error."),
        description: str | None = Field(default=None, description="Optional description. For example, \"We'll be learning about the structure of living creatures from a combination of textbooks, guest lectures, and lab work. Expect to be excited!\" If set, this field must be a valid UTF-8 string and no longer than 30,000 characters."),
        description_heading: str | None = Field(default=None, description="Optional heading for the description. For example, \"Welcome to 10th Grade Biology.\" If set, this field must be a valid UTF-8 string and no longer than 3600 characters."),
        levels: str | None = Field(default=None, description="Optional. Levels for the course. Examples: \"9th grade\", \"Middle school\", \"4th - 5th\", \"K-2\", \"3000\". If set, this field must be a valid UTF-8 string and fewer than 1000 characters. This field can only be cleared using the `PatchCourse` method."),
    ) -> CreateCourseResult:
        tlog = ToolLogger(logger, "create_course")
        body = {k: v for k, v in {"name": name, "section": section, "subject": subject, "room": room, "courseState": course_state, "id": id, "description": description, "descriptionHeading": description_heading, "ownerId": owner_id, "levels": levels}.items() if v is not None}
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().create(body=body))
            if 200 <= status < 300:
                tlog.success()
                return CreateCourseResult(success=True, statusCode=status, data=CreateCourseData(**data))
            return _upstream_err(CreateCourseResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CreateCourseResult, tlog, exc)

    @mcp.tool(
        name="delete_course",
        description=(
            "DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes a course. This "
            "action is irreversible — the course and its classwork, announcements and roster links cannot be "
            "recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell "
            "the user exactly what will be deleted and that it is permanent, and wait for their explicit written "
            "confirmation before proceeding."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=True),
    )
    def delete_course(
        course_id: str = Field(description="Identifier of the course to delete. This identifier can be either the Classroom-assigned identifier or an alias."),
    ) -> DeleteCourseResult:
        tlog = ToolLogger(logger, "delete_course")
        if not course_id.strip():
            return _err(DeleteCourseResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().delete(id=course_id))
            if 200 <= status < 300:
                tlog.success()
                return DeleteCourseResult(success=True, statusCode=status, data=DeleteCourseData(deleted=True, id=course_id))
            return _upstream_err(DeleteCourseResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(DeleteCourseResult, tlog, exc)

    @mcp.tool(
        name="get_course",
        description=(
            "Retrieves one course by ID or alias and returns its settings, state, links, owner and teacher/course "
            "group emails."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_course(
        course_id: str = Field(description="Identifier of the course to return. This identifier can be either the Classroom-assigned identifier or an alias."),
    ) -> GetCourseResult:
        tlog = ToolLogger(logger, "get_course")
        if not course_id.strip():
            return _err(GetCourseResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().get(id=course_id))
            if 200 <= status < 300:
                tlog.success()
                return GetCourseResult(success=True, statusCode=status, data=GetCourseData(**data))
            return _upstream_err(GetCourseResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetCourseResult, tlog, exc)

    @mcp.tool(
        name="get_grading_period_settings",
        description=(
            "Retrieves the grading period settings of a course and returns each grading period with its start and "
            "end dates, plus whether the settings apply to existing coursework."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def get_grading_period_settings(
        course_id: str = Field(description="The identifier of the course."),
    ) -> GetGradingPeriodSettingsResult:
        tlog = ToolLogger(logger, "get_grading_period_settings")
        if not course_id.strip():
            return _err(GetGradingPeriodSettingsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        try:
            data, status, retry_after = service.execute(lambda s: s.courses().getGradingPeriodSettings(courseId=course_id))
            if 200 <= status < 300:
                tlog.success()
                return GetGradingPeriodSettingsResult(success=True, statusCode=status, data=GetGradingPeriodSettingsData(**data))
            return _upstream_err(GetGradingPeriodSettingsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(GetGradingPeriodSettingsResult, tlog, exc)

    @mcp.tool(
        name="list_courses",
        description=(
            "Lists the courses the user can view, most recently created first, optionally filtered by "
            "`student_id`, `teacher_id` (mutually exclusive) and `course_states`. Returns courses plus "
            "`nextPageToken` for paging."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    )
    def list_courses(
        course_states: list[str] | None = Field(default=None, description="Restricts returned courses to those in one of the specified states. If unspecified, Courses in any state are returned. One of: ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED."),
        page_size: int | None = Field(default=None, description="Maximum number of items to return. Zero or unspecified indicates that the server may assign a maximum. The server may return fewer than the specified number of results."),
        teacher_id: str | None = Field(default=None, description="Restricts returned courses to those having a teacher with the specified identifier. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user If specified, `student_id` must be empty."),
        student_id: str | None = Field(default=None, description="Restricts returned courses to those having a student with the specified identifier. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user If specified, `teacher_id` must be empty."),
        page_token: str | None = Field(default=None, description="nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned. The list request must be otherwise identical to the one that resulted in this token."),
    ) -> ListCoursesResult:
        tlog = ToolLogger(logger, "list_courses")
        try:
            query = {k: v for k, v in {"courseStates": course_states, "pageSize": page_size, "teacherId": teacher_id, "studentId": student_id, "pageToken": page_token}.items() if v is not None}
            data, status, retry_after = service.execute(lambda s: s.courses().list(**query))
            if 200 <= status < 300:
                tlog.success()
                return ListCoursesResult(success=True, statusCode=status, data=ListCoursesData(**data))
            return _upstream_err(ListCoursesResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ListCoursesResult, tlog, exc)

    @mcp.tool(
        name="replace_course",
        description=(
            "Replaces a course with the supplied field values (full update); `name` and `owner_id` are required, "
            "and `levels` is the one field kept when omitted. Use update_course to change only some fields or to "
            "clear `levels`. NOTE: this overwrites the current field values — the original state is not stored by "
            "the API after the call. The response includes both the before and after state so you have a full "
            "record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def replace_course(
        course_id: str = Field(description="Identifier of the course to update. This identifier can be either the Classroom-assigned identifier or an alias."),
        name: str = Field(description="Name of the course. For example, \"10th Grade Biology\". It must be between 1 and 750 characters and a valid UTF-8 string."),
        owner_id: str = Field(description="The identifier of the owner of a course. When specified as a parameter of a create course request, this field is required. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user This must be set in a create request. Admins can also specify this field in a patch course request to transfer ownership. In other contexts, it is read-only."),
        section: str | None = Field(default=None, description="Section of the course. For example, \"Period 2\". If set, this field must be a valid UTF-8 string and no longer than 2800 characters."),
        subject: str | None = Field(default=None, description="Optional. The subject of the course."),
        room: str | None = Field(default=None, description="Optional room location. For example, \"301\". If set, this field must be a valid UTF-8 string and no longer than 650 characters."),
        course_state: str | None = Field(default=None, description="State of the course. If unspecified, the default state is `PROVISIONED`. One of: ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED."),
        description: str | None = Field(default=None, description="Optional description. For example, \"We'll be learning about the structure of living creatures from a combination of textbooks, guest lectures, and lab work. Expect to be excited!\" If set, this field must be a valid UTF-8 string and no longer than 30,000 characters."),
        description_heading: str | None = Field(default=None, description="Optional heading for the description. For example, \"Welcome to 10th Grade Biology.\" If set, this field must be a valid UTF-8 string and no longer than 3600 characters."),
        levels: str | None = Field(default=None, description="Optional. Levels for the course. Examples: \"9th grade\", \"Middle school\", \"4th - 5th\", \"K-2\", \"3000\". If set, this field must be a valid UTF-8 string and fewer than 1000 characters. This field can only be cleared using the `PatchCourse` method."),
    ) -> ReplaceCourseResult:
        tlog = ToolLogger(logger, "replace_course")
        if not course_id.strip():
            return _err(ReplaceCourseResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"name": name, "section": section, "subject": subject, "room": room, "courseState": course_state, "description": description, "descriptionHeading": description_heading, "ownerId": owner_id, "levels": levels}.items() if v is not None}
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().get(id=course_id))
            if not 200 <= status < 300:
                return _upstream_err(ReplaceCourseResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().update(id=course_id, body=body))
            if 200 <= status < 300:
                tlog.success()
                return ReplaceCourseResult(success=True, statusCode=status, data=ReplaceCourseData(before=Course(**before_data), after=Course(**data)))
            return _upstream_err(ReplaceCourseResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(ReplaceCourseResult, tlog, exc)

    @mcp.tool(
        name="update_course",
        description=(
            "Updates only the provided fields of a course and returns the updated course. Fails if the course is "
            "not modifiable or the title contains a URL. NOTE: this overwrites the current field values — the "
            "original state is not stored by the API after the call. The response includes both the before and "
            "after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_course(
        course_id: str = Field(description="Identifier of the course to update. This identifier can be either the Classroom-assigned identifier or an alias."),
        name: str | None = Field(default=None, description="Name of the course. For example, \"10th Grade Biology\". It must be between 1 and 750 characters and a valid UTF-8 string."),
        section: str | None = Field(default=None, description="Section of the course. For example, \"Period 2\". If set, this field must be a valid UTF-8 string and no longer than 2800 characters."),
        subject: str | None = Field(default=None, description="Optional. The subject of the course."),
        room: str | None = Field(default=None, description="Optional room location. For example, \"301\". If set, this field must be a valid UTF-8 string and no longer than 650 characters."),
        course_state: str | None = Field(default=None, description="State of the course. If unspecified, the default state is `PROVISIONED`. One of: ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED."),
        description: str | None = Field(default=None, description="Optional description. For example, \"We'll be learning about the structure of living creatures from a combination of textbooks, guest lectures, and lab work. Expect to be excited!\" If set, this field must be a valid UTF-8 string and no longer than 30,000 characters."),
        description_heading: str | None = Field(default=None, description="Optional heading for the description. For example, \"Welcome to 10th Grade Biology.\" If set, this field must be a valid UTF-8 string and no longer than 3600 characters."),
        owner_id: str | None = Field(default=None, description="The identifier of the owner of a course. When specified as a parameter of a create course request, this field is required. The identifier can be one of the following: * the numeric identifier for the user * the email address of the user * the string literal `\"me\"`, indicating the requesting user This must be set in a create request. Admins can also specify this field in a patch course request to transfer ownership. In other contexts, it is read-only."),
        levels: str | None = Field(default=None, description="Optional. Levels for the course. Examples: \"9th grade\", \"Middle school\", \"4th - 5th\", \"K-2\", \"3000\". If set, this field must be a valid UTF-8 string and fewer than 1000 characters. This field can only be cleared using the `PatchCourse` method."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateCourseResult:
        tlog = ToolLogger(logger, "update_course")
        if not course_id.strip():
            return _err(UpdateCourseResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"name": name, "section": section, "subject": subject, "room": room, "courseState": course_state, "description": description, "descriptionHeading": description_heading, "ownerId": owner_id, "levels": levels}.items() if v is not None}
        if not body:
            return _err(UpdateCourseResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().get(id=course_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateCourseResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().patch(id=course_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateCourseResult(success=True, statusCode=status, data=UpdateCourseData(before=Course(**before_data), after=Course(**data)))
            return _upstream_err(UpdateCourseResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateCourseResult, tlog, exc)

    @mcp.tool(
        name="update_grading_period_settings",
        description=(
            "Adds, removes or modifies grading periods in a course's grading period settings. Both the requesting "
            "user and the course owner must be licensed to modify grading periods. NOTE: this overwrites the "
            "current field values — the original state is not stored by the API after the call. The response "
            "includes both the before and after state so you have a full record of what changed."
        ),
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=True),
    )
    def update_grading_period_settings(
        course_id: str = Field(description="The identifier of the course."),
        apply_to_existing_coursework: bool | None = Field(default=None, description="Supports toggling the application of grading periods on existing stream items. Once set, this value is persisted meaning that it does not need to be set in every request to update `GradingPeriodSettings`. If not previously set, the default is False."),
        grading_periods: list[dict[str, Any]] | None = Field(default=None, description="The list of grading periods in a specific course. Grading periods must not have overlapping date ranges and must be listed in chronological order. Each grading period must have a unique title within a course. Keys: title, startDate, endDate."),
        update_mask: str | None = Field(default=None, description="Comma-separated field mask of the fields to update. Omit to update exactly the fields you provide."),
    ) -> UpdateGradingPeriodSettingsResult:
        tlog = ToolLogger(logger, "update_grading_period_settings")
        if not course_id.strip():
            return _err(UpdateGradingPeriodSettingsResult, tlog, "VALIDATION_ERROR", "course_id must not be empty", 400)
        body = {k: v for k, v in {"applyToExistingCoursework": apply_to_existing_coursework, "gradingPeriods": grading_periods}.items() if v is not None}
        if not body:
            return _err(UpdateGradingPeriodSettingsResult, tlog, "VALIDATION_ERROR", "Provide at least one field to change", 400)
        try:
            before_data, status, retry_after = service.execute(lambda s: s.courses().getGradingPeriodSettings(courseId=course_id))
            if not 200 <= status < 300:
                return _upstream_err(UpdateGradingPeriodSettingsResult, tlog, status, before_data, retry_after)
            data, status, retry_after = service.execute(lambda s: s.courses().updateGradingPeriodSettings(courseId=course_id, updateMask=update_mask or ",".join(body), body=body))
            if 200 <= status < 300:
                tlog.success()
                return UpdateGradingPeriodSettingsResult(success=True, statusCode=status, data=UpdateGradingPeriodSettingsData(before=GradingPeriodSettings(**before_data), after=GradingPeriodSettings(**data)))
            return _upstream_err(UpdateGradingPeriodSettingsResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(UpdateGradingPeriodSettingsResult, tlog, exc)
